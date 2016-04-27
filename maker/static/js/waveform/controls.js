'use strict';

WaveformPlaylist.AudioControls = {
    groups: {
        "audio-select": ["btns_audio_tools"]
    },

    classes: {
        "disabled": "disabled",
        "active": "active"
    },

    events: {
       "btn-rewind": {
            click: "rewindAudio"
        },

        "btn-fast-forward": {
            click: "fastForwardAudio"
        },

       "btn-play": {
            click: "playAudio"
        },

        "btn-pause": {
            click: "pauseAudio"
        },
     
        "btn-stop": {
            click: "stopAudio"
        },

        "btn-cursor": {
            click: "changeState"
        },

        "btn-select": {
            click: "changeState"
        },

        "btn-shift": {
            click: "changeState"
        },

        "btn-fadein": {
            click: "changeState"
        },

        "btn-fadeout": {
            click: "changeState"
        },

        "btn-save": {
            click: "save"
        },

        "btn-open": {
            click: "open"
        },
        
        "btn-trim-audio": {
            click: "trimAudio"
        },

        "time-format": {
            change: "changeTimeFormat"
        },

        "audio-pos": {

        },

        "audio-start": {
            blur: "validateCueIn"
        },

        "audio-end": {
            blur: "validateCueOut"
        },

        "btn-logarithmic": {
            click: "changeDefaultFade"
        },

        "btn-linear": {
            click: "changeDefaultFade"
        },

        "btn-exponential": {
            click: "changeDefaultFade"
        },

        "btn-sCurve": {
            click: "changeDefaultFade"
        },

        "btn-zoom-in": {
            click: "zoomIn"
        },

        "btn-zoom-out": {
            click: "zoomOut"
        },

        "btn-new-track": {
            click: "newTrack"
        }
    },

    validateCue: function(value) {
        var validators,
            regex,
            result;

        validators = {
            "seconds": /^\d+$/,

            "thousandths": /^\d+\.\d{3}$/,

            "hh:mm:ss": /^[0-9]{2,}:[0-5][0-9]:[0-5][0-9]$/,

            "hh:mm:ss.u": /^[0-9]{2,}:[0-5][0-9]:[0-5][0-9]\.\d{1}$/,

            "hh:mm:ss.uu": /^[0-9]{2,}:[0-5][0-9]:[0-5][0-9]\.\d{2}$/,

            "hh:mm:ss.uuu": /^[0-9]{2,}:[0-5][0-9]:[0-5][0-9]\.\d{3}$/
        };

        regex = validators[this.timeFormat];
        result = regex.test(value);

        return result;
    },

    cueToSeconds: function(value) {
        var converter,
            func,
            seconds;

        function clockConverter(value) {
            var data = value.split(":"),
                hours = parseInt(data[0], 10) * 3600,
                mins = parseInt(data[1], 10) * 60,
                secs = parseFloat(data[2]),
                seconds;

            seconds = hours + mins + secs;

            return seconds;
        }

        converter = {
            "seconds": function(value) {
                return parseInt(value, 10);
            },

            "thousandths": function(value) {
                return parseFloat(value);
            },

            "hh:mm:ss": function(value) {
                return clockConverter(value);
            },

            "hh:mm:ss.u": function(value) {
                return clockConverter(value);
            },

            "hh:mm:ss.uu": function(value) {
                return clockConverter(value);
            },

            "hh:mm:ss.uuu": function(value) {
                return clockConverter(value);
            } 
        };

        func = converter[this.timeFormat];
        seconds = func(value);

        return seconds;
    },

    cueFormatters: function(format) {

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
    },

    init: function() {
        var that = this,
            className,
            event,
            events = this.events,
            tmpEl,
            func,
            state,
            container,
            fadeType,
            tmpBtn;

        this.maxCrop = $('#maxCrop').val();
        this.lastCheck = true;

        WaveformPlaylist.makePublisher(this);

        this.ctrls = {};
        container = this.config.getContainer();
        state = this.config.getState();
        fadeType = this.config.getFadeType();

        ["btn-"+state, "btn-"+fadeType].forEach(function(buttonClass) {
            tmpBtn = document.getElementsByClassName(buttonClass)[0];

            if (tmpBtn) {
                this.activateButton(tmpBtn);
            }
        }, this);  

        for (className in events) {
        
            tmpEl = container.getElementsByClassName(className)[0];
            this.ctrls[className] = tmpEl;

            for (event in events[className]) {

                if (tmpEl) {
                    func = that[events[className][event]].bind(that);
                    tmpEl.addEventListener(event, func);
                }
            }
        } 

        if (this.ctrls["time-format"]) {
            this.ctrls["time-format"].value = this.config.getTimeFormat();
        }


        this.timeFormat = this.config.getTimeFormat();

        //Kept in seconds so time format change can update fields easily.
        this.currentSelectionValues = undefined;
      
        this.onCursorSelection({
            start: 0,
            end: 0
        });
    },

    changeDefaultFade: function(e) {
        var el = e.currentTarget,
            prevEl = el.parentElement.getElementsByClassName('active')[0],
            type = el.dataset.fade;

        this.deactivateButton(prevEl);
        this.activateButton(el);

        this.config.setFadeType(type);
    },

    changeTimeFormat: function(e) {
        var format = e.target.value,
            func, start, end;

        format = (this.cueFormatters(format) !== undefined) ? format : "hh:mm:ss";
        this.config.setTimeFormat(format);
        this.timeFormat = format;

        if (this.currentSelectionValues !== undefined) {
            func = this.cueFormatters(format);
            start = this.currentSelectionValues.start;
            end = this.currentSelectionValues.end;

            if (this.ctrls["audio-start"]) {
                this.ctrls["audio-start"].value = func(start);
            }

            if (this.ctrls["audio-end"]) {
                this.ctrls["audio-end"].value = func(end);
            }
        }
    },

    zoomIn: function() {
        var newRes = this.config.getResolution() * (3/4),
            min = this.config.getMinResolution();

        newRes = (newRes < min) ? min : newRes;

        if (newRes > min) {
            this.zoom(newRes);
        }
    },

    zoomOut: function() {
        var newRes = this.config.getResolution() * (4/3),
            max = this.config.getMaxResolution();

        newRes = (newRes > max) ? max : newRes;

        if (newRes < max) {
            this.zoom(newRes);
        }
    },

    zoom: function(res) {
        this.config.setResolution(res);
        this.fire("changeresolution", res);
    },

    newTrack: function() {
        this.fire("newtrack");
    },

    validateCueIn: function(e) {
        var value = e.target.value,
            end,
            startSecs;

        if (this.validateCue(value)) {
            end = this.currentSelectionValues.end;
            startSecs = this.cueToSeconds(value);

            if (startSecs <= end) {
                this.notifySelectionUpdate(startSecs, end);
                this.currentSelectionValues.start = startSecs;
                return;
            }
        }

        //time entered was otherwise invalid.
        e.target.value = this.cueFormatters(this.timeFormat)(this.currentSelectionValues.start);
    },

    validateCueOut: function(e) {
        var value = e.target.value,
            start,
            endSecs;

        if (this.validateCue(value)) {
            start = this.currentSelectionValues.start;
            endSecs = this.cueToSeconds(value);

            if (endSecs >= start) {
                this.notifySelectionUpdate(start, endSecs);
                this.currentSelectionValues.end = endSecs;
                return;
            }
        }

        //time entered was otherwise invalid.
        e.target.value = this.cueFormatters(this.timeFormat)(this.currentSelectionValues.end);
    },

    activateButtonGroup: function(id) {
        var el = document.getElementById(id),
            btns,
            classes = this.classes,
            i, len;

        if (el === null) {
            return;
        }

        btns = el.children;

        for (i = 0, len = btns.length; i < len; i++) {
            btns[i].classList.remove(classes["disabled"]);
        }
    },

    deactivateButtonGroup: function(id) {
        var el = document.getElementById(id),
            btns,
            classes = this.classes,
            i, len;

        if (el === null) {
            return;
        }

        btns = el.children;

        for (i = 0, len = btns.length; i < len; i++) {
            btns[i].classList.add(classes["disabled"]);
        }
    },

    activateAudioSelection: function() {
        var ids = this.groups["audio-select"],
            i, len;

        for (i = 0, len = ids.length; i < len; i++) {
            this.activateButtonGroup(ids[i]);
        }
    },

    deactivateAudioSelection: function() {
        var ids = this.groups["audio-select"],
            i, len;

        for (i = 0, len = ids.length; i < len; i++) {
            this.deactivateButtonGroup(ids[i]);
        }
    },

    save: function() {
        this.fire('playlistsave', this);
    },

    open: function() {
        this.fire('playlistrestore', this);
    },

    rewindAudio: function() {
        this.fire('rewindaudio', this);
    },

    fastForwardAudio: function() {
        this.fire('fastforwardaudio', this);
    },

    playAudio: function() {
        this.fire('playaudio', this);
        updatedSelectedLocalMusic('play');
    },

    pauseAudio: function() {
        this.fire('pauseaudio', this);
        updatedSelectedLocalMusic('pause');
    },

    stopAudio: function() {
        this.fire('stopaudio', this);
        updatedSelectedLocalMusic('pause');
    },

    activateButton: function(el) {
        if (el) {
            el.classList.add(this.classes["active"]);
        }
    },

    deactivateButton: function(el) {
        if (el) {
            el.classList.remove(this.classes["active"]);
        }
    },

    enableButton: function(el) {
        if (el) {
            el.classList.remove(this.classes["disabled"]);
        }
    },

    disableButton: function(el) {
        if (el) {
            el.classList.add(this.classes["disabled"]);
        }
    },

    changeState: function(e) {
        var el = e.currentTarget,
            prevEl = el.parentElement.getElementsByClassName('active')[0],
            state = el.dataset.state;

        this.deactivateButton(prevEl);
        this.activateButton(el);

        this.config.setState(state);
        this.fire('changestate', this);
    },

    trimAudio: function(e) {
        var el = e.target,
            disabled,
            classes = this.classes;

        disabled = el.classList.contains(classes["disabled"]);

        if (!disabled) {
            this.fire('trackedit', {
                type: "trimAudio"
            });
        }  
    },

    createFade: function(e) {
        var el = e.target,
            shape = el.dataset.shape,
            type = el.dataset.type,
            disabled,
            classes = this.classes;

        disabled = el.classList.contains(classes["disabled"]);

        if (!disabled) {
            this.fire('trackedit', {
                type: "createFade",
                args: {
                    type: type, 
                    shape: shape
                }
            });
        }  
    },

    onAudioSelection: function() {
        this.activateAudioSelection();
    },

    onAudioDeselection: function() {
        this.deactivateAudioSelection();
    },

    /*
        start, end in seconds
    */
    notifySelectionUpdate: function(start, end) {
        
        this.fire('changeselection', {
            start: start,
            end: end
        });
    },

    /*
        start, end in seconds
    */

    onCursorSelection: function(args) {
        var startFormat = this.cueFormatters(this.timeFormat)(args.start),
            endFormat = this.cueFormatters(this.timeFormat)(args.end),
            start = this.cueToSeconds(startFormat),
            end = this.cueToSeconds(endFormat);

        this.currentSelectionValues = {
            start: start,
            end:end
        };

        if (this.ctrls["audio-start"]) {
            this.ctrls["audio-start"].value = startFormat;
        }

        if (this.ctrls["audio-end"]) {
            this.ctrls["audio-end"].value = endFormat;
        }

        if ((end - start) > this.maxCrop) {
            if (this.lastCheck) {
                showToast('error',"请截取长度小于"+ this.maxCrop +"秒的片段");
            }
            
            var expected_end = parseFloat(start) + parseFloat(this.maxCrop);
            var selected_val = {
                start: parseFloat(start),
                end: parseFloat(expected_end),
            }

            this.notifySelectionUpdate(start, expected_end);
            this.lastCheck = false;
        }
        else {
            this.lastCheck = true;
        }

    },

    /*
        args {seconds, pixels}
    */
    onAudioUpdate: function(args) {
        if (this.ctrls["audio-pos"]) {
            this.ctrls["audio-pos"].innerHTML = this.cueFormatters(this.timeFormat)(args.seconds);
        } 
    }
};
