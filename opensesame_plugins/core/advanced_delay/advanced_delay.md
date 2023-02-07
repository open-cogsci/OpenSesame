# Advanced_delay

The `advanced_delay` plug-in delays the experiment for a pre-specified average duration plus a random margin.

- *Duration* is the average duration of the delay in milliseconds.
- *Jitter* is the size of the variation in the delay in milliseconds.
- *Jitter mode* is the how the jitter is calculated:
	- *Standard deviation* will draw the variation from a Gaussian distribution with Jitter as the standard deviation.
	- *Uniform* will draw the variation in duration from a uniform distribution.
