//@ts-check
import Recorder from "../recorder";
import noise_capture from "../recorder/noise-capture";
import { visualize } from "./visualize";

// set up basic variables for app

/** @type {HTMLButtonElement} */
const record = document.querySelector(".record");

/**
 * @type {HTMLButtonElement}
 */
const stopEl = document.querySelector(".stop");
// disable stop button while not recording
stopEl.disabled = true;

const soundClips = document.querySelector(".sound-clips");
/** @type {HTMLElement} */
const mainSection = document.querySelector(".main-controls");

/** @type {HTMLCanvasElement} */
const canvas = document.querySelector(".visualizer");
// get canvas 2d context
const canvasCtx = canvas.getContext("2d");

const audio_options = { sampleRate: 16000 };

const config = {
  app: "webapp",
  server_host: "ws://localhost",
  server_port: "2781",
  min_decibels: -40, // Noise detection sensitivity
  max_blank_time: 1000, // Maximum time to consider a blank (ms)
};

/**
 * @type {AudioContext}
 */
let audioContext = new AudioContext(audio_options);

const serverUrl = `${config.server_host}:${config.server_port}`;

const clientIo = {
  socket: new WebSocket(serverUrl),
  new_socket() {
    this.socket = new WebSocket(serverUrl);
    return new Promise((resolve) =>
      this.socket.addEventListener("open", resolve, { once: true })
    );
  },
};

/**
 * @param {  MessageEvent<any>} e
 */
const asr_message = (e) => {
  var data = e.data;
  if (data instanceof Object && !(data instanceof Blob)) {
    console.log("WebSocket: onEvent: got Object that is not a Blob");
  } else if (data instanceof Blob) {
    console.log("WebSocket: got Blob");
  } else {
    var res = JSON.parse(data);
    if (res.continue) {
      // do nothing
    } else if (res.partial) {
      console.log("partial: ", res.partial);
    } else if (res.text) {
      console.log("text: ", res.text);
    }
  }
};

// use media agent constraints
var constraints = {
  audio: {
    echoCancellation: true,
    noiseSuppression: true,
    channelCount: 1,
    sampleRate: audio_options.sampleRate,
  },
  video: false,
};

navigator.mediaDevices.getUserMedia(constraints).then(async function (stream) {
  console.log(
    "getUserMedia() success, stream created, initializing Recorder.js ..."
  );

  await audioContext.resume();

  /* Create the Recorder object and configure to record mono sound (1 channel) Recording 2 channels will double the file size */
  const rec = new Recorder(audioContext);

  // visual audio frequency
  visualize(stream, canvas, canvasCtx, audioContext);

  //initialize the recording process
  rec.init(stream);

  /**
   * @param {Recorder.RecorderResult} value
   */
  const data_recorder = async (value) => {
    // if connection has closed, inistiate a new one when message listener
    if (clientIo.socket.readyState === 3) {
      await clientIo.new_socket();
      //  response from socket
      clientIo.socket.onmessage = asr_message;
    }

    // send the audio content sample rate
    if (value.sampleRate) {
      clientIo.socket.send(
        `{ "config" : { "sample_rate" : ${value.sampleRate} } }`
      );
    }
    Recorder.download(value.blob, "sample");
    clientIo.socket.send(value.blob);
    clientIo.socket.send('{"eof" : 1}');
  };

  const stoppable = function () {
    if (!rec.audioRecorder.recording) return;

    console.log("recorder stopped");
    record.style.background = "";
    record.style.color = "";

    stopEl.disabled = true;
    record.disabled = false;

    rec.stop().then(data_recorder);
  };

  record.onclick = function () {
    rec.start().then(() => {
      window.setTimeout(stoppable, 1000 * 20);
    });
    console.log("recorder started");
    record.style.background = "grey";

    stopEl.disabled = false;
    record.disabled = true;
  };

  stopEl.onclick = stoppable;

  //  response from socket
  clientIo.socket.onmessage = asr_message;

  // if no noise captured then close recoder
  noise_capture.listening(
    audioContext,
    stream,
    config.min_decibels,
    config.max_blank_time,
    () => {},
    stoppable
  );
});

window.onresize = function () {
  canvas.width = (mainSection ?? document.body).offsetWidth;
};

// @ts-ignore
window.onresize();
