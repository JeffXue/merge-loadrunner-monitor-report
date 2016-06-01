# -*- coding:utf-8 -*-
import os
import re
import sys
import time
import shutil
import ConfigParser

import util
from ftplib import FTP
from jinja2 import Environment, FileSystemLoader

reload(sys)
sys.setdefaultencoding('utf8')


env = Environment(loader=FileSystemLoader('./templates'))
template = env.get_template('report.html')


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
        for parent, dirnames, filenames in os.walk(path):
            for filename in filenames:
                if filename in ignore_png:
                    continue
                if filename.endswith('.png'):
                    shutil.copy(os.path.join(parent, filename), '../tmp/resource')
                if filename.find('monitor') != -1 and filename.endswith('.html'):
                    html_body = ''
                    with open(os.path.join(parent, filename), 'r') as f:
                        for line in f.readlines():
                            html_body += line

                    html_body_list.append({'type': 'performance_monitor', 'html_body': html_body})
                if filename.find('lr') != -1 and filename.endswith('.html'):
                    html_body = ''
                    with open(os.path.join(parent, filename), 'r') as f:
                        for line in f.readlines():
                            html_body += line
                    html_body_list.append({'type': 'lr_report', 'html_body': html_body})
    return html_body_list


def decorate_tab_html_body(html_body):
    temp = html_body.split('<body>')[1].split('</body>')[0]
    temp = temp.replace('href="', 'href="resource/').replace('img src="', 'img src="resource/')
    new = temp.replace('An_Report1/', '')
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
        self.ftp_user = config.get('ftp', 'user')
        self.ftp_password = config.get('ftp', 'password')

    def merge_report(self):

        html_body = template.render(scenario_name=self.scenario_name,
                                    version=self.version,
                                    scenario_explain=self.scenario_explain,
                                    scenario_result=self.scenario_result,
                                    total_rowspan=self.total_rowspan,
                                    vuser=self.vuser,
                                    hit=self.hit,
                                    total_success_rate=self.total_success_rate,
                                    lr_rowspan=self.lr_rowspan,
                                    pm_rowspan=self.pm_rowspan,
                                    too_much_data_flag=self.too_much_data_flag,
                                    lr_summary_data=self.lr_summary_data,
                                    pm_summary_data=self.pm_summary_data,
                                    lr_html_body=self.lr_html_body,
                                    pm_html_body=self.pm_html_body)
        
        f = open(self.report_file, "w")
        try:
            f.write(html_body.encode('utf-8'))
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

