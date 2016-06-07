#! /usr/bin/env python

from coliw import coliw


if __name__ == "__main__":
    coliw.run(host="0.0.0.0", port=1337, threaded=True)
