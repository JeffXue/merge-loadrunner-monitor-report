# -*- coding:utf-8 -*-

report_header = """
<html>
<style type="text/css">
th{
    background: #a6caf0;
    align:center;
    vertical-align:middle;
}
td{
    background:#bfbfbf;
    font-weight:bold;
}
</style>
<head>
    <title>%(scenario_name)s</title>
    <link href="resource/bootstrap.min.css" rel="stylesheet" media="screen">
    <script src="resource/jquery.min.js"></script>
    <script src="resource/bootstrap.min.js"></script>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
<body>
<div class="container">

<h2>%(scenario_name)s性能测试报告</h2>
<table class="table table-bordered">
    <tr>
        <th>场景名称</th>
        <td colspan='6'>%(scenario_name)s</td>
        <th>版本</th>
        <td colspan="3">%(version)s</td>
    </tr>
    <tr>
        <th>场景说明</th>
        <td colspan='10'>%(scenario_explain)s</td>
    </tr>
"""

report_lr_title1 = """
    <tr>
        <th rowspan="%(total_rowspan)d">测试数据</th>
        <th>并发</th>
        <th colspan="4">事务</th>
        <th>通过事务数</th>
        <th>平均响应时间(s)</th>
        <th>90%%响应时间(s)</th>
        <th>TPS</th>
        <th>成功率</th>
    </tr>
"""

report_lr_title2 = """
    <tr>
        <th rowspan="%(total_rowspan)d">测试数据</th>
        <th>并发</th>
        <th colspan="4">事务</th>
        <th>通过事务数</th>
        <th>平均响应时间(s)</th>
        <th>90%响应时间(s)</th>
        <th>点击率</th>
        <th>成功率</th>
    </tr>
"""

report_lr_data_null = """
    <tr>
        <td align="center" colspan="10">N/A</td>
    </tr>
"""

report_lr_data_too_much = """
    <tr>
        <td rowspan="%(lr_rowspan)s">%(vuser)s</td>
        <td colspan="7">数据过多，请查看详情</td>
        <td>%(hit)s</td>
        <td>%(total_success_rate)s(Total)</td>
    </tr>
"""

report_lr_data_first = """
    <tr>
        <td rowspan="%(lr_rowspan)s">%(vuser)s</td>
        <td colspan="4">%(name)s</td>
        <td>%(transaction_pass)s</td>
        <td>%(trs)s</td>
        <td>%(trs_90percent)s</td>
        <td>%(tps)s</td>
        <td>%(success_rate)s%%</td>
    </tr>
"""

report_lr_data_normal = """
    <tr>
        <td colspan="4">%(name)s</td>
        <td>%(transaction_pass)s</td>
        <td>%(trs)s</td>
        <td>%(trs_90percent)s</td>
        <td>%(tps)s</td>
        <td>%(success_rate)s%%</td>
    </tr>
"""
report_pm_header = """
    <tr>
        <th>主机名</th>
        <th>CPU</th>
        <th>IOWait</th>
        <th>Load1</th>
        <th>Memory</th>
        <th>写磁盘(MB/s)</th>
        <th>读磁盘(MB/s)</th>
        <th>Eth接收(MB/s)</th>
        <th>Eth发送(MB/s)</th>
        <th>数据库连接数</th>
    </tr>
"""

report_pm_body_null = """
    <tr>
        <td colspan="10">N/A</td>
    </tr>
"""

report_pm_body_normal = """
    <tr>
        <td>%(hostname)s</td>
        <td>%(cpu)s%%</td>
        <td>%(iowait)s%%</td>
        <td>%(load1)s</td>
        <td>%(memory)s%%</td>
        <td>%(write_disk_speed)s</td>
        <td>%(read_disk_speed)s</td>
        <td>%(eth_received)s</td>
        <td>%(eth_transmitted)s</td>
        <td>%(mysql_threads_connected)s</td>
    </tr>
"""

report_result = """
    <tr>
        <th>分析结果</th>
        <td colspan='10'>%(scenario_result)s</td>
    </tr>
</table>
"""

report_nav_tab_header = """
<ul id="checkTab" class="nav nav-tabs">
"""

report_nav_dropdown_body = """
    <li class="dropdown">
        <a href="#" id="%(type)s" class="dropdown-toggle" data-toggle="dropdown">%(type)s<b class="caret"></b></a>
        <ul class="dropdown-menu" role="menu" aria-labelledby="%(type)s">
"""

report_nav_tab_body = """
            <li><a href="#%(id)d" tabindex="-1" data-toggle="tab">%(hostname)s</a></li>
"""

report_nav_dropdown_end = """
        </ul>
    </li>
"""

report_nav_tab_end = """
</ul>
"""

report_tab_content_header = """
<div id="checkTabContent" class="tab-content">
"""

report_tab_content_body = """
    <div class="tab-pane fade" id="%(id)d">
        %(html_body)s
    </div>

"""

report_end = """
</div>
</body>
</html>
"""
