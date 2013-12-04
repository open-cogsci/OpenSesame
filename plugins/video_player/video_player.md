# Video_player

The `video_player` plug-in plays back a video file. This plug-in is for basic image-only video playback, and requires the `legacy` back-end. If you are looking for more advanced video-playback functionality, you may want to use the `media_player_vlc` plug-in.

The following options are available:

- *Video file*: A video file from the file pool. Which formats are supported depends on your platform, but most common formats (such as `.avi` and `.mpeg`) are supported everywhere.
- *Resize to fit screen*: Indicates if the video needs to be resized so that it fits the entire screen. If not, the video will be displayed in the center of the display.
- *Duration*: A duration in milliseconds, 'keypres' (to stop when a key is pressed) or 'mouseclick' (to stop when a mousbutton is clicked).
- *Frame duration*: The duration in milliseconds of a single frame. This essentially controls the playback speed. Note that the maximum playback speed depends on the speed of the computer.


