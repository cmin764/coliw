import pkgutil
import os
import shlex

from coliw import exceptions
from coliw.utils import (
    PACKAGE,
    read_content, write_content,
    WebArgumentParser,
)


PLUGINS_DIR = os.path.join(PACKAGE, "plugins")


def discover_plugins():
    """Return a list of all discovered plugins under the parent directory."""
    plugins = {}
    importer = pkgutil.get_importer(PLUGINS_DIR)
    for name, _ in importer.iter_modules():
        module = importer.find_module(name)
        plugin = module.load_module(name)
        plugins[name] = plugin
    return plugins


def postparse(parser, cmd):
    """Returns the file I/O normalized parse arguments.

    A tuple of (args, name, append).
    """
    name, append = None, None
    if cmd.count("<") > 1 or cmd.count(">") + cmd.count(">>") > 1:
        raise exceptions.ParseError("invalid number of I/O operators")

    if "<" in cmd:
        idx = cmd.index("<")
        _cmd = cmd[:idx]
        data = read_content(cmd[idx + 1])
        _cmd.append(data)
        _cmd.extend(cmd[idx + 2:])
        cmd = _cmd
    for op in (">", ">>"):
        if op not in cmd:
            continue
        idx = cmd.index(op)
        _cmd = cmd[:idx]
        _cmd.extend(cmd[idx + 2:])
        name = cmd[idx + 1]
        append = True if op == ">>" else False
        cmd = _cmd
        break

    return parser.parse_args(cmd), name, append


def parse(cmd):
    """Split given command into sub-commands and analyse requested actions."""
    plugins = discover_plugins()

    parser = WebArgumentParser(
        prog="web",
        description="Execute CLI commands over the supported APIs."
    )
    parser.sio.truncate(0)
    subparsers = parser.add_subparsers(title="commands")
    for name, plugin in plugins.items():
        subparsers.add_parser(name, parents=[plugin.parser], help=plugin.HELP)

    cmds = shlex.split(cmd)
    if cmds[0] == "web":
        cmds.pop(0)
    # Filter pipes and chain commands.
    while cmds.count("|"):
        idx = cmds.index("|")
        data = (yield)
        crt = cmds[:idx] + ([data] if data is not None else [])
        cmds = cmds[idx + 1:]
        yield postparse(parser, crt)
    data = (yield)
    crt = cmds + ([data] if data is not None else [])
    yield postparse(parser, crt)


def call(cmd):
    """Parse the command and execute it."""
    parser = WebArgumentParser()
    try:
        parse_gen = parse(cmd)
        data = None
        for _ in parse_gen:
            args, name, append = parse_gen.send(data)
            data = args.func(args)
            if name:
                write_content(name, data, append=append)
                data = None
    except Exception as exc:
        msg = "{}{}".format(parser.sio.getvalue(), str(exc)).strip()
        return exceptions.get_code(exc), msg
    finally:
        parser.sio.close()
        del parser.sio
    return 0, data
