# Port_reader plug-in

The port_reader plug-in reads input from an arbitrary port, such as a parallel or serial port, and interprets the return value as a participant's response (i.e., a button press).

- **Dummy mode** -- If set to 'yes', the keyboard is used instead.
Useful for testing purposes.
- **Port number** -- The number of the port that you want to use.
- **Resting-state value** -- The value that should be interpreted
as 'no button pressed'.
- **Correct response** -- The expected response.
- **Timeout** -- The maximum allowed response time, after which a
timeout should be signaled.
