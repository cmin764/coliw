import requests

from coliw import exceptions
from coliw.utils import EOL, ENCODING, WebArgumentParser


HELP = "retrieve geo location and other information from an IP"

URL = "http://ipinfo.io/{input}"


def ipinfo(args):
    # Make request and check response status.
    url = URL.format(input=args.input or "")
    resp = requests.get(url)
    if not resp.ok:
        raise exceptions.ExecError("invalid request {}".format(resp.reason))
    info = resp.json()
    enabled = {
        "ip": args.ip,
        "hostname": False,
        "city": args.city,
        "region": False,
        "country": args.country,
        "loc": args.loc,
        "org": False,
        "postal": False,
    }
    if any(enabled.values()):
        info = {key: value for key, value in info.items()
                if enabled[key]}
    # Extract results.
    return EOL.join([value.encode(ENCODING)
                     if isinstance(value, unicode) else str(value)
                     for value in info.values()])


parser = WebArgumentParser(add_help=False)
parser.add_argument(
    "input", metavar="IP", nargs="?",
    help="IP address"
)
parser.add_argument(
    "-c", "--city", action="store_true",
    help="show the city"
)
parser.add_argument(
    "-C", "--country", action="store_true",
    help="show the city"
)
parser.add_argument(
    "-l", "--loc", action="store_true",
    help="show the location"
)
parser.add_argument(
    "-i", "--ip", action="store_true",
    help="show the location"
)
parser.set_defaults(func=ipinfo)
