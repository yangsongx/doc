'use strict';

var WaveformPlaylist = {

    init: function(tracks) {
        var that = this,
            i,
            len,
            container = this.config.getContainer(),
            div = container.querySelector(".playlist-tracks"),
            fragment = document.createDocumentFragment(),
            trackEditor,
            trackElem,
            audioControls;

        tracks = tracks || [];

        WaveformPlaylist.makePublisher(this);

        this.storage = Object.create(WaveformPlaylist.Storage);

        container.style.overflow = "hidden";

        this.trackContainer = div;
        this.trackContainer.style.position = "relative";
        this.trackContainer.style.overflow = "auto";

        this.trackEditors = [];

        audioControls = Object.create(WaveformPlaylist.AudioControls, {
            config: {
                value: this.config
            }
        });
        audioControls.init();

        if (this.config.isTimeScaleEnabled()) {
            this.timeScale = Object.create(WaveformPlaylist.TimeScale, {
                config: {
                    value: this.config
                }
            });
            this.timeScale.init();

            audioControls.on("changeresolution", "onResolutionChange", this.timeScale);
            this.on("trackscroll", "onTrackScroll", this.timeScale);
        }
        
        for (i = 0, len = tracks.length; i < len; i++) {

            trackEditor = Object.create(WaveformPlaylist.TrackEditor, {
                config: {
                    value: this.config
                }
            });
            trackElem = trackEditor.loadTrack(tracks[i]);
        
            this.trackEditors.push(trackEditor);
            fragment.appendChild(trackElem);

            trackEditor.on("trackloaded", "onTrackLoad", this);
        }

        this.trackEditors[0].activate();
        this.activeTrack = this.trackEditors[0];

        this.trackContainer.appendChild(fragment);
        this.trackContainer.onscroll = this.onTrackScroll.bind(this);

        this.sampleRate = this.config.getSampleRate();
       
        this.scrollTimeout = false;

        //for requestAnimationFrame that's toggled during play/stop.
        this.animationRequest;
        this.animationCallback = this.updateEditor.bind(this);

        this.on("playbackcursor", "onAudioUpdate", audioControls);

        audioControls.on("newtrack", "createTrack", this);
        audioControls.on("playlistsave", "save", this);
        audioControls.on("playlistrestore", "restore", this);
        audioControls.on("rewindaudio", "rewind", this);
        audioControls.on("fastforwardaudio", "fastForward", this);
        audioControls.on("playaudio", "play", this);
        audioControls.on("pauseaudio", "pause", this);
        audioControls.on("stopaudio", "stop", this);
        audioControls.on("trimaudio", "onTrimAudio", this);
        audioControls.on("changestate", "onStateChange", this);
        audioControls.on("changeselection", "onSelectionChange", this);

        this.audioControls = audioControls;
    },

    removeTrack: function(trackEditor) {
        var i, 
            len, 
            editor,
            editors = this.trackEditors;
        
        for (i = 0, len = editors.length; i < len; i++) {
            editor = editors[i];

            if (editor === trackEditor) {
                editors.splice(i, 1);
                return;
            }
        }
    },

    resize: function() {
        this.timeScale.onResize();
    },

    onTrimAudio: function() {
        this.activeTrack && this.activeTrack.trim(); 
    },

    /*
        Called when a user manually updates the cue points in the UI.
        args start/end are in seconds
    */
    onSelectionChange: function(args) {
        this.config.setCursorPos(args.start);
        this.activeTrack && this.activeTrack.setSelectedArea(args.start, args.end);
    },

    onStateChange: function() {
         var editors = this.trackEditors,
            i,
            len,
            state = this.config.getState();

        for (i = 0, len = editors.length; i < len; i++) {
            editors[i].deactivate();
            editors[i].setState(state);
        }
    },

    onTrackScroll: function() {
        var that = this;

        if (that.scrollTimeout) return;

        //limit the scroll firing to every 25ms.
        that.scrollTimeout = setTimeout(function() {
            
            that.config.setTrackScroll(that.trackContainer.scrollLeft, that.trackContainer.scrollTop);
            that.fire('trackscroll');
            that.scrollTimeout = false;
        }, 25);   
    },

    activateTrack: function(trackEditor) {
        var editors = this.trackEditors,
            i,
            len,
            editor;

        for (i = 0, len = editors.length; i < len; i++) {
            editor = editors[i];

            if (editor === trackEditor) {
                editor.activate();
                this.activeTrack = trackEditor;
            }
            else {
                editor.deactivate();
            }
        }
    },

    onSelectUpdate: function(event) {
        this.activateTrack(event.editor);
        this.stop();
    },

    onChangeShift: function(event) {
        var editors = this.trackEditors,
            i,
            len,
            maxTrackLengthPixels = 0,
            maxTrackLengthSeconds = 0;

        for (i = 0, len = editors.length; i < len; i++) {
            maxTrackLengthPixels = Math.max(maxTrackLengthPixels, editors[i].drawer.containerWidth);
            maxTrackLengthSeconds = Math.max(maxTrackLengthSeconds, editors[i].endTime);
        }

        //set the width so that the entire area will be selectable when needed.
        for (i = 0, len = editors.length; i < len; i++) {
            editors[i].drawer.container.style.width = maxTrackLengthPixels+'px';
        }

        this.duration = maxTrackLengthSeconds;
    },

    rewind: function() {
        if (this.activeTrack !== undefined) {
            this.activeTrack.notifySelectUpdate(0, 0);
        }
        else {
            this.config.setCursorPos(0);
        } 

        this.stop();

        this.trackContainer.scrollLeft = 0;
        this.config.setTrackScroll(0);
        this.fire('trackscroll');
    },

    fastForward: function() {
        var totalWidth = this.trackContainer.scrollWidth,
            clientWidth = this.trackContainer.offsetWidth,
            maxOffset = Math.max(totalWidth - clientWidth, 0);

        if (this.activeTrack !== undefined) {
            this.activeTrack.notifySelectUpdate(this.duration, this.duration);
        }
        else {
            this.config.setCursorPos(this.duration);
        }

        this.stop();

        this.trackContainer.scrollLeft = maxOffset;
        this.config.setTrackScroll(maxOffset);
        this.fire('trackscroll');
    },

    /*
        returns selected time in global (playlist relative) seconds.
    */
    getSelected: function() {
        if (this.activeTrack) {
            return this.activeTrack.selectedArea;
        }
    },

    isPlaying: function() {
         var editors = this.trackEditors,
            i,
            len,
            isPlaying = false;

        for (i = 0, len = editors.length; i < len; i++) {
            isPlaying = isPlaying || editors[i].isPlaying();
        }

        return isPlaying;
    },

    play: function() {
        var editors = this.trackEditors,
            i,
            len,
            currentTime = this.config.getCurrentTime(),
            startTime = this.config.getCursorPos(),
            endTime,
            selected = this.getSelected();
        if (this.isPlaying())
            return;

        if (selected !== undefined && selected.endTime > startTime) {
            startTime = selected.startTime;
            endTime = selected.endTime;
        }

        if (this.pausedAt) {
            startTime = this.pausedAt;
        }

        pause_single_sound();
        editors[0].schedulePlay(currentTime, startTime, endTime);

        this.lastPlay = currentTime;
        this.animationRequest = window.requestAnimationFrame(this.animationCallback);
    },

    pause: function() {
        var editors = this.trackEditors,
            i,
            len,
            currentTime = this.config.getCurrentTime(),
            startTime = this.config.getCursorPos();

        if (this.pausedAt) {
            startTime = this.pausedAt;
        }

        this.pausedAt = currentTime - this.lastPlay + startTime;

        window.cancelAnimationFrame(this.animationRequest);

        for (i = 0, len = editors.length; i < len; i++) {
            editors[i].scheduleStop(currentTime);
        }
    },

    stop: function() {
        var editors = this.trackEditors,
            i,
            len,
            currentTime = this.config.getCurrentTime();

        this.pausedAt = undefined;

        window.cancelAnimationFrame(this.animationRequest);

        for (i = 0, len = editors.length; i < len; i++) {
            editors[i].scheduleStop(currentTime);
            editors[i].showProgress(0);
        }
    },

    createTrack: function() {
        var trackEditor = Object.create(WaveformPlaylist.TrackEditor, {
            config: {
                value: this.config
            }
        });
        var trackElem = trackEditor.init();

        trackEditor.setState('fileDrop');
    
        this.trackEditors.push(trackEditor);
        this.trackContainer.appendChild(trackElem);

        trackEditor.on("trackloaded", "onTrackLoad", this);
    },

    onTrackLoad: function(trackEditor) {

        this.audioControls.on("trackedit", "onTrackEdit", trackEditor);
        this.audioControls.on("changeresolution", "onResolutionChange", trackEditor);

        trackEditor.on("activateSelection", "onAudioSelection", this.audioControls);
        trackEditor.on("deactivateSelection", "onAudioDeselection", this.audioControls);
        trackEditor.on("changecursor", "onCursorSelection", this.audioControls);
        trackEditor.on("changecursor", "onSelectUpdate", this);
        trackEditor.on("changeshift", "onChangeShift", this);
    },

    updateEditor: function() {
        var editors = this.trackEditors,
            i,
            len,
            currentTime = this.config.getCurrentTime(),
            elapsed = currentTime - this.lastPlay,
            cursorPos = this.config.getCursorPos(),
            playbackSec;

        //update drawer to start drawing from where last paused.
        if (this.pausedAt) {
            cursorPos = this.pausedAt;
        }

        if (this.isPlaying()) {
            //if there's a change for the UI show progress.
            if (elapsed) {
                playbackSec = cursorPos + elapsed;

                for (i = 0, len = editors.length; i < len; i++) {
                    editors[i].showProgress(playbackSec);
                }

                this.fire("playbackcursor", {
                    "seconds": playbackSec
                });
            }
            this.animationRequest = window.requestAnimationFrame(this.animationCallback);
        }
        else {
            //reset view to not playing look
            for (i = 0, len = editors.length; i < len; i++) {
                editors[i].showProgress(0);
            }

            this.pausedAt = undefined;
            window.cancelAnimationFrame(this.animationRequest);
            updatedSelectedLocalMusic('pause');
        } 
    },

    getJson: function() {
        var editors = this.trackEditors,
            i,
            len,
            info = [],
            json;

        for (i = 0, len = editors.length; i < len; i++) {
            info.push(editors[i].getTrackDetails());
        }

        json = JSON.stringify(info);

        return info;
    },

    save: function() {
         var editors = this.trackEditors,
            i,
            len,
            info = [];

        for (i = 0, len = editors.length; i < len; i++) {
            info.push(editors[i].getTrackDetails());
        }

        this.storage.save("test", info);
    },

    restore: function() {
        var state;

        state = this.storage.restore("test");

        this.destroy();
        this.init(state);
    },

    destroy: function() {
        var editors = this.trackEditors,
            i,
            len,
            info = [];
        if (this.isPlaying())
            this.stop();

        for (i = 0, len = editors.length; i < len; i++) {
            editors[i].reset();
        }

        this.audioControls.reset();
        this.timeScale && this.timeScale.reset();
        this.reset();
        this.onSelectionChange({start:0});

        this.trackContainer.innerHTML='';
    }
};
