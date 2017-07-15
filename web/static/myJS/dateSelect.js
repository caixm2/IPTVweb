/**
 * Created by ChenQi on 2017/7/15.
 */
window.onload = function () {
    var myDate = new Date();
    myDate.setDate(myDate.getDate() - 1);
    var year = myDate.getFullYear();
    var month = myDate.getMonth() + 1;
    var lastMonth = myDate.getMonth();
    var day = myDate.getDate();
    if (document.getElementById('id_dRptdate_year')) {
        var dyear = document.getElementById('id_dRptdate_year');
        var dmonth = document.getElementById('id_dRptdate_month');
        var dday = document.getElementById('id_dRptdate_day');

        for (var i = 0; i < dyear.options.length; i++) {
            if (dyear.options[i].value == year) {
                dyear.options[i].selected = true;
                break;
            }
        }

        for (var i = 0; i < dmonth.options.length; i++) {
            if (dmonth.options[i].value == month) {
                dmonth.options[i].selected = true;
                break;
            }
        }

        for (var i = 0; i < dday.options.length; i++) {
            if (dday.options[i].value == day) {
                dday.options[i].selected = true;
                break;
            }
        }
    }
    if (document.getElementById('id_wRptstartdate_year')) {
        var startyear = document.getElementById('id_wRptstartdate_year');
        var startmonth = document.getElementById('id_wRptstartdate_month');
        var startday = document.getElementById('id_wRptstartdate_day');
        var endyear = document.getElementById('id_wRptenddate_year');
        var endmonth = document.getElementById('id_wRptenddate_month');
        var endday = document.getElementById('id_wRptenddate_day');
        for (var i = 0; i < startyear.options.length; i++) {
            if (startyear.options[i].value == year) {
                startyear.options[i].selected = true;
                break;
            }
        }

        for (var i = 0; i < startmonth.options.length; i++) {
            if (startmonth.options[i].value == lastMonth) {
                startmonth.options[i].selected = true;
                break;
            }
        }

        for (var i = 0; i < startday.options.length; i++) {
            if (startday.options[i].value == day) {
                startday.options[i].selected = true;
                break;
            }
        }

        for (var i = 0; i < endyear.options.length; i++) {
            if (endyear.options[i].value == year) {
                endyear.options[i].selected = true;
                break;
            }
        }

        for (var i = 0; i < endmonth.options.length; i++) {
            if (endmonth.options[i].value == month) {
                endmonth.options[i].selected = true;
                break;
            }
        }

        for (var i = 0; i < endday.options.length; i++) {
            if (endday.options[i].value == day) {
                endday.options[i].selected = true;
                break;
            }
        }
    }
}