# Synth items

The `synth` item is a basic sound synthesizer. You can specify a
number of options:

- *Waveform* can be set to sine, sawtooth, square, or white noise
- *Attack* is the time it takes for the sound the reach maximum volume (i.e. fade in).
- *Decay* is the time it takes for the sound to die out (i.e. fade out). Note that the decay occurs within the length of the sound.
- *Volume* between 0 and 100%
- *Pan* turns the right (negative values) or left (positive values) channel down. Setting pan to -20 or 20 completely mutes the right or left channel, respectively.
- *Length* indicates the length of the sound (in milliseconds).
- *Duration* indicates the duration of the `synth` item, before the next item is presented. This doesn't need to match the length of the sound. For example, the duration of the `synth` may be set to 0ms, in order to advance directly to the next item (e.g., a `sketchpad`), while the sound continues playing in the background. In addition to a numeric value, you can set the duration to 'keypress', to wait for a keyboard press, 'mouseclick', to wait for a mouse click, or 'sound', to wait until the `synth` has finished playing.

For more information about sound playback, see:

- <http://osdoc.cogsci.nl/usage/sound/>
