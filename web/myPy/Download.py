#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import xlsxwriter,os
from datetime import timedelta, datetime
from django.http import StreamingHttpResponse
from django.utils.http import  urlquote_plus
from web.models import Thwdayrpt, Tztedayrpt, Tfhdayrpt

# 本类中分为两个主要方法，都是在当需要下载相关的文件时才会进行操作
# createFile主要是生成excel文件，将传递来的之前获得的数据进行操作生成相关的excel文件
# downloadFile方法是传输之前生成的文件，下载中文名在火狐中会乱码，但是在别的浏览器中正常


class Download:

    def __init__(self,data):
        self.data = data

    @staticmethod
    def setAddDay(date):
        setAddDay = date + timedelta(days=1)
        return setAddDay

    # 时间转换成字符串,格式为2008-01-01
    @staticmethod
    def datetostr(date):
        return str(date)[0:10]

    def createFile(self):
        day = int(self.data['day'])
        platformname = self.data['platformname']
        date = self.data['date']
        startdate = self.data['wRptstartdate']
        enddate = self.data['wRptenddate']

        # 华为中兴日报标题
        titledRpt = ['节点名称', '平均码流(Mbps)', '设计带宽(Gbps)', '输出带宽(Gbps)', '输出带宽占比%', 'EPG总并发(个)', 'EPG峰值并发(个)', 'EPG并发率%',
                     '流媒体总并发(个)', '流媒体峰值并发(个)', '流媒体并发率%', '存储空间(T)', '已使用空间(T)', '空间使用率%']  # 标题部分
        # 烽火日报标题
        titlefhdRpt = ['节点名称', '区域', '平均码流', '设计带宽(Gbps)', '输出带宽(Gbps)', '输出带宽占比%', '流媒体总并发(个)', '流媒体峰值并发(个)',
                       '流媒体并发率%',
                       '存储空间(T)', '已使用空间(T)', '空间使用率%', '芒果tv(Mbps)', '芒果tv(%)', '4K(Mbps)', '4K(%)', '优酷(Mbps)',
                       '优酷(%)',
                       '机顶盒下载(Mbps)', '机顶盒下载(%)', '百事通回源(Mbps)', '百事通回源(%)', '测速(Mbps)', '测速(％)', '播播(Mbps)', '播播(%)',
                       '天翼视讯(Mbps)', '天翼视讯(%)', '教育中心(Mbps)', '教育中心(%)', '华数(Mbps)', '华数(%)', '嘉攸(Mbps)', '嘉攸(%)',
                       '嘉攸直播(Mbps)', '嘉攸直播(%)']
        # 华为中兴周报标题
        titlewRpt = ['日期','流媒体并发(个)','epg并发(个)','流量数据(GBps)']
        # 烽火部分的周报标题
        titlefhwRpt = ['日期', '设计带宽(GBps)','输出带宽(GBps)','输出带宽占比%','流媒体总并发(个)',
                        '流媒体峰值并发(个)','流媒体并发率%','芒果tv(Mbps)', '4K(Mbps)', '优酷(Mbps)',
                       '机顶盒下载(Mbps)', '百事通回源(Mbps)',  '测速(Mbps)', '播播(Mbps)','天翼视讯(Mbps)',
                       '教育中心(Mbps)', '华数(Mbps)', '嘉攸(Mbps)','嘉攸直播(Mbps)']

        # 日报部分
        if day == 1:

            row = 2
            col = 0
            # 查询天数与生成日期差异，所以要先加一天
            tmp_dayDate = datetime.strptime(date, "%Y-%m-%d")
            tmp_dayDate = self.setAddDay(tmp_dayDate)
            checkdate = self.datetostr(tmp_dayDate)

            # 三个平台分别操作不同的类（获得数据库数据）
            if platformname == 'HW':
                excelname = os.getcwd() + '/files/' + '华为并发日报' + date + '.xlsx'  # excel文档名字
            elif platformname == 'zte':
                excelname = os.getcwd() + '/files/' + '中兴并发日报' + date + '.xlsx'  # excel文档名字
            elif platformname == 'FH':
                excelname = os.getcwd() + '/files/' + '烽火并发日报' + date + '.xlsx'  # excel文档名字

            # 判断是否已经生成了相关的文件，如果生成了就不执行生成部分
            if os.path.exists(excelname):
                print('OK, the file exists!')
            else:
                workbook = xlsxwriter.Workbook(excelname)
                # 一些表格的设置
                formattitle = workbook.add_format()
                formattitle.set_bold(2)
                formattitle.set_border(2)
                formattitle.set_align('center')
                formattitle.set_align('vcenter')
                formathead = workbook.add_format()
                formathead.set_bold(3)
                formathead.set_align('center')
                formattitle.set_align('vcenter')
                formathead.set_font_size(20)
                formatcell = workbook.add_format()
                formatcell.set_border(1)
                formatcell.set_align('center')
                formattitle.set_align('vcenter')

                # 设置标题，取数据
                if platformname == 'HW':
                    worksheet = workbook.add_worksheet('华为')
                    worksheet.merge_range(0, 0, 0, 13,'华为并发日报' + date,formathead)
                    sql = Thwdayrpt.objects.filter(updatetime__contains=checkdate). \
                        values_list('nodename', 'avgwidth',
                                    'sjjdll', 'peakjdll', 'jdllper',
                                    'sjepgbf', 'peakepgbf', 'epgbfper',
                                    'sjhmsbf', 'peakhmsbf', 'hmsbfper',
                                    'sjdbkj', 'peakdbkj', 'dbkjper')
                    worksheet.write_row(1, 0, titledRpt, formattitle)
                    worksheet.set_column(0, 1, 24)
                    worksheet.set_column(1, 14, 20)

                elif platformname == 'zte':
                    worksheet = workbook.add_worksheet('中兴')
                    worksheet.merge_range(0, 0, 0, 13,'中兴并发日报' + date,formathead)
                    sql = Tztedayrpt.objects.filter(updatetime__contains=checkdate). \
                        values_list('nodename', 'avgwidth',
                                    'sjjdll', 'peakjdll', 'jdllper',
                                    'sjepgbf', 'peakepgbf', 'epgbfper',
                                    'sjhmsbf', 'peakhmsbf', 'hmsbfper',
                                    'sjdbkj', 'peakdbkj', 'dbkjper')
                    worksheet.write_row(1, 0, titledRpt, formattitle)
                    worksheet.set_column(0, 1, 24)
                    worksheet.set_column(1, 14, 20)

                elif platformname == 'FH':
                    worksheet = workbook.add_worksheet('烽火')
                    worksheet.merge_range(0, 0, 0, 35,'烽火并发日报' + date,formathead)
                    sql = Tfhdayrpt.objects.filter(updatetime__contains=checkdate). \
                        values_list('nodecname','quju','avgwidth',
                                    'sjjdll','peakjdll','jdllper',
                                    'sjjdbf','peakjdbf','jdbfper',
                                    'sjdbkj','peakdbkj','dbkjper',
                                    'mangguoll','mangguoper','number_4kll','number_4kper',
                                    'youkull','youkuper','stbdown',
                                    'stbdownper','bestvll','bestvoper',
                                    'cesull','cesuper','boboll','boboper',
                                    'tianyill','tianyiper','jiaoyull','jiaoyuper',
                                    'huasull','huasuper','jiayoull',
                                    'jiayouper','jylivell','jyliveper')
                    worksheet.write_row(1, 0, titlefhdRpt,formattitle)
                    worksheet.set_column(0, 1, 24)
                    worksheet.set_column(1, 35, 20)

                # 获取得到的数据写入到excel中
                for x in sql.iterator():
                    for y in x:
                        if type(y) == str:
                            worksheet.write_row(row,col,[y],formatcell)
                            col += 1

                        elif platformname != 'FH':
                            if (col == 4 or col == 7 or col == 10 or col == 13) and y >= 90:
                                # 百分比超过90显示红色
                                worksheet.write_number(row, col, y,workbook.add_format({'fg_color':'#FFC7CE','border':1,'align':'center'}))
                            elif (col == 4 or col ==7 or col == 10 or col == 13) and y <= 20:
                                # 百分比低于20显示黄色
                                worksheet.write_number(row, col, y,workbook.add_format({'fg_color':'#FFD700','border':1,'align':'center'}))
                            else:
                                worksheet.write_number(row, col, y,formatcell)
                            col += 1

                        elif platformname == 'FH':
                            if (col == 5 or col == 8 or col == 11) and y >= 90:
                                # 百分比超过90显示红色
                                worksheet.write_number(row, col, y,workbook.add_format({'fg_color':'#FFC7CE','border':1,'align':'center'}))
                            elif (col == 5 or col ==8 or col == 11) and y <= 20:
                                # 百分比低于20显示黄色
                                worksheet.write_number(row, col, y,workbook.add_format({'fg_color':'#FFD700','border':1,'align':'center'}))
                            else:
                                worksheet.write_number(row, col, y,formatcell)
                            col += 1
                    col = 0
                    row += 1

                worksheet.freeze_panes('B3')
                workbook.close()
                print(excelname)

        # 周报部分
        elif day > 1:

            row = 2
            # 把两个时间都转成xxxx-xx-xx形式
            tmp_startdate = datetime.strptime(startdate, "%Y-%m-%d")
            tmp_enddate = datetime.strptime(enddate, "%Y-%m-%d")
            startdate = self.datetostr(tmp_startdate)
            enddate = self.datetostr(tmp_enddate)

            # 三个平台分别操作不同的类（获得数据库数据）
            if platformname == 'HW':
                excelname = os.getcwd() + '\\files\\' + '华为并发月报' + startdate+ '至'+ enddate + '.xlsx'  # excel文档名字
            elif platformname == 'zte':
                excelname = os.getcwd() + '\\files\\' + '中兴并发月报' + startdate+ '至'+ enddate + '.xlsx'  # excel文档名字
            elif platformname == 'FH':
                excelname = os.getcwd() + '\\files\\' + '烽火并发月报' + startdate+ '至'+ enddate + '.xlsx'  # excel文档名字

            # 判断是否已经生成了相关的文件，如果生成了就不执行生成部分
            if os.path.exists(excelname):
                print('OK, the file exists!')
            else:
                workbook = xlsxwriter.Workbook(excelname)
                # 一些表格的设置
                formathead = workbook.add_format()
                formathead.set_bold(3)
                formathead.set_align('center')
                formathead.set_align('vcenter')
                formathead.set_font_size(20)

                formattitle = workbook.add_format()
                formattitle.set_border(1)
                formattitle.set_bold(2)
                formattitle.set_align('center')
                formattitle.set_align('vcenter')
                
                formatcell = workbook.add_format()
                formatcell.set_border(1)
                formatcell.set_align('center')
                formatcell.set_align('vcenter')

                # 设置标题，取数据
                if platformname == 'HW':
                    worksheet = workbook.add_worksheet('华为并发')
                    worksheet.merge_range(0, 0, 0, 5, '华为并发报表', formathead)
                    worksheet.write_row(1, 1, titlewRpt, formattitle)
                    worksheet.set_column(1, 2, 10)
                    worksheet.set_column(2, 4, 18)

                    while startdate <= enddate:
                        sumhms = 0
                        sumepg = 0
                        sumll = 0

                        tmp_dayDate = datetime.strptime(startdate, "%Y-%m-%d")
                        tmp_dayDate = self.setAddDay(tmp_dayDate)
                        checkdate = self.datetostr(tmp_dayDate)  # 比选择的开始日期多一天

                        sql = Thwdayrpt.objects.filter(updatetime__contains=checkdate). \
                            values_list('peakhmsbf', 'peakepgbf', 'peakjdll')
                        for peakhmsbf, peakepgbf, peakjdll in sql.iterator():
                            sumhms = sumhms + peakhmsbf
                            sumepg = sumepg + peakepgbf
                            sumll = sumll + peakjdll

                        worksheet.write_string(row, 1, startdate[5:],formatcell)
                        worksheet.write_number(row, 2, sumhms,formatcell)
                        worksheet.write_number(row, 3, sumepg,formatcell)
                        worksheet.write_number(row, 4, int(sumll),formatcell)
                        row += 1
                        startdate = checkdate

                    # 只有在选取超过一周的数据才会生成表格，和界面一样
                    if day > 6:
                        chart1 = workbook.add_chart({'type': 'line'})  # 创建表格,表格类型为离散型
                        chart2 = workbook.add_chart({'type': 'line'})
                        for i in ['C', 'D']:
                            chart1.add_series({
                                'categories': '=华为并发!$B$3:$B$' + str(day+3),  # 设置图表类型标签范围
                                'values': '=华为并发!$' + i + '$3:$' + i + '$' + str(day+3),  # 设置图表取值范围
                                'name': '=华为并发!$' + i + '$2',  # 设置名称
                            })
                        for i in ['E']:
                            chart2.add_series({
                                'categories': '=华为并发!$B$3:$B$' + str(day+3),
                                'values': '=华为并发!$' + i + '$3:$' + i + '$' + str(day+3),
                                'name': '=华为并发!$' + i + '$2',
                                'line': {'color': 'green'},
                            })

                        chart1.set_title({'name': u'并发数据图表'})  # 设置表格的title
                        chart2.set_title({'name': u'流量数据图表'})  # 设置表格的title
                        chart1.set_size({'width': 800, 'height': 400})  # 设置表格的大小
                        chart2.set_size({'width': 800, 'height': 400})
                        chart1.set_style(10)  # 设置表格的样式
                        chart2.set_style(10)
                        worksheet.insert_chart('G1', chart1)  # 插入表格，设置起始位置
                        worksheet.insert_chart('G22', chart2)

                    print('huawei file ok！')

                # 设置标题，取数据
                elif platformname == 'zte':
                    worksheet = workbook.add_worksheet('中兴并发')
                    worksheet.merge_range(0, 0, 0, 5, '中兴并发报表', formathead)
                    worksheet.write_row(1, 1, titlewRpt, formattitle)
                    worksheet.set_column(1, 2, 10)
                    worksheet.set_column(2, 4, 18)

                    while startdate <= enddate:
                        sumhms = 0
                        sumepg = 0
                        sumll = 0

                        tmp_dayDate = datetime.strptime(startdate, "%Y-%m-%d")
                        tmp_dayDate = self.setAddDay(tmp_dayDate)
                        checkdate = self.datetostr(tmp_dayDate)  # 比选择的开始日期多一天

                        sql = Tztedayrpt.objects.filter(updatetime__contains=checkdate). \
                            values_list('peakhmsbf', 'peakepgbf', 'peakjdll')
                        for peakhmsbf, peakepgbf, peakjdll in sql.iterator():
                            sumhms = sumhms + peakhmsbf
                            sumepg = sumepg + peakepgbf
                            sumll = sumll + peakjdll
                        worksheet.write_string(row, 1, startdate[5:],formatcell)
                        worksheet.write_number(row, 2, sumhms,formatcell)
                        worksheet.write_number(row, 3, sumepg,formatcell)
                        worksheet.write_number(row, 4, int(sumll),formatcell)
                        row += 1
                        startdate = checkdate

                    # 只有在选取超过一周的数据才会生成表格，和界面一样
                    if day > 6:
                        chart1 = workbook.add_chart({'type': 'line'})  # 创建表格,表格类型为离散型
                        chart2 = workbook.add_chart({'type': 'line'})
                        for i in ['C', 'D']:
                            chart1.add_series({
                                'categories': '=中兴并发!$B$3:$B$' + str(day+3),  # 设置图表类型标签范围
                                'values': '=中兴并发!$' + i + '$3:$' + i + '$' + str(day+3),  # 设置图表取值范围
                                'name': '=中兴并发!$' + i + '$2',  # 设置名称
                            })
                        for i in ['E']:
                            chart2.add_series({
                                'categories': '=中兴并发!$B$3:$B$' + str(day+3),
                                'values': '=中兴并发!$' + i + '$3:$' + i + '$' + str(day+3),
                                'name': '=中兴并发!$' + i + '$2',
                                'line': {'color': 'green'},
                            })

                        chart1.set_title({'name': u'并发数据图表'})  # 设置表格的title
                        chart2.set_title({'name': u'流量数据图表'})  # 设置表格的title
                        chart1.set_size({'width': 800, 'height': 400})  # 设置表格的大小
                        chart2.set_size({'width': 800, 'height': 400})
                        chart1.set_x_axis({'name_font':{'size':28,'bold':True},})
                        chart1.set_style(10)  # 设置表格的样式
                        chart2.set_style(10)
                        worksheet.insert_chart('G1', chart1)  # 插入表格，设置起始位置
                        worksheet.insert_chart('G22', chart2)

                    print('zhongxin file ok！')

                elif platformname == 'FH':
                    worksheet = workbook.add_worksheet('烽火并发')
                    worksheet.merge_range(0, 0, 0, 18, '烽火并发报表', formathead)
                    worksheet.write_row(1, 0, titlefhwRpt, formattitle)
                    worksheet.set_column(0, 1, 10)
                    worksheet.set_column(1, 18, 18)

                    while startdate <= enddate:

                        sumhms = sumll =  mangguoll = number_4kll = youkull = stbdown = bestvll = 0
                        cesull = boboll = tianyill = jiaoyull = huasull = jiayoull = jylivell = 0

                        tmp_dayDate = datetime.strptime(startdate, "%Y-%m-%d")
                        tmp_dayDate = self.setAddDay(tmp_dayDate)
                        checkdate = self.datetostr(tmp_dayDate)  # 比选择的开始日期多一天

                        p = Tfhdayrpt.objects.filter(updatetime__icontains=checkdate).filter(
                            nodecname__icontains='烽火汇总'). \
                            values_list('sjjdll', 'peakjdll', 'jdllper',
                                        'sjjdbf', 'peakjdbf', 'jdbfper')
                        if p:
                            for sjjdll, peakjdll, jdllper, sjjdbf, peakjdbf, jdbfper in p.iterator():
                                sjjdll = sjjdll
                                sumll = peakjdll
                                jdllper = jdllper
                                sjjdbf = sjjdbf
                                sumhms = peakjdbf
                                jdbfper = jdbfper
                        else:
                            sjjdll = sumll = jdllper = sjjdbf = sumhms = jdbfper = 0

                        sql = Tfhdayrpt.objects.filter(updatetime__icontains=checkdate).\
                                values_list('mangguoll','number_4kll','youkull','stbdown','bestvll',
                                'cesull','boboll','tianyill','jiaoyull','huasull','jiayoull','jylivell')
                        for mangguo, number_4k, youku, stb, bestv, cesu, bobo, tianyi, jiayu, huasu, jiayou, jylive in sql.iterator():
                            mangguoll = mangguoll + mangguo
                            number_4kll = number_4kll + number_4k
                            youkull = youkull + youku
                            stbdown = stbdown + stb
                            bestvll = bestvll + bestv
                            cesull = cesull + cesu
                            boboll = boboll + bobo
                            tianyill = tianyill + tianyi
                            jiaoyull = jiaoyull + jiayu
                            huasull = huasull + huasu
                            jiayoull = jiayoull + jiayou
                            jylivell = jylivell + jylive

                        tup = (int(sjjdll), int(sumll), int(jdllper), int(sjjdbf), int(sumhms), int(jdbfper),
                            int(mangguoll), int(number_4kll), int(youkull), int(stbdown), int(bestvll), int(cesull),
                            int(boboll), int(tianyill), int(jiaoyull), int(huasull), int(jiayoull), int(jylivell))

                        worksheet.write_string(row, 0, startdate[5:], formatcell)

                        for x in range(0,len(tup)):
                            if tup[x] < 10000000:
                                if (x+1 == 3 or x+1 == 6 ) and tup[x] >= 90:
                                    # 百分比超过90显示红色
                                    worksheet.write_number(row, x+1, tup[x], workbook.add_format(
                                        {'fg_color': '#FFC7CE', 'border': 1, 'align': 'center'}))
                                elif (x+1 == 3 or x+1 == 6 ) and tup[x] <= 20:
                                    # 百分比低于20显示黄色
                                    worksheet.write_number(row, x+1, tup[x], workbook.add_format(
                                        {'fg_color': '#FFD700', 'border': 1, 'align': 'center'}))
                                else:
                                    worksheet.write_number(row, x+1, tup[x], formatcell)
                            else:
                                worksheet.write_string(row, x+1, ' ', formatcell)
                        row += 1
                        startdate = checkdate
                    worksheet.freeze_panes('B3')
                workbook.close()
        print(excelname)
        return excelname

    def downloadFile(self,filename):
        if '\\' in filename:
            name = filename.split('\\')                # 分割路径，得到文件名称，window和linux不同，就用两种分割
        elif '/' in filename:
            name = filename.split('/')
        the_file_name = name[len(name) - 1]       # 显示在弹出对话框中的默认的下载文件名
        print(the_file_name)
        def readFile(filename, chunk_size=512):
            with open(filename, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        filename = filename  # 要下载的文件路径
        response = StreamingHttpResponse(readFile(filename))
        response['Content-Encoding'] = 'utf-8'
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote_plus(the_file_name))
        return response



