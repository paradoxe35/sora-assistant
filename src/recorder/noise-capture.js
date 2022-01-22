//@ts-check
const noise_capture = {};

/**
 *
 * @param {AudioContext} audioContext
 * @param {MediaStream} stream
 * @param {number} minDecibels
 * @param {number} maxBlankTime
 * @param {() => void} cbOnStart
 * @param {() => void} cbOnEnd
 */
noise_capture.listening = (
  audioContext,
  stream,
  minDecibels,
  maxBlankTime,
  cbOnStart,
  cbOnEnd
) => {
  const analyser = audioContext.createAnalyser();
  const streamNode = audioContext.createMediaStreamSource(stream);
  streamNode.connect(analyser);
  analyser.minDecibels = minDecibels;

  const data = new Uint8Array(analyser.frequencyBinCount);
  let silenceStart = performance.now();
  let triggered = false;

  const loop = (time) => {
    requestAnimationFrame(loop);

    analyser.getByteFrequencyData(data);

    if (data.some((v) => v)) {
      if (triggered) {
        triggered = false;

        cbOnStart();
      }
      silenceStart = time;
    }

    if (!triggered && time - silenceStart > maxBlankTime) {
      cbOnEnd();

      triggered = true;
    }
  };

  loop();
};

export default noise_capture;
