# Keyboard_response items

The `keyboard_response` item is the primary way to collect keypress responses.

## Options

- *Correct response* is the name of the expected response. Usually you will set the `correct_response` variable elsewhere (e.g., in a `loop` item) and you can leave this field empty.
- *Allowed responses* is a semicolon-separated list of keys that are accepted, e.g., 'a;b;/'.
- *Timeout* contains a maximum response time in milliseconds or 'infinite' for no timeout.
- *Flush pending keypresses* indicates that old, pending responses should be discarded.

## Response variables

- `response` is the name of the response key or 'None' if a timeout occurs.
- `response_time` is the time between the start of the response interval and the response.
- `correct` is 1 if `response` matches `correct_response` and 0 otherwise.
- `average_response_time` is the average response time since the last feedback item.
- `avg_rt` is a synonym for `average_response_time`.
- `accuracy` is the average percentage of correct responses since the last feedback item.
- `acc` is a synonym for `accuracy`.

For more information about response variables, see:
	
- <http://osdoc.cogsci.nl/usage/variables-and-conditional-statements/#responsevariables>

## Names of keys

Keys are generally identified by their character and/ or their description (depending on which is applicable). For example, the `/` key is identified as 'slash' and '/'. The `a` is just identified as 'a'. The left-arrow key is just identified as 'left'. For a full list of available key names, click on the 'List available keys' button.

For more information, see:
	
- <http://osdoc.cogsci.nl/usage/collecting-responses/>
