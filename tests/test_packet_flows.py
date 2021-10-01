#!/usr/bin/env python3


############################################################################
#                                                                          #
#  PyTCP - Python TCP/IP stack                                             #
#  Copyright (C) 2020-2021  Sebastian Majewski                             #
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


#
# tests/test_packet_handler.py - unit tests for PacketHandler class
#


from testslide import StrictMock, TestCase

from pytcp.lib.ip4_address import Ip4Address, Ip4Host
from pytcp.lib.ip6_address import Ip6Address, Ip6Host
from pytcp.lib.mac_address import MacAddress
from pytcp.misc.packet import PacketRx
from pytcp.misc.packet_stats import PacketStatsRx, PacketStatsTx
from pytcp.subsystems.arp_cache import ArpCache
from pytcp.subsystems.nd_cache import NdCache
from pytcp.subsystems.packet_handler import PacketHandler
from pytcp.subsystems.tx_ring import TxRing

PACKET_HANDLER_MODULES = [
    "pytcp.subsystems.packet_handler",
    "protocols.ether.phrx",
    "protocols.ether.phtx",
    "protocols.arp.phrx",
    "protocols.arp.phtx",
    "protocols.ip4.phrx",
    "protocols.ip4.phtx",
    "protocols.ip6.phrx",
    "protocols.ip6.phtx",
    "protocols.icmp4.phrx",
    "protocols.icmp4.phtx",
    "protocols.icmp6.phrx",
    "protocols.icmp6.phtx",
    "protocols.udp.phrx",
    "protocols.udp.phtx",
    "protocols.tcp.phrx",
    "protocols.tcp.phtx",
]

CONFIG_PATCHES = {
    "IP6_SUPPORT": True,
    "IP4_SUPPORT": True,
    "PACKET_INTEGRITY_CHECK": True,
    "PACKET_SANITY_CHECK": True,
    "TAP_MTU": 1500,
    "UDP_ECHO_NATIVE_DISABLE": False,
}


class TestPacketHandler(TestCase):
    def setUp(self):
        super().setUp()

        self._patch_logger()
        self._patch_config()

        self.arp_cache_mock = StrictMock(ArpCache)
        self.nd_cache_mock = StrictMock(NdCache)
        self.tx_ring_mock = StrictMock(TxRing)

        self.mock_callable(self.arp_cache_mock, "find_entry").for_call(Ip4Address("192.168.9.102")).to_return_value(MacAddress("52:54:00:df:85:37"))
        self.mock_callable(self.nd_cache_mock, "find_entry").for_call(Ip6Address("2603:9000:e307:9f09::1fa1")).to_return_value(MacAddress("52:54:00:df:85:37"))
        self.mock_callable(self.tx_ring_mock, "enqueue").with_implementation(lambda _: _.assemble(self.frame_tx))

        self.packet_handler = PacketHandler(None)
        self.packet_handler.mac_address = MacAddress("02:00:00:77:77:77")
        self.packet_handler.ip4_host = [Ip4Host("192.168.9.7/24")]
        self.packet_handler.ip6_host = [Ip6Host("2603:9000:e307:9f09:0:ff:fe77:7777/64")]
        self.packet_handler.arp_cache = self.arp_cache_mock
        self.packet_handler.nd_cache = self.nd_cache_mock
        self.packet_handler.tx_ring = self.tx_ring_mock

        self.frame_tx = memoryview(bytearray(2048))

    def _patch_config(self):
        for module in PACKET_HANDLER_MODULES:
            for variable, value in CONFIG_PATCHES.items():
                try:
                    self.patch_attribute(f"{module}.config", variable, value)
                except ModuleNotFoundError:
                    continue

    def _patch_logger(self):
        for module in PACKET_HANDLER_MODULES:
            try:
                self.mock_callable(module, "log").to_return_value(None)
            except ModuleNotFoundError:
                continue

    def test_packet_flow__ip4_ping(self):
        with open("tests/packets/rx_tx/ip4_ping.rx", "rb") as _:
            frame_rx = _.read()
        with open("tests/packets/rx_tx/ip4_ping.tx", "rb") as _:
            frame_tx = _.read()
        self.packet_handler._phrx_ether(PacketRx(frame_rx))
        self.assertEqual(
            self.packet_handler.packet_stats_rx,
            PacketStatsRx(
                ether__pre_parse=1,
                ether__dst_unicast=1,
                ip4__pre_parse=1,
                ip4__dst_unicast=1,
                icmp4__pre_parse=1,
                icmp4__echo_request=1,
            ),
        )
        self.assertEqual(
            self.packet_handler.packet_stats_tx,
            PacketStatsTx(
                icmp4__pre_assemble=1,
                icmp4__echo_reply__send=1,
                ip4__pre_assemble=1,
                ip4__mtu_ok__send=1,
                ether__pre_assemble=1,
                ether__src_unspec__fill=1,
                ether__dst_unspec=1,
                ether__dst_unspec__ip4_lookup=1,
                ether__dst_unspec__ip4_lookup__loc_net__nd_cache_hit__send=1,
            ),
        )
        self.assertEqual(self.frame_tx[: len(frame_tx)], frame_tx)

    def test_packet_flow__ip4_udp_to_closed_port(self):
        with open("tests/packets/rx_tx/ip4_udp_to_closed_port.rx", "rb") as _:
            frame_rx = _.read()
        with open("tests/packets/rx_tx/ip4_udp_to_closed_port.tx", "rb") as _:
            frame_tx = _.read()
        self.packet_handler._phrx_ether(PacketRx(frame_rx))
        self.assertEqual(
            self.packet_handler.packet_stats_rx,
            PacketStatsRx(
                ether__pre_parse=1,
                ether__dst_unicast=1,
                ip4__pre_parse=1,
                ip4__dst_unicast=1,
                udp__pre_parse=1,
                udp__no_socket_match__respond_icmp4_unreachable=1,
            ),
        )
        self.assertEqual(
            self.packet_handler.packet_stats_tx,
            PacketStatsTx(
                icmp4__pre_assemble=1,
                icmp4__unreachable__send=1,
                ip4__pre_assemble=1,
                ip4__mtu_ok__send=1,
                ether__pre_assemble=1,
                ether__src_unspec__fill=1,
                ether__dst_unspec=1,
                ether__dst_unspec__ip4_lookup=1,
                ether__dst_unspec__ip4_lookup__loc_net__nd_cache_hit__send=1,
            ),
        )
        self.assertEqual(self.frame_tx[: len(frame_tx)], frame_tx)

    def test_packet_flow__ip4_udp_echo(self):
        with open("tests/packets/rx_tx/ip4_udp_echo.rx", "rb") as _:
            frame_rx = _.read()
        with open("tests/packets/rx_tx/ip4_udp_echo.tx", "rb") as _:
            frame_tx = _.read()
        self.packet_handler._phrx_ether(PacketRx(frame_rx))
        self.assertEqual(
            self.packet_handler.packet_stats_rx,
            PacketStatsRx(
                ether__pre_parse=1,
                ether__dst_unicast=1,
                ip4__pre_parse=1,
                ip4__dst_unicast=1,
                udp__pre_parse=1,
                udp__echo_native=1,
            ),
        )
        self.assertEqual(
            self.packet_handler.packet_stats_tx,
            PacketStatsTx(
                udp__pre_assemble=1,
                udp__send=1,
                ip4__pre_assemble=1,
                ip4__mtu_ok__send=1,
                ether__pre_assemble=1,
                ether__src_unspec__fill=1,
                ether__dst_unspec=1,
                ether__dst_unspec__ip4_lookup=1,
                ether__dst_unspec__ip4_lookup__loc_net__nd_cache_hit__send=1,
            ),
        )
        self.assertEqual(self.frame_tx[: len(frame_tx)], frame_tx)

    def test_packet_flow__ip4_tcp_syn_to_closed_port(self):
        with open("tests/packets/rx_tx/ip4_tcp_syn_to_closed_port.rx", "rb") as _:
            frame_rx = _.read()
        with open("tests/packets/rx_tx/ip4_tcp_syn_to_closed_port.tx", "rb") as _:
            frame_tx = _.read()
        self.packet_handler._phrx_ether(PacketRx(frame_rx))
        self.assertEqual(
            self.packet_handler.packet_stats_rx,
            PacketStatsRx(
                ether__pre_parse=1,
                ether__dst_unicast=1,
                ip4__pre_parse=1,
                ip4__dst_unicast=1,
                tcp__pre_parse=1,
                tcp__no_socket_match__respond_rst=1,
            ),
        )
        self.assertEqual(
            self.packet_handler.packet_stats_tx,
            PacketStatsTx(
                tcp__pre_assemble=1,
                tcp__flag_rst=1,
                tcp__flag_ack=1,
                tcp__send=1,
                ip4__pre_assemble=1,
                ip4__mtu_ok__send=1,
                ether__pre_assemble=1,
                ether__src_unspec__fill=1,
                ether__dst_unspec=1,
                ether__dst_unspec__ip4_lookup=1,
                ether__dst_unspec__ip4_lookup__loc_net__nd_cache_hit__send=1,
            ),
        )
        self.assertEqual(self.frame_tx[: len(frame_tx)], frame_tx)

    def test_packet_flow__ip6_ping(self):
        with open("tests/packets/rx_tx/ip6_ping.rx", "rb") as _:
            frame_rx = _.read()
        with open("tests/packets/rx_tx/ip6_ping.tx", "rb") as _:
            frame_tx = _.read()
        self.packet_handler._phrx_ether(PacketRx(frame_rx))
        self.assertEqual(
            self.packet_handler.packet_stats_rx,
            PacketStatsRx(
                ether__pre_parse=1,
                ether__dst_unicast=1,
                ip6__pre_parse=1,
                ip6__dst_unicast=1,
                icmp6__pre_parse=1,
                icmp6__echo_request=1,
            ),
        )
        self.assertEqual(
            self.packet_handler.packet_stats_tx,
            PacketStatsTx(
                icmp6__pre_assemble=1,
                icmp6__echo_reply__send=1,
                ip6__pre_assemble=1,
                ip6__mtu_ok__send=1,
                ether__pre_assemble=1,
                ether__src_unspec__fill=1,
                ether__dst_unspec=1,
                ether__dst_unspec__ip6_lookup=1,
                ether__dst_unspec__ip6_lookup__loc_net__nd_cache_hit__send=1,
            ),
        )
        self.assertEqual(self.frame_tx[: len(frame_tx)], frame_tx)

    def test_packet_flow__ip6_udp_to_closed_port(self):
        with open("tests/packets/rx_tx/ip6_udp_to_closed_port.rx", "rb") as _:
            frame_rx = _.read()
        with open("tests/packets/rx_tx/ip6_udp_to_closed_port.tx", "rb") as _:
            frame_tx = _.read()
        self.packet_handler._phrx_ether(PacketRx(frame_rx))
        self.assertEqual(
            self.packet_handler.packet_stats_rx,
            PacketStatsRx(
                ether__pre_parse=1,
                ether__dst_unicast=1,
                ip6__pre_parse=1,
                ip6__dst_unicast=1,
                udp__pre_parse=1,
                udp__no_socket_match__respond_icmp6_unreachable=1,
            ),
        )
        self.assertEqual(
            self.packet_handler.packet_stats_tx,
            PacketStatsTx(
                icmp6__pre_assemble=1,
                icmp6__unreachable__send=1,
                ip6__pre_assemble=1,
                ip6__mtu_ok__send=1,
                ether__pre_assemble=1,
                ether__src_unspec__fill=1,
                ether__dst_unspec=1,
                ether__dst_unspec__ip6_lookup=1,
                ether__dst_unspec__ip6_lookup__loc_net__nd_cache_hit__send=1,
            ),
        )
        self.assertEqual(self.frame_tx[: len(frame_tx)], frame_tx)

    def test_packet_flow__ip6_udp_echo(self):
        with open("tests/packets/rx_tx/ip6_udp_echo.rx", "rb") as _:
            frame_rx = _.read()
        with open("tests/packets/rx_tx/ip6_udp_echo.tx", "rb") as _:
            frame_tx = _.read()
        self.packet_handler._phrx_ether(PacketRx(frame_rx))
        self.assertEqual(
            self.packet_handler.packet_stats_rx,
            PacketStatsRx(
                ether__pre_parse=1,
                ether__dst_unicast=1,
                ip6__pre_parse=1,
                ip6__dst_unicast=1,
                udp__pre_parse=1,
                udp__echo_native=1,
            ),
        )
        self.assertEqual(
            self.packet_handler.packet_stats_tx,
            PacketStatsTx(
                udp__pre_assemble=1,
                udp__send=1,
                ip6__pre_assemble=1,
                ip6__mtu_ok__send=1,
                ether__pre_assemble=1,
                ether__src_unspec__fill=1,
                ether__dst_unspec=1,
                ether__dst_unspec__ip6_lookup=1,
                ether__dst_unspec__ip6_lookup__loc_net__nd_cache_hit__send=1,
            ),
        )
        self.assertEqual(self.frame_tx[: len(frame_tx)], frame_tx)

    def test_packet_flow__ip6_tcp_syn_to_closed_port(self):
        with open("tests/packets/rx_tx/ip6_tcp_syn_to_closed_port.rx", "rb") as _:
            frame_rx = _.read()
        with open("tests/packets/rx_tx/ip6_tcp_syn_to_closed_port.tx", "rb") as _:
            frame_tx = _.read()
        self.packet_handler._phrx_ether(PacketRx(frame_rx))
        self.assertEqual(
            self.packet_handler.packet_stats_rx,
            PacketStatsRx(
                ether__pre_parse=1,
                ether__dst_unicast=1,
                ip6__pre_parse=1,
                ip6__dst_unicast=1,
                tcp__pre_parse=1,
                tcp__no_socket_match__respond_rst=1,
            ),
        )
        self.assertEqual(
            self.packet_handler.packet_stats_tx,
            PacketStatsTx(
                tcp__pre_assemble=1,
                tcp__flag_rst=1,
                tcp__flag_ack=1,
                tcp__send=1,
                ip6__pre_assemble=1,
                ip6__mtu_ok__send=1,
                ether__pre_assemble=1,
                ether__src_unspec__fill=1,
                ether__dst_unspec=1,
                ether__dst_unspec__ip6_lookup=1,
                ether__dst_unspec__ip6_lookup__loc_net__nd_cache_hit__send=1,
            ),
        )
        self.assertEqual(self.frame_tx[: len(frame_tx)], frame_tx)

    def test_packet_flow__arp_request(self):
        with open("tests/packets/rx_tx/arp_request.rx", "rb") as _:
            frame_rx = _.read()
        with open("tests/packets/rx_tx/arp_request.tx", "rb") as _:
            frame_tx = _.read()
        self.mock_callable(self.arp_cache_mock, "add_entry").for_call(Ip4Address("192.168.9.102"), MacAddress("52:54:00:df:85:37")).to_return_value(
            None
        ).and_assert_called_once()
        self.packet_handler._phrx_ether(PacketRx(frame_rx))
        self.assertEqual(
            self.packet_handler.packet_stats_rx,
            PacketStatsRx(
                ether__pre_parse=1,
                ether__dst_broadcast=1,
                arp__pre_parse=1,
                arp__op_request=1,
                arp__op_request__update_cache=1,
            ),
        )
        self.assertEqual(
            self.packet_handler.packet_stats_tx,
            PacketStatsTx(
                arp__pre_assemble=1,
                arp__op_reply__send=1,
                ether__pre_assemble=1,
                ether__src_spec=1,
                ether__dst_spec__send=1,
            ),
        )
        self.assertEqual(self.frame_tx[: len(frame_tx)], frame_tx)


    def test_packet_flow__ether_unknown_dst(self):
        with open("tests/packets/rx/ether_unknown_dst.rx", "rb") as _:
            frame_rx = _.read()
        self.packet_handler._phrx_ether(PacketRx(frame_rx))
        self.assertEqual(
            self.packet_handler.packet_stats_rx,
            PacketStatsRx(
                ether__pre_parse=1,
                ether__dst_unknown__drop=1,
            ),
        )
        self.assertEqual(
            self.packet_handler.packet_stats_tx,
            PacketStatsTx(),
        )

    def test_packet_flow__ip4_unknown_dst(self):
        with open("tests/packets/rx/ip4_unknown_dst.rx", "rb") as _:
            frame_rx = _.read()
        self.packet_handler._phrx_ether(PacketRx(frame_rx))
        self.assertEqual(
            self.packet_handler.packet_stats_rx,
            PacketStatsRx(
                ether__pre_parse=1,
                ether__dst_unicast=1,
                ip4__pre_parse=1,
                ip4__dst_unknown__drop=1,
            ),
        )
        self.assertEqual(
            self.packet_handler.packet_stats_tx,
            PacketStatsTx(),
        )
    
    def test_packet_flow__ip6_unknown_dst(self):
        with open("tests/packets/rx/ip6_unknown_dst.rx", "rb") as _:
            frame_rx = _.read()
        self.packet_handler._phrx_ether(PacketRx(frame_rx))
        self.assertEqual(
            self.packet_handler.packet_stats_rx,
            PacketStatsRx(
                ether__pre_parse=1,
                ether__dst_unicast=1,
                ip6__pre_parse=1,
                ip6__dst_unknown__drop=1,
            ),
        )
        self.assertEqual(
            self.packet_handler.packet_stats_tx,
            PacketStatsTx(),
        )
    
    def test_packet_flow__arp_unknown_tpa(self):
        with open("tests/packets/rx/arp_unknown_tpa.rx", "rb") as _:
            frame_rx = _.read()
        self.packet_handler._phrx_ether(PacketRx(frame_rx))
        self.assertEqual(
            self.packet_handler.packet_stats_rx,
            PacketStatsRx(
                ether__pre_parse=1,
                ether__dst_broadcast=1,
                arp__pre_parse=1,
                arp__op_request=1,
                arp__op_request__tpa_unknown__drop=1,
            ),
        )
        self.assertEqual(
            self.packet_handler.packet_stats_tx,
            PacketStatsTx(),
        )
