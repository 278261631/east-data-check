#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试Excel同步功能
"""

import os
import sys
import django

# 设置Django环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from data.excel_manager import sync_new_rows_from_original

def test_sync(date):
    """测试同步功能"""
    print(f"开始测试同步功能，日期: {date}")
    print("-" * 50)
    
    result = sync_new_rows_from_original(date)
    
    print(f"同步结果:")
    print(f"  成功: {result['success']}")
    print(f"  新增行数: {result['added_rows']}")
    print(f"  总行数: {result['total_rows']}")
    print(f"  消息: {result['message']}")
    print("-" * 50)
    
    return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python test_sync.py <日期>")
        print("示例: python test_sync.py 20240101")
        sys.exit(1)
    
    date = sys.argv[1]
    test_sync(date)

