# data/excel_manager.py - Excel 文件管理模块

import shutil
from pathlib import Path
from datetime import datetime
from django.conf import settings


def get_working_excel_path(date):
    """
    获取工作用Excel文件路径，仅复制一次

    Args:
        date: 日期字符串 (YYYYMMDD 格式)

    Returns:
        Path: 工作Excel文件的完整路径 (candidate-final-YYYYMMDD-HHmmss.xlsx)

    Raises:
        FileNotFoundError: 原始Excel文件不存在
    """
    data_root = Path(settings.DATA_ROOT)
    data_file = settings.DATA_FILE

    # 原始文件路径
    original_path = data_root / date / data_file

    if not original_path.exists():
        raise FileNotFoundError(f"原始Excel文件不存在: {original_path}")

    # 工作文件目录 (与原始文件同目录)
    excel_dir = original_path.parent

    # 查找是否已存在该日期的工作文件
    existing_file = _find_existing_working_file(excel_dir, date)

    if existing_file:
        return existing_file

    # 生成新的工作文件名（带时间戳）
    now = datetime.now().strftime('%H%M%S')
    working_filename = f"candidate-final-{date}-{now}.xlsx"
    working_path = excel_dir / working_filename

    # 复制原始文件一次
    shutil.copy2(original_path, working_path)

    return working_path


def _find_existing_working_file(excel_dir, date):
    """
    查找该日期是否已存在工作文件

    Args:
        excel_dir: Excel文件所在目录
        date: 日期字符串 (YYYYMMDD)

    Returns:
        Path: 找到的工作文件路径，未找到返回None
    """
    pattern = f"candidate-final-{date}-*.xlsx"
    matching_files = list(excel_dir.glob(pattern))

    if matching_files:
        # 返回找到的文件（应该只有一个）
        return matching_files[0]

    return None


def reset_working_excel(date):
    """
    重置工作Excel文件 - 删除工作副本，从原始文件重新复制

    Args:
        date: 日期字符串 (YYYYMMDD)

    Returns:
        Path: 新创建的工作文件路径
    """
    data_root = Path(settings.DATA_ROOT)
    data_file = settings.DATA_FILE
    excel_dir = data_root / date / Path(data_file).parent

    # 删除该日期的工作文件
    pattern = f"candidate-final-{date}-*.xlsx"
    for old_file in excel_dir.glob(pattern):
        old_file.unlink()

    # 从原始文件重新复制一次
    return get_working_excel_path(date)

