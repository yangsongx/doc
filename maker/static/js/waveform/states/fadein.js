'use strict';

WaveformPlaylist.states = WaveformPlaylist.states || {};

/*
  called with an instance of Track as 'this'
*/
WaveformPlaylist.states.fadein = {

  classes: "state-fadein",

  enter: function() {
    var stateObject = this.currentState;

    this.container.onmousedown = stateObject.event.bind(this);
    this.container.classList.add(stateObject.classes);
  },

  leave: function() {
    var stateObject = this.currentState;

    this.container.onmousedown = null;
    this.container.classList.remove(stateObject.classes);
  },

  event: function(e) {
    var startX = this.drawer.findClickedPixel(e), //relative to e.target
        FADETYPE = "FadeIn",
        shape = this.config.getFadeType(),
        trackStartPix = this.drawer.pixelOffset,
        trackEndPix = trackStartPix + this.drawer.width;

    this.removeFadeType(FADETYPE);

    if (trackStartPix <= startX && trackEndPix >= startX) {
      this.createFade(FADETYPE, shape, 0, (startX - trackStartPix));
    }
  }
};