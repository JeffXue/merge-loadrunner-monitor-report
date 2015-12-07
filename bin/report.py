# -*- coding:utf-8 -*-
import os
import re
import sys
import time
import shutil
import ConfigParser

import util
from ftplib import FTP
from template import *

reload(sys)
sys.setdefaultencoding('utf8')  

def clean_tmp_dir():
    shutil.rmtree('../tmp')
    os.mkdir('../tmp')
    os.mkdir('../tmp/resource')
    shutil.copy('../resource/bootstrap.min.css', '../tmp/resource')
    shutil.copy('../resource/bootstrap.min.js', '../tmp/resource')
    shutil.copy('../resource/jquery.min.js', '../tmp/resource')

def get_data_from_path(result_path_list):
    ignore_png = ['bgnav.png', 'dot_pewter.png', 'lab_analreports.png',
            'logo_lr.png', 'LR_anal_reports.png', 'tbic_toexcel.png', 'top_grad.png']
    html_body_list = []
    for path in result_path_list:
        for parent,dirnames,filenames in os.walk(path):
            for filename in filenames:
                if filename in ignore_png:
                    continue
                if filename.endswith('.png'):
                    shutil.copy(os.path.join(parent, filename), '../tmp/resource')
                if filename.find('monitor_statistical_data') != -1 and filename.endswith('.html'):
                    html_body = ''
                    with open(os.path.join(parent, filename), 'r') as f:
                        for line in f.readlines():
                            html_body += line

                    html_body_list.append({'type': 'performance_monitor', 'html_body': html_body})
                if filename.find('lr_statistical_data') != -1 and filename.endswith('.html'):
                    html_body = ''
                    with open(os.path.join(parent, filename), 'r') as f:
                        for line in f.readlines():
                            html_body += line
                    html_body_list.append({'type': 'lr_report', 'html_body': html_body})
    return html_body_list

def decorate_tab_html_body(html_body):
    temp = html_body.split('<body>')[1].split('</body>')[0]
    temp = temp.replace('href="', 'href="resource/').replace('img src="', 'img src="resource/')
    temp = temp.replace('An_Report1/', '')
    temp = temp.replace('<table border="0" cellpadding="5" cellspacing="2"  width="60%">', '<table class="table table-bordered">')
    new = temp.replace('<table border="0" cellpadding="5" cellspacing="2"  width="50%">', '<table class="table table-bordered">')
    return new

class Report:

    def __init__(self, performance_monitor_summary_data, lr_report_summary_data,
            scenario_name, version, scenario_explain, scenario_result, html_body_list):
        self.pm_summary_data = performance_monitor_summary_data
        self.lr_summary_data = lr_report_summary_data.get('data')
        self.scenario_name = scenario_name.replace('\n', '<br/>').replace(' ', '&nbsp;')
        self.version = version.replace('\n', '<br/>').replace(' ', '&nbsp;')
        self.scenario_explain = scenario_explain.replace('\n', '<br/>').replace(' ', '&nbsp;')
        self.scenario_result = scenario_result.replace('\n', '<br/>').replace(' ', '&nbsp;')

        timestramp = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        self.report_file = '../tmp/'+scenario_name+'_'+version+'_'+u'性能测试报告'+'_'+timestramp+'.html'

        self.vuser = lr_report_summary_data.get('vuser')
        self.hit = lr_report_summary_data.get('hit')
        self.total_success_rate = lr_report_summary_data.get('total_success_rate')
        self.lr_html_body = []
        self.pm_html_body = []

        for html_body in html_body_list:
            if html_body['type'] == 'lr_report':
                self.lr_html_body.append(decorate_tab_html_body(html_body['html_body']))
            if html_body['type'] == 'performance_monitor':
                self.pm_html_body.append(decorate_tab_html_body(html_body['html_body']))

        if len(lr_report_summary_data.get('data')) > 10:
            self.too_much_data_flag = True
            self.lr_rowspan = 1
        else:
            self.too_much_data_flag = False
            self.lr_rowspan = len(lr_report_summary_data.get('data'))
        self.pm_rowspan = len(performance_monitor_summary_data)
        self.total_rowspan = self.lr_rowspan + self.pm_rowspan + 2

        config = ConfigParser.ConfigParser()
        with open('../conf/report.ini', 'r') as cfg_file:
            config.readfp(cfg_file)
        self.ftp_flag = int(config.get('ftp', 'flag'))
        self.ftp_ip = config.get('ftp', 'ip')
        self.ftp_user =  config.get('ftp', 'user')
        self.ftp_password = config.get('ftp', 'password')

    def merge_report(self):
        data_dic = {'scenario_name': self.scenario_name, 'version': self.version,
                'scenario_explain': self.scenario_explain, 'scenario_result': self.scenario_result,
                'total_rowspan': self.total_rowspan, 'vuser': self.vuser,
                'hit': self.hit, 'total_success_rate': self.total_success_rate,
                'lr_rowspan': self.lr_rowspan, 'pm_rowspan': self.pm_rowspan}

        html_body = report_header % data_dic
        if self.too_much_data_flag:
            html_body += report_lr_title2 % data_dic
        else:
            html_body += report_lr_title1 % data_dic
        if self.lr_summary_data[0].name == 'N/A':
            html_body += report_lr_data_null 
        else:
            if self.too_much_data_flag:
                html_body += report_lr_data_too_much % data_dic
            else:
                for i in xrange(len(self.lr_summary_data)):
                    lr_data = self.lr_summary_data[i]
                    data_dic['name'] = lr_data.name
                    data_dic['transaction_pass'] = lr_data.transaction_pass
                    data_dic['trs'] = lr_data.trs
                    data_dic['trs_90percent'] = lr_data.trs_90percent
                    data_dic['tps'] = lr_data.tps
                    data_dic['success_rate'] = lr_data.success_rate
                    if i == 0:
                        html_body += report_lr_data_first % data_dic
                    else:
                        html_body += report_lr_data_normal % data_dic
        
        html_body += report_pm_header
        if self.pm_summary_data[0].hostname == 'N/A':
            html_body += report_pm_body_null
        else:
            for data in self.pm_summary_data:
                data_dic['hostname'] = data.hostname
                data_dic['cpu'] = data.cpu
                data_dic['iowait'] = data.iowait
                data_dic['load1'] = data.load1
                data_dic['memory'] = data.memory
                data_dic['write_disk_speed'] = data.write_disk_speed
                data_dic['read_disk_speed'] = data.read_disk_speed
                data_dic['eth_received'] = data.eth_received
                data_dic['eth_transmitted'] = data.eth_transmitted
                data_dic['mysql_threads_connected'] = data.mysql_threads_connected
                html_body += report_pm_body_normal % data_dic
        html_body += report_result % data_dic
        

        html_body += report_nav_tab_header
        if len(self.lr_html_body):
            lr_nav_data_dic = {'hostname': 'window', 'type': u'LoadRunner运行记录', 'id': 999}
            html_body += report_nav_dropdown_body % lr_nav_data_dic
            html_body += report_nav_tab_body % lr_nav_data_dic
            html_body += report_nav_dropdown_end
        
        if len(self.pm_html_body):
            html_body += report_nav_dropdown_body % {'type': u'服务器资源监控记录'}
            for i in xrange(len(self.pm_summary_data)):
                data = self.pm_summary_data[i]
                pm_nav_data_dic = {'hostname': data.hostname, 'id': i}
                html_body += report_nav_tab_body % pm_nav_data_dic
            html_body += report_nav_dropdown_end
        html_body += report_nav_tab_end

        html_body += report_tab_content_header
        if len(self.lr_html_body):
            lr_report_data_dic = {'html_body': self.lr_html_body[0], 'id': 999}
            html_body += report_tab_content_body % lr_report_data_dic
        
        if len(self.pm_html_body):
            for i in xrange(len(self.pm_html_body)):
                data = self.pm_html_body[i]
                pm_report_data_dic = {'html_body': data, 'id': i}
                html_body += report_tab_content_body % pm_report_data_dic
        html_body += report_end
        
        f = open(self.report_file, "w")
        try:
            f.write(html_body)
        finally:
            f.close()

    def ftp_upload(self):
        ftp = FTP()
        ftp.set_debuglevel(0)
        ftp.connect(self.ftp_ip, '21')
        ftp.login(self.ftp_user, self.ftp_password)
        try:
            ftp.mkd('report')
        except Exception, e:
            print ("[INFO]ftp directory: report existed")
            print e
        ftp.cwd('report')
        ftp.mkd(os.path.basename(self.report_file).split(".html")[0].encode('gbk'))
        ftp.cwd(os.path.basename(self.report_file).split(".html")[0].encode('gbk'))
        buffer_size = 1024
        file_handler = open(self.report_file, 'rb')
        ftp.storbinary('STOR %s' % os.path.basename(self.report_file).encode('gbk'), file_handler, buffer_size)
        ftp.mkd('resource')
        ftp.cwd('resource')
        for datafile in util.get_dir_files('../tmp/resource'):
            file_handler = open('../tmp/resource/' + datafile, 'rb')
            ftp.storbinary('STOR %s' % datafile, file_handler, buffer_size)
        ftp.set_debuglevel(0)
        file_handler.close()
        ftp.quit()

    def work(self):
        self.merge_report()
        if self.ftp_flag:
            self.ftp_upload()

