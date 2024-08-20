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
This module contains the IPv4 packet header class.

pytcp/protocols/ip4/ip4__header.py

ver 3.0.0
"""


from __future__ import annotations

import struct
from abc import ABC
from dataclasses import dataclass
from typing import override

from pytcp.lib.int_checks import (
    UINT_16__MAX,
    is_8_byte_alligned,
    is_uint2,
    is_uint6,
    is_uint8,
    is_uint13,
    is_uint16,
)
from pytcp.lib.ip4_address import Ip4Address
from pytcp.lib.proto_struct import ProtoStruct
from pytcp.protocols.ip4.ip4__enums import Ip4Proto

# The IPv4 packet header [RFC 791].

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |Version|  IHL  |   DSCP    |ECN|          Packet length        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |         Identification        | |D|M|      Fragment offset    |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |  Time to live |    Protocol   |         Header checksum       |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                       Source address                          |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |                    Destination address                        |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# ~                                                               ~
# ~                            Options                            ~
# ~                                                               ~
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

IP4__HEADER__LEN = 20
IP4__HEADER__STRUCT = "! BBH HH BBH L L"
IP4__PAYLOAD__MAX_LEN = UINT_16__MAX - IP4__HEADER__LEN


@dataclass(frozen=True, kw_only=True)
class Ip4Header(ProtoStruct):
    """
    The IPv4 packet header.
    """

    ver: int = 4
    hlen: int
    dscp: int
    ecn: int
    plen: int
    id: int
    flag_df: bool
    flag_mf: bool
    offset: int
    ttl: int
    proto: Ip4Proto
    cksum: int
    src: Ip4Address
    dst: Ip4Address

    @override
    def __post_init__(self) -> None:
        """
        Ensure integrity of the Ip4 header fields.
        """

        assert self.ver == 4, f"The 'ver' field must be 4. Got: {self.ver!r}"

        assert (
            is_uint6(self.hlen) and self.hlen >= IP4__HEADER__LEN
        ), f"The 'hlen' field must be a 4-bit unsigned integer greater than or equal to 20. Got: {self.hlen!r}"

        assert is_uint6(
            self.dscp
        ), f"The 'dscp' field must be a 6-bit unsigned integer. Got: {self.dscp!r}"

        assert is_uint2(
            self.ecn
        ), f"The 'ecn' field must be a 2-bit unsigned integer. Got: {self.ecn!r}"

        assert (
            is_uint16(self.plen) and self.plen >= IP4__HEADER__LEN
        ), f"The 'plen' field must be a 16-bit unsigned integer greater than or equal to 20. Got: {self.plen!r}"

        assert is_uint16(
            self.id
        ), f"The 'id' field must be a 16-bit unsigned integer. Got: {self.id!r}"

        assert isinstance(
            self.flag_df, bool
        ), f"The 'flag_df' field must be a boolean. Got: {type(self.flag_df)!r}"

        assert isinstance(
            self.flag_mf, bool
        ), f"The 'flag_mf' field must be a boolean. Got: {type(self.flag_mf)!r}"

        assert is_uint13(
            self.offset
        ), f"The 'offset' field must be a 13-bit unsigned integer. Got: {self.offset!r}"

        assert is_8_byte_alligned(
            self.offset
        ), f"The 'offset' field must be 8-byte aligned. Got: {self.offset!r}"

        assert is_uint8(
            self.ttl
        ), f"The 'ttl' field must be an 8-bit unsigned integer. Got: {self.ttl!r}"

        assert isinstance(
            self.proto, Ip4Proto
        ), f"The 'proto' field must be an Ip4Proto. Got: {type(self.proto)!r}"

        assert is_uint16(
            self.cksum
        ), f"The 'cksum' field must be a 16-bit unsigned integer. Got: {self.cksum!r}"

        assert isinstance(
            self.src, Ip4Address
        ), f"The 'src' field must be an Ip4Address. Got: {type(self.src)!r}"

        assert isinstance(
            self.dst, Ip4Address
        ), f"The 'dst' field must be an Ip4Address. Got: {type(self.dst)!r}"

    @override
    def __len__(self) -> int:
        """
        Get the IPv4 header length.
        """

        return IP4__HEADER__LEN

    @override
    def __bytes__(self) -> bytes:
        """
        Get the IPv4 header as bytes.
        """

        return struct.pack(
            IP4__HEADER__STRUCT,
            self.ver << 4 | self.hlen >> 2,
            self.dscp << 2 | self.ecn,
            self.plen,
            self.id,
            self.flag_df << 14 | self.flag_mf << 13 | self.offset >> 3,
            self.ttl,
            int(self.proto),
            0,
            int(self.src),
            int(self.dst),
        )

    @override
    @staticmethod
    def from_bytes(_bytes: bytes) -> Ip4Header:
        """
        Initialize the IPv4 header from bytes.
        """

        (
            ver__hlen,
            dscp__ecn,
            plen,
            id,
            flag__offset,
            ttl,
            proto,
            cksum,
            src,
            dst,
        ) = struct.unpack(IP4__HEADER__STRUCT, _bytes[:IP4__HEADER__LEN])

        return Ip4Header(
            ver=ver__hlen >> 4,
            hlen=(ver__hlen & 0b00001111) << 2,
            dscp=dscp__ecn >> 2,
            ecn=dscp__ecn & 0b00000011,
            plen=plen,
            id=id,
            flag_df=bool(flag__offset >> 8 & 0b01000000),
            flag_mf=bool(flag__offset >> 8 & 0b00100000),
            offset=(flag__offset & 0b0001111111111111) << 3,
            ttl=ttl,
            proto=Ip4Proto.from_int(proto),
            cksum=cksum,
            src=Ip4Address(src),
            dst=Ip4Address(dst),
        )


class Ip4HeaderProperties(ABC):
    """
    Properties used to access the IPv4 header fields.
    """

    _header: Ip4Header

    @property
    def ver(self) -> int:
        """
        Get the IPv4 header 'ver' field.
        """

        return self._header.ver

    @property
    def hlen(self) -> int:
        """
        Get the IPv4 header 'hlen' field.
        """

        return self._header.hlen

    @property
    def dscp(self) -> int:
        """
        Get the IPv4 header 'dscp' field.
        """

        return self._header.dscp

    @property
    def ecn(self) -> int:
        """
        Get the IPv4 header 'ecn' field.
        """

        return self._header.ecn

    @property
    def plen(self) -> int:
        """
        Get the IPv4 header 'plen' field.
        """

        return self._header.plen

    @property
    def id(self) -> int:
        """
        Get the IPv4 header 'id' field.
        """

        return self._header.id

    @property
    def flag_df(self) -> bool:
        """
        Get the IPv4 header 'flag_df' field.
        """

        return self._header.flag_df

    @property
    def flag_mf(self) -> bool:
        """
        Get the IPv4 header 'flag_mf' field.
        """

        return self._header.flag_mf

    @property
    def offset(self) -> int:
        """
        Get the IPv4 header 'offset' field.
        """

        return self._header.offset

    @property
    def ttl(self) -> int:
        """
        Get the IPv4 header 'ttl' field.
        """

        return self._header.ttl

    @property
    def proto(self) -> Ip4Proto:
        """
        Get the IPv4 header 'proto' field.
        """

        return self._header.proto

    @property
    def cksum(self) -> int:
        """
        Get the IPv4 header 'cksum' field.
        """

        return self._header.cksum

    @property
    def src(self) -> Ip4Address:
        """
        Get the IPv4 header 'src' field.
        """

        return self._header.src

    @property
    def dst(self) -> Ip4Address:
        """
        Get the IPv4 header 'dst' field.
        """

        return self._header.dst
