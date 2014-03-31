# Feedback items

`feedback` items can be used to inform participants of their performance. `feedback` items are very similar to `sketchpad` items, but differ in the moment at which they are prepared. `feedback` items are not prepared in advance, which means that they can be used to display up-to-date information about response times, etc. On the other hand, this lack of preparation also means that they may introduce a small delay in your experiment. Therefore, you should not use `feedback` items to present time-critical displays.

To provide feedback, you can make use of the built-in feedback variables, such as `avg_rt` and `acc`, for example by adding the following lines of text to your `feedback` item:

	Your average response time was [avg_rt] ms
	Your accuracy was [acc] %

For more information, see:

- <http://osdoc.cogsci.nl/usage/feedback/>
