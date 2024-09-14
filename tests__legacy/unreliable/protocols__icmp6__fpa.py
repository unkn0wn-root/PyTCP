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


#
# tests/icmp6_fpa.py -  tests specific for ICMPv6 fpa module
#
# ver 3.0.2
#

from testslide import TestCase

from net_addr import Ip6Address, Ip6Network, MacAddress
from pytcp.lib.tracker import Tracker
from pytcp.protocols.icmp4.icmp4__assembler import (
    Icmp4EchoReplyMessageAssembler,
)
from pytcp.protocols.icmp6.icmp6__assembler import (
    Icmp6Assembler,
    Icmp6EchoReplyMessageAssembler,
    Icmp6EchoRequestMessageAssembler,
    Icmp6Mld2AddressRecordAssembler,
    Icmp6Mld2ReportMessageAssembler,
    Icmp6NdNeighborAdvertisementMessageAssembler,
    Icmp6NdNeighborSolicitationMessageAssembler,
    Icmp6NdOptPiAssembler,
    Icmp6NdOptSllaAssembler,
    Icmp6NdOptTllaAssembler,
    Icmp6NdRouterAdvertisementMessageAssembler,
    Icmp6NdRouterSolicitationMessageAssembler,
    Icmp6PortUnreachableMessageAssembler,
)
from pytcp.protocols.icmp6.icmp6__base import (
    ICMP6_MESSAGE_LEN__ECHO_REPLY,
    ICMP6_MESSAGE_LEN__ECHO_REQUEST,
    ICMP6_MESSAGE_LEN__ND_NEIGHBOR_ADVERTISEMENT,
    ICMP6_MESSAGE_LEN__ND_NEIGHBOR_SOLICITATION,
    ICMP6_MESSAGE_LEN__ND_ROUTER_ADVERTISEMENT,
    ICMP6_MESSAGE_LEN__ND_ROUTER_SOLICITATION,
    ICMP6_MESSAGE_LEN__UNREACHABLE,
    Icmp6EchoRequestMessage,
    Icmp6Mld2RecordType,
    Icmp6NdNeighborAdvertisementMessage,
    Icmp6NdNeighborSolicitationMessage,
    Icmp6NdRouterAdvertisementMessage,
    Icmp6NdRouterSolicitationMessage,
    Icmp6PortUnreachableMessage,
)
from pytcp.protocols.icmp6.icmp6__parser import Icmp6Mld2ReportMessageParser
from pytcp.protocols.ip6.ip6__base import IP6_NEXT_ICMP6


class TestIcmp6Assembler(TestCase):
    """
    ICMPv6 protocol packet assembler unit test class.
    """

    def setUp(self) -> None:
        """
        Set up the test environment.
        """
        super().setUp()

        self._dummy__mac_address_1 = MacAddress("11:22:33:44:55:66")
        self._dummy__mac_address_2 = MacAddress("66:55:44:33:22:11")

        self._dummy__id = 12345
        self._dummy__seq = 54321
        self._dummy__data = b"0123456789ABCDEF" * 50

        self._dummy__nd_options = [
            Icmp6NdOptSllaAssembler(slla=self._dummy__mac_address_1),
            Icmp6NdOptTllaAssembler(tlla=self._dummy__mac_address_2),
        ]

        self._dummy__hop = 255
        self._dummy__flag_m = True
        self._dummy__flag_o = True
        self._dummy__flag_r = True
        self._dummy__flag_s = True
        self._dummy__router_lifetime = 12345
        self._dummy__reachable_time = 12345678
        self._dummy__retrans_timer = 87654321
        self._dummy__target_address = Ip6Address("1:2:3:4:5:6:7:8")

    def test_icmp6_fpa__ip6_next_icmp6(self) -> None:
        """
        Make sure the 'Icmp6Assembler' class has the proper 'ip6_next' set.
        """

        self.assertEqual(Icmp6Assembler.ip6_next, IP6_NEXT_ICMP6)

    def test_icmp6_fpa____init____unreachable_port(self) -> None:
        """
        Test packet constructor for the 'Unreachable Port' message.
        """

        packet = Icmp6Assembler(
            message=Icmp6PortUnreachableMessageAssembler(
                data=self._dummy__data,
            ),
        )

        assert isinstance(packet.message, Icmp6PortUnreachableMessage)

        self.assertEqual(packet.message._reserved, 0)
        self.assertEqual(packet.message.data, self._dummy__data[:520])

    def test_icmp6_fpa____init____echo_request(self) -> None:
        """
        Test packet constructor for the 'Echo Request' message.
        """

        packet = Icmp6Assembler(
            message=Icmp6EchoRequestMessageAssembler(
                id=self._dummy__id,
                seq=self._dummy__seq,
                data=self._dummy__data,
            ),
        )

        assert isinstance(packet.message, Icmp6EchoRequestMessage)

        self.assertEqual(packet.message.id, self._dummy__id)
        self.assertEqual(packet.message.seq, self._dummy__seq)
        self.assertEqual(packet.message.data, self._dummy__data)

    def test_icmp6_fpa____init____echo_request__assert_id__under(
        self,
    ) -> None:
        """
        Test assertion for the 'id' argument.
        """

        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6EchoRequestMessageAssembler(
                    id=-1,
                    seq=self._dummy__seq,
                    data=self._dummy__data,
                ),
            )

    def test_icmp6_fpa____init____echo_request__assert_id__over(
        self,
    ) -> None:
        """
        Test assertion for the 'id' argument.
        """

        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6EchoRequestMessageAssembler(
                    id=0x10000,
                    seq=self._dummy__seq,
                    data=self._dummy__data,
                ),
            )

    def test_icmp6_fpa____init____echo_request__assert_seq__under(
        self,
    ) -> None:
        """
        Test assertion for the 'id' argument.
        """

        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6EchoRequestMessageAssembler(
                    id=self._dummy__id,
                    seq=-1,
                    data=self._dummy__data,
                ),
            )

    def test_icmp6_fpa____init____echo_request__assert_ec_seq__over(
        self,
    ) -> None:
        """
        Test assertion for the 'seq' argument.
        """

        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6EchoRequestMessageAssembler(
                    id=self._dummy__id,
                    seq=0x10000,
                    data=self._dummy__data,
                ),
            )

    def test_icmp6_fpa____init____echo_reply(self) -> None:
        """
        Test packet constructor for the 'Echo Reply' message.
        """

        packet = Icmp6Assembler(
            message=Icmp6EchoReplyMessageAssembler(
                id=self._dummy__id,
                seq=self._dummy__seq,
                data=self._dummy__data,
            ),
        )

        assert isinstance(packet.message, Icmp4EchoReplyMessageAssembler)

        self.assertEqual(packet.message.id, self._dummy__id)
        self.assertEqual(packet.message.seq, self._dummy__seq)
        self.assertEqual(packet.message.data, self._dummy__data)

    def test_icmp6_fpa____init____echo_reply__assert_id__under(
        self,
    ) -> None:
        """
        Test assertion for the 'id' argument.
        """

        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6EchoReplyMessageAssembler(
                    id=-1,
                    seq=self._dummy__seq,
                    data=self._dummy__data,
                ),
            )

    def test_icmp6_fpa____init____echo_reply__assert_id__over(
        self,
    ) -> None:
        """
        Test assertion for the 'id' argument.
        """

        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6EchoReplyMessageAssembler(
                    id=0x10000,
                    seq=self._dummy__seq,
                    data=self._dummy__data,
                ),
            )

    def test_icmp6_fpa____init____echo_reply__assert_seq__under(
        self,
    ) -> None:
        """
        Test assertion for the 'id' argument.
        """

        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6EchoReplyMessageAssembler(
                    id=self._dummy__id,
                    seq=-1,
                    data=self._dummy__data,
                ),
            )

    def test_icmp6_fpa____init____echo_reply__assert_ec_seq__over(
        self,
    ) -> None:
        """
        Test assertion for the 'ec_seq' argument.
        """

        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6EchoReplyMessageAssembler(
                    id=self._dummy__id,
                    seq=0x10000,
                    data=self._dummy__data,
                ),
            )

    def test_icmp6_fpa____init____nd_router_solicitation(self) -> None:
        """
        Test packet constructor for the 'ND Router Solicitation' message.
        """

        packet = Icmp6Assembler(
            message=Icmp6NdRouterSolicitationMessageAssembler(
                nd_options=self._dummy__nd_options,
            ),
        )

        assert isinstance(packet.message, Icmp6NdRouterSolicitationMessage)

        self.assertEqual(packet.message._reserved, 0)
        self.assertEqual(packet.message.nd_options, self._dummy__nd_options)

    def test_icmp6_fpa____init____nd_router_advertisement(self) -> None:
        """
        Test packet constructor for the 'ND Router Advertisement' message.
        """

        packet = Icmp6Assembler(
            message=Icmp6NdRouterAdvertisementMessageAssembler(
                hop=self._dummy__hop,
                flag_m=self._dummy__flag_m,
                flag_o=self._dummy__flag_o,
                router_lifetime=self._dummy__router_lifetime,
                reachable_time=self._dummy__reachable_time,
                retrans_timer=self._dummy__retrans_timer,
                nd_options=self._dummy__nd_options,
            ),
        )

        assert isinstance(packet.message, Icmp6NdRouterAdvertisementMessage)

        self.assertEqual(packet.message.hop, self._dummy__hop)
        self.assertEqual(packet.message.flag_m, self._dummy__flag_m)
        self.assertEqual(packet.message.flag_o, self._dummy__flag_o)
        self.assertEqual(
            packet.message.router_lifetime, self._dummy__router_lifetime
        )
        self.assertEqual(
            packet.message.reachable_time, self._dummy__reachable_time
        )
        self.assertEqual(
            packet.message.retrans_timer, self._dummy__retrans_timer
        )
        self.assertEqual(packet.message.nd_options, self._dummy__nd_options)

    def test_icmp6_fpa____init____nd_router_advertisement__assert_hop__under(
        self,
    ) -> None:
        """
        Test packet constructor for the 'ND Router Advertisement' message.
        """

        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6NdRouterAdvertisementMessageAssembler(
                    hop=-1,
                    flag_m=self._dummy__flag_m,
                    flag_o=self._dummy__flag_o,
                    router_lifetime=self._dummy__router_lifetime,
                    reachable_time=self._dummy__reachable_time,
                    retrans_timer=self._dummy__retrans_timer,
                    nd_options=self._dummy__nd_options,
                ),
            )

    def test_icmp6_fpa____init____nd_router_advertisement__assert_hop__over(
        self,
    ) -> None:
        """
        Test packet constructor for the 'ND Router Advertisement' message.
        """
        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6NdRouterAdvertisementMessageAssembler(
                    hop=0x100,
                    flag_m=self._dummy__flag_m,
                    flag_o=self._dummy__flag_o,
                    router_lifetime=self._dummy__router_lifetime,
                    reachable_time=self._dummy__reachable_time,
                    retrans_timer=self._dummy__retrans_timer,
                    nd_options=self._dummy__nd_options,
                ),
            )

    def test_icmp6_fpa____init____nd_router_advertisement__assert_router_lifetime__under(
        self,
    ) -> None:
        """
        Test packet constructor for the 'ND Router Advertisement' message.
        """
        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6NdRouterAdvertisementMessageAssembler(
                    hop=self._dummy__hop,
                    flag_m=self._dummy__flag_m,
                    flag_o=self._dummy__flag_o,
                    router_lifetime=-1,
                    reachable_time=self._dummy__reachable_time,
                    retrans_timer=self._dummy__retrans_timer,
                    nd_options=self._dummy__nd_options,
                ),
            )

    def test_icmp6_fpa____init____nd_router_advertisement__assert_router_lifetime__over(
        self,
    ) -> None:
        """
        Test packet constructor for the 'ND Router Advertisement' message.
        """
        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6NdRouterAdvertisementMessageAssembler(
                    hop=self._dummy__hop,
                    flag_m=self._dummy__flag_m,
                    flag_o=self._dummy__flag_o,
                    router_lifetime=0x10000,
                    reachable_time=self._dummy__reachable_time,
                    retrans_timer=self._dummy__retrans_timer,
                    nd_options=self._dummy__nd_options,
                ),
            )

    def test_icmp6_fpa____init____nd_router_advertisement__assert_reachable_time__under(
        self,
    ) -> None:
        """
        Test packet constructor for the 'ND Router Advertisement' message.
        """
        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6NdRouterAdvertisementMessageAssembler(
                    hop=self._dummy__hop,
                    flag_m=self._dummy__flag_m,
                    flag_o=self._dummy__flag_o,
                    router_lifetime=self._dummy__router_lifetime,
                    reachable_time=-1,
                    retrans_timer=self._dummy__retrans_timer,
                    nd_options=self._dummy__nd_options,
                ),
            )

    def test_icmp6_fpa____init____nd_router_advertisement__assert_reachable_time__over(
        self,
    ) -> None:
        """
        Test packet constructor for the 'ND Router Advertisement' message.
        """
        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6NdRouterAdvertisementMessageAssembler(
                    hop=self._dummy__hop,
                    flag_m=self._dummy__flag_m,
                    flag_o=self._dummy__flag_o,
                    router_lifetime=self._dummy__router_lifetime,
                    reachable_time=0x100000000,
                    retrans_timer=self._dummy__retrans_timer,
                    nd_options=self._dummy__nd_options,
                ),
            )

    def test_icmp6_fpa____init____nd_router_advertisement__assert_retrans_timer__under(
        self,
    ) -> None:
        """
        Test packet constructor for the 'ND Router Advertisement' message.
        """
        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6NdRouterAdvertisementMessageAssembler(
                    hop=self._dummy__hop,
                    flag_m=self._dummy__flag_m,
                    flag_o=self._dummy__flag_o,
                    router_lifetime=self._dummy__router_lifetime,
                    reachable_time=self._dummy__reachable_time,
                    retrans_timer=-1,
                    nd_options=self._dummy__nd_options,
                ),
            )

    def test_icmp6_fpa____init____nd_router_advertisement__assert_retrans_timer__over(
        self,
    ) -> None:
        """
        Test packet constructor for the 'ND Router Advertisement' message.
        """
        with self.assertRaises(AssertionError):
            Icmp6Assembler(
                message=Icmp6NdRouterAdvertisementMessageAssembler(
                    hop=self._dummy__hop,
                    flag_m=self._dummy__flag_m,
                    flag_o=self._dummy__flag_o,
                    router_lifetime=self._dummy__router_lifetime,
                    reachable_time=self._dummy__reachable_time,
                    retrans_timer=0x100000000,
                    nd_options=self._dummy__nd_options,
                ),
            )

    def test_icmp6_fpa____init____nd_neighbor_solicitation(self) -> None:
        """
        Test packet constructor for the 'ND Neighbor Solicitation' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdNeighborSolicitationMessageAssembler(
                target_address=self._dummy__target_address,
                nd_options=self._dummy__nd_options,
            ),
        )

        assert isinstance(packet.message, Icmp6NdNeighborSolicitationMessage)

        self.assertEqual(
            packet.message.target_address, self._dummy__target_address
        )
        self.assertEqual(packet.message.nd_options, self._dummy__nd_options)

    def test_icmp6_fpa____init____nd_neighbor_advertisement(self) -> None:
        """
        Test packet constructor for the 'ND Neighbor Advertisement' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdNeighborAdvertisementMessageAssembler(
                flag_r=self._dummy__flag_r,
                flag_s=self._dummy__flag_s,
                flag_o=self._dummy__flag_o,
                target_address=self._dummy__target_address,
                nd_options=self._dummy__nd_options,
            ),
        )

        assert isinstance(packet.message, Icmp6NdNeighborAdvertisementMessage)

        self.assertEqual(packet.message.flag_r, self._dummy__flag_r)
        self.assertEqual(packet.message.flag_s, self._dummy__flag_s)
        self.assertEqual(packet.message.flag_o, self._dummy__flag_o)
        self.assertEqual(packet.message._reserved, 0)
        self.assertEqual(
            packet.message.target_address, self._dummy__target_address
        )
        self.assertEqual(packet.message._nd_options, self._dummy__nd_options)

    def test_icmp6_fpa____init____mld2_report(self) -> None:
        """
        Test packet constructor for the 'Multicast Discovery v2 Report' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6Mld2ReportMessageAssembler(
                records=[
                    Icmp6Mld2AddressRecordAssembler(
                        record_type=Icmp6Mld2RecordType.MODE_IS_INCLUDE,
                        multicast_address=Ip6Address("FF00:2:3:4:5:6:7:8"),
                    ),
                    Icmp6Mld2AddressRecordAssembler(
                        record_type=Icmp6Mld2RecordType.MODE_IS_EXCLUDE,
                        multicast_address=Ip6Address("FF00:8:7:6:5:4:3:2"),
                    ),
                ],
            ),
        )

        assert isinstance(packet.message, Icmp6Mld2ReportMessageParser)

        self.assertEqual(packet.message._reserved, 0)
        self.assertEqual(
            packet.message.records,
            [
                Icmp6Mld2AddressRecordAssembler(
                    record_type=Icmp6Mld2RecordType.MODE_IS_INCLUDE,
                    multicast_address=Ip6Address("FF00:2:3:4:5:6:7:8"),
                ),
                Icmp6Mld2AddressRecordAssembler(
                    record_type=Icmp6Mld2RecordType.MODE_IS_EXCLUDE,
                    multicast_address=Ip6Address("FF00:8:7:6:5:4:3:2"),
                ),
            ],
        )

    def test_icmp6_fpa____len____port_unreachable(self) -> None:
        """
        Test the '__len__()' dunder for 'Port Unreachable' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6PortUnreachableMessageAssembler(
                data=self._dummy__data,
            ),
        )

        self.assertEqual(
            len(packet), ICMP6_MESSAGE_LEN__UNREACHABLE + len(self._dummy__data)
        )

    def test_icmp6_fpa____len____echo_request(self) -> None:
        """
        Test the '__len__()' dunder for 'Echo Request' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6EchoRequestMessageAssembler(
                id=self._dummy__id,
                seq=self._dummy__seq,
                data=self._dummy__data,
            ),
        )

        self.assertEqual(
            len(packet),
            ICMP6_MESSAGE_LEN__ECHO_REQUEST + len(self._dummy__data),
        )

    def test_icmp6_fpa____len____echo_reply(self) -> None:
        """
        Test the '__len__()' dunder for 'Echo Reply' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6EchoReplyMessageAssembler(
                id=self._dummy__id,
                seq=self._dummy__seq,
                data=self._dummy__data,
            ),
        )

        self.assertEqual(
            len(packet), ICMP6_MESSAGE_LEN__ECHO_REPLY + len(self._dummy__data)
        )

    def test_icmp6_fpa____len____nd_router_solicitation(self) -> None:
        """
        Test the '__len__()' dunder for 'Router Solicitation' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdRouterSolicitationMessageAssembler(
                nd_options=self._dummy__nd_options,
            ),
        )
        self.assertEqual(
            len(packet),
            ICMP6_MESSAGE_LEN__ND_ROUTER_SOLICITATION
            + sum(len(opt) for opt in self._dummy__nd_options),
        )

    def test_icmp6_fpa____len____nd_router_advertisement(self) -> None:
        """
        Test the '__len__() dunder for 'Router Advertisement' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdRouterAdvertisementMessageAssembler(
                hop=self._dummy__hop,
                flag_m=self._dummy__flag_m,
                flag_o=self._dummy__flag_o,
                router_lifetime=self._dummy__router_lifetime,
                reachable_time=self._dummy__reachable_time,
                retrans_timer=self._dummy__retrans_timer,
                nd_options=self._dummy__nd_options,
            ),
        )
        self.assertEqual(
            len(packet),
            ICMP6_MESSAGE_LEN__ND_ROUTER_ADVERTISEMENT
            + sum(len(opt) for opt in self._dummy__nd_options),
        )

    def test_icmp6_fpa____len____nd_neighbor_solicitation(self) -> None:
        """
        Test the '__len__() dunder for 'Neighbor Solicitation' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdNeighborSolicitationMessageAssembler(
                target_address=self._dummy__target_address,
                nd_options=self._dummy__nd_options,
            ),
        )
        self.assertEqual(
            len(packet),
            ICMP6_MESSAGE_LEN__ND_NEIGHBOR_SOLICITATION
            + sum(len(opt) for opt in self._dummy__nd_options),
        )

    def test_icmp6_fpa____len____nd_neighbor_advertisement(self) -> None:
        """
        Test the '__len__()' dunder for 'Neighbor Advertisement' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdNeighborAdvertisementMessageAssembler(
                flag_r=self._dummy__flag_r,
                flag_s=self._dummy__flag_s,
                flag_o=self._dummy__flag_o,
                target_address=self._dummy__target_address,
                nd_options=self._dummy__nd_options,
            ),
        )
        self.assertEqual(
            len(packet),
            ICMP6_MESSAGE_LEN__ND_NEIGHBOR_ADVERTISEMENT
            + sum(len(opt) for opt in self._dummy__nd_options),
        )

    def test_icmp6_fpa____str____unreachable_port(self) -> None:
        """
        Test the '__str__()' dunder for 'Unreachable Port' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6PortUnreachableMessageAssembler(
                data=self._dummy__data,
            ),
        )
        self.assertEqual(
            str(packet),
            f"ICMPv6 Unreachable Port, dlen {len(self._dummy__data)}",
        )

    def test_icmp6_fpa____str____echo_request(self) -> None:
        """
        Test the '__str__() dunder for 'Echo Request' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6EchoRequestMessageAssembler(
                id=self._dummy__id,
                seq=self._dummy__seq,
                data=self._dummy__data,
            ),
        )
        self.assertEqual(
            str(packet),
            f"ICMPv6 Echo Request, id {self._dummy__id}, seq {self._dummy__seq}, "
            f"dlen {len(self._dummy__data)}",
        )

    def test_icmp6_fpa____str____echo_reply(self) -> None:
        """
        Test the '__str__()'dunder for 'Echo Reply' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6EchoReplyMessageAssembler(
                id=self._dummy__id,
                seq=self._dummy__seq,
                data=self._dummy__data,
            ),
        )
        self.assertEqual(
            str(packet),
            f"ICMPv6 Echo Reply, id {self._dummy__id}, seq {self._dummy__seq}, "
            f"dlen {len(self._dummy__data)}",
        )

    def test_icmp6_fpa____str____nd_router_solicitation(self) -> None:
        """
        Test the '__str__()' dunder for 'Router Solicitation' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdRouterSolicitationMessageAssembler(
                nd_options=self._dummy__nd_options,
            ),
        )
        self.assertEqual(
            str(packet),
            "ICMPv6 ND Router Solicitation, "
            "slla 11:22:33:44:55:66, "
            "tlla 66:55:44:33:22:11",
        )

    def test_icmp6_fpa____str____nd_router_solicitation__no_options(
        self,
    ) -> None:
        """
        Test the '__str__()' dunder for 'Router Solicitation' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdRouterSolicitationMessageAssembler(
                nd_options=[],
            ),
        )
        self.assertEqual(str(packet), "ICMPv6 133/0 (nd_router_solicitation)")

    def test_icmp6_fpa____str____nd_router_advertisement(self) -> None:
        """
        Test the '__str__()' dunder for the 'Router Advertisement' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdRouterAdvertisementMessageAssembler(
                hop=255,
                flag_m=True,
                flag_o=True,
                router_lifetime=12345,
                reachable_time=12345678,
                retrans_timer=87654321,
                nd_options=[
                    Icmp6NdOptSllaAssembler(
                        slla=MacAddress("11:22:33:44:55:66")
                    ),
                    Icmp6NdOptTllaAssembler(
                        tlla=MacAddress("66:55:44:33:22:11")
                    ),
                ],
            ),
        )
        self.assertEqual(
            str(packet),
            "ICMPv6 134/0 (nd_router_advertisement), hop 255, flags MO, "
            "rlft 12345, reacht 12345678, retrt 87654321, "
            "slla 11:22:33:44:55:66, tlla 66:55:44:33:22:11",
        )

    def test_icmp6_fpa____str____nd_router_advertisement__no_options(
        self,
    ) -> None:
        """
        Test the '__str__ ()' dunder for 'Router Advertisement' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdRouterAdvertisementMessageAssembler(
                hop=self._dummy__hop,
                flag_m=self._dummy__flag_m,
                flag_o=self._dummy__flag_o,
                router_lifetime=self._dummy__router_lifetime,
                reachable_time=self._dummy__reachable_time,
                retrans_timer=self._dummy__retrans_timer,
                nd_options=[],
            ),
        )
        self.assertEqual(
            str(packet),
            "ICMPv6 ND Router Advertisement, hop 255, flags MO, "
            "rlft 12345, reacht 12345678, retrt 87654321",
        )

    def test_icmp6_fpa____str____nd_neighbor_solicitation(self) -> None:
        """
        Test the '__str__()' dunder for 'Neighbor Solicitation' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdNeighborSolicitationMessageAssembler(
                target_address=self._dummy__target_address,
                nd_options=self._dummy__nd_options,
            ),
        )
        self.assertEqual(
            str(packet),
            "ICMPv6 Neighbor Solicitation, target 1:2:3:4:5:6:7:8, "
            "slla 11:22:33:44:55:66, tlla 66:55:44:33:22:11",
        )

    def test_icmp6_fpa____str____nd_neighbor_solicitation__no_options(
        self,
    ) -> None:
        """
        Test the '__str__()' dunder for 'Neighbor Solicitation' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdNeighborSolicitationMessageAssembler(
                target_address=self._dummy__target_address,
                nd_options=[],
            )
        )
        self.assertEqual(
            str(packet),
            "ICMPv6 135/0 (nd_neighbor_solicitation), target 1:2:3:4:5:6:7:8",
        )

    def test_icmp6_fpa____str____nd_neighbor_advertisement(self) -> None:
        """
        Test '__str__()' dunder for 'Neighbor Advertisement' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdNeighborAdvertisementMessageAssembler(
                flag_r=True,
                flag_s=True,
                flag_o=True,
                target_address=Ip6Address("1:2:3:4:5:6:7:8"),
                nd_options=[
                    Icmp6NdOptSllaAssembler(
                        slla=MacAddress("11:22:33:44:55:66")
                    ),
                    Icmp6NdOptTllaAssembler(
                        tlla=MacAddress("66:55:44:33:22:11")
                    ),
                ],
            ),
        )
        self.assertEqual(
            str(packet),
            "ICMPv6 136/0 (nd_neighbor_advertisement), target 1:2:3:4:5:6:7:8, "
            "flags RSO, slla 11:22:33:44:55:66, tlla 66:55:44:33:22:11",
        )

    def test_icmp6_fpa____str____nd_neighbor_advertisement__no_options(
        self,
    ) -> None:
        """
        Test the '__str__()' dunder for 'Neighbor Advertisement' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdNeighborAdvertisementMessageAssembler(
                flag_r=self._dummy__flag_r,
                flag_s=self._dummy__flag_s,
                flag_o=self._dummy__flag_o,
                target_address=self._dummy__target_address,
                nd_options=[],
            ),
        )
        self.assertEqual(
            str(packet),
            "ICMPv6 136/0 (nd_neighbor_advertisement), "
            "target 1:2:3:4:5:6:7:8, flags RSO",
        )

    def test_icmp6_fpa__tracker_getter(self) -> None:
        """
        Test the '_tracker' attribute getter.
        """
        packet = Icmp6Assembler(
            message=Icmp6PortUnreachableMessageAssembler(data=b""),
            echo_tracker=Tracker(prefix="TX"),
        )
        self.assertTrue(
            repr(packet.tracker).startswith("Tracker(serial='<lr>TX")
        )

    def test_icmp6_fpa__asssemble__unreachable_port(self) -> None:
        """
        Test the 'assemble()' method for 'Unreachable Port' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6PortUnreachableMessageAssembler(
                data=b"0123456789ABCDEF"
            )
        )
        frame = memoryview(bytearray(len(packet)))
        packet.assemble(frame, 1234567)
        self.assertEqual(
            bytes(frame), b"\x01\x04Y\x8b\x00\x00\x00\x000123456789ABCDEF"
        )

    def test_icmp6_fpa__assemble__echo_request(self) -> None:
        """
        Test the 'assemble()' method for 'Echo Request' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6EchoRequestMessageAssembler(
                id=12345,
                seq=54321,
                data=b"0123456789ABCDEF",
            ),
        )
        frame = memoryview(bytearray(len(packet)))
        packet.assemble(frame, 12345678)
        self.assertEqual(bytes(frame), b"\x80\x00J\xb309\xd410123456789ABCDEF")

    def test_icmp6_fpa__assemble__echo_reply(self) -> None:
        """
        Test the 'assemble() method for 'Echo Reply' message..
        """
        packet = Icmp6Assembler(
            message=Icmp6EchoReplyMessageAssembler(
                id=12345,
                seq=54321,
                data=b"0123456789ABCDEF",
            ),
        )
        frame = memoryview(bytearray(len(packet)))
        packet.assemble(frame, 12345678)
        self.assertEqual(bytes(frame), b"\x81\x00I\xb309\xd410123456789ABCDEF")

    def test_icmp6_fpa__assemble__nd_router_solicitation(self) -> None:
        """
        Test the 'assemble()' method for 'Router Solicitation' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdRouterSolicitationMessageAssembler(
                nd_options=[
                    Icmp6NdOptSllaAssembler(
                        slla=MacAddress("11:22:33:44:55:66")
                    ),
                    Icmp6NdOptTllaAssembler(
                        tlla=MacAddress("66:55:44:33:22:11")
                    ),
                ],
            ),
        )
        frame = memoryview(bytearray(len(packet)))
        packet.assemble(frame, 12345678)
        self.assertEqual(
            bytes(frame),
            b"\x85\x00\xaf\x8c\x00\x00\x00\x00\x01\x01"
            b'\x11"3DUf\x02\x01fUD3"\x11',
        )

    def test_icmp6_fpa__assemble__nd_router_advertisement(self) -> None:
        """
        Test 'assemble()' method for 'Router Advertisement' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdRouterAdvertisementMessageAssembler(
                hop=255,
                flag_m=True,
                flag_o=True,
                router_lifetime=12345,
                reachable_time=12345678,
                retrans_timer=87654321,
                nd_options=[
                    Icmp6NdOptSllaAssembler(
                        slla=MacAddress("11:22:33:44:55:66")
                    ),
                    Icmp6NdOptTllaAssembler(
                        tlla=MacAddress("66:55:44:33:22:11")
                    ),
                ],
            )
        )
        frame = memoryview(bytearray(len(packet)))
        packet.assemble(frame, 12345678)
        self.assertEqual(
            bytes(frame),
            b"\x86\x00\x97\x9d\xff\xc009\x00\xbcaN\x059\x7f\xb1\x01\x01"
            b'\x11"3DUf\x02\x01fUD3"\x11',
        )

    def test_icmp6_fpa__assemble__nd_neighbor_solicitation(self) -> None:
        """
        Test the 'assemble() method for 'Neighbor Solicitation' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdNeighborSolicitationMessageAssembler(
                target_address=Ip6Address("1:2:3:4:5:6:7:8"),
                nd_options=[
                    Icmp6NdOptSllaAssembler(
                        slla=MacAddress("11:22:33:44:55:66")
                    ),
                    Icmp6NdOptTllaAssembler(
                        tlla=MacAddress("66:55:44:33:22:11")
                    ),
                ],
            ),
        )
        frame = memoryview(bytearray(len(packet)))
        packet.assemble(frame, 12345678)
        self.assertEqual(
            bytes(frame),
            b"\x87\x00\xadh\x00\x00\x00\x00\x00\x01\x00\x02\x00\x03\x00\x04"
            b'\x00\x05\x00\x06\x00\x07\x00\x08\x01\x01\x11"3DUf\x02\x01fUD3"\x11',
        )

    def test_icmp6_fpa__assemble__nd_neighbor_advertisement(self) -> None:
        """
        Test the 'assemble()' method for 'Neighbor Advertisement' message.
        """
        packet = Icmp6Assembler(
            message=Icmp6NdNeighborAdvertisementMessageAssembler(
                flag_r=True,
                flag_s=True,
                flag_o=True,
                target_address=Ip6Address("1:2:3:4:5:6:7:8"),
                nd_options=[
                    Icmp6NdOptSllaAssembler(
                        slla=MacAddress("11:22:33:44:55:66")
                    ),
                    Icmp6NdOptTllaAssembler(
                        tlla=MacAddress("66:55:44:33:22:11")
                    ),
                ],
            ),
        )
        frame = memoryview(bytearray(len(packet)))
        packet.assemble(frame, 12345678)
        self.assertEqual(
            bytes(frame),
            b"\x88\x00\xccg\xe0\x00\x00\x00\x00\x01\x00\x02\x00\x03\x00\x04"
            b"\x00\x05\x00\x06\x00\x07\x00\x08\x01\x01\x11"
            b'"3DUf\x02\x01fUD3"\x11',
        )


class TestIcmp6NdOptSLLA(TestCase):
    """
    ICMPv6 ND SLLA Option unit test class.
    """

    def test_icmp6_fpa_nd_opt_slla____init__(self) -> None:
        """
        Test the option constructor.
        """

        option = Icmp6NdOptSllaAssembler(slla=MacAddress("11:22:33:44:55:66"))
        self.assertEqual(option._slla, MacAddress("11:22:33:44:55:66"))

    def test_icmp6_fpa_nd_opt_slla____str__(self) -> None:
        """
        Test the '__str__()' dunder.
        """

        option = Icmp6NdOptSllaAssembler(slla=MacAddress("11:22:33:44:55:66"))
        self.assertEqual(str(option), "slla 11:22:33:44:55:66")

    def test_icmp6_fpa_nd_opt_slla____repr__(self) -> None:
        """
        Test the '__repr__()' dunder.
        """

        option = Icmp6NdOptSllaAssembler(slla=MacAddress("11:22:33:44:55:66"))
        self.assertEqual(repr(option), f"Icmp6NdOptSLLA({repr(option._slla)})")

    def test_icmp6_fpa_nd_opt_slla____bytes__(self) -> None:
        """
        Test the '__bytes__()' dunder.
        """

        option = Icmp6NdOptSllaAssembler(slla=MacAddress("11:22:33:44:55:66"))
        self.assertEqual(bytes(option), b'\x01\x01\x11"3DUf')

    def test_icmp6_fpa_nd_opt_slla____eq__(self) -> None:
        """
        Test the '__eq__()' dunder.
        """

        option = Icmp6NdOptSllaAssembler(slla=MacAddress("11:22:33:44:55:66"))
        self.assertEqual(
            option,
            Icmp6NdOptSllaAssembler(slla=MacAddress("11:22:33:44:55:66")),
        )


class TestIcmp6NdOptTLLA(TestCase):
    """
    ICMPv6 ND TLLA Option unit test class.
    """

    def test_icmp6_fpa_nd_opt_tlla____init__(self) -> None:
        """
        Test the option constructor.
        """

        option = Icmp6NdOptTllaAssembler(tlla=MacAddress("66:55:44:33:22:11"))
        self.assertEqual(option._tlla, MacAddress("66:55:44:33:22:11"))

    def test_icmp6_fpa_nd_opt_tlla____str__(self) -> None:
        """
        Test the '__str__()' dunder.
        """

        option = Icmp6NdOptTllaAssembler(tlla=MacAddress("66:55:44:33:22:11"))
        self.assertEqual(str(option), "tlla 66:55:44:33:22:11")

    def test_icmp6_fpa_nd_opt_tlla____repr__(self) -> None:
        """
        Test the '__repr__()' dunder.
        """

        option = Icmp6NdOptTllaAssembler(tlla=MacAddress("66:55:44:33:22:11"))
        self.assertEqual(repr(option), f"Icmp6NdOptTLLA({repr(option._tlla)})")

    def test_icmp6_fpa_nd_opt_tlla____bytes__(self) -> None:
        """
        Test the '__bytes__()' dunder.
        """

        option = Icmp6NdOptTllaAssembler(tlla=MacAddress("66:55:44:33:22:11"))
        self.assertEqual(bytes(option), b'\x02\x01fUD3"\x11')

    def test_icmp6_fpa_nd_opt_tlla____eq__(self) -> None:
        """
        Test the '__eq__()' dunder.
        """

        option = Icmp6NdOptTllaAssembler(tlla=MacAddress("66:55:44:33:22:11"))
        self.assertEqual(
            option,
            Icmp6NdOptTllaAssembler(tlla=MacAddress("66:55:44:33:22:11")),
        )


class TestIcmp6NdOptPI(TestCase):
    """
    ICMPv6 ND PI Option unit test class.
    """

    def test_icmp6_fpa_nd_opt_pi____init__(self) -> None:
        """
        Test the option constructor.
        """

        option = Icmp6NdOptPiAssembler(
            valid_lifetime=12345678,
            prefer_lifetime=87654321,
            prefix=Ip6Network("1:2:3:4::/64"),
            flag_l=True,
            flag_a=True,
            flag_r=True,
        )
        self.assertEqual(option._valid_lifetime, 12345678)
        self.assertEqual(option._prefer_lifetime, 87654321)
        self.assertEqual(option._prefix, Ip6Network("1:2:3:4::/64"))
        self.assertEqual(option._flag_l, True)
        self.assertEqual(option._flag_a, True)
        self.assertEqual(option._flag_r, True)

    def test_icmp6_fpa_nd_opt_pi____init____assert_valid_lifetime__under(
        self,
    ) -> None:
        """
        Test assertion for the 'valid_lifetime' argument.
        """
        with self.assertRaises(AssertionError):
            Icmp6NdOptPiAssembler(
                valid_lifetime=-1,
                prefer_lifetime=87654321,
                prefix=Ip6Network("1:2:3:4::/64"),
            )

    def test_icmp6_fpa_nd_opt_pi____init____assert_valid_lifetime__over(
        self,
    ) -> None:
        """
        Test assertion for the 'valid_lifetime' argument.
        """
        with self.assertRaises(AssertionError):
            Icmp6NdOptPiAssembler(
                valid_lifetime=0x100000000,
                prefer_lifetime=87654321,
                prefix=Ip6Network("1:2:3:4::/64"),
            )

    def test_icmp6_fpa_nd_opt_pi____init____assert_prefer_lifetime__under(
        self,
    ) -> None:
        """
        Test assertion for the 'prefer_lifetime' argument.
        """
        with self.assertRaises(AssertionError):
            Icmp6NdOptPiAssembler(
                valid_lifetime=12345678,
                prefer_lifetime=-1,
                prefix=Ip6Network("1:2:3:4::/64"),
            )

    def test_icmp6_fpa_nd_opt_pi____init____assert_prefer_lifetime__over(
        self,
    ) -> None:
        """
        Test assertion for the 'prefer_lifetime' argument.
        """
        with self.assertRaises(AssertionError):
            Icmp6NdOptPiAssembler(
                valid_lifetime=12345678,
                prefer_lifetime=0x100000000,
                prefix=Ip6Network("1:2:3:4::/64"),
            )

    def test_icmp6_fpa_nd_opt_pi____str__(self) -> None:
        """
        Test the '__str__()' dunder.
        """
        option = Icmp6NdOptPiAssembler(
            valid_lifetime=12345678,
            prefer_lifetime=87654321,
            prefix=Ip6Network("1:2:3:4::/64"),
            flag_l=True,
            flag_a=True,
            flag_r=True,
        )
        self.assertEqual(
            str(option),
            "prefix_info 1:2:3:4::/64, valid 12345678, prefer 87654321, "
            "flags LAR",
        )

    def test_icmp6_fpa_nd_opt_pi____repr__(self) -> None:
        """
        Test the '__repr__()' dunder.
        """
        option = Icmp6NdOptPiAssembler(
            valid_lifetime=12345678,
            prefer_lifetime=87654321,
            prefix=Ip6Network("1:2:3:4::/64"),
            flag_l=True,
            flag_a=True,
            flag_r=True,
        )
        self.assertEqual(
            repr(option),
            "Icmp6NdOptIP(valid_lifetime=12345678, prefer_lifetime=87654321, "
            "prefix=Ip6Network('1:2:3:4::/64'), flag_l=True, flag_s=True, "
            "flag_r=True)",
        )

    def test_icmp6_fpa_nd_opt_pi____bytes__(self) -> None:
        """
        Test the '__bytes__() dunder.
        """
        option = Icmp6NdOptPiAssembler(
            valid_lifetime=12345678,
            prefer_lifetime=87654321,
            prefix=Ip6Network("1:2:3:4::/64"),
            flag_l=True,
            flag_a=True,
            flag_r=True,
        )
        self.assertEqual(
            bytes(option),
            b"\x03\x04@\xc0\x00\xbcaN\x059\x7f\xb1\x00\x00\x00\x00\x00\x01\x00"
            b"\x02\x00\x03\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00",
        )

    def test_icmp6_fpa_nd_opt_pi____eq__(self) -> None:
        """
        Test the '__eq__()' dunder.
        """
        option = Icmp6NdOptPiAssembler(
            valid_lifetime=12345678,
            prefer_lifetime=87654321,
            prefix=Ip6Network("1:2:3:4::/64"),
            flag_l=True,
            flag_a=True,
            flag_r=True,
        )
        self.assertEqual(
            option,
            Icmp6NdOptPiAssembler(
                valid_lifetime=12345678,
                prefer_lifetime=87654321,
                prefix=Ip6Network("1:2:3:4::/64"),
                flag_l=True,
                flag_a=True,
                flag_r=True,
            ),
        )
