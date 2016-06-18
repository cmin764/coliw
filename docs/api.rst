.. _api:

API reference
=============

- `/command`
    + methods: *POST*
    + data: *cmd* (json serialized command string)
    + response: {"code": ..., "response": ...}

- `/history`
    + methods: *GET* *POST*
    + data: *data* (json serialized history contents and index) (POST)
    + response: {"status": ...[, ...]}

Plugins
-------

The available list of commands is given by auto-discovering all the plugins
present into *coliw/plugins* directory. All of these have to follow a simple
standard:
Implement an instance of `WebArgumentParser` under the `parser` name that
will have a default function attached for command execution.

Backend
-------

.. automodule:: coliw.caller
    :members:

.. autoclass:: coliw.utils.WebArgumentParser
    :members:
