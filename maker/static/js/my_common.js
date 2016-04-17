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


