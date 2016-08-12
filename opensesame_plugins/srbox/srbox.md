# SR Box

The SR (serial response) box item collects responses from a button box connected to the serial port or via USB to a 'virtual serial port'. This item can be used with the SR Box (Psychology Software Tools, Inc.) and compatible devices.

## Dummy mode

In dummy mode the SR Box is emulated by the numeric keys of the keyboard. This is convenient when you want to test your experiment without an SR Box.

## Ignore buttons that are already pressed

If you enable the 'Ignore buttons that are already pressed' option, the plugin will only respond to buttons that go from not being pressed to being pressed. This generally what you want, because it avoids a single button press from triggering a series of responses. However, for backwards compatibility this option is disabled by default.

## Names of buttons and lights

Buttons and lights are identified by a single digit between 1 and 8. How many buttons there are and which button corresponds to which digit depends on your specific button box. On the SR Box sold by Psychology Software Tools, Inc. there are 5 buttons and 5 lights, where button 1 and light 1 are on the left. On other SR Boxes lights may not be available, in which case the light input is ignored.

## More information

On the Psychology Software Tools site:

- <http://www.pstnet.com/hardware.cfm?ID=102>.

On the OpenSesame documentation site:

- <http://osdoc.cogsci.nl/3.1/manual/response/srbox/>
