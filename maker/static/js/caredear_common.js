function getCookie(cookie_name) {
    var allcookies = document.cookie;
    var value = "";
    if (allcookies == null || typeof(allcookies) == "undefined") {
        return "";
    }
    var cookie_pos = allcookies.indexOf(cookie_name);
    if (cookie_pos != -1) {
        cookie_pos += cookie_name.length + 1;
        var cookie_end = allcookies.indexOf(";", cookie_pos);
        if (cookie_end == -1) {
            cookie_end = allcookies.length;
        }
        value = unescape(allcookies.substring(cookie_pos, cookie_end));
    }
    return value;
}

function setCookie(c_name, value, expiredays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + expiredays);
    document.cookie = c_name + "=" + escape(value) + ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString()) + "; path=/";
}

function clearCookie(c_name) {
    document.cookie = c_name + "=" + escape('') + ";expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
}

function deleteAllCookies() {
    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        var eqPos = cookie.indexOf("=");
        var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        //var domain = document.domain
        //var path ='/';
        clearCookie(name);
    }
}

var slide_handle;

function startSlide() {
    $("#slideshow > div:gt(0)").hide();
    slide_handle = setInterval(function() {
            $('#slideshow > div:first')
                .fadeOut(500)
                .next()
                .fadeIn(500)
                .end()
                .appendTo('#slideshow');
        },
        2000);
}

function stopSlide() {
    window.clearInterval(slide_handle);
}


function loadCustomItemCount() {
    var count = 0;
    var filename = "";
    //load welcome message
    filename = getCookie("welcome-changefilename");
    if (filename != "") {
        $("#si-mcheck-ecard").css('visibility','visible');
        count++;
    }
    //load boot animation list
    filename = getCookie("boot-0");
    if (filename != "") {
        $("#si-mcheck-anim").css('visibility','visible');
        count++;
    }
    //load bootup ringtone
    filename = getCookie("music_boot_filename");
    if (filename != "") {
        $("#si-mcheck-rboot").css('visibility','visible');
        count++;
    }
    //load call ringtone
    filename = getCookie("callring_filename");
    if (filename != "") {
        $("#si-mcheck-rcall").css('visibility','visible');
        count++;
    }
    //load lockwallpaper
    filename = getCookie("lockwp");
    if (filename != "") {
        $("#si-mcheck-wlock").css('visibility','visible');
        count++;
    }
    //load desktop wallpaper
    filename = getCookie("dkpwp");
    if (filename != "") {
        $("#si-mcheck-wdkp").css('visibility','visible');
        count++;
    }
    //load app list
    filename = getCookie("app-0");
    if (filename != "") {
        $("#si-mcheck-app").css('visibility','visible');
        count++;
    }
    var tmp = document.getElementById("nav-btn-preview-count");
    if (tmp) {
        tmp.setAttribute("data-count", count);
        if (count > 0) {
            document.getElementById("nav-btn-preview-count").innerHTML = count;
        } else {
            document.getElementById("nav-btn-preview-count").innerHTML = "";
        }
    }
}

function increaseCustomItemCount() {
    var count = 0;
    var tmp = document.getElementById("nav-btn-preview-count");
    if (tmp) {
        count = parseInt(tmp.getAttribute("data-count"));
        count++;
        tmp.setAttribute("data-count", count);
        if (count > 0) {
            document.getElementById("nav-btn-preview-count").innerHTML = count;
        } else {
            document.getElementById("nav-btn-preview-count").innerHTML = "";
        }
    }

    previewBtnAnimation();
}

function decreaseCustomItemCount() {
    var count = 0;
    var tmp = document.getElementById("nav-btn-preview-count");
    if (tmp) {
        count = parseInt(tmp.getAttribute("data-count"));
        count--;
        if (count > 0) {
            tmp.setAttribute("data-count", count);
            document.getElementById("nav-btn-preview-count").innerHTML = count;
        } else {
            tmp.setAttribute("data-count", "0");
            document.getElementById("nav-btn-preview-count").innerHTML = "";
        }
    }

    previewBtnAnimation();
}

function showAppDetail(res_pkg) {
    cdLog(res_pkg);
    $.ajax({
        url: '/v1/maker/getappdetail/',
        async: false,
        dataType: 'json',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({
            "package": res_pkg
        }),
        success: function(data) {
            var result = JSON.parse(JSON.stringify(data));
            $('#appDetailModal').modal('hide');
            document.getElementById("detail_title").innerHTML = result.name;
            document.getElementById("detail_logo").innerHTML = '<img width="68px" height="68px" src="' + result.logo + '" title="' + result.name + '">';
            document.getElementById("detail_head").innerHTML = '版本号： ' + result.ver + '<br>软件大小: ' + result.size + ' MB<br>下载量: ' + result.down + '<br>';
            document.getElementById("detail_intro").innerHTML = result.desp;

            var content = '<div id="imglist" style="width:650px;">';
            if (result.pic0) {
                content += '<img src="' + result.pic0 + '?imageView2/3/w/120/h/200" style="border-radius: 8px; margin-right:5px;">';
            }
            if (result.pic1) {
                content += '<img src="' + result.pic1 + '?imageView2/3/w/120/h/200" style="border-radius: 8px; margin-right:5px;">';
            }
            if (result.pic2) {
                content += '<img src="' + result.pic2 + '?imageView2/3/w/120/h/200" style="border-radius: 8px; margin-right:5px;">';
            }
            if (result.pic3) {
                content += '<img src="' + result.pic3 + '?imageView2/3/w/120/h/200" style="border-radius: 8px; margin-right:5px;">';
            }
            if (result.pic4) {
                content += '<img src="' + result.pic4 + '?imageView2/3/w/120/h/200" style="border-radius: 8px;">';
            }
            content += '</div>';
            document.getElementById("detail_pics").innerHTML = content;

            $('#appDetailModal').modal('show');

        },
        error: function(jqXhr, textStatus, errorThrown) {
            cdLog("SHIT");
        }
    });
}

function loadExampleCookies() {
    setCookie("welcome-changefilename", "http://7xio6q.com1.z0.glb.clouddn.com/cdtemplate-02.jpg?watermark/3/text/54i454i4Og==/font/5qW35L2T/fontsize/1600/fill/cmVk/gravity/NorthWest/dx/120/dy/310/text/ICDnlJ_ml6Xlv6vkuZDvvIHvvIEKICAgICAgICAgIOWEv-WtkA==/font/5qW35L2T/fontsize/1400/fill/cmVk/gravity/NorthWest/dx/120/dy/410");
    setCookie("music_boot_filename", "");
    setCookie("music_boot_prebuilt", "");
    setCookie("music_boot_md5", "");
    setCookie("music_boot_crop", "");
    setCookie("music_boot_pic", "");
    setCookie("music_boot_singer", "");
    setCookie("music_boot_songname", "");
    setCookie("callring_filename", "http://7jpr9t.com1.z0.glb.clouddn.com/9529_%u5343%u5E74%u7B49%u4E00%u56DE.mp3");
    setCookie("callring_prebuilt", "75");
    setCookie("callring_md5", "");
    setCookie("callring_crop", "");
    setCookie("callring_pic", "");
    setCookie("callring_singer", "高胜美");
    setCookie("callring_songname", "千年等一回");
    setCookie("makerid", "4d772aeeb2169107c9b3e24f28b0f81a");
    Cookies.set('boot-0', {
        "name": "http://7xio6q.com1.z0.glb.clouddn.com/10a489ca33c958b238ca4b9b3405aae2",
        "md5": "",
        "pb": "11",
        "crop": ""
    });
    Cookies.set('boot-1', {
        "name": "http://7xio6q.com1.z0.glb.clouddn.com/0a562a9279985d7eea0e2c70411e9eb5",
        "md5": "",
        "pb": "12",
        "crop": ""
    });
    Cookies.set('boot-2', {
        "name": "http://7xio6q.com1.z0.glb.clouddn.com/d07484b87152fad2555f9a8bf0745a71",
        "md5": "",
        "pb": "13",
        "crop": ""
    });
    Cookies.set('boot-3', {
        "name": "http://7xio6q.com1.z0.glb.clouddn.com/ef78220c02dccc76797869767cb078fc",
        "md5": "",
        "pb": "10",
        "crop": ""
    });
    Cookies.set('lockwp', {
        "name": "http://7xio6q.com1.z0.glb.clouddn.com/0a562a9279985d7eea0e2c70411e9eb5",
        "md5": "",
        "pb": "12",
        "crop": ""
    });
    Cookies.set('dkpwp', {
        "name": "http://7xio6q.com1.z0.glb.clouddn.com/wp_480x498_01.png",
        "md5": "",
        "pb": "127",
        "crop": ""
    });
    Cookies.set('app-0', {
        "name": "一起打麻将（四川麻将）",
        "icon": "http://7jpr9t.com1.z0.glb.clouddn.com/com_phoneu_yqdmj_mi15d706cbaf013aae11cc09e7b72c0aa1_1410339295/app_label_320/icon.png",
        "pkg": "com.phoneu.yqdmj"
    });
}

function clearExampleCookies() {
    deleteAllCookies();
}

function cdLog(log) {
    if (isIE) {
        //ignore console log for IE
    } else {
        console.log(log);
    }
}
var isIE = false;
var mclass;
$(function() {
    var  nav=navigator.userAgent.toLowerCase();
    if (!!window.ActiveXObject || "ActiveXObject" in window) {
        isIE = true;
    } else if (nav.match(/opr\/([\d\.]+)/)) {
        isIE = true;
    }
    var tmp = getCookie("model");
    if (tmp == '3') {
        mclass="m3";
    } else {
        mclass="m2c";
    }
    w1 = $(window).width();
    $('html').addClass('scrollbar-test');
    w2 = $(window).width();
    $('html').removeClass('scrollbar-test');
    $("<style type='text/css'>.modal-open {margin-right:" + (w2 - w1) + "px;}</style>").appendTo("head");
});

function showMenu() {

    if (window.location.pathname == '/v1/maker/cust/submit/') {
        if (getCookie('hidden') != "1") {
            $("#menu_left").hide("slow");
            setCookie('hidden', '1');
        } else {
            document.getElementById('menu_left').style.display = "none";
        }
    } else {
        if (getCookie('hidden') == "1") {
            document.getElementById('menu_left').style.display = "none";
            $("#menu_left").show("slow");
            clearCookie('hidden');
        }
    }

    //menuItemAnimation();

}

function menuItemAnimation() {

    var tmp = window.location.pathname;
    var tag = tmp.substring(tmp.lastIndexOf("/", tmp.length - 2));
    $("a[href$='cust" + tag + "']").addClass('animated pulse');
}


function previewBtnAnimation(style) {
    var elm = $("#nav-btn-preview-count");
    var newone = elm.clone(true);
    elm.after(newone);
    elm.remove();
    newone.addClass('animated bounceIn');
}

function showToast(level, str) {
    toastr.remove();
    toastr.options = {
        "closeButton": false,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-top-full-width",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "2000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };

    if (level == 'success') {
        toastr.success(str);
    } else if  (level == 'warning') {
        toastr.warning(str);
    } else if  (level == 'error') {
        toastr.error(str);
    }

}

function restoreAllCookies(result) {
    var ID_TYPE=0;
    var ID_PBID=1;
    var ID_NAME=2;
    var ID_URL=3;
    var ID_OTHER=4;
    var ID_CROP=6;
    var data = result.data;
    var indexApp = 0;
    Cookies.set("model", result.model);
    Cookies.set("makerid", result.makerID);
    for (var i = 0; i < data.length; i++) {
        var cookieName = ""
        switch(data[i][ID_TYPE]) {
        case 1:
            cookieName = "callring_";
            break;
        case 2:
            cookieName = "music_boot_";
            break;
        case 3:
            cookieName = "lockwp";
            break;
        case 4:
            cookieName = "dkpwp";
            break;
        case 6:
            cookieName = "app-";
            break;
        case 7:
            cookieName = "welcome-changefilename";
            break;
        case 1001:
            cookieName = "boot-0";
            break;
        case 1002:
            cookieName = "boot-1";
            break;
        case 1003:
            cookieName = "boot-2";
            break;
        case 1004:
            cookieName = "boot-3";
            break;
        }
        if (data[i][ID_TYPE]==1 || data[i][ID_TYPE]==2) {
            var filename = "";
            var md5="";
            if (data[i][ID_PBID]==-1) {
                md5 = data[i][ID_URL]==null?"":data[i][ID_URL];
                md5 = md5.split(".com/", 2)[1];
                filename = md5 + "_" + data[i][ID_NAME];
            } else {
                filename = data[i][ID_URL]==null?"":data[i][ID_URL];
            }
            setCookie(cookieName+"filename", filename);
            setCookie(cookieName+"md5", md5);
            setCookie(cookieName+"pic", "");
            setCookie(cookieName+"singer", data[i][ID_OTHER]==null?"自定义铃声":data[i][ID_OTHER]);
            setCookie(cookieName+"prebuilt", data[i][ID_PBID]==-1?"":data[i][ID_PBID].toString());
            setCookie(cookieName+"songname", data[i][ID_NAME]==null?"":data[i][ID_NAME]);
            setCookie(cookieName+"crop", data[i][ID_CROP]==null?"":data[i][ID_CROP]);
        } else if (data[i][ID_TYPE]==3 || data[i][ID_TYPE]==4 || (data[i][ID_TYPE] >= 1001 && data[i][ID_TYPE] <=1004)) {
            var img=new Object();
            img.name=data[i][ID_URL]==null?"":data[i][ID_URL];
            img.md5=data[i][ID_NAME]==null?"":data[i][ID_NAME];
            img.pb=data[i][ID_PBID]==-1?"":data[i][ID_PBID].toString();
            img.crop=data[i][ID_CROP]==null?"":data[i][ID_CROP];
            Cookies.set(cookieName, JSON.stringify(img));
        } else if (data[i][ID_TYPE]==6) {
            var app=new Object();
            app.name=data[i][ID_OTHER]==null?"":data[i][ID_OTHER];
            app.icon=data[i][ID_URL]==null?"":data[i][ID_URL];
            app.pkg=data[i][ID_NAME]==null?"":data[i][ID_NAME];;
            Cookies.set(cookieName+indexApp, JSON.stringify(app));
            indexApp++;
        } else if (data[i][ID_TYPE]==7) {
            Cookies.set(cookieName, data[i][ID_URL]==null?"":data[i][ID_URL]);
        }
    }
}



function getNowFormatDate() {
    var date = new Date();
    var seperator1 = "-";
    var seperator2 = ":";
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
            + " " + date.getHours() + seperator2 + date.getMinutes()
            + seperator2 + date.getSeconds();
    return currentdate;
}

