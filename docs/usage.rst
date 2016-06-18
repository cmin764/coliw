.. _usage:

Usage
=====

As the welcome screen says, write `--help` (or just simply `-h`) for getting
a list of the available commands and their usage. To view additional help
regarding each of the commands, type `<command> -h` and in this way, you'll
be able to explore the available API commands and see them in action by also
placing input.


Clear & History
---------------

Use the *Clear* button to clear the screen or activate the auto-clear
checkbox for letting the app doing this automatically every time you test a
new command.

In case you close the window and get back under a certain amount of time,
your history will be kept and left in the same state.


Commands
--------

IP & GEO
++++++++

.. code-block:: shell

    > ipinfo -i -l
    46.5757,26.8712
    91.202.91.119

Shows current IP information, regarding location coordinates and IP address.
Run `ipinfo 8.8.4.4` for showing info about a certain IP (not yours).

Weather
+++++++

.. code-block:: shell

    > weather Iasi
    Clear
    clear sky

Shows current basic weather conditions in the given city.

WolframAlpha
++++++++++++

.. code-block:: shell

    > walpha pi
    3.1415926535

Computes and/or shows details regarding math expressions/equations and more.


Advanced
--------

The web shell also supports basic pipe "|" operators and temporary files I/O
with "<" (read), ">" (write) and ">>" (append). You can use these to chain
together outputs from previous commands as inputs for the next ones or saving
huge outputs to temporary named files (based on your current session).

.. code-block:: shell

    > ipinfo --city | weather
    Clear
    clear sky

Get current city by IP and show how's weather there.

.. code-block:: shell

    > walpha 2^3 > 8.txt
    > walpha -v < 8.txt
    8
    eight

Save output into files and retrieve it back when needed.
