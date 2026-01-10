from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
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
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i == 0:
                    headers = list(row)
                else:
                    rows.append(list(row))
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
