import urllib2
import xml.etree.ElementTree as ET

from coliw.utils import EOL, ENCODING, TIMEOUT, OPENER, WebArgumentParser


HELP = "compute/retrieve mathematical expressions/info"

KEY = "HUA8LU-84PXX37URW"
URL = ("http://api.wolframalpha.com/v2/query?appid={key}"
       "&input={input}&format=plaintext").format(key=KEY, input="{input}")


def walpha(args):
    # Get all the data in XML format.
    url = URL.format(input=urllib2.quote(args.input))
    data = OPENER.open(url, timeout=TIMEOUT).read()
    # Extract results.
    root = ET.fromstring(data)
    results = list(root.iter("plaintext"))
    if not args.verbose:
        results = [results[1]]
    return EOL.join(result.text.encode(ENCODING)
                    for result in results
                    if result.text)


parser = WebArgumentParser(add_help=False)
parser.add_argument(
    "input", metavar="INPUT",
    help="for which relevant results will be retrieved"
)
parser.add_argument(
    "-v", "--verbose", action="store_true",
    help="show full information regarding the results"
)
parser.set_defaults(func=walpha)
