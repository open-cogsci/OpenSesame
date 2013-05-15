# Joystick items

In psychological research a large amount of input devices are being used to record participants' responses. This joystick item can handle input from joystick devices, including trackballs and video-game-style gamepads. Using the joystick module of PyGame, joystick allows for the use of a joystick with buttons, axes, trackballs and hats.

## Options

You can set the following options:

- `Correct response` is the name of the expected response. Usually you will set the correct_response variable elsewhere (e.g., in a loop item) and you can leave this field empty. Please note that setting correct responses via the joystick_response item is only possible for button input.
- `Allowed responses` is a semicolon-separated list of buttons that are accepted, e.g., '1;2'.
- `Timeout` contains a maximum response time in milliseconds or 'infinite' for no timeout.

## Variables set by joystick

The keyboard_response item sets a number of variables based on your response.

- `response` is the name of the response key.
- `response_time` is the time between the start of the response interval and the response.
- `correct` is 1 if the response matches the correct_response and 0 otherwise.
- `avg_rt` / `average_response_time` is the average response time since the last feedback item.
- `acc` / `accuracy` is the average percentage of correct responses since the last feedback item.

## Button names

Depending on the kind of joystick or gamepad you use, a different number of buttons, axes, tracksballs and hats are available. Please make sure you know which button corresponds to which buttonnumber (same goes for axes, hats and trackballs).

## Inline scripting

See <http://osdoc.cogsci.nl/devices/joystick/>

