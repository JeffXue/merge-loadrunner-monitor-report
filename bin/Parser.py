# -*- coding:utf-8 -*-
from sgmllib import SGMLParser

server_eth = 'server_eth1'

class ReportSummaryData():

    def __init__(self, scenario, performance_monitor_summary_data, lr_report_summary_data,
                 lr_rowspan, pm_rowspan, too_much_data_flag, history_ids):
        self.scenario = scenario
        self.performance_monitor_summary_data = performance_monitor_summary_data
        self.lr_report_summary_data = lr_report_summary_data.get('data')
        self.vuser = lr_report_summary_data.get('vuser')
        self.hit = lr_report_summary_data.get('hit')
        self.total_success_rate = lr_report_summary_data.get('total_success_rate')
        self.lr_rowspan = lr_rowspan
        self.pm_rowspan = pm_rowspan
        self.too_much_data_flag = too_much_data_flag
        self.history_ids = history_ids


class LRReportHTMLSummaryData():

    def __init__(self):
        self.name = 'N/A'
        self.tps = 'N/A'
        self.trs = 'N/A'
        self.trs_90percent = 'N/A'
        self.transaction_pass = 'N/A'
        self.transaction_failed = 'N/A'
        self.success_rate = 'N/A'


class LRReportHTMLParser(SGMLParser):

    def reset(self):
        self.summary_data = []
        self.vuser = 'N/A'
        self.total_hit = 'N/A'
        self.success_rate = 'N/A'
        self.hit_flag = False
        self.vuser_flag = False

        self.trs_start_flag = False
        self.trs_count = 0

        self.tps_start_flag = False
        self.tps_count = 0
        self.tps_name = 'N/A'

        SGMLParser.reset(self)

    def start_table(self, attrs):
        pass

    def end_table(self):
        self.trs_start_flag = False
        self.tps_start_flag = False

    def start_img(self, attrs):
        self.trs_start_flag = False
        self.tps_start_flag = False

    def end_img(self):
        pass

    def start_tr(self, attrs):
        if self.trs_start_flag:
            self.summary_data.append(LRReportHTMLSummaryData())
            self.trs_count = 0
            if len(self.summary_data) > 1:
                self.summary_data[-2].success_rate = '%0.2f' % float(self.summary_data[-2].transaction_pass*100.00/float(self.summary_data[-2].transaction_pass+self.summary_data[-2].transaction_failed))
        if self.tps_start_flag:
            self.tps_count = 0

    def end_tr(self):
        self.hit_flag = False
        self.vuser_flag = False

    def start_td(self, attrs):
        if self.trs_start_flag:
            self.trs_count += 1
        if self.tps_start_flag:
            self.tps_count += 1

    def end_td(self):
        pass

    def handle_data(self, data):
        if self.hit_flag:
            self.total_hit = data.replace(',', '')
        if self.vuser_flag:
            self.vuser = data
        if self.trs_start_flag:
            if self.trs_count == 1:
                self.summary_data[-1].name = data
            if self.trs_count == 3:
                self.summary_data[-1].trs = data
            if self.trs_count == 5:
                self.summary_data[-1].trs_90percent = data
            if self.trs_count == 6:
                self.summary_data[-1].transaction_pass = int(data.replace(',', ''))
            if self.trs_count == 7:
                self.summary_data[-1].transaction_failed = int(data.replace(',', ''))
        if self.tps_start_flag:
            if self.tps_count == 1:
                self.tps_name = data.strip()
            if self.tps_count == 2:
                for index, item in enumerate(self.summary_data):
                    if item.name+':Pass' == self.tps_name:
                        self.summary_data[index].tps = data
        if data == u'并发虚拟用户数':
            self.vuser_flag = True
        if data == u'点击率/秒':
            self.hit_flag = True
        if data.find(u'成功率') != -1:
            self.success_rate = data.split(':')[-1].strip().replace(r'%', '')
        if data == u'停止事务数':
            self.trs_start_flag = True
        if data == u'每秒处理事务平均数':
            self.tps_start_flag = True

    def work(self):
        return {'data': self.summary_data[:-1],
                'vuser': self.vuser,
                'hit': self.total_hit,
                'total_success_rate': self.success_rate}


class PerformanceMonitorHTMLSummaryData():

    def __init__(self):
        self.hostname = 'N/A'
        self.cpu = 'N/A'
        self.memory = 'N/A'
        self.iowait = 'N/A'
        self.write_disk_speed = 'N/A'
        self.read_disk_speed = 'N/A'
        self.load1 = 'N/A'
        self.eth_received = 'N/A'
        self.eth_transmitted = 'N/A'
        self.mysql_threads_connected = 'N/A'


class PerformanceMonitorHTMLParser(SGMLParser):

    def reset(self):
        self.summary_data = PerformanceMonitorHTMLSummaryData()
        self.hostname_flag = False

        self.cpu_flag = False
        self.cpu_count_flag = False
        self.cpu_count = 0

        self.load1_flag = False
        self.load1_count_flag = False
        self.load1_count = 0

        self.memory_flag = False
        self.memory_count_flag = False
        self.memory_count = 0

        self.iowait_flag = False
        self.iowait_count_flag = False
        self.iowait_count = 0

        self.iowrite_flag = False
        self.iowrite_count_flag = False
        self.iowrite_count = 0

        self.ioread_flag = False
        self.ioread_count_flag = False
        self.ioread_count = 0

        self.eth_flag = False

        self.eth_received_flag = False
        self.eth_received_count_flag = False
        self.eth_received_count = 0

        self.eth_transmitted_flag = False
        self.eth_transmitted_count_flag = False
        self.eth_transmitted_count = 0

        self.mysql_flag = False

        self.mysql_threads_flag = False
        self.mysql_threads_count_flag = False
        self.mysql_threads_count = 0

        SGMLParser.reset(self)

    def start_tr(self, attrs):
        pass

    def end_tr(self):
        self.cpu_flag = False
        self.cpu_count_flag = False
        self.cpu_count = 0

        self.memory_flag = False
        self.memory_count_flag = False
        self.memory_count = 0

        self.iowait_flag = False
        self.iowait_count_flag = False
        self.iowait_count = 0

        self.iowrite_flag = False
        self.iowrite_count_flag = False
        self.iowrite_count = 0

        self.ioread_flag = False
        self.ioread_count_flag = False
        self.ioread_count = 0

        self.load1_flag = False
        self.load1_count_flag = False
        self.load1_count = 0

        self.eth_received_flag = False
        self.eth_received_count_flag = False
        self.eth_recieved_count = 0

        self.eth_transmitted_flag = False
        self.eth_transmitted_count_flag = False
        self.eth_transmitted_count = 0

        self.mysql_threads_flag = False
        self.mysql_threads_count_flag = False
        self.mysql_threads_count = 0

        self.hostname_flag = False

    def start_td(self, attrs):
        if self.eth_flag:
            for key, value in attrs:
                if key == 'rowspan':
                    self.eth_flag = False
        if self.mysql_flag:
            for key, value in attrs:
                if key == 'rowspan':
                    self.mysql_flag = False
        if self.cpu_count_flag:
            self.cpu_count += 1
            if self.cpu_count == 3:
                self.cpu_flag = True
                self.cpu_count_flag = False
                self.cpu_count = 0
        if self.memory_count_flag:
            self.memory_count += 1
            if self.memory_count == 3:
                self.memory_flag =  True
                self.memory_count_flag = False
                self.memory_count = 0
        if self.iowait_count_flag:
            self.iowait_count += 1
            if self.iowait_count == 3:
                self.iowait_flag = True
                self.iowait_count_flag = False
                self.iowait_count = 0
        if self.iowrite_count_flag:
            self.iowrite_count += 1
            if self.iowrite_count == 3:
                self.iowrite_flag = True
                self.iowrite_count_flag = False
                self.iowrite_count = 0
        if self.load1_count_flag:
            self.load1_count += 1
            if self.load1_count == 3:
                self.load1_flag = True
                self.load1_count_flag = False
                self.load1_count = 0
        if self.ioread_count_flag:
            self.ioread_count += 1
            if self.ioread_count == 3:
                self.ioread_flag = True
                self.ioread_count_flag = False
                self.ioread_count = 0
        if self.eth_received_count_flag:
            self.eth_received_count += 1
            if self.eth_received_count == 3:
                self.eth_received_flag = True
                self.eth_received_count_flag = False
                self.eth_received_count = 0
        if self.eth_transmitted_count_flag:
            self.eth_transmitted_count += 1
            if self.eth_transmitted_count == 3:
                self.eth_transmitted_flag = True
                self.eth_transmitted_count_flag = False
                self.eth_transmitted_count = 0
        if self.mysql_threads_count_flag:
            self.mysql_threads_count += 1
            if self.mysql_threads_count == 3:
                self.mysql_threads_flag = True
                self.mysql_threads_count_flag = False
                self.mysql_threads_count = 0

    def end_td(self):
        self.cpu_flag = False
        self.memory_flag = False
        self.iowait_flag = False
        self.iowrite_flag = False
        self.load1_flag = False
        self.ioread_flag = False
        self.eth_received_flag = False
        self.eth_transmitted_flag = False
        self.mysql_threads_flag = False

    def handle_data(self, data):
        if self.hostname_flag:
            self.summary_data.hostname = data
        if self.cpu_flag:
            self.summary_data.cpu = data
        if self.memory_flag:
            self.summary_data.memory = data
        if self.iowait_flag:
            self.summary_data.iowait = data
        if self.iowrite_flag:
            self.summary_data.write_disk_speed = data
        if self.load1_flag:
            self.summary_data.load1 = data
        if self.ioread_flag:
            self.summary_data.read_disk_speed = data
        if self.eth_received_flag:
            self.summary_data.eth_received = data
        if self.eth_transmitted_flag:
            self.summary_data.eth_transmitted = data
        if self.mysql_threads_flag:
            self.summary_data.mysql_threads_connected = data
        if data == u'主机名':
            self.hostname_flag = True
        if data == 'used(%)':
            self.cpu_count_flag = True
        if data == 'memused--(%)':
            self.memory_count_flag = True
        if data == 'iowait(%)':
            self.iowait_count_flag = True
        if data == 'wrtn/s(MB)' or data == 'MBwrtn/s':
            self.iowrite_count_flag = True
        if data == 'read/s(MB)' or data == 'MBread/s':
            self.ioread_count_flag = True
        if self.eth_flag:
            if data == 'rx/s(MB)' or data == 'rxMB/s':
                self.eth_received_count_flag = True
            if data == 'tx/s(MB)' or data == 'txMB/s':
                self.eth_transmitted_count_flag = True
        if data == server_eth:
            self.eth_flag = True
        if self.mysql_flag:
            if data == 'Threads' or data == 'Threads_connected':
                self.mysql_threads_count_flag = True
        if data == 'mysql':
            self.mysql_flag = True
        if data == 'ldavg-1':
            self.load1_count_flag = True

    def work(self):
        return self.summary_data


def html_body_parser(html_body_list):
    performance_monitor_summary_data = []
    lr_report_summary_data = {}
    for html_body_dic in html_body_list:
        if html_body_dic.get('type') == 'performance_monitor':
            performance_monitor_parser = PerformanceMonitorHTMLParser()
            for line in html_body_dic.get('html_body').split('\n'):
                performance_monitor_parser.feed(line.strip())
            performance_monitor_summary_data.append(performance_monitor_parser.work())
        if html_body_dic.get('type') == 'lr_report':
            lr_report_parser = LRReportHTMLParser()
            for line in html_body_dic.get('html_body').split('\n'):
                lr_report_parser.feed(line.strip())
            lr_report_summary_data = lr_report_parser.work()
    if len(performance_monitor_summary_data) == 0:
        performance_monitor_summary_data.append(PerformanceMonitorHTMLSummaryData())
    if not lr_report_summary_data.has_key('data'):
        lr_report_summary_data = {'data': [LRReportHTMLSummaryData()],
                                  'vuser': 'N/A',
                                  'hit': 'N/A',
                                  'total_success_rate': 'N/A'}
    return performance_monitor_summary_data, lr_report_summary_data

