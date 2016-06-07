import pkgutil
import os
import shlex

from coliw import exceptions
from coliw.utils import PACKAGE, WebArgumentParser


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


def parse(cmd):
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
        yield parser.parse_args(crt)
    data = (yield)
    crt = cmds + ([data] if data is not None else [])
    yield parser.parse_args(crt)


def call(cmd):
    """Parse the command and execute it."""
    parser = WebArgumentParser()
    try:
        parse_gen = parse(cmd)
        data = None
        for _ in parse_gen:
            args = parse_gen.send(data)
            data = args.func(args)
    except Exception as exc:
        msg = "{}{}".format(parser.sio.getvalue(), str(exc)).strip()
        return exceptions.get_code(exc), msg
    finally:
        parser.sio.close()
        del parser.sio
    return 0, data
