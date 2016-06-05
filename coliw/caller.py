import pkgutil
import os

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

    # TODO(cmiN): take care of |, <, >, <<, >> symbols
    cmds = cmd.split()
    if cmds[0] == "web":
        cmds.pop(0)
    args = parser.parse_args(cmds)
    return args


def call(cmd):
    """Parse the command and execute it."""
    parser = WebArgumentParser()
    try:
        args = parse(cmd)
        data = args.func(args)
    except Exception as exc:
        msg = "{}{}".format(parser.sio.getvalue(), str(exc)).strip()
        return exceptions.get_code(exc), msg
    finally:
        parser.sio.close()
        del parser.sio
    return 0, data
