import json
import urllib2

from coliw.utils import EOL, TIMEOUT, ENCODING, OPENER, WebArgumentParser


HELP = "get weather by giving a city name"

KEY = "db310acfbeeb7a7697f13bb18c43a073"

URL = ("http://api.openweathermap.org/data/2.5/"
       "weather?q={input}&appid={key}").format(key=KEY, input="{input}")


def weather(args):
    url = URL.format(input=urllib2.quote(args.city))
    data = OPENER.open(url, timeout=TIMEOUT).read()
    wdict = json.loads(data)
    # Extract results.
    info = wdict["weather"][0]
    info.update(wdict["main"])
    if not args.verbose:
        info = {key: value for key, value in info.items()
                if key in ("main", "description")}
    return EOL.join([value.encode(ENCODING)
                     if isinstance(value, unicode) else str(value)
                     for value in info.values()])


parser = WebArgumentParser(add_help=False)
parser.add_argument(
    "city", metavar="CITY",
    help="city for which weather will be shown"
)
parser.add_argument(
    "-v", "--verbose", action="store_true",
    help="show full information regarding the results"
)
parser.set_defaults(func=weather)
