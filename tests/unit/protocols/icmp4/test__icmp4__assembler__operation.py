#!/usr/bin/env python3

################################################################################
##                                                                            ##
##   PyTCP - Python TCP/IP stack                                              ##
##   Copyright (C) 2020-present Sebastian Majewski                            ##
##                                                                            ##
##   This program is free software: you can redistribute it and/or modify     ##
##   it under the terms of the GNU General Public License as published by     ##
##   the Free Software Foundation, either version 3 of the License, or        ##
##   (at your option) any later version.                                      ##
##                                                                            ##
##   This program is distributed in the hope that it will be useful,          ##
##   but WITHOUT ANY WARRANTY; without even the implied warranty of           ##
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the             ##
##   GNU General Public License for more details.                             ##
##                                                                            ##
##   You should have received a copy of the GNU General Public License        ##
##   along with this program. If not, see <https://www.gnu.org/licenses/>.    ##
##                                                                            ##
##   Author's email: ccie18643@gmail.com                                      ##
##   Github repository: https://github.com/ccie18643/PyTCP                    ##
##                                                                            ##
################################################################################


"""
Module contains tests for the ICMPv4 packet assembler operation.

tests/unit/protocols/icmp4/test__icmp4__assembler__operation.py

ver 3.0.1
"""


from typing import Any

from parameterized import parameterized_class  # type: ignore
from testslide import TestCase

from pytcp.lib.tracker import Tracker
from pytcp.protocols.icmp4.icmp4__assembler import Icmp4Assembler
from pytcp.protocols.icmp4.message.icmp4_message import Icmp4Code, Icmp4Type
from pytcp.protocols.icmp4.message.icmp4_message__destination_unreachable import (
    Icmp4DestinationUnreachableCode,
    Icmp4DestinationUnreachableMessage,
)
from pytcp.protocols.icmp4.message.icmp4_message__echo_reply import (
    Icmp4EchoReplyCode,
    Icmp4EchoReplyMessage,
)
from pytcp.protocols.icmp4.message.icmp4_message__echo_request import (
    Icmp4EchoRequestCode,
    Icmp4EchoRequestMessage,
)
from pytcp.protocols.icmp4.message.icmp4_message__unknown import (
    Icmp4UnknownMessage,
)


@parameterized_class(
    [
        {
            "_description": "ICMPv4 Echo Reply message.",
            "_args": {
                "icmp4__message": Icmp4EchoReplyMessage(),
            },
            "_results": {
                "__len__": 8,
                "__str__": "ICMPv4 Echo Reply, id 0, seq 0, len 8 (8+0)",
                "__repr__": (
                    "Icmp4EchoReplyMessage(code=<Icmp4EchoReplyCode.DEFAULT: 0>, "
                    "cksum=0, id=0, seq=0, data=b'')"
                ),
                "__bytes__": b"\x00\x00\xff\xff\x00\x00\x00\x00",
                "message": Icmp4EchoReplyMessage(
                    code=Icmp4EchoReplyCode.DEFAULT,
                    cksum=0,
                    id=0,
                    seq=0,
                    data=b"",
                ),
            },
        },
        {
            "_description": "ICMPv4 Destination Unreachable message.",
            "_args": {
                "icmp4__message": Icmp4DestinationUnreachableMessage(
                    code=Icmp4DestinationUnreachableCode.PORT,
                ),
            },
            "_results": {
                "__len__": 8,
                "__str__": "ICMPv4 Destination Unreachable - Port, len 8 (8+0)",
                "__repr__": (
                    "Icmp4DestinationUnreachableMessage(code=<Icmp4DestinationUnreachableCode"
                    ".PORT: 3>, cksum=0, mtu=None, data=b'')"
                ),
                "__bytes__": b"\x03\x03\xfc\xfc\x00\x00\x00\x00",
                "message": Icmp4DestinationUnreachableMessage(
                    code=Icmp4DestinationUnreachableCode.PORT,
                    cksum=0,
                    mtu=None,
                    data=b"",
                ),
            },
        },
        {
            "_description": "ICMPv4 Echo Request message.",
            "_args": {
                "icmp4__message": Icmp4EchoRequestMessage(),
            },
            "_results": {
                "__len__": 8,
                "__str__": "ICMPv4 Echo Request, id 0, seq 0, len 8 (8+0)",
                "__repr__": (
                    "Icmp4EchoRequestMessage(code=<Icmp4EchoRequestCode.DEFAULT: 0>, "
                    "cksum=0, id=0, seq=0, data=b'')"
                ),
                "__bytes__": b"\x08\x00\xf7\xff\x00\x00\x00\x00",
                "message": Icmp4EchoRequestMessage(
                    code=Icmp4EchoRequestCode.DEFAULT,
                    cksum=0,
                    id=0,
                    seq=0,
                    data=b"",
                ),
            },
        },
        {
            "_description": "ICMPv4 unknown message.",
            "_args": {
                "icmp4__message": Icmp4UnknownMessage(
                    type=Icmp4Type.from_int(255),
                    code=Icmp4Code.from_int(255),
                ),
            },
            "_results": {
                "__len__": 4,
                "__str__": (
                    "ICMPv4 Unknown Message, type 255, code 255, cksum 0, len 4 (4+0)"
                ),
                "__repr__": (
                    "Icmp4UnknownMessage(type=<Icmp4Type.UNKNOWN_255: 255>, "
                    "code=<Icmp4Code.UNKNOWN_255: 255>, cksum=0, raw=b'')"
                ),
                "__bytes__": b"\xff\xff\x00\x00",
                "message": Icmp4UnknownMessage(
                    type=Icmp4Type.from_int(255),
                    code=Icmp4Code.from_int(255),
                    cksum=0,
                    raw=b"",
                ),
            },
        },
    ]
)
class TestIcmp4AssemblerOperation(TestCase):
    """
    The ICMPv4 packet assembler operation tests.
    """

    _description: str
    _args: dict[str, Any]
    _results: dict[str, Any]

    def setUp(self) -> None:
        """
        Initialize the ICMPv4 packet assembler object with testcase arguments.
        """

        self._icmp4__assembler = Icmp4Assembler(**self._args)

    def test__icmp4__assembler__len(self) -> None:
        """
        Ensure the ICMPv4 packet assembler '__len__()' method returns a correct
        value.
        """

        self.assertEqual(
            len(self._icmp4__assembler),
            self._results["__len__"],
        )

    def test__icmp4__assembler__str(self) -> None:
        """
        Ensure the ICMPv4 packet assembler '__str__()' method returns a correct
        value.
        """

        self.assertEqual(
            str(self._icmp4__assembler),
            self._results["__str__"],
        )

    def test__icmp4__assembler__repr(self) -> None:
        """
        Ensure the ICMPv4 packet assembler '__repr__()' method returns a correct
        value.
        """

        self.assertEqual(
            repr(self._icmp4__assembler),
            self._results["__repr__"],
        )

    def test__icmp4__assembler__bytes(self) -> None:
        """
        Ensure the ICMPv4 packet assembler '__bytes__()' method returns a correct
        value.
        """

        self.assertEqual(
            bytes(self._icmp4__assembler),
            self._results["__bytes__"],
        )

    def test__icmp4__assembler__message(self) -> None:
        """
        Ensure the ICMPv4 packet assembler 'message' property returns a correct
        value.
        """

        self.assertEqual(
            self._icmp4__assembler.message,
            self._results["message"],
        )


class TestIcmp4AssemblerMisc(TestCase):
    """
    The ICMPv4 packet assembler miscellaneous functions tests.
    """

    def test__icmp4__assembler__echo_tracker(self) -> None:
        """
        Ensure the ICMPv4 packet assembler 'tracker' property returns
        a correct value.
        """

        echo_tracker = Tracker(prefix="RX")

        icmp4__assembler = Icmp4Assembler(
            icmp4__message=Icmp4EchoReplyMessage(),
            echo_tracker=echo_tracker,
        )

        self.assertEqual(
            icmp4__assembler.tracker.echo_tracker,
            echo_tracker,
        )
