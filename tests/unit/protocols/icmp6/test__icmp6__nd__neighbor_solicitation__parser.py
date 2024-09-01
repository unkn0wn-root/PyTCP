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
Module contains tests for the ICMPv6 ND Neighbor Solicitation message parser.

tests/unit/protocols/icmp6/test__icmp6__message__nd__neighbor_solicitation__parser.py

ver 3.0.2
"""


from typing import Any

from parameterized import parameterized_class  # type: ignore

from pytcp.lib.net_addr import Ip6Address, MacAddress
from pytcp.lib.packet import PacketRx
from pytcp.protocols.icmp6.icmp6__parser import Icmp6Parser
from pytcp.protocols.icmp6.message.nd.icmp6_nd_message__neighbor_solicitation import (
    Icmp6NdNeighborSolicitationMessage,
)
from pytcp.protocols.icmp6.message.nd.option.icmp6_nd_option__slla import (
    Icmp6NdOptionSlla,
)
from pytcp.protocols.icmp6.message.nd.option.icmp6_nd_options import (
    Icmp6NdOptions,
)
from tests.lib.testcase__packet_rx__ip6 import TestCasePacketRxIp6


@parameterized_class(
    [
        {
            "_description": "ICMPv6 ND Neighbor Solicitation message, no options.",
            "_args": {
                "bytes": (
                    b"\x87\x00\x4b\x45\x00\x00\x00\x00\x20\x01\x0d\xb8\x00\x00\x00\x00"
                    b"\x00\x00\x00\x00\x00\x00\x00\x01"
                ),
            },
            "_mocked_values": {
                "ip6__hop": 255,
                "ip6__src": Ip6Address("2001:db8::2"),
                "ip6__dst": Ip6Address("2001:db8::1"),
            },
            "_results": {
                "message": Icmp6NdNeighborSolicitationMessage(
                    cksum=19269,
                    target_address=Ip6Address("2001:db8::1"),
                    options=Icmp6NdOptions(),
                ),
            },
        },
        {
            "_description": "ICMPv6 ND Neighbor Solicitation message, Slla option present.",
            "_args": {
                "bytes": (
                    b"\x87\x00\xe3\xa9\x00\x00\x00\x00\x20\x01\x0d\xb8\x00\x00\x00\x00"
                    b"\x00\x00\x00\x00\x00\x00\x00\x02\x01\x01\x00\x11\x22\x33\x44\x55"
                ),
            },
            "_mocked_values": {
                "ip6__hop": 255,
                "ip6__src": Ip6Address("2001:db8::1"),
                "ip6__dst": Ip6Address("2001:db8::2"),
            },
            "_results": {
                "message": Icmp6NdNeighborSolicitationMessage(
                    cksum=58281,
                    target_address=Ip6Address("2001:db8::2"),
                    options=Icmp6NdOptions(
                        Icmp6NdOptionSlla(slla=MacAddress("00:11:22:33:44:55")),
                    ),
                ),
            },
        },
    ]
)
class TestIcmp6MessageNdNeighborSolicitationParser(TestCasePacketRxIp6):
    """
    The ICMPv6 ND Neighbor Solicitation message parser tests.
    """

    _description: str
    _args: dict[str, Any]
    _mocked_values: dict[str, Any]
    _results: dict[str, Any]

    _packet_rx: PacketRx

    def test__icmp6__nd__neighbor_solicitation__parser__from_bytes(
        self,
    ) -> None:
        """
        Ensure the ICMPv6 ND Neighbor Solicitation message 'from_bytes()' method
        creates a proper message object.
        """

        icmp6_parser = Icmp6Parser(packet_rx=self._packet_rx)

        self.assertEqual(
            icmp6_parser.message,
            self._results["message"],
        )
