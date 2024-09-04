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
This module contains tests for the Ethernet 802.3 packet sanity checks.

tests/unit/protocols/ethernet_802_3/test__ethernet_802_3__parser__sanity_check.py

ver 3.0.2
"""


from typing import Any

from parameterized import parameterized_class  # type: ignore

from pytcp.lib.packet import PacketRx
from pytcp.protocols.ethernet_802_3.ethernet_802_3__errors import (
    Ethernet8023SanityError,
)
from pytcp.protocols.ethernet_802_3.ethernet_802_3__parser import (
    Ethernet8023Parser,
)
from tests.lib.testcase__packet_rx import TestCasePacketRx


@parameterized_class([])
class TestEthernet8023ParserSanityChecks(TestCasePacketRx):
    """
    The Ethernet 802.3 packet parser sanity checks tests.
    """

    _description: str
    _args: list[Any]
    _results: dict[str, Any]

    _packet_rx: PacketRx

    def test__ethernet__parser__from_bytes(self) -> None:
        """
        Ensure the Ethernet 802.3 packet parser raises sanity errors on crazy packets.
        """

        with self.assertRaises(Ethernet8023SanityError) as error:
            Ethernet8023Parser(self._packet_rx)

        self.assertEqual(
            str(error.exception),
            f"[SANITY ERROR][Ethernet 802.3] {self._results["error_message"]}",
        )
