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
This module contains tests for the ICMPv6 Destination Unreachable message assembler.

tests/unit/protocols/icmp4/test__icmp6__message__destination_unreachable__assembler.py

ver 3.0.0
"""


from typing import Any

from parameterized import parameterized_class  # type: ignore
from testslide import TestCase

from pytcp.protocols.icmp6.message.icmp6_message import Icmp6Type
from pytcp.protocols.icmp6.message.icmp6_message__destination_unreachable import (
    Icmp6DestinationUnreachableCode,
    Icmp6DestinationUnreachableMessage,
)


@parameterized_class(
    [
        {
            "_description": "ICMPv6 Destination Unreachable (No Route) message.",
            "_args": {
                "code": Icmp6DestinationUnreachableCode.NO_ROUTE,
                "cksum": 12345,
                "data": b"",
            },
            "_results": {
                "__len__": 8,
                "__str__": "ICMPv6 Destination Unreachable - No Route, len 8 (8+0)",
                "__repr__": (
                    "Icmp6DestinationUnreachableMessage("
                    "code=<Icmp6DestinationUnreachableCode.NO_ROUTE: 0>, cksum=12345, "
                    "data=b'')"
                ),
                "__bytes__": b"\x01\x00\x00\x00\x00\x00\x00\x00",
                "type": Icmp6Type.DESTINATION_UNREACHABLE,
                "code": Icmp6DestinationUnreachableCode.NO_ROUTE,
                "cksum": 12345,
                "data": b"",
            },
        },
        {
            "_description": "ICMPv6 Destination Unreachable (Prohibited) message.",
            "_args": {
                "code": Icmp6DestinationUnreachableCode.PROHIBITED,
                "cksum": 12345,
                "data": b"",
            },
            "_results": {
                "__len__": 8,
                "__str__": "ICMPv6 Destination Unreachable - Prohibited, len 8 (8+0)",
                "__repr__": (
                    "Icmp6DestinationUnreachableMessage("
                    "code=<Icmp6DestinationUnreachableCode.PROHIBITED: 1>, cksum=12345, "
                    "data=b'')"
                ),
                "__bytes__": b"\x01\x01\x00\x00\x00\x00\x00\x00",
                "type": Icmp6Type.DESTINATION_UNREACHABLE,
                "code": Icmp6DestinationUnreachableCode.PROHIBITED,
                "cksum": 12345,
                "data": b"",
            },
        },
        {
            "_description": "ICMPv6 Destination Unreachable (Scope) message.",
            "_args": {
                "code": Icmp6DestinationUnreachableCode.SCOPE,
                "cksum": 12345,
                "data": b"",
            },
            "_results": {
                "__len__": 8,
                "__str__": "ICMPv6 Destination Unreachable - Scope, len 8 (8+0)",
                "__repr__": (
                    "Icmp6DestinationUnreachableMessage("
                    "code=<Icmp6DestinationUnreachableCode.SCOPE: 2>, cksum=12345, "
                    "data=b'')"
                ),
                "__bytes__": b"\x01\x02\x00\x00\x00\x00\x00\x00",
                "type": Icmp6Type.DESTINATION_UNREACHABLE,
                "code": Icmp6DestinationUnreachableCode.SCOPE,
                "cksum": 12345,
                "data": b"",
            },
        },
        {
            "_description": "ICMPv6 Destination Unreachable (Address) message.",
            "_args": {
                "code": Icmp6DestinationUnreachableCode.ADDRESS,
                "cksum": 12345,
                "data": b"",
            },
            "_results": {
                "__len__": 8,
                "__str__": "ICMPv6 Destination Unreachable - Address, len 8 (8+0)",
                "__repr__": (
                    "Icmp6DestinationUnreachableMessage("
                    "code=<Icmp6DestinationUnreachableCode.ADDRESS: 3>, cksum=12345, "
                    "data=b'')"
                ),
                "__bytes__": b"\x01\x03\x00\x00\x00\x00\x00\x00",
                "type": Icmp6Type.DESTINATION_UNREACHABLE,
                "code": Icmp6DestinationUnreachableCode.ADDRESS,
                "cksum": 12345,
                "data": b"",
            },
        },
        {
            "_description": "ICMPv6 Destination Unreachable (Port) message.",
            "_args": {
                "code": Icmp6DestinationUnreachableCode.PORT,
                "cksum": 12345,
                "data": b"",
            },
            "_results": {
                "__len__": 8,
                "__str__": "ICMPv6 Destination Unreachable - Port, len 8 (8+0)",
                "__repr__": (
                    "Icmp6DestinationUnreachableMessage("
                    "code=<Icmp6DestinationUnreachableCode.PORT: 4>, cksum=12345, "
                    "data=b'')"
                ),
                "__bytes__": b"\x01\x04\x00\x00\x00\x00\x00\x00",
                "type": Icmp6Type.DESTINATION_UNREACHABLE,
                "code": Icmp6DestinationUnreachableCode.PORT,
                "cksum": 12345,
                "data": b"",
            },
        },
        {
            "_description": "ICMPv6 Destination Unreachable (Failed Policy) message.",
            "_args": {
                "code": Icmp6DestinationUnreachableCode.FAILED_POLICY,
                "cksum": 12345,
                "data": b"",
            },
            "_results": {
                "__len__": 8,
                "__str__": "ICMPv6 Destination Unreachable - Failed Policy, len 8 (8+0)",
                "__repr__": (
                    "Icmp6DestinationUnreachableMessage("
                    "code=<Icmp6DestinationUnreachableCode.FAILED_POLICY: 5>, cksum=12345, "
                    "data=b'')"
                ),
                "__bytes__": b"\x01\x05\x00\x00\x00\x00\x00\x00",
                "type": Icmp6Type.DESTINATION_UNREACHABLE,
                "code": Icmp6DestinationUnreachableCode.FAILED_POLICY,
                "cksum": 12345,
                "data": b"",
            },
        },
        {
            "_description": "ICMPv6 Destination Unreachable (Reject Route) message.",
            "_args": {
                "code": Icmp6DestinationUnreachableCode.REJECT_ROUTE,
                "cksum": 12345,
                "data": b"",
            },
            "_results": {
                "__len__": 8,
                "__str__": "ICMPv6 Destination Unreachable - Reject Route, len 8 (8+0)",
                "__repr__": (
                    "Icmp6DestinationUnreachableMessage("
                    "code=<Icmp6DestinationUnreachableCode.REJECT_ROUTE: 6>, cksum=12345, "
                    "data=b'')"
                ),
                "__bytes__": b"\x01\x06\x00\x00\x00\x00\x00\x00",
                "type": Icmp6Type.DESTINATION_UNREACHABLE,
                "code": Icmp6DestinationUnreachableCode.REJECT_ROUTE,
                "cksum": 12345,
                "data": b"",
            },
        },
        {
            "_description": "ICMPv6 Destination Unreachable (Source Routing Header) message.",
            "_args": {
                "code": Icmp6DestinationUnreachableCode.SOURCE_ROUTING_HEADER,
                "cksum": 12345,
                "data": b"",
            },
            "_results": {
                "__len__": 8,
                "__str__": "ICMPv6 Destination Unreachable - Source Routing Header, len 8 (8+0)",
                "__repr__": (
                    "Icmp6DestinationUnreachableMessage("
                    "code=<Icmp6DestinationUnreachableCode.SOURCE_ROUTING_HEADER: 7>, cksum=12345, "
                    "data=b'')"
                ),
                "__bytes__": b"\x01\x07\x00\x00\x00\x00\x00\x00",
                "type": Icmp6Type.DESTINATION_UNREACHABLE,
                "code": Icmp6DestinationUnreachableCode.SOURCE_ROUTING_HEADER,
                "cksum": 12345,
                "data": b"",
            },
        },
        {
            "_description": "ICMPv6 Destination Unreachable message, non-empty payload.",
            "_args": {
                "code": Icmp6DestinationUnreachableCode.PORT,
                "cksum": 12345,
                "data": b"0123456789ABCDEF",
            },
            "_results": {
                "__len__": 24,
                "__str__": "ICMPv6 Destination Unreachable - Port, len 24 (8+16)",
                "__repr__": (
                    "Icmp6DestinationUnreachableMessage("
                    "code=<Icmp6DestinationUnreachableCode.PORT: 4>, cksum=12345, "
                    "data=b'0123456789ABCDEF')"
                ),
                "__bytes__": (
                    b"\x01\x04\x00\x00\x00\x00\x00\x00\x30\x31\x32\x33\x34\x35\x36\x37"
                    b"\x38\x39\x41\x42\x43\x44\x45\x46"
                ),
                "type": Icmp6Type.DESTINATION_UNREACHABLE,
                "code": Icmp6DestinationUnreachableCode.PORT,
                "cksum": 12345,
                "data": b"0123456789ABCDEF",
            },
        },
        {
            "_description": "ICMPv6 Destination Unreachable message, maximum length payload.",
            "_args": {
                "code": Icmp6DestinationUnreachableCode.PORT,
                "cksum": 12345,
                "data": b"X" * 65527,
            },
            "_results": {
                "__len__": 1240,
                "__str__": "ICMPv6 Destination Unreachable - Port, len 1240 (8+1232)",
                "__repr__": (
                    "Icmp6DestinationUnreachableMessage("
                    "code=<Icmp6DestinationUnreachableCode.PORT: 4>, cksum=12345, "
                    f"data=b'{"X" * 1232}')"
                ),
                "__bytes__": b"\x01\x04\x00\x00\x00\x00\x00\x00" + b"X" * 1232,
                "type": Icmp6Type.DESTINATION_UNREACHABLE,
                "code": Icmp6DestinationUnreachableCode.PORT,
                "cksum": 12345,
                "data": b"X" * 1232,
            },
        },
    ]
)
class TestIcmp6MessageDestinationUnreachableAssembler(TestCase):
    """
    The ICMPv6 Destination Unreachable message assembler tests.
    """

    _description: str
    _args: dict[str, Any]
    _results: dict[str, Any]

    def setUp(self) -> None:
        """
        Initialize the ICMPv6 Destination Unreachable message assembler
        object with testcase arguments.
        """

        self._icmp6__destination_unreachable__message = (
            Icmp6DestinationUnreachableMessage(**self._args)
        )

    def test__icmp6__message__destination_unreachable__assembler__len(
        self,
    ) -> None:
        """
        Ensure the ICMPv6 Destination Unreachable message '__len__()' method
        returns a correct value.
        """

        self.assertEqual(
            len(self._icmp6__destination_unreachable__message),
            self._results["__len__"],
        )

    def test__icmp6__message__destination_unreachable__assembler__str(
        self,
    ) -> None:
        """
        Ensure the ICMPv6 Destination Unreachable message '__str__()' method
        returns a correct value.
        """

        self.assertEqual(
            str(self._icmp6__destination_unreachable__message),
            self._results["__str__"],
        )

    def test__icmp6__message__destination_unreachable__assembler__repr(
        self,
    ) -> None:
        """
        Ensure the ICMPv6 Destination Unreachable message '__repr__()' method
        returns a correct value.
        """

        self.assertEqual(
            repr(self._icmp6__destination_unreachable__message),
            self._results["__repr__"],
        )

    def test__icmp6__message__destination_unreachable__assembler__bytes(
        self,
    ) -> None:
        """
        Ensure the ICMPv6 Destination Unreachable message '__bytes__()' method
        returns a correct value.
        """

        self.assertEqual(
            bytes(self._icmp6__destination_unreachable__message),
            self._results["__bytes__"],
        )

    def test__icmp6__message__destination_unreachable__assembler__type(
        self,
    ) -> None:
        """
        Ensure the ICMPv6 Destination Unreachable message 'type' property
        returns a correct value.
        """

        self.assertEqual(
            self._icmp6__destination_unreachable__message.type,
            self._results["type"],
        )

    def test__icmp6__message__destination_unreachable__assembler__code(
        self,
    ) -> None:
        """
        Ensure the ICMPv6 Destination Unreachable message 'code' property
        returns a correct value.
        """

        self.assertEqual(
            self._icmp6__destination_unreachable__message.code,
            self._results["code"],
        )

    def test__icmp6__message__destination_unreachable__assembler__cksum(
        self,
    ) -> None:
        """
        Ensure the ICMPv6 Destination Unreachable message 'cksum' property
        returns a correct value.
        """

        self.assertEqual(
            self._icmp6__destination_unreachable__message.cksum,
            self._results["cksum"],
        )

    def test__icmp6__message__destination_unreachable__assembler__data(
        self,
    ) -> None:
        """
        Ensure the ICMPv6 Destination Unreachable message 'data' property
        returns a correct value.
        """

        self.assertEqual(
            self._icmp6__destination_unreachable__message.data,
            self._results["data"],
        )
