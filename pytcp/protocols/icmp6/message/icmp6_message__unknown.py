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
This module contains the unknown ICMPv6 message support class.

pytcp/protocols/icmp6/message/icmp6_message__unknown.py

ver 3.0.0
"""


from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import override

from pytcp.lib.int_checks import is_uint16
from pytcp.protocols.icmp6.message.icmp6_message import (
    ICMP6__HEADER__LEN,
    ICMP6__HEADER__STRUCT,
    Icmp6Code,
    Icmp6Message,
    Icmp6Type,
)


@dataclass(frozen=True, kw_only=True)
class Icmp6UnknownMessage(Icmp6Message):
    """
    The ICMPv6 unknown message support.
    """

    type: Icmp6Type
    code: Icmp6Code
    cksum: int

    @override
    def __post_init__(self) -> None:
        """
        Validate the ICMPv6 unknown message fields.
        """

        assert isinstance(
            self.type, Icmp6Type
        ), f"The 'type' field must be an Icmp4Type. Got: {type(self.type)!r}"

        assert isinstance(
            self.code, Icmp6Code
        ), f"The 'code' field must be an Icmp4Code. Got: {type(self.code)!r}"

        assert is_uint16(
            self.cksum
        ), f"The 'cksum' field must be a 16-bit unsigned integer. Got: {self.cksum!r}"

    @override
    def __len__(self) -> int:
        """
        Get the ICMPv6 unknown message length.
        """

        raise NotImplementedError

    @override
    def __str__(self) -> str:
        """
        Get the ICMPv6 unknown message log string.
        """

        return f"ICMPv6 Unknown Message, type {int(self.type)}, code {int(self.code)}"

    @override
    def __bytes__(self) -> bytes:
        """
        Get the ICMPv6 unknown message as bytes.
        """

        raise NotImplementedError

    @staticmethod
    def from_bytes(_bytes: bytes) -> Icmp6UnknownMessage:
        """
        Initialize the ICMPv6 unknown message from bytes.
        """

        _type, code, cksum = struct.unpack(
            ICMP6__HEADER__STRUCT, _bytes[:ICMP6__HEADER__LEN]
        )

        return Icmp6UnknownMessage(
            type=Icmp6Type.from_int(_type),
            code=Icmp6Code.from_int(code),
            cksum=cksum,
        )
