#! /usr/bin/env python

import sys

from coliw import coliw


port = 1337
if len(sys.argv) > 1:
    port = int(sys.argv[1])

coliw.run(host="0.0.0.0", port=port, threaded=True)
