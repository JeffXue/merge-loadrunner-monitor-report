# -*- coding:utf-8 -*-

result_path_list = [
r'/root/tmp/ydh-1127Round1-index_ptest_monitor_statistical_data_201512071132',
r'/root/tmp/ydh-1127Round1-index_ptest_monitor_statistical_data_201512071127',
r'/root/tmp/ydh-1127Round1-index_lr_statistical_data_201512071124']
scenario_name = u"场景名称"
version = u"v1.0.0"
scenario_explain = u"""1. 说明1
2. 说明2
3. 说明3
4. 说明4
"""
scenario_result = u"""1. 分析结果1
2. 分析结果2
3. 分析结果3
4. 分析结果4
"""

import os
import shutil

from Parser import html_body_parser
from report import clean_tmp_dir
from report import get_data_from_path
from report import Report

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  

if __name__ == '__main__':
    clean_tmp_dir()
    html_body_list = get_data_from_path(result_path_list)
    performance_monitor_summary_data, lr_report_summary_data = html_body_parser(html_body_list)
    merge_report = Report(performance_monitor_summary_data,
            lr_report_summary_data, 
            scenario_name, 
            version, 
            scenario_explain, 
            scenario_result,
            html_body_list)
    merge_report.work()
