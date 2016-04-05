var selectedMusic = new Object();
var currTag="";
selectedMusic.filename = "";
selectedMusic.songname = "";
selectedMusic.singer = "";
selectedMusic.md5 = "";
selectedMusic.prebuilt = "";
selectedMusic.singer_pic = "";
selectedMusic.crop = "";
var curr_custom_song = "";
var curr_custom_md5 = "";
var mEnd = 0;
var mTag = "";

function initCategory() {
    var categrory = 0;
    if (window.location.pathname == '/v1/maker/cust/ringtone_boot/') {
        categrory = 1;
    } else if (window.location.pathname == '/v1/maker/cust/ringtone_call/') {
        categrory = 2;
    } else if (window.location.pathname == '/v1/maker/cust/ringtone_sms/') {
        categrory = 3;
    }

    switch (categrory) {
        case 1:
            currTag = "music_boot";
            break;
        case 2:
            currTag = "callring";
            break;
        case 3:
            currTag = "smstone";
            break;
        default:
            //not support
            currTag = "";
            return;
    }
}

function deleteMusic(event) {
    setCookie(currTag+"_filename", "");
    setCookie(currTag+"_songname", "");
    setCookie(currTag+"_pic", "");
    setCookie(currTag+"_singer", "");
    setCookie(currTag+"_prebuilt", "");
    setCookie(currTag+"_md5", "");
    setCookie(currTag+"_crop", "");
    selectedMusic.filename = "";
    selectedMusic.singer_pic = "";
    selectedMusic.singer = "";
    selectedMusic.prebuilt = "";
    selectedMusic.md5 = "";
    selectedMusic.songname = "";
    selectedMusic.crop = "";
    document.getElementById("preview_content").innerHTML = "<span class='preview-ringtone-icon-"+mclass+"'><img src='/static/images/cd_none.png'></span><span class='preview-ringtone-play-"+mclass+" si si-playd' ></span>";
    updateMusicList();
    decreaseCustomItemCount();
    if (event) {
        event.stopPropagation();
    }

}

function selectMusic(event, prebuilt, songname, singer, singer_pic, md5, filename) {
    if (selectedMusic.songname == "") {
        increaseCustomItemCount();
    }
    if (document.getElementById("uploadSelect")) {
        unselectPlainMusic(event)
    }
    var singername = '';
    if (prebuilt != '') { 
        singername = singer;
    }
    document.getElementById("preview_content").innerHTML = "\
        <span id='selected_music_img' class='preview-ringtone-icon-"+mclass+"'>\
            <img src='/static/images/cd_pause.png'>\
        </span>\
        <audio id='selected1' src='" + filename + "' preload='none'></audio>\
        <div id='selected_music_btn'></div>\
        <div class='preview-ringtone-text-"+mclass+"'>" + songname + "</div>\
        <div class='preview-ringtone-singer-"+mclass+"'>" + singername + "</div>";
    setCookie(currTag+"_filename", filename);
    setCookie(currTag+"_songname", songname);
    setCookie(currTag+"_pic", singer_pic);
    setCookie(currTag+"_singer", singer);
    setCookie(currTag+"_prebuilt", prebuilt);
    setCookie(currTag+"_md5", md5);
    setCookie(currTag+"_crop", "");
    selectedMusic.filename = filename;
    selectedMusic.singer_pic = singer_pic;
    selectedMusic.singer = singer;
    selectedMusic.prebuilt = prebuilt;
    selectedMusic.md5 = md5;
    selectedMusic.songname = songname;
    selectedMusic.crop = "";
    updateSelectedMusic();
    updateMusicList();
    if (event) {
        event.stopPropagation();
    }
}

function setLocalMusicCookie(filename, md5, crop) {
    setCookie(currTag+"_filename", filename);
    setCookie(currTag+"_md5", md5);
    setCookie(currTag+"_crop", crop);

    selectedMusic.filename = filename;
    selectedMusic.md5 = md5;
    selectedMusic.crop = crop;
    if ($('#pmPanel').css('display')=='block' && document.getElementById("plainMusic")) {
        document.getElementById("selected1").src = document.getElementById("plainMusic").src;
    } else {
        document.getElementById("selected1").src = "http://7xio6q.com1.z0.glb.clouddn.com/" + md5;
    }
    updateSelectedMusic();
}

function updateNetMusicCrop(crop) {
    var md5 = getCookie(currTag+"_md5");
    if (md5 != "") {
        setCookie(currTag+"_crop", crop);
        return true;
    }
    return false;
}

$(function() {
    initCategory();
    var clicked = 0;
    $("#maker_help > i").html("&nbsp;&nbsp;页面向导");
    $('#maker_help').on('click', function() {
        introJs().onchange(function(targetElement) {
            switch(this._currentStep) {
            case 0:
                $('#tab_pb').trigger("click");
                if (selectedMusic.filename == "") {
                    $('#music-select-0').trigger("click");
                    clicked = 1;
                }
                break;
            case 1:
                $('#tab_cust').trigger("click");
                break;
            }
        }).
        oncomplete(function() {
            if (clicked == 1) {
                $('#tab_pb').trigger("click");
                $('#music-delete-0').trigger("click");
                clicked = 0;
            }
        }).
        onexit(function() {
            if (clicked == 1) {
                $('#tab_pb').trigger("click");
                $('#music-delete-0').trigger("click");
                clicked = 0;
            }
        }).
        start();
    });
});

window.onload = function() {
    setCookie("played_url", '');
    selectedMusic.filename = getCookie(currTag+"_filename");
    var url = '';
    var singername = '';
    if (selectedMusic.filename != "") {
        selectedMusic.singer_pic = getCookie(currTag+"_pic");
        selectedMusic.singer = getCookie(currTag+"_singer");
        selectedMusic.prebuilt = getCookie(currTag+"_prebuilt");
        selectedMusic.md5 = getCookie(currTag+"_md5");  
        selectedMusic.songname = getCookie(currTag+"_songname");
        selectedMusic.crop = getCookie(currTag+"_crop");
        if (selectedMusic.prebuilt == '') {
            url = "http://7xio6q.com1.z0.glb.clouddn.com/" + selectedMusic.md5;
        } else {
            url = selectedMusic.filename;
            singername = selectedMusic.singer;
        }
        document.getElementById("preview_content").innerHTML = "<span id='selected_music_img' class='preview-ringtone-icon-"+mclass+"'><img src='/static/images/cd_pause.png'></span><audio id='selected1' src='" + url + "' preload='auto'></audio><div id='selected_music_btn'></div><div class='preview-ringtone-text-"+mclass+"'>"+selectedMusic.songname+"</div><div class='preview-ringtone-singer-"+mclass+"'>" + singername + "</div>";
        updateSelectedMusic();
        curr_custom_song=selectedMusic.songname;
        curr_custom_md5=selectedMusic.md5;
    }
    else {
        document.getElementById("preview_content").innerHTML = "<span class='preview-ringtone-icon-"+mclass+"'><img src='/static/images/cd_none.png'></span><span class='preview-ringtone-play-"+mclass+" si si-playd' ></span>";
        updateMusicList();
        loadCustomItemCount();
        activateOption('1');
        return;
    }
    if (selectedMusic.prebuilt == '') {
        if (selectedMusic.crop != '') {
            showWave(url, selectedMusic.crop);
        } else {
            showPlainMusic(url, selectedMusic.songname);
        }
    }
    activateOption(selectedMusic.prebuilt);
    loadCustomItemCount();
    updateMusicList();
}

function updatedSelectedLocalMusic(type) {
    if (type == 'play') {
        if (selectedMusic.prebuilt != '') {
            setCookie("played_url", '');
        } else {
            setCookie("played_url", selectedMusic.filename);
        }
    } else {
        setCookie("played_url", "");
    }
    updateSelectedMusic();
    updatePlainMusic();
}

function play_single_sound(url, currTag, songname, crop) {
    pause_single_sound();

    try {
        pauseLocalMusic();
    } catch (err) {}
    var player = document.getElementById(currTag);
    if (crop != undefined && crop != "") {
        var tmp = crop.split(",");
        if (tmp.length == 2) {
            try {
                mEnd = parseFloat(tmp[1]);
                player.currentTime = parseFloat(tmp[0]);
            } catch (err) {}
        }
    } else if (window.location.pathname == '/v1/maker/cust/submit/') {
        try {
            mEnd = player.duration;
            player.currentTime = 0;
        } catch (err) {}
    }

    if (player) {
        player.addEventListener("timeupdate", timeUpdate, false);
        mTag = currTag;    	
        player.play();
        setCookie("played_songname", songname);
        setCookie("played_url", url);
        setCookie("played_music", currTag);
        
        if (window.location.pathname == '/v1/maker/cust/ringtone_boot/' || 
            window.location.pathname == '/v1/maker/cust/ringtone_call/') {
            updateSelectedMusic();
            updateMusicList();
            updatePlainMusic();
        } else if (window.location.pathname == '/v1/maker/cust/submit/') {
            updateSubmit();
        } else {
            updatePreview(0);
        }
    }
    updateOnEnded();
}

function pause_single_sound() {
    var selected = getCookie("played_music");

    if (selected != '') {
        var tmp = document.getElementById(selected);
        if (tmp) {
            tmp.pause();
            setCookie("played_music", '');
            setCookie("played_url", '');
        }
    }
    
    if (window.location.pathname == '/v1/maker/cust/ringtone_boot/' || 
        window.location.pathname == '/v1/maker/cust/ringtone_call/') {
        updateMusicList();
        updateSelectedMusic();
        updatePlainMusic();
    } else if (window.location.pathname == '/v1/maker/cust/submit/') {
        updateSubmit();
    } else {
        updatePreview(0);
    }
}

function timeUpdate() {
    var player = document.getElementById(mTag);
    if (player && (player.paused == false) && ((mEnd > 0 && player.currentTime >= mEnd) || player.currentTime >= player.duration)) {
        pause_single_sound();
    }
}


//for cust_ringtone_xx pages
function updateMusicList() {
    var content = "";
    var count = 10; //apps per page
    var played_url = getCookie("played_url");
    for (var i = 0; i < count; i++) {
        var tmp = document.getElementById("app-" + i);
        if (tmp) {
            if (played_url == tmp.getAttribute("data-url")) {
                tmp.innerHTML = '<a href="javascript:void(0);" title="暂停"><span class="si si-pause-s"></span></a>';
            } else {
                tmp.innerHTML = '';
            }
            var tmp_select = document.getElementById("app-" + i + "-select");
            if (tmp_select) {
                if (selectedMusic.filename == tmp.getAttribute("data-url")) {
                    tmp_select.innerHTML = '<a href="javascript:void(0);" title="取消"><span class="si si-select" id="music-delete-' + i + '" onclick="deleteMusic(event)"></span></a>';
                } else {
                    tmp_select.innerHTML = '<a href="javascript:void(0);" title="选择"><span class="si si-unselect" id="music-select-' + i + '" onclick="selectMusic(event, \'' + tmp.getAttribute("data-id") + '\',\'' + tmp.getAttribute("data-name") + '\',\'' + tmp.getAttribute("data-author") + '\',\'' + tmp.getAttribute("data-pic") + '\',\'\',\'' + tmp.getAttribute("data-url") + '\')"></span></a>';
                }
            }
        } else {
            break;
        }
    }
}

function updateSelectedMusic() {
    var tmp_btn = document.getElementById("selected_music_btn");
    var tmp_img = document.getElementById("selected_music_img");
    if (tmp_btn && tmp_img) {
        var tmp_pause, tmp_play;
        var url = selectedMusic.filename;
        if (selectedMusic.prebuilt != '') {
            tmp_pause = "pause_single_sound()";
            tmp_play = "play_single_sound(\""+selectedMusic.filename+"\", \"selected1\", \""+selectedMusic.songname+"\", \""+selectedMusic.crop+"\")";
        } else {
            if (selectedMusic.crop != '') {
                tmp_pause = "pauseLocalMusic()";
                tmp_play = "playLocalMusic()";
            } else {
                if (document.getElementById("selected1")) {
                    url = document.getElementById("selected1").src;
                } else {
                    url = "http://7xio6q.com1.z0.glb.clouddn.com/" + selectedMusic.md5;
                }
                tmp_play = "playPlainMusic(\""+url+"\", \"selected1\", \""+selectedMusic.songname+"\", \"\")";
                tmp_pause = tmp_play;
            }
        }
        if (getCookie("played_url") == url ) {
            tmp_btn.innerHTML = "<a href='javascript:void(0);' title='暂停'>\
                           <span class='preview-ringtone-play-"+mclass+" si si-pause' onclick='"+tmp_pause+"'></span>\
                       </a>";
            tmp_img.innerHTML = "<img src='/static/images/cd_play.gif'>";
        } else {
            tmp_btn.innerHTML = "<a href='javascript:void(0);' title='播放'>\
                           <span class='preview-ringtone-play-"+mclass+" si si-play' onclick='"+tmp_play+"'></span>\
                       </a>";
            tmp_img.innerHTML = "<img src='/static/images/cd_pause.png'>";
        }
    }
}

function updatePlainMusic() {
    var played_url = getCookie("played_url");
    var player_plain = document.getElementById("plainMusic");
    var player_plain_btn = document.getElementById("uploadPlay");
    if (player_plain_btn && player_plain) {
        if (played_url == player_plain.src) {
            player_plain_btn.innerHTML='<a href="javascript:void(0);" title="暂停"><span class="si si-pause-s"></span></a>';
        } else {
            player_plain_btn.innerHTML='';
        }
    }
}

//for preview page on android device
function updatePreview(init) {

    var content = "";
    var played = getCookie("played_music");

    var tmp = document.getElementById("music_selected1");
    if (tmp) {
        if ((played == 'selected1') && (init != 1)) {
            content += '<a href="javascript:void(0);"><img src="/static/images/icon-pause.png" style="margin-right:5px" onclick="pause_single_sound()"></a>';
        } else {
            content += '<a href="javascript:void(0);"><img src="/static/images/icon-play.png" style="margin-right:5px" onclick="play_single_sound(\'\', \'selected1\')"></a>';
        }
        tmp.innerHTML = content;
    }

    content = "";
    var tmp = document.getElementById("music_selected2");
    if (tmp) {
        if ((played == 'selected2') && (init != 1)) {
            content += '<a href="javascript:void(0);"><img src="/static/images/icon-pause.png" style="margin-right:5px" onclick="pause_single_sound()"></a>';
        } else {
            content += '<a href="javascript:void(0);"><img src="/static/images/icon-play.png" style="margin-right:5px" onclick="play_single_sound(\'\', \'selected2\')"></a>';
        }
        tmp.innerHTML = content;
    }
}

function updateSubmit() {
    if ($("#bootuptone_active").attr("class") == "active") {
        updateSubmitPreviewBlock("selected1", bootuptone);
    }
    if ($("#callingtone_active").attr("class") == "active") {
        updateSubmitPreviewBlock("selected2", callingtone);
    }
}

function updateSubmitPreviewBlock(currTag, ringtone) {
    var tmp = document.getElementById("preview_content");
    if (tmp) {
        var singername = '';
        if (ringtone.prebuilt != '') { 
            singername = ringtone.singer;
        }
        var played_url = getCookie("played_url");
        if (played_url !="" ) {
            tmp.innerHTML = "<span class='preview-ringtone-icon-"+mclass+"'>\
                            <img src='/static/images/cd_play.gif'>\
                        </span>\
                        <a href='javascript:void(0);' title='暂停'>\
                            <span class='preview-ringtone-play-"+mclass+" si si-pause' onclick='pause_single_sound()'></span>\
                        </a>\
                        <div class='preview-ringtone-text-"+mclass+"'>" + ringtone.songname + "</div>\
                        <div class='preview-ringtone-singer-"+mclass+"'>" + singername + "</div>";
        } else {
            tmp.innerHTML = "<span class='preview-ringtone-icon-"+mclass+"'>\
                            <img src='/static/images/cd_pause.png'>\
                        </span>\
                        <a href='javascript:void(0);' title='播放'>\
                            <span class='preview-ringtone-play-"+mclass+" si si-play' onclick='play_single_sound(\""+ringtone.filename+"\", \""+currTag+"\", \""+ringtone.songname+"\", \""+ringtone.crop+"\")'></span>\
                        </a>\
                        <div class='preview-ringtone-text-"+mclass+"'>" + ringtone.songname + "</div>\
                        <div class='preview-ringtone-singer-"+mclass+"'>" + singername + "</div>";
        }
    }
}

function activateOption(prebuilt) {
    if (window.location.search != '') {
        var tmp = document.getElementById("option_prebuilt");
        if (tmp) {
            tmp.setAttribute("class", "active");
        }
        return;
    }

    if (prebuilt != '') {
        var tmp = document.getElementById("option_prebuilt");
        if (tmp) {
            tmp.setAttribute("class", "active");
            tmp = document.getElementById("option_custom");
            tmp.setAttribute("class", "");
            tmp = document.getElementById("prebuilt");
            tmp.setAttribute("class", "tab-pane fade in active");
            tmp = document.getElementById("custom");
            tmp.setAttribute("class", "tab-pane fade");
        }
    } else {
        var tmp = document.getElementById("option_prebuilt");
        if (tmp) {
            tmp.setAttribute("class", "");
            tmp = document.getElementById("option_custom");
            tmp.setAttribute("class", "active");
            tmp = document.getElementById("prebuilt");
            tmp.setAttribute("class", "tab-pane fade");
            tmp = document.getElementById("custom");
            tmp.setAttribute("class", "tab-pane fade in active");
        }
    }

}

function updateOnEnded() {
    $("audio").each(function() {
        $(this).bind("ended", function() {
            setCookie("played_url", '');
            setCookie("played_music", '');
            updateMusicList();
            updateSubmit();
            updateSelectedMusic();
            updatePlainMusic();
        });
    });
}

$('.table-pb-music').on('click', 'tr', function (event) {
    $(this).parent().children().removeClass("active");
    $(this).addClass("active");
});

function playPrebuiltMusic(id) {
    var tmp = document.getElementById(id);
    if (tmp) {
        var played_url = getCookie("played_url");
        if (played_url == tmp.getAttribute("data-url")) {
            pause_single_sound();
        } else {
            play_single_sound(tmp.getAttribute("data-url"), "audiotag" + tmp.getAttribute("data-id"), tmp.getAttribute("data-name"));
        }
    }
}