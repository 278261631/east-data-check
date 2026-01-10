from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse, FileResponse, Http404
from pathlib import Path
import os
import re
import openpyxl


@login_required
def date_list(request):
    data_root = Path(settings.DATA_ROOT)
    data_file = settings.DATA_FILE
    dates = []

    if data_root.exists():
        for item in sorted(data_root.iterdir(), reverse=True):
            if item.is_dir() and re.match(r'^\d{8}$', item.name):
                has_data = (item / data_file).exists()
                dates.append({
                    'name': item.name,
                    'has_data': has_data
                })

    return render(request, 'data/date_list.html', {'dates': dates})


def get_row_files(date, attribute, seq_num, fits_new, fits_old):
    """Generate file info for a row"""
    data_root = Path(settings.DATA_ROOT)
    data_file = settings.DATA_FILE
    base_dir = data_root / date / Path(data_file).parent

    # Extract base names (remove _new.fits suffix)
    base_new = fits_new.replace('_new.fits', '') if fits_new else None
    base_old = fits_old.replace('_new.fits', '') if fits_old else None

    # Build file prefix: attribute_seqnum_basename
    prefix = f"{attribute}_{seq_num:04d}_"

    files = {'new_time': [], 'old_time': []}

    for base, time_key in [(base_new, 'new_time'), (base_old, 'old_time')]:
        if not base:
            continue
        file_prefix = prefix + base

        # Check for fits files
        for suffix in ['_lib.fits', '_new.fits']:
            fpath = base_dir / (file_prefix + suffix)
            if fpath.exists():
                files[time_key].append({
                    'name': fpath.name,
                    'type': 'fits',
                    'path': str(fpath)
                })

        # Check for jpg files
        for suffix in ['_SEPlib.jpg', '_SEPnew.jpg']:
            fpath = base_dir / (file_prefix + suffix)
            if fpath.exists():
                files[time_key].append({
                    'name': fpath.name,
                    'type': 'jpg',
                    'subtype': 'lib' if 'lib' in suffix else 'new',
                    'path': str(fpath)
                })

    return files


@login_required
def date_detail(request, date):
    data_root = Path(settings.DATA_ROOT)
    data_file = settings.DATA_FILE
    file_path = data_root / date / data_file

    rows = []
    headers = []
    error = None

    if file_path.exists():
        try:
            wb = openpyxl.load_workbook(file_path, read_only=True)
            ws = wb.active
            header_map = {}
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0:
                    headers = list(row)
                    header_map = {h: idx for idx, h in enumerate(headers)}
                else:
                    rows.append({
                        'index': i,
                        'data': list(row)
                    })
            wb.close()
        except Exception as e:
            error = str(e)
    else:
        error = f'File not found: {file_path}'

    return render(request, 'data/date_detail.html', {
        'date': date,
        'headers': headers,
        'rows': rows,
        'error': error
    })


@login_required
def row_files(request, date, row_index):
    """API to get files for a specific row"""
    data_root = Path(settings.DATA_ROOT)
    data_file = settings.DATA_FILE
    file_path = data_root / date / data_file

    if not file_path.exists():
        return JsonResponse({'error': 'File not found'}, status=404)

    try:
        wb = openpyxl.load_workbook(file_path, read_only=True)
        ws = wb.active
        headers = []
        target_row = None

        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                headers = list(row)
            elif i == row_index:
                target_row = list(row)
                break
        wb.close()

        if not target_row:
            return JsonResponse({'error': 'Row not found'}, status=404)

        # Get column indices
        h_map = {h: idx for idx, h in enumerate(headers)}
        attribute = target_row[h_map.get('attribute', 1)]
        seq_num = target_row[h_map.get('sequence_number', 2)]
        fits_new = target_row[h_map.get('fits_filename_new', 11)]
        fits_old = target_row[h_map.get('fits_filename_old', 15)]
        time_new = target_row[h_map.get('time_utc_new', 10)]
        time_old = target_row[h_map.get('time_utc_old', 14)]

        files = get_row_files(date, attribute, int(seq_num), fits_new, fits_old)

        # Determine which is earlier
        if time_old and time_new and str(time_old) < str(time_new):
            result = {'left': files['old_time'], 'right': files['new_time'],
                      'left_time': str(time_old), 'right_time': str(time_new)}
        else:
            result = {'left': files['new_time'], 'right': files['old_time'],
                      'left_time': str(time_new), 'right_time': str(time_old)}

        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def serve_image(request, date, filename):
    """Serve image file"""
    data_root = Path(settings.DATA_ROOT)
    data_file = settings.DATA_FILE
    file_path = data_root / date / Path(data_file).parent / filename

    if not file_path.exists() or not filename.endswith('.jpg'):
        raise Http404("Image not found")

    return FileResponse(open(file_path, 'rb'), content_type='image/jpeg')


@login_required
def serve_fits(request, date, filename):
    """Serve fits file for download"""
    data_root = Path(settings.DATA_ROOT)
    data_file = settings.DATA_FILE
    file_path = data_root / date / Path(data_file).parent / filename

    if not file_path.exists() or not filename.endswith('.fits'):
        raise Http404("File not found")

    response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
