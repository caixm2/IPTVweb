/**
 * Created by ChenQi on 2017/7/14.
 */
function myfunction(var1,var2,var3,var4,var5,var6) {
    var pre_scrollTop = 0;  // 滚动条事件之前文档滚动高度
    var pre_scrollLeft = 0;
    var obj_topic;
    var obj_left;
    var scroll_top;
    var scroll_left;
    window.onload = function () {

        pre_scrollTop = (document.documentElement.scrollTop);
        pre_scrollLeft = (document.documentElement.scrollLeft);
        obj_topic = document.getElementById("topic");
        obj_left = document.getElementById("left");
        var table = document.getElementById("table");
        var left = document.getElementById('left_title');
        var trs = table.getElementsByTagName("tr");

        for (var i = 1; i < trs.length; i++) {
            var tr = trs[i]
            var tds = tr.getElementsByTagName("td");

            var td = tds[0];
            var tdDiv = td.getElementsByTagName("div");
            if (left) {
                var _tr = left.insertRow(i);
                var _th = _tr.insertCell();
                _th.innerHTML = tdDiv[0].innerHTML;
                _th.className = 'th';
            }
            // 把中间哪部门数字做成整数型
            for (var a = var1; a <= var2; a += var3) {
                var td = tds[a];
                var tdDiv = td.getElementsByTagName("div");
                if (tdDiv[0].innerHTML > 10000000)
                    tdDiv[0].innerHTML = ""
                else
                    tdDiv[0].innerHTML = parseInt(tdDiv[0].innerHTML)
            }

            // 这个方法是判断单元格颜色
            for (var j = var4; j <= var5; j += var6) {
                var _td = tds[j];
                var tdDiv = _td.getElementsByTagName('div');
                tdDiv[0].innerHTML = parseInt(tdDiv[0].innerHTML)
                if (tdDiv[0].innerHTML >= 90)
                    _td.style.backgroundColor = 'pink';
                else if (tdDiv[0].innerHTML < 20)
                    _td.style.backgroundColor = 'yellow';
            }
        }
    }
    window.onscroll = function () {
        // 因为google有个bug，不认可documentElement，所以要先判断兼容
        if (document.documentElement && document.documentElement.scrollTop) {
            scroll_top = document.documentElement.scrollTop;
        }
        else if (document.body) {
            scroll_top = document.body.scrollTop;
        }
         if (document.documentElement && document.documentElement.scrollLeft)
             scroll_left = document.documentElement.scrollLeft;
         else if (document.body)
             scroll_left = document.body.scrollLeft;

        // 这个方法是冻结表头
        if (pre_scrollTop != (scroll_top)) {
            pre_scrollTop = (scroll_top);
            if (pre_scrollTop > 107) {
                obj_topic.style.top = pre_scrollTop + "px";
            } else {
                obj_topic.style.top = 107 + "px";
            }
        }
        // 这个方法是冻结表左侧
        if (pre_scrollLeft != (scroll_left)) {
            pre_scrollLeft = (scroll_left);
            if (pre_scrollLeft > 20) {
                obj_left.style.left = pre_scrollLeft - 20 + "px";
            } else {
                obj_left.style.left = 0 + "px";
            }
        }
    }
}