import unittest

import mock

from coliw import caller, exceptions


class TestColiw(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch("coliw.caller.read_content")
    def test_parse_ops(self, read_content):
        parser = mock.MagicMock()
        parser.parse_args.side_effect = lambda arg: arg
        read_content.side_effect = lambda arg: arg.rsplit(".", 1)[0]

        cmd_dict = (
            (["walpha", "-v", "pi"],
             (["walpha", "-v", "pi"], None, None)),
            (["walpha", "<", "pi.txt"],
             (["walpha", "pi"], None, None)),
            (["walpha", "pi", ">", "pi.txt"],
             (["walpha", "pi"], "pi.txt", False)),
            (["walpha", "pi", ">>", "pi.txt"],
             (["walpha", "pi"], "pi.txt", True)),
        )

        for cmd, expect in cmd_dict:
            resp = caller.postparse(parser, cmd)
            self.assertEqual(expect, resp)

        wrongs = (
            ["walpha", "pi", ">", "pi.txt", ">", "pi.txt"],
            ["walpha", "pi", ">>", "pi.txt", ">", "pi.txt"],
            ["walpha", "pi", ">>", "pi.txt", ">>", "pi.txt"],
        )
        with self.assertRaises(exceptions.ParseError):
            for wrong in wrongs:
                caller.postparse(parser, wrong)
