#!/usr/bin/env python3

############################################################################
#                                                                          #
#  PyTCP - Python TCP/IP stack                                             #
#  Copyright (C) 2020-present Sebastian Majewski                           #
#                                                                          #
#  This program is free software: you can redistribute it and/or modify    #
#  it under the terms of the GNU General Public License as published by    #
#  the Free Software Foundation, either version 3 of the License, or       #
#  (at your option) any later version.                                     #
#                                                                          #
#  This program is distributed in the hope that it will be useful,         #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#  GNU General Public License for more details.                            #
#                                                                          #
#  You should have received a copy of the GNU General Public License       #
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.  #
#                                                                          #
#  Author's email: ccie18643@gmail.com                                     #
#  Github repository: https://github.com/ccie18643/PyTCP                   #
#                                                                          #
############################################################################


"""
This module contains tests for the ICMPv6 Echo Reply message parser.

tests/unit/protocols/icmp6/test__icmp6__message__echo_reply__parser.py

ver 3.0.0
"""


from typing import Any

from parameterized import parameterized_class  # type: ignore
from testslide import TestCase

from pytcp.protocols.icmp6.message.icmp6_message__echo_reply import (
    Icmp6EchoReplyMessage,
)


@parameterized_class(
    [
        {
            "_description": "ICMP6 Echo Reply message, empty data.",
            "_args": {
                "bytes": b"\x81\x00\x00\x00\x30\x39\xd4\x31",
            },
            "_results": {
                "from_bytes": Icmp6EchoReplyMessage(
                    cksum=0,
                    id=12345,
                    seq=54321,
                    data=b"",
                ),
            },
        },
        {
            "_description": "ICMP6 Echo Reply message, non-empty data.",
            "_args": {
                "bytes": (
                    b"\x81\x00\x00\x00\x30\x39\xd4\x31\x30\x31\x32\x33\x34\x35\x36\x37"
                    b"\x38\x39\x41\x42\x43\x44\x45\x46"
                ),
            },
            "_results": {
                "from_bytes": Icmp6EchoReplyMessage(
                    cksum=0,
                    id=12345,
                    seq=54321,
                    data=b"0123456789ABCDEF",
                ),
            },
        },
        {
            "_description": "ICMP6 Echo Reply message, maximum length of data.",
            "_args": {
                "bytes": b"\x81\x00\x00\x00\x2b\x67\x56\xce" + b"X" * 65527,
            },
            "_results": {
                "from_bytes": Icmp6EchoReplyMessage(
                    cksum=0,
                    id=11111,
                    seq=22222,
                    data=b"X" * 65527,
                ),
            },
        },
        {
            "_description": "ICMPv6 Echo Reply message, incorrect 'type' field.",
            "_args": {
                "bytes": b"\xff\x00\x00\x00\x00\x00\x00\x00",
            },
            "_results": {
                "error": (
                    "The 'type' field must be <Icmp6Type.ECHO_REPLY: 129>. "
                    "Got: <Icmp6Type.UNKNOWN_255: 255>"
                ),
            },
        },
    ]
)
class TestIcmp6MessageEchoReplyParser(TestCase):
    """
    The ICMPv6 Echo Reply message parser tests.
    """

    _description: str
    _args: dict[str, Any]
    _results: dict[str, Any]

    def test__icmp6__message__echo_reply__parser__from_bytes(self) -> None:
        """
        Ensure the ICMPv6 'Echo Reply' message 'from_bytes()' method
        creates a proper message object.
        """

        if "error" in self._results:
            with self.assertRaises(AssertionError) as error:
                Icmp6EchoReplyMessage.from_bytes(self._args["bytes"])

            self.assertEqual(
                str(error.exception),
                self._results["error"],
            )

        if "from_bytes" in self._results:
            self.assertEqual(
                Icmp6EchoReplyMessage.from_bytes(self._args["bytes"]),
                self._results["from_bytes"],
            )
