The variable inspector {.western}
======================

The variable inspector provides an overview of all the variables that
are used in your experiment and could be logged using a logger item.
Local variables (i.e., variables that are only available from within an
item, such as 'duration' in a sketchpad item) are not shown. The
variable inspector tries to extract variables created in an
inline\_script item, although slight mistakes may occur.

For more information, see
\<[http://osdoc.cogsci.nl/usage/variables-and-conditional-qifq-statements](http://osdoc.cogsci.nl/usage/variables-and-conditional-qifq-statements)\>.

Using variables in an inline\_script item {.western}
-----------------------------------------

The preferred way to set variables in an inline script item is by using:

self.experiment.set('var\_name', value)

The preferred way to retrieve variables in an inline\_script is by
using:

value = self.get('var\_name')

You can also get and set variables more directly, using:

self.experiment.var\_name = value

and

value = self.experiment.var\_name

This will usually work equally well, but is not preferred as it
circumvents OpenSesame's internal variable management system.

Why use self.experiment.set(), instead of self.set()? {.western}
-----------------------------------------------------

The command

self.set('var\_name', value)

will set a local variable, i.e. a variable which is not accessible
outside of the current inline\_script item. To create global variables,
which can be logged and accessed from anywhere, use

self.experiment.set('var\_name', value)
