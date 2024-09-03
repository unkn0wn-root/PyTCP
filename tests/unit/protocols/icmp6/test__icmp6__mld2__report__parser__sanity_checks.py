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
Module contains tests for the ICMPv6 MLDv2 Report message parser sanity checks.

tests/unit/protocols/icmp6/test__icmp6__mld2__report__parser__sanity_checks.py

ver 3.0.2
"""


from typing import Any

from parameterized import parameterized_class  # type: ignore

from pytcp.lib.packet import PacketRx
from pytcp.protocols.icmp6.icmp6__errors import Icmp6SanityError
from pytcp.protocols.icmp6.icmp6__parser import Icmp6Parser
from tests.lib.testcase__packet_rx__ip6 import TestCasePacketRxIp6


@parameterized_class(
    [
        {
            "_description": "The value of the 'ip6__hop' field must be 1. It's 64.",
            "_args": {
                "bytes": b"\x8f\x00\x70\xff\x00\x00\x00\x00",
            },
            "_mocked_values": {
                "ip6__hop": 64,
            },
            "_results": {
                "error_message": (
                    "MLDv2 Report - [RFC 3810] The 'ip6__hop' field must be 1. Got: 64"
                ),
            },
        },
        {
            "_description": "The value of the 'ip6__hop' field must be 1. It's 1.",
            "_args": {
                "bytes": b"\x8f\x00\x70\xff\x00\x00\x00\x00",
            },
            "_mocked_values": {
                "ip6__hop": 1,
            },
            "_results": {},
        },
    ]
)
class TestIcmp4Mld2ReportParserSanityChecks(TestCasePacketRxIp6):
    """
    The ICMPv4 MLDv2 Report message parser sanity checks tests.
    """

    _description: str
    _args: dict[str, Any]
    _mocked_values: dict[str, Any]
    _results: dict[str, Any]

    _packet_rx: PacketRx

    def test__icmp6__mld2__report__parser__from_bytes(self) -> None:
        """
        Ensure the ICMPv6 MLDv2 Report parser raises sanity errors
        on crazy packets.
        """

        if "error_message" in self._results:
            with self.assertRaises(Icmp6SanityError) as error:
                Icmp6Parser(self._packet_rx)

            self.assertEqual(
                str(error.exception),
                f"[SANITY ERROR][ICMPv6] {self._results["error_message"]}",
            )

        else:
            Icmp6Parser(self._packet_rx)
