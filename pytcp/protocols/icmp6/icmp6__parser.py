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
This module contains the ICMPv6 packet parser.

pytcp/protocols/icmp6/icmp6__parser.py

ver 3.0.0
"""


from __future__ import annotations

from typing import TYPE_CHECKING, override

from pytcp.lib.inet_cksum import inet_cksum
from pytcp.lib.ip6_address import Ip6Address
from pytcp.lib.proto_parser import ProtoParser
from pytcp.protocols.icmp6.icmp6__base import Icmp6
from pytcp.protocols.icmp6.icmp6__errors import (
    Icmp6IntegrityError,
    Icmp6SanityError,
)
from pytcp.protocols.icmp6.message.icmp6_message import (
    ICMP6__HEADER__LEN,
    Icmp6Type,
)
from pytcp.protocols.icmp6.message.icmp6_message__destination_unreachable import (
    ICMP6__DESTINATION_UNREACHABLE__LEN,
    Icmp6DestinationUnreachableMessage,
)
from pytcp.protocols.icmp6.message.icmp6_message__echo_reply import (
    ICMP6__ECHO_REPLY__LEN,
    Icmp6EchoReplyMessage,
)
from pytcp.protocols.icmp6.message.icmp6_message__echo_request import (
    ICMP6__ECHO_REQUEST__LEN,
    Icmp6EchoRequestMessage,
)
from pytcp.protocols.icmp6.message.icmp6_message__unknown import (
    Icmp6UnknownMessage,
)
from pytcp.protocols.icmp6.message.mld2.icmp6_mld2__multicast_address_record import (
    ICMP6__MLD2__MULTICAST_ADDRESS_RECORD__LEN,
)
from pytcp.protocols.icmp6.message.mld2.icmp6_mld2_message__report import (
    ICMP6__MLD2__REPORT__LEN,
    Icmp6Mld2ReportMessage,
)
from pytcp.protocols.icmp6.message.nd.icmp6_nd_message__neighbor_advertisement import (
    ICMP6__ND__NEIGHBOR_ADVERTISEMENT__LEN,
    Icmp6NdNeighborAdvertisementMessage,
)
from pytcp.protocols.icmp6.message.nd.icmp6_nd_message__neighbor_solicitation import (
    ICMP6__ND__NEIGHBOR_SOLICITATION__LEN,
    Icmp6NdNeighborSolicitationMessage,
)
from pytcp.protocols.icmp6.message.nd.icmp6_nd_message__router_advertisement import (
    ICMP6__ND__ROUTER_ADVERTISEMENT__LEN,
    Icmp6NdRouterAdvertisementMessage,
)
from pytcp.protocols.icmp6.message.nd.icmp6_nd_message__router_solicitation import (
    ICMP6__ND__ROUTER_SOLICITATION__LEN,
    Icmp6NdRouterSolicitationMessage,
)

if TYPE_CHECKING:
    from pytcp.lib.packet import PacketRx


class Icmp6Parser(Icmp6, ProtoParser):
    """
    The ICMPv6 packet parser.
    """

    def __init__(self, *, packet_rx: PacketRx) -> None:
        """
        Initialize the ICMPv6 packet parser.
        """

        self._frame = packet_rx.frame
        self._ip6__dlen = packet_rx.ip6.dlen
        self._ip6__pshdr_sum = packet_rx.ip6.pshdr_sum
        self._ip6__src = packet_rx.ip6.src
        self._ip6__dst = packet_rx.ip6.dst
        self._ip6__hop = packet_rx.ip6.hop

        self._validate_integrity()
        self._parse()
        self._validate_sanity()

        packet_rx.icmp6 = self
        packet_rx.frame = packet_rx.frame[len(self._frame) :]

    def _nd_option_integrity_check(self, offset: int) -> None:
        """
        Check integrity of the ICMPv6 ND options.
        """

        while offset < len(self._frame):
            if offset + 1 > len(self._frame):
                raise Icmp6IntegrityError(
                    "Wrong ND option length (I).",
                )
            if self._frame[offset + 1] == 0:
                raise Icmp6IntegrityError(
                    "Wrong ND option length (II).",
                )
            offset += self._frame[offset + 1] << 3
            if offset > len(self._frame):
                raise Icmp6IntegrityError(
                    "Wrong ND option length (III).",
                )

    @override
    def _validate_integrity(self) -> None:
        """
        Validate integrity of the ICMPv6 packet before parsing it.
        """

        if inet_cksum(self._frame[: self._ip6__dlen], self._ip6__pshdr_sum):
            raise Icmp6IntegrityError(
                "Wrong packet checksum.",
            )

        if not ICMP6__HEADER__LEN <= self._ip6__dlen <= len(self._frame):
            raise Icmp6IntegrityError(
                "Wrong packet length (I).",
            )

        match self._frame[0]:
            case Icmp6Type.DESTINATION_UNREACHABLE:
                if (
                    not ICMP6__DESTINATION_UNREACHABLE__LEN
                    <= self._ip6__dlen
                    <= len(self._frame)
                ):
                    raise Icmp6IntegrityError(
                        "Wrong packet length (II).",
                    )

            case Icmp6Type.ECHO_REQUEST:
                if (
                    not ICMP6__ECHO_REQUEST__LEN
                    <= self._ip6__dlen
                    <= len(self._frame)
                ):
                    raise Icmp6IntegrityError(
                        "Wrong packet length (II).",
                    )

            case Icmp6Type.ECHO_REPLY:
                if (
                    not ICMP6__ECHO_REPLY__LEN
                    <= self._ip6__dlen
                    <= len(self._frame)
                ):
                    raise Icmp6IntegrityError(
                        "Wrong packet length (II).",
                    )

            case Icmp6Type.ND__ROUTER_SOLICITATION:
                if (
                    not ICMP6__ND__ROUTER_SOLICITATION__LEN
                    <= self._ip6__dlen
                    <= len(self._frame)
                ):
                    raise Icmp6IntegrityError(
                        "Wrong packet length (II).",
                    )
                self._nd_option_integrity_check(
                    ICMP6__HEADER__LEN + ICMP6__ND__ROUTER_SOLICITATION__LEN
                )

            case Icmp6Type.ND__ROUTER_ADVERTISEMENT:
                if (
                    not ICMP6__ND__ROUTER_ADVERTISEMENT__LEN
                    <= self._ip6__dlen
                    <= len(self._frame)
                ):
                    raise Icmp6IntegrityError(
                        "Wrong packet length (II).",
                    )
                self._nd_option_integrity_check(
                    ICMP6__ND__ROUTER_ADVERTISEMENT__LEN
                )

            case Icmp6Type.ND__NEIGHBOR_SOLICITATION:
                if (
                    not ICMP6__ND__NEIGHBOR_SOLICITATION__LEN
                    <= self._ip6__dlen
                    <= len(self._frame)
                ):
                    raise Icmp6IntegrityError(
                        "Wrong packet length (II).",
                    )
                self._nd_option_integrity_check(
                    ICMP6__ND__ROUTER_SOLICITATION__LEN
                )

            case Icmp6Type.ND__NEIGHBOR_ADVERTISEMENT:
                if (
                    not ICMP6__ND__NEIGHBOR_ADVERTISEMENT__LEN
                    <= self._ip6__dlen
                    <= len(self._frame)
                ):
                    raise Icmp6IntegrityError(
                        "Wrong packet length (II).",
                    )
                self._nd_option_integrity_check(
                    ICMP6__ND__ROUTER_ADVERTISEMENT__LEN
                )

            case Icmp6Type.MLD2__REPORT:
                if (
                    not ICMP6__MLD2__REPORT__LEN
                    <= self._ip6__dlen
                    <= len(self._frame)
                ):
                    raise Icmp6IntegrityError(
                        "Wrong packet length (II).",
                    )
                offset = ICMP6__MLD2__REPORT__LEN
                for _ in range(int.from_bytes(self._frame[6:8])):
                    if (
                        offset + ICMP6__MLD2__MULTICAST_ADDRESS_RECORD__LEN
                        > self._ip6__dlen
                    ):
                        raise Icmp6IntegrityError(
                            "Wrong packet length (III).",
                        )
                    offset += (
                        ICMP6__MLD2__MULTICAST_ADDRESS_RECORD__LEN
                        + self._frame[offset + 1]
                        + int.from_bytes(self._frame, offset + 2) * 16
                    )
                if offset != self._ip6__dlen:
                    raise Icmp6IntegrityError(
                        "Wrong packet length (IV).",
                    )

    @override
    def _parse(self) -> None:
        """
        Parse the ICMPv6 packet.
        """

        match Icmp6Type.from_bytes(self._frame[0:1]):
            case Icmp6Type.DESTINATION_UNREACHABLE:
                self._message = Icmp6DestinationUnreachableMessage.from_bytes(
                    self._frame,
                )

            case Icmp6Type.ECHO_REQUEST:
                self._message = Icmp6EchoRequestMessage.from_bytes(
                    self._frame,
                )

            case Icmp6Type.ECHO_REPLY:
                self._message = Icmp6EchoReplyMessage.from_bytes(
                    self._frame,
                )

            case Icmp6Type.ND__ROUTER_SOLICITATION:
                self._message = Icmp6NdRouterSolicitationMessage.from_bytes(
                    self._frame,
                )

            case Icmp6Type.ND__ROUTER_ADVERTISEMENT:
                self._message = Icmp6NdRouterAdvertisementMessage.from_bytes(
                    self._frame,
                )

            case Icmp6Type.ND__NEIGHBOR_SOLICITATION:
                self._message = Icmp6NdNeighborSolicitationMessage.from_bytes(
                    self._frame,
                )

            case Icmp6Type.ND__NEIGHBOR_ADVERTISEMENT:
                self._message = Icmp6NdNeighborAdvertisementMessage.from_bytes(
                    self._frame,
                )

            case _:
                self._message = Icmp6UnknownMessage.from_bytes(
                    self._frame,
                )

    @override
    def _validate_sanity(self) -> None:
        """
        Validate sanity of the ICMPv6 packet after parsing it.
        """

        if isinstance(self._message, Icmp6DestinationUnreachableMessage):
            return

        if isinstance(self._message, Icmp6EchoRequestMessage):
            return

        if isinstance(self._message, Icmp6EchoReplyMessage):
            return

        if isinstance(self._message, Icmp6NdRouterSolicitationMessage):
            if not self._ip6__hop == 255:
                raise Icmp6SanityError(
                    "The 'hop' field must be '255'. [RFC 4861]",
                )
            if not (self._ip6__src.is_unicast or self._ip6__src.is_unspecified):
                raise Icmp6SanityError(
                    "The 'src' address must be unicast or unspecified. [RFC 4861]",
                )
            if not self._ip6__dst == Ip6Address("ff02::2"):
                raise Icmp6SanityError(
                    "The 'dst' must be all-routers. [RFC 4861]",
                )
            if self._ip6__src.is_unspecified and self._message.option_slla:
                raise Icmp6SanityError(
                    "The 'nd_opt_slla' field must not be included if "
                    "the 'src' address is unspecified. [RFC 4861]",
                )

            # TODO: Enforce proper option presence.

        if isinstance(self._message, Icmp6NdRouterAdvertisementMessage):
            if not self._ip6__hop == 255:
                raise Icmp6SanityError(
                    "The 'hop' field must be '255'. [RFC 4861]",
                )
            if not self._ip6__src.is_link_local:
                raise Icmp6SanityError(
                    "The 'src' address must be link local. [RFC 4861]",
                )
            if not (
                self._ip6__dst.is_unicast
                or self._ip6__dst == Ip6Address("ff02::1")
            ):
                raise Icmp6SanityError(
                    "The 'dst' address must be unicast or all-nodes. [RFC 4861]",
                )

            # TODO: Enforce proper option presence.

        if isinstance(self._message, Icmp6NdNeighborSolicitationMessage):
            if not self._ip6__hop == 255:
                raise Icmp6SanityError(
                    "The 'hop' field must be '255'. [RFC 4861]",
                )
            if not (self._ip6__src.is_unicast or self._ip6__src.is_unspecified):
                raise Icmp6SanityError(
                    "The 'src' address must be unicast or unspecified. [RFC 4861]",
                )
            if self._ip6__dst not in {
                self._message.target_address,
                self._message.target_address.solicited_node_multicast,
            }:
                raise Icmp6SanityError(
                    "The 'dst' address must be 'ns_target_address' address or it's "
                    "solicited-node multicast address. [RFC 4861]",
                )
            if not self._message.target_address.is_unicast:
                raise Icmp6SanityError(
                    "The 'ns_target_address' address must be unicast. [RFC 4861]",
                )
            if (
                self._ip6__src.is_unspecified
                and self._message.option_slla is not None
            ):
                raise Icmp6SanityError(
                    "The 'nd_opt_slla' address must not be included if "
                    "the 'src' is unspecified. [RFC 4861]",
                )

            # TODO: Enforce proper option presence.

        if isinstance(self._message, Icmp6NdNeighborAdvertisementMessage):
            if not self._ip6__hop == 255:
                raise Icmp6SanityError(
                    "The 'hop' field must be '255'. [RFC 4861]",
                )
            if not self._ip6__src.is_unicast:
                raise Icmp6SanityError(
                    "The 'src' address must be unicast. [RFC 4861]",
                )
            if self._message.flag_s is True and not (
                self._ip6__dst.is_unicast
                or self._ip6__dst == Ip6Address("ff02::1")
            ):
                raise Icmp6SanityError(
                    "If 'na_flag_s' flag is set then 'dst' address must be "
                    "either unicast or all-nodes. [RFC 4861]",
                )
            if (
                self._message.flag_s is False
                and not self._ip6__dst == Ip6Address("ff02::1")
            ):
                raise Icmp6SanityError(
                    "If 'na_flag_s' flag is not set then 'dst' address must "
                    "be all-nodes address. [RFC 4861]",
                )

            # TODO: Enforce proper option presence.

        if isinstance(self._message, Icmp6Mld2ReportMessage):
            if not self._ip6__hop == 1:
                raise Icmp6SanityError(
                    "The 'hop' field must be set to '1'. [RFC 3810]",
                )
