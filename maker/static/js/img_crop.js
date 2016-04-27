var boundx, boundy;
var scale = 1, jcrop_api;
var img_crop = "#image_crop";
var screenHeight, screenWidth;
var panelHeight = 480;
var xx=0, yy=0, ww=0, hh=0;
var cur_url, cur_key;

function updateInfo(e) {
    xx = Math.ceil(e.x * scale);
    yy = Math.ceil(e.y * scale);
    ww = Math.ceil(e.w * scale);
    hh = Math.ceil(e.h * scale);
}

function cropRelease() {
    xx = yy = ww = hh = 0;
}

function cropSave() {
    if (ww == 0 || hh == 0) {
        alert("请选取区域");
        return;
    }

    var ret = cur_url + "?imageMogr2/crop/!"+ww+"x"+hh+"a"+xx+"a"+yy;
    selectImage(ret,cur_key,'',ww+"x"+hh+"a"+xx+"a"+yy,'');
}

function cropImage(url, key, origin_width, origin_height) {
    var cache = new Image();
    if (window.location.href.search("wallpaper_head") != -1) {
        if (mclass && mclass == 'm3') {
            screenHeight = 804;
            screenWidth = 720;
        } else {
            screenHeight = 498;
            screenWidth = 480;
        }
    } else {
        if (mclass && mclass == 'm3') {
            screenHeight = 1280;
            screenWidth = 720;
        } else {
            screenHeight = 800;
            screenWidth = 480;
        }
    }
    cur_url = url;
    cur_key = key;
    $(cache).attr('src', url);
    $(cache).on('load', function() {
        $(img_crop).attr('src', url);
        var oh = origin_height;
        var ow = origin_width;
        scale = oh / panelHeight;

        $(img_crop).width(ow / scale);
        $(img_crop).height(oh / scale);
        if (typeof jcrop_api != 'undefined')
            jcrop_api.destroy();

        $(img_crop).Jcrop({
            boxWidth: parseInt(ow / scale),
            boxHeight: parseInt(oh / scale),
            bgFade: true, // use fade effect
            bgOpacity: .3, // fade opacity
            onSelect: updateInfo,
            onRelease: cropRelease,
            aspectRatio: screenWidth / screenHeight,
            minSize: [screenWidth/10, screenHeight/10],
            setSelect: [0, 0, panelHeight/screenHeight*screenWidth, panelHeight],
        }, function () {
            var bounds = this.getBounds();
            boundx = bounds[0];
            boundy = bounds[1];
            jcrop_api = this;
            // Store the API in the jcrop_api variable
            // Move the preview into the jcrop container for css positioning
            //$("#preview").appendTo(jcrop_api.ui.holder);
        });
    });
}

/*global Qiniu */
/*global plupload */
/*global FileProgress */
/*global hljs */


$(function() {
    var uploader = Qiniu.uploader({
        runtimes: 'html5,flash,html4',
        browse_button: 'pickfiles',
        uptoken_url: '/v1/maker/uptoken2',
        domain: 'http://7xio6q.com1.z0.glb.clouddn.com/',
        container: 'container',
        drop_element: 'container',
        max_file_size: '10mb',
        flash_swf_url: '/static/js/plupload/Moxie.swf',
        dragdrop: true,
        multi_selection:false,
        filters : [
            {title : "图片文件", extensions : "jpg,png,jpeg"}
        ],
        chunk_size: '4mb',
        uptoken_url: $('#uptoken_url').val(),
        domain: $('#domain').val(),
        // downtoken_url: '/downtoken',
        // unique_names: true,
        // save_key: true,
        // x_vars: {
        //     'id': '1234',
        //     'time': function(up, file) {
        //         var time = (new Date()).getTime();
        //         // do something with 'time'
        //         return time;pipeline
        //     },
        // },
        auto_start: true,
        init: {
            'FilesAdded': function(up, files) {
                $('table').show();
                $('#success').hide();
                plupload.each(files, function(file) {
                    var progress = new FileProgress(file, 'fsUploadProgress');
                    progress.setStatus("等待...");
                });
            },
            'BeforeUpload': function(up, file) {
                var progress = new FileProgress(file, 'fsUploadProgress');
                var chunk_size = plupload.parseSize(this.getOption('chunk_size'));
                if (up.runtime === 'html5' && chunk_size) {
                    progress.setChunkProgess(chunk_size);
                }
                $('#uploadingModal').modal('show');
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

            },
            'Error': function(up, err, errTip) {
                $('table').show();
                var progress = new FileProgress(err.file, 'fsUploadProgress');
                progress.setError();
                progress.setStatus(errTip);
                setCookie("qiniu_token", '');                           ////yuan
            },

            'Key': function(up, file) {
                var d = new Date();
                var seed = d.getTime() + "";
                var key = hex_md5(seed);
                //cdLog(key);
                //var now = new Date();
                // do something with key
                //return key+"_"+now.getTime()+"_"+file.name;
                return key +"_"+file.name;
            }


            // ,
            // 'Key': function(up, file) {
            //     var key = "";
            //     // do something with key
            //     return key
            // }
        }
    });

    uploader.bind('FileUploaded', function() {
        //cdLog('hello man,a file is uploaded');
        $('#img-upload-panel').css('display','block');
        $('#cropimage').css('display','block');
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


    $('body').on('click', 'table button.btn', function() {
        $(this).parents('tr').next().toggle();
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

