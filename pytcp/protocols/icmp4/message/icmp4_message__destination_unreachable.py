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
Module contains the ICMPv4 Destination Unreachable message support class.

pytcp/protocols/icmp4/message/icmp4_message__destination_unreachable.py

ver 3.0.2
"""


from __future__ import annotations

import struct
from dataclasses import dataclass, field
from typing import override

from pytcp.lib.int_checks import is_uint16
from pytcp.protocols.defaults import IP4__MIN_MTU
from pytcp.protocols.icmp4.icmp4__errors import Icmp4IntegrityError
from pytcp.protocols.icmp4.message.icmp4_message import (
    Icmp4Code,
    Icmp4Message,
    Icmp4Type,
)
from pytcp.protocols.ip4.ip4__header import (
    IP4__HEADER__LEN,
    IP4__PAYLOAD__MAX_LEN,
)

# The ICMPv4 Destination Unreachable message (3/[0-3, 5-15]) [RFC 792].

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |     Type      |     Code      |           Checksum            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                           Reserved                            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# ~                             Data                              ~
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


# The ICMPv4 Destination Unreachable message (3/4)
# (Fragmentation Needed and DF Set) [RFC 1191].

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |     Type      |     Code      |           Checksum            |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |           Reserved            |          Link MTU / 0         |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# ~                             Data                              ~
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


ICMP4__DESTINATION_UNREACHABLE__LEN = 8
ICMP4__DESTINATION_UNREACHABLE__STRUCT = "! BBH L"
ICMP4__DESTINATION_UNREACHABLE__FRAGMENTATION_NEEDED__STRUCT = "! BBH HH"


class Icmp4DestinationUnreachableCode(Icmp4Code):
    """
    The ICMPv4 Destination Unreachable 'code' field values.
    """

    NETWORK = 0
    HOST = 1
    PROTOCOL = 2
    PORT = 3
    FRAGMENTATION_NEEDED = 4
    SOURCE_ROUTE_FAILED = 5
    NETWORK_UNKNOWN = 6
    HOST_UNKNOWN = 7
    SOURCE_HOST_ISOLATED = 8
    NETWORK_PROHIBITED = 9
    HOST_PROHIBITED = 10
    NETWORK_TOS = 11
    HOST_TOS = 12
    COMMUNICATION_PROHIBITED = 13
    HOST_PRECEDENCE = 14
    PRECEDENCE_CUTOFF = 15

    @override
    def __str__(self) -> str:
        """
        Get the value as a string.
        """

        match self:
            case Icmp4DestinationUnreachableCode.NETWORK_TOS:
                return "Network TOS"
            case Icmp4DestinationUnreachableCode.HOST_TOS:
                return "Host TOS"
            case _:
                return super().__str__()


@dataclass(frozen=True, kw_only=True)
class Icmp4DestinationUnreachableMessage(Icmp4Message):
    """
    The ICMPv4 Destination Unreachable message support.
    """

    type: Icmp4Type = field(
        repr=False,
        init=False,
        default=Icmp4Type.DESTINATION_UNREACHABLE,
    )
    code: Icmp4DestinationUnreachableCode
    cksum: int = 0

    mtu: int | None = None
    data: bytes = bytes()

    @override
    def __post_init__(self) -> None:
        """
        Validate the ICMPv4 Destination Unreachable message fields.
        """

        assert isinstance(self.code, Icmp4DestinationUnreachableCode), (
            f"The 'code' field must be an Icmp4DestinationUnreachableCode. "
            f"Got: {type(self.code)!r}"
        )

        if self.code == Icmp4DestinationUnreachableCode.FRAGMENTATION_NEEDED:
            assert self.mtu is not None and is_uint16(self.mtu), (
                f"The 'mtu' field must be a 16-bit unsigned integer. "
                f"Got: {self.mtu}"
            )

        if self.code != Icmp4DestinationUnreachableCode.FRAGMENTATION_NEEDED:
            assert (
                self.mtu is None
            ), f"The 'mtu' field must not be set. Got: {self.mtu}"

        assert is_uint16(self.cksum), (
            f"The 'cksum' field must be a 16-bit unsigned integer. "
            f"Got: {self.cksum}"
        )

        assert (
            len(self.data)
            <= IP4__PAYLOAD__MAX_LEN - ICMP4__DESTINATION_UNREACHABLE__LEN
        ), (
            "The 'data' field length must be a 16-bit unsigned integer less than or "
            f"equal to {IP4__PAYLOAD__MAX_LEN - ICMP4__DESTINATION_UNREACHABLE__LEN}. "
            f"Got: {len(self.data)}"
        )

        # Hack to bypass the 'frozen=True' dataclass decorator.
        object.__setattr__(
            self,
            "data",
            self.data[
                : IP4__MIN_MTU
                - IP4__HEADER__LEN
                - ICMP4__DESTINATION_UNREACHABLE__LEN
            ],
        )

    @override
    def __len__(self) -> int:
        """
        Get the ICMPv4 Destination Unreachable message length.
        """

        return ICMP4__DESTINATION_UNREACHABLE__LEN + len(self.data)

    @override
    def __str__(self) -> str:
        """
        Get the ICMPv4 Destination Unreachable message log string.
        """

        return (
            f"ICMPv4 Destination Unreachable - {self.code}, "
            f"{(
                f'mtu {self.mtu}, '
                if self.code
                == Icmp4DestinationUnreachableCode.FRAGMENTATION_NEEDED
                else ''
            )}"
            f"len {len(self)} "
            f"({ICMP4__DESTINATION_UNREACHABLE__LEN}+{len(self.data)})"
        )

    @override
    def __bytes__(self) -> bytes:
        """
        Get the ICMPv4 Destination Unreachable message as bytes.
        """

        match self.code:
            case Icmp4DestinationUnreachableCode.FRAGMENTATION_NEEDED:
                return struct.pack(
                    ICMP4__DESTINATION_UNREACHABLE__FRAGMENTATION_NEEDED__STRUCT,
                    int(self.type),
                    int(self.code),
                    0,
                    0,
                    self.mtu,
                ) + bytes(self.data)
            case _:
                return struct.pack(
                    ICMP4__DESTINATION_UNREACHABLE__STRUCT,
                    int(self.type),
                    int(self.code),
                    0,
                    0,
                ) + bytes(self.data)

    @override
    def validate_sanity(self) -> None:
        """
        Validate the ICMPv4 Destination Unreachable message sanity after
        parsing it.
        """

        # Currently no sanity checks are implemented.

    @override
    @staticmethod
    def validate_integrity(*, frame: bytes, ip4__payload_len: int) -> None:
        """
        Validate the ICMPv4 Destination Unreachable message integrity before parsing it.
        """

        if not (
            ICMP4__DESTINATION_UNREACHABLE__LEN
            <= ip4__payload_len
            <= len(frame)
        ):
            raise Icmp4IntegrityError(
                "The condition 'ICMP4__DESTINATION_UNREACHABLE__LEN <= "
                "ip4__payload_len <= len(frame)' must be met. Got: "
                f"{ICMP4__DESTINATION_UNREACHABLE__LEN=}, "
                f"{ip4__payload_len=}, {len(frame)=}"
            )

    @override
    @staticmethod
    def from_bytes(_bytes: bytes, /) -> Icmp4DestinationUnreachableMessage:
        """
        Initialize the ICMPv4 Destination Unreachable message from bytes.
        """

        match Icmp4DestinationUnreachableCode.from_int(_bytes[1]):
            case Icmp4DestinationUnreachableCode.FRAGMENTATION_NEEDED:
                type, code, cksum, _, mtu = struct.unpack(
                    ICMP4__DESTINATION_UNREACHABLE__FRAGMENTATION_NEEDED__STRUCT,
                    _bytes[:ICMP4__DESTINATION_UNREACHABLE__LEN],
                )
            case _:
                type, code, cksum, _ = struct.unpack(
                    ICMP4__DESTINATION_UNREACHABLE__STRUCT,
                    _bytes[:ICMP4__DESTINATION_UNREACHABLE__LEN],
                )
                mtu = None

        assert (received_type := Icmp4Type.from_int(type)) == (
            valid_type := Icmp4Type.DESTINATION_UNREACHABLE
        ), f"The 'type' field must be {valid_type!r}. Got: {received_type!r}"

        return Icmp4DestinationUnreachableMessage(
            code=Icmp4DestinationUnreachableCode.from_int(code),
            cksum=cksum,
            mtu=mtu,
            data=_bytes[ICMP4__DESTINATION_UNREACHABLE__LEN:],
        )
