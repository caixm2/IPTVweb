/**
 * Created by ChenQi on 2017/7/14.
 */
 var all = [];
        var time = [];
        var hms = [];
        var epg = [];
        var ll = [];
        window.onload = function() {
            // 获取表格数据，分成几个list方便做图表
            var tbl = document.getElementById("table");
            var trs = tbl.getElementsByTagName("tr");

            for (var i = 1; i < trs.length; i++) {
                var tr = trs[i]
                var tds = tr.getElementsByTagName("td");
                for (var j = 0; j < 4; j++) {
                    var td = tds[j];
                    var tdDiv = td.getElementsByTagName("div");
                    all.push(tdDiv[0].innerHTML)
                }
            }
            for (var i = 0; i < all.length; i++) {
                if (i % 4 == 0) {
                    time.push(all[i])
                }
                if (i % 4 == 1) {
                    hms.push(eval(all[i]))
                }
                if (i % 4 == 2) {
                    epg.push(eval(all[i]))
                }
                if (i % 4 == 3) {
                    ll.push(eval(all[i]))
                }
            }
            // 单数据为大于5条，会出现图表，如果数据超过90条，会隐藏x轴坐标
            if (time.length > 6 ) {
                Highcharts.setOptions({
                    colors: ['#f47961', '#60be7b', '#4b5d69', '#9fdbea']
                });

                $('#areaChart1').highcharts({
                    chart: {
                        type: 'line',
                        zoomType: 'x'
                    },
                    title: {
                        text: '并发数据图表'
                    },

                    legend: {
                        enabled: true
                    },
                    xAxis: {
                        tickInterval: time.length/30,
                        labels: {rotation: -45},
                        type: 'datetime',
                        categories: time,
                    },

                    yAxis: {
                        title: {
                            text: null
                        },
                        min: 0,
                        labels: {
                            formatter: function () {
                                return this.value / 10000 + '万';
                            }
                        }
                    },

                    tooltip: {
                        shared: true
                    },

                    credits: {
                        enabled: false
                    },

                    series: [{
                        name: '流媒体并发',
                        data: hms
                    }, {
                        name: 'epg并发',
                        data: epg
                    }]
                });
                $('#areaChart2').highcharts({
                    chart: {
                        type: 'line',
                        zoomType: 'x'
                    },
                    title: {
                        text: '流量数据图表'
                    },

                    legend: {
                        enabled: true
                    },

                    xAxis: {
                        tickInterval: time.length/30,
                        labels: {rotation: -45},
                        type: 'datetime',
                        categories: time,
                    },

                    yAxis: {
                        title: {
                            text: null
                        },
                        min: 0,
                    },

                    tooltip: {
                        shared: true
                    },

                    credits: {
                        enabled: false
                    },

                    series: [{
                        name: '流量',
                        data: ll
                    }]
                });
            }
        }