/*global Qiniu */
/*global plupload */
/*global FileProgress */
/*global hljs */
var decMd5Sum = function(file) {
    var fname = file.name;
    var i = fname.indexOf('_');
    if (i != 32) {
        var d = new Date();
        var md5 = hex_md5(d.getTime());
        file.name = md5 + "_" + file.name;
        return md5;
    } else
        return fname.slice(0, 32);
}

var encMd5Sum = function(file, md5) {
    file.name = md5 + "_" + file.getSource().getSource().name;
}

var musicLoaded;
function saveMusicCrop() {
    var crop = "";
    if (isIE) {
        if ($('#audioPlayerPanel').css('display')=='block') {
            if (mEnd > 0) {
                crop = mStart+","+mEnd;
            }
        }
    } else {
        if ($('#playlist').css('display')=='block') {
            try {
                var sel = playlistEditor.getSelected();
                crop = sel.startTime + "," + sel.endTime;
            } catch (err) {}
        }
    }

    //selectMusic('', curr_custom_song, "自定义铃声", null, curr_custom_md5, null);
    selectMusic(null, '', curr_custom_song, "自定义铃声", null,null,null);

    if (musicLoaded == undefined) {
        if (updateNetMusicCrop(crop)) {
//            return;
        } else {
            alert("请先选择一首本地歌曲");
            return;
        }
    }

    pauseLocalMusic();

    if  (musicLoaded == undefined) {
       setLocalMusicCookie(curr_custom_song, curr_custom_md5, crop);
    } else {
       var md5 = decMd5Sum(musicLoaded);
       setLocalMusicCookie(musicLoaded.name, md5, crop);
    }
}

function playLocalMusic() {
    if (isIE) {
        play();
    } else {
        playlistEditor.play();
        updatedSelectedLocalMusic('play');
    }
}

function pauseLocalMusic() {
    if (isIE) {
        pause();
    } else {
        try {
            updatedSelectedLocalMusic('pause');
            if (!playlistEditor.isPlaying())
                return;
            playlistEditor.pause();
        } catch (err) {};
    }
}

var config = new WaveformPlaylist.Config({
    resolution: 10000,
    mono: false,
    waveHeight: 80,
    container: document.getElementById("playlist"),
    timescale: true,
    UITheme: "bootstrap",
    state: 'select'
});

var playlistEditor = Object.create(WaveformPlaylist, {
    config: {
        value: config
    }
});

var isIE = false;
var maxCrop;
$(function() {
    var  nav=navigator.userAgent.toLowerCase();
    if (!!window.ActiveXObject || "ActiveXObject" in window) {
        isIE = true;
    } else if (nav.match(/opr\/([\d\.]+)/)) {
        isIE = true;
    }
    $("#playlist").hide();
    maxCrop = $('#maxCrop').val();
});

function loadLocalMusic(file) {
    var f = file.getSource().getSource();
    var url = window.URL.createObjectURL(f);
    pause_single_sound();
//    showWave(url);
    musicLoaded = file;
    curr_custom_song = f.name;
    showPlainMusic(url, f.name);
    //selectMusic_noui('', f.name, "自定义铃声", null, null, null);
}

function showPlainMusic(url, name) {
    var tmp = document.getElementById("pmPanel");
    if (tmp) {
        $("#cropMusic").hide();
        $("#fsUploadProgress").hide();
        $("#playlist").hide();
        $("#audioPlayerPanel").hide();
        var tmp_select = '<a href="javascript:void(0);" title="选择"><span class="si si-unselect" onclick="selectPlainMusic(event)"></span></a>';
        if (selectedMusic.md5 != '' && url.indexOf(selectedMusic.md5) != -1) {
            tmp_select = '<a href="javascript:void(0);" title="取消"><span class="si si-select" onclick="unselectPlainMusic(event)"></span></a>';
        }
        tmp.innerHTML = '\
        <table class="table table-hover table-pb-music" style="margin-top:10px">\
          <thead>\
          </thead>\
          <tbody style="border-bottom:1px solid #dddddd;border-top:1px solid #dddddd">\
            <tr class="active" onclick="playPlainMusic(\''+url+'\', \'plainMusic\', \''+curr_custom_song+'\', \'\')">\
              <td>'+curr_custom_song+'</td>\
              <audio id="plainMusic" preload="auto" src="'+url+'"></audio>\
              <td id="uploadPlay" class="table-pb-music-btn"></td>\
              <td id="uploadSelect" class="table-pb-music-btn">'+tmp_select+'</td>\
            </tr>\
          </tbody>\
        </table>\
        <button class="btn btn-cd-gray" onclick="showWave(\''+url+'\')">时段选择</button>';
        tmp.style.display="block";
    }
}

function selectPlainMusic(event) {
    pause_single_sound();
    saveMusicCrop();
    var tmp = document.getElementById("uploadSelect");
    if (tmp) {
        tmp.innerHTML = '<a href="javascript:void(0);" title="取消"><span class="si si-select" onclick="unselectPlainMusic(event)"></span></a>';
    }
    if (event) {
        event.stopPropagation();
    }
}

function unselectPlainMusic(event) {
    deleteMusic();
    var tmp = document.getElementById("uploadSelect");
    if (tmp) {
        tmp.innerHTML = '<a href="javascript:void(0);" title="选择"><span class="si si-unselect" onclick="selectPlainMusic(event)"></span></a>';
    }
    if (event) {
        event.stopPropagation();
    }
}

function playPlainMusic(url, tag, name, crop) {
    var player = document.getElementById(tag);
    if (player) {
        var played_url = getCookie("played_url");
        var player_selected = document.getElementById("selected1");
        var player_plain = document.getElementById("plainMusic");
        if (played_url == url) {
            if (player_selected) player_selected.pause();
            if (player_plain) player_plain.pause();
            setCookie("played_music", '');
            setCookie("played_url", '');
        } else {
            pause_single_sound();
            player.play();
            setCookie("played_url", url);
            setCookie("played_music", tag);
        }
    }
    updateSelectedMusic();
    updatePlainMusic();
    updateOnEnded();
}


function showWave(url, crop) {
    var selected;
    pause_single_sound();
    $("#cropMusic").show();
    $("#pmPanel").hide();
    $("#fsUploadProgress").hide();
    if (crop != undefined) {
        var tmp = crop.split(",");
        if (tmp.length == 2) {
            try {
                if (isIE) {
                    mStart=tmp[0];
                    mEnd=tmp[1];
                } else {
                    selected = {start:tmp[0], end:tmp[1]};
                }
            } catch (err) {
            }
        }
    } else {
        mStart = 0;
        mEnd = 0;
    }
    if (isIE) {
        document.getElementById("uploadMusic").src=url;
        document.getElementById("audioPlayerPanel").style.display="block";
        document.getElementById("apTimeline").style.width=($(".panel-cd-main").width()-80)+"px";
        uploadMusic.load();
    } else {
        var tracks = [
            {
                "start":0,
                "end":235.83344671201814,
                "fades":[
                    {
                        "type":"FadeOut",
                        "shape":"sCurve",
                        "start":234.69387755102042,
                        "end":235.83344671201814
                    }
                ],
                "src":url,
                "cuein":0,
                "cueout":235.83344671201814,
                "selected": selected,
            },
        ];
    
        try {
            playlistEditor.audioControls.open(); //destroy the old one
        } catch (err) {}
        playlistEditor.init(tracks);
    
        if (selected == undefined) {
        } else {
            var selected_val = {
                start: parseFloat(selected.start),
                end: parseFloat(selected.end),
            }
            playlistEditor.onSelectionChange(selected_val);
            playlistEditor.audioControls.onCursorSelection(selected_val);
            playlistEditor.audioControls.onAudioUpdate({seconds: selected.start});
        }
        $("#playlist").show();
    }
}

$(function() {
    var qiniu = Qiniu.uploader({
        runtimes: 'html5,flash,html4',
        browse_button: 'pickfiles',
        uptoken_url: '/v1/maker/uptoken2',
        domain: 'http://7xio6q.com1.z0.glb.clouddn.com/',
        container: 'container',
        drop_element: 'container',
        max_file_size: '20mb',
        flash_swf_url: '/static/js/plupload/Moxie.swf',
        dragdrop: true,
        multi_selection:false,
        filters : [
            {title : "音乐文件", extensions : "mp3"}
        ],
        chunk_size: '4mb',
        //uptoken_url: $('#uptoken_url').val(),
        //domain: $('#domain').val(),
        // downtoken_url: '/downtoken',
        // unique_names: true,
        // save_key: true,
        // x_vars: {
        //     'id': '1234',
        //     'time': function(up, file) {
        //         var time = (new Date()).getTime();
        //         // do something with 'time'
        //         return time;
        //     },
        // },
        auto_start: false,
        init: {
            'FilesAdded': function(up, files) {
                $('table').show();
                $('#success').hide();
                plupload.each(files, function(file) {
                    var progress = new FileProgress(file, 'fsUploadProgress');
                    progress.setStatus("等待...");
                    //load_music(window.URL.createObjectURL(f), f.name);
                    loadLocalMusic(file);
                    md5sum(file.getSource().getSource(), function (ret) {
                        // use md5sum as file id
                        encMd5Sum(file, ret);
                        up.start();
                    });
                });
            },
            'BeforeUpload': function(up, file) {
                var progress = new FileProgress(file, 'fsUploadProgress');
                var chunk_size = plupload.parseSize(this.getOption('chunk_size'));
                if (up.runtime === 'html5' && chunk_size) {
                    progress.setChunkProgess(chunk_size);
                }
            },
            'UploadProgress': function(up, file) {
                var progress = new FileProgress(file, 'fsUploadProgress');
                var chunk_size = plupload.parseSize(this.getOption('chunk_size'));

                progress.setProgress(file.percent + "%", file.speed, chunk_size);
            },
            'UploadComplete': function() {
                $('#success').show();
            },
            'FileUploaded': function(up, file, info) {
                var progress = new FileProgress(file, 'fsUploadProgress');
                progress.setComplete(up, info);
                //saveMusicCrop();
            },
            'Error': function(up, err, errTip) {
                $('table').show();
                var progress = new FileProgress(err.file, 'fsUploadProgress');
                progress.setError();
                progress.setStatus(errTip);
                setCookie("qiniu_token", '', 10);                           ////yuan
            },

            'Key': function(up, file) {
                return decMd5Sum(file);
            }

            // ,
            // 'Key': function(up, file) {
            //     var key = "";
            //     // do something with key
            //     return key
            // }
        }
    });

    $('#container').on(
        'dragenter',
        function(e) {
            e.preventDefault();
            $('#container').addClass('draging');
            e.stopPropagation();
        }
    ).on('drop', function(e) {
        e.preventDefault();
        $('#container').removeClass('draging');
        e.stopPropagation();
    }).on('dragleave', function(e) {
        e.preventDefault();
        $('#container').removeClass('draging');
        e.stopPropagation();
    }).on('dragover', function(e) {
        e.preventDefault();
        $('#container').addClass('draging');
        e.stopPropagation();
    });

    $('#show_code').on('click', function() {
        $('#myModal-code').modal();
        $('pre code').each(function(i, e) {
            hljs.highlightBlock(e);
        });
    });

    var getRotate = function(url) {
        if (!url) {
            return 0;
        }
        var arr = url.split('/');
        for (var i = 0, len = arr.length; i < len; i++) {
            if (arr[i] === 'rotate') {
                return parseInt(arr[i + 1], 10);
            }
        }
        return 0;
    };

    $('#myModal-img .modal-body-footer').find('a').on('click', function() {
        var img = $('#myModal-img').find('.modal-body img');
        var key = img.data('key');
        var oldUrl = img.attr('src');
        var originHeight = parseInt(img.data('h'), 10);
        var fopArr = [];
        var rotate = getRotate(oldUrl);
        if (!$(this).hasClass('no-disable-click')) {
            $(this).addClass('disabled').siblings().removeClass('disabled');
            if ($(this).data('imagemogr') !== 'no-rotate') {
                fopArr.push({
                    'fop': 'imageMogr2',
                    'auto-orient': true,
                    'strip': true,
                    'rotate': rotate,
                    'format': 'png'
                });
            }
        } else {
            $(this).siblings().removeClass('disabled');
            var imageMogr = $(this).data('imagemogr');
            if (imageMogr === 'left') {
                rotate = rotate - 90 < 0 ? rotate + 270 : rotate - 90;
            } else if (imageMogr === 'right') {
                rotate = rotate + 90 > 360 ? rotate - 270 : rotate + 90;
            }
            fopArr.push({
                'fop': 'imageMogr2',
                'auto-orient': true,
                'strip': true,
                'rotate': rotate,
                'format': 'png'
            });
        }

        $('#myModal-img .modal-body-footer').find('a.disabled').each(function() {

            var watermark = $(this).data('watermark');
            var imageView = $(this).data('imageview');
            var imageMogr = $(this).data('imagemogr');

            if (watermark) {
                fopArr.push({
                    fop: 'watermark',
                    mode: 1,
                    image: 'http://www.b1.qiniudn.com/images/logo-2.png',
                    dissolve: 100,
                    gravity: watermark,
                    dx: 100,
                    dy: 100
                });
            }

            if (imageView) {
                var height;
                switch (imageView) {
                    case 'large':
                        height = originHeight;
                        break;
                    case 'middle':
                        height = originHeight * 0.5;
                        break;
                    case 'small':
                        height = originHeight * 0.1;
                        break;
                    default:
                        height = originHeight;
                        break;
                }
                fopArr.push({
                    fop: 'imageView2',
                    mode: 3,
                    h: parseInt(height, 10),
                    q: 100,
                    format: 'png'
                });
            }

            if (imageMogr === 'no-rotate') {
                fopArr.push({
                    'fop': 'imageMogr2',
                    'auto-orient': true,
                    'strip': true,
                    'rotate': 0,
                    'format': 'png'
                });
            }
        });

        var newUrl = Qiniu.pipeline(fopArr, key);

        var newImg = new Image();
        img.attr('src', '/static/images/loading.gif');
        newImg.onload = function() {
            img.attr('src', newUrl);
            img.parent('a').attr('href', newUrl);
        };
        newImg.src = newUrl;
        return false;
    });

});

var uploadMusic = document.getElementById('uploadMusic'); // id for audio element
var apBtnPlay = document.getElementById('apBtnPlay'); // play button
var playhead = document.getElementById('apPlayhead'); // playhead
var timeline = document.getElementById('apTimeline'); // timeline
var timelineWidth = timeline.offsetWidth - playhead.offsetWidth;
var duration; // Duration of audio clip
var apSelection  = document.getElementById('apSelection');

// timeupdate event listener
uploadMusic.addEventListener("timeupdate", timeUpdate, false);

//Makes timeline clickable
//timeline.addEventListener("click", function (event) {
//    moveplayhead(event);
//    if (duration) {
//        uploadMusic.currentTime = duration * clickPercent(event);
//    }
//}, false);

// returns click as decimal (.77) of the total timelineWidth
function clickPercent(e) {
    return (e.pageX - $('#apTimeline').offset().left) / timelineWidth;
}

// Makes playhead draggable 
audioplayer.addEventListener('mousedown', mouseDown, false);
window.addEventListener('mouseup', mouseUp, false);

// Boolean value so that mouse is moved on mouseUp only when the playhead is released 
var onplayhead = false;
// mouseDown EventListener
function mouseDown(e) {
    if (e.pageX <= $('#apTimeline').offset().left) 
        return;
    onplayhead = true;
    moveplayhead(e);
    selectStart();
    window.addEventListener('mousemove', moveplayhead, true);
    uploadMusic.removeEventListener('timeupdate', timeUpdate, false);
}
// mouseUp EventListener
// getting input from all mouse clicks
function mouseUp(e) {
    if (onplayhead == true) {
        moveplayhead(e);
        window.removeEventListener('mousemove', moveplayhead, true);
        // change current time
        uploadMusic.currentTime = duration * clickPercent(e);
        uploadMusic.addEventListener('timeupdate', timeUpdate, false);
        mSelectStart = 0;
    }
    onplayhead = false;
}
// mousemove EventListener
// Moves playhead as user drags
function moveplayhead(e) {
    if (onplayhead == false) {
        return;
    }
    var currentTime = duration * clickPercent(e);
    if (mSelectStart != 0 && Math.abs(currentTime-mSelectStart) > maxCrop) {
        onplayhead = false;
        mSelectStart = 0;
        window.removeEventListener('mousemove', moveplayhead, true);
        uploadMusic.addEventListener('timeupdate', timeUpdate, false);
        showToast('error', "请截取长度小于"+ maxCrop +"秒的片段");
        return;
    }
    //var newMargLeft = e.pageX - timeline.offsetLeft;
    var newMargLeft = e.pageX - $('#apTimeline').offset().left;
    if (newMargLeft >= 0 && newMargLeft <= timelineWidth) {
        playhead.style.marginLeft = timeline.offsetLeft + newMargLeft + "px";
    }
    if (newMargLeft < 0) {
        playhead.style.marginLeft = timeline.offsetLeft + "px";
    }
    if (newMargLeft > timelineWidth) {
        playhead.style.marginLeft = timeline.offsetLeft + timelineWidth + "px";
    }
    uploadMusic.currentTime = currentTime;
    selectUpdate();
}

// timeUpdate 
// Synchronizes playhead position with current point in audio 
function timeUpdate() {
    var playPercent = timelineWidth * (uploadMusic.currentTime / duration);
    playhead.style.marginLeft = timeline.offsetLeft + playPercent + "px";
    if ((uploadMusic.paused==false) && ((mEnd > 0 && uploadMusic.currentTime >= mEnd) || uploadMusic.currentTime >= uploadMusic.duration)) {
        uploadMusic.pause();
        uploadMusic.currentTime=mStart;
        apBtnPlay.className = "";
        apBtnPlay.className = "apBtnPlay";
        updatedSelectedLocalMusic('pause');
    }
    document.getElementById("mCurrent").innerHTML=cueFormatters("hh:mm:ss.uu")(uploadMusic.currentTime);
}

function play() {
    if (uploadMusic.paused) {
        if ((mStart > 0 && uploadMusic.currentTime < mStart) || (mEnd > 0 && uploadMusic.currentTime >= mEnd)) {
            uploadMusic.currentTime=mStart;
        }
        uploadMusic.play();
        // remove play, add pause
        apBtnPlay.className = "";
        apBtnPlay.className = "apBtnPause";
        updatedSelectedLocalMusic('play');
    } else {
        pause();
    }
}

function pause() {
    if (!uploadMusic.paused) {
        uploadMusic.pause();
        apBtnPlay.className = "";
        apBtnPlay.className = "apBtnPlay";
        updatedSelectedLocalMusic('pause');
    }
}

// Gets audio file duration
uploadMusic.addEventListener("canplaythrough", function () {
    duration = uploadMusic.duration;
    if (mEnd==0) {
        mEnd = uploadMusic.duration;
    }
    timelineWidth = timeline.offsetWidth - playhead.offsetWidth;
    updateSelectedMusic();
    document.getElementById("apBtnPlay").style.visibility="visible";
    document.getElementById("mStart").innerHTML=cueFormatters("hh:mm:ss.uu")(mStart);
    document.getElementById("mEnd").innerHTML=cueFormatters("hh:mm:ss.uu")(mEnd);
    document.getElementById("mCurrent").innerHTML=cueFormatters("hh:mm:ss.uu")(mStart);
    if (mStart!=0) {
        uploadMusic.currentTime=mStart;
        updateSelection();
    }
}, false);

var mSelectStart=0, mStart=0, mEnd=0;
function selectStart() {
    mSelectStart = uploadMusic.currentTime;
    mStart=0;
    mEnd = 0;
    updateSelection();
}
function selectUpdate() {
    if (uploadMusic.currentTime > mSelectStart) {
        mStart = mSelectStart;
        mEnd = uploadMusic.currentTime;
    } else if (uploadMusic.currentTime == mSelectStart) {
        mStart = 0;
        mEnd = uploadMusic.duration;
        return;
    } else {
        mStart = uploadMusic.currentTime;
        mEnd = mSelectStart;
    }
    updateSelection();
}

function updateSelection() {
    var start = timelineWidth * (mStart / duration);
    var end = timelineWidth * (mEnd / duration);
    if (start > end) {
        var tmp = start;
        start = end;
        end = tmp;
    }
    apSelection.style.left = timeline.offsetLeft+start+"px";
    apSelection.style.width = (end-start)+"px";
    document.getElementById("mStart").innerHTML=cueFormatters("hh:mm:ss.uu")(mStart);
    document.getElementById("mEnd").innerHTML=cueFormatters("hh:mm:ss.uu")(mEnd==0?duration:mEnd);
}
function cueFormatters (format) {

    function clockFormat(seconds, decimals) {
        var hours,
            minutes,
            secs,
            result;

        hours = parseInt(seconds / 3600, 10) % 24;
        minutes = parseInt(seconds / 60, 10) % 60;
        secs = seconds % 60;
        secs = secs.toFixed(decimals);

        result = (hours < 10 ? "0" + hours : hours) + ":" + (minutes < 10 ? "0" + minutes : minutes) + ":" + (secs < 10 ? "0" + secs : secs);

        return result;
    }

    var formats = {
        "seconds": function (seconds) {
            return seconds.toFixed(0);
        },

        "thousandths": function (seconds) {
            return seconds.toFixed(3);
        },

        "hh:mm:ss": function (seconds) {
            return clockFormat(seconds, 0);
        },

        "hh:mm:ss.u": function (seconds) {
            return clockFormat(seconds, 1);
        },

        "hh:mm:ss.uu": function (seconds) {
            return clockFormat(seconds, 2);
        },

        "hh:mm:ss.uuu": function (seconds) {
            return clockFormat(seconds, 3);
        }
    };

    return formats[format];
}

$(window).resize(function() {
    if (selectedMusic.prebuilt == '' && selectedMusic.md5 != "") {
        var url = "http://7xio6q.com1.z0.glb.clouddn.com/" + selectedMusic.md5;
        if (selectedMusic.crop != '') {
            showWave(url, selectedMusic.crop);
        } else {
            showPlainMusic(url, selectedMusic.songname);
        }
    }
});

