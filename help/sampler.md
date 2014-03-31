# Sampler items

`Sampler` items allow you to play sound files. Only files in `.wav or` `.ogg` format can be used. If you need to convert sound files, for example from `.mp3` format, you can use [Audacity], an excellent open-source sound editor.

## Options

You can specify a number of options:

- *Volume* between 0 and 100%
- *Pan* turns the right (negative values) or left (positive values) channel down. Setting pan to -20 or 20 completely mutes the right or left channel, respectively.
- *Pitch* indicates the speed at which the sample is played. Values higher than 100% indicate a speed-up, values lower than 100% indicate a slowing down.
- *Stop after* indicates how long the sample should be played. For example, a value of 100 ms means that the sample will be stopped after 100 ms, regardless of how long the sample is. A value of 0 ms means playing the full sample.
- *Fade in* indicates the fade in time for the sample.
- *Duration* indicates the duration of the sampler item, before the next item is presented. This doesn't need to match the length of the sample. For example, the duration of the sampler may be set to 0 ms, to advance directly to the next item (e.g., a sketchpad), while the sample continues playing. In addition to a numeric value, you can set duration to 'keypress', to wait for a keyboard press, 'mouseclick', to wait for a mouse click, or 'sound', to wait until the sampler has finished playing.

## Sampling rate

Sound files are always played back at the sampling rate that is used by the OpenSesame sampler back-end. If your sample appears to be sped up or slowed down, you can adjust the sampling rate of your sound file in a sound editor or change the sampling rate used by the OpenSesame sampler back-end (under 'Show back-end settings and info' in the General tab).

For more information, see:

- <http://osdoc.cogsci.nl/usage/sound/>

[audacity]: http://audacity.sourceforge.net/
