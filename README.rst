===========================
Lack of cohesion of methods
===========================

Cohesion metrics measure how well methods of a class are related to each other.
A cohesive class has one responsibility. A non-cohesive class has more
unrelated functions, thus more than one responsibility.

**LCOM4** considers method as related with other method, when both of them use common attribute or method call.
Methods are not compared with constructors / initializers eg. ``__init__``, since they often involve all attributes.
Also all inherited methods are ignored - as they come from different class.

Score:

- ``==1`` - indicates a cohesive class, which is the "good" class;
- ``>=2`` - indicates a problem. The class should be split into so many smaller classes;
- ``==0`` -  happens when there are no methods in a class. This is also a "bad" class.

Usage
=====

Just point it to a module or a package that needs to be measured:

.. code-block:: cli

	bin/lcom src

This will result in such output:

.. code-block:: cli

	Calculating LCOM using LCOM4
	+---------------------------------+------+
	| Method                          | LCOM |
	+---------------------------------+------+
	| src.command.FileSystem          | 1    |
	| src.command.LCOMFactory         | 0    |
	| src.command.Printer             | 0    |
	| src.command.PrinterFactory      | 0    |
	| src.command.Runner              | 1    |
	| src.command.STDOut              | 0    |
	| src.lcom.LCOM4                  | 1    |
	| src.lcom.LCOMAlgorithm          | 0    |
	| src.reflection.ClassReflection  | 1    |
	| src.reflection.MethodReflection | 1    |
	| src.reflection.ModuleReflection | 1    |
	| src.reflection.Reflection       | 0    |
	| src.reflection.ReflectionError  | 0    |
	+---------------------------------+------+
	| Average                         | 0.46 |
	+---------------------------------+------+


It is also possible to measure single module:


.. code-block:: cli

	bin/lcom src/command.py

Or mix them:

.. code-block:: cli

	bin/lcom src/command.py tests
