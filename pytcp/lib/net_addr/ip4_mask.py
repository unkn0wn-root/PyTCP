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
Module contains IPv4 mask support class.

pytcp/lib/net_addr/ip4_mask.py

ver 3.0.2
"""


from __future__ import annotations

import re
import socket
from typing import override

from .errors import Ip4MaskFormatError
from .ip4_address import IP4__ADDRESS_LEN, IP4__REGEX
from .ip_mask import IpMask


class Ip4Mask(IpMask):
    """
    IPv4 mask support class.
    """

    _version: int = 4

    def __init__(
        self,
        /,
        mask: (
            Ip4Mask | str | bytes | bytearray | memoryview | int | None
        ) = None,
    ) -> None:
        """
        Create a new IPv4 mask object.
        """

        if mask is None:
            self._mask = 0
            return

        if isinstance(mask, int):
            if mask & 0xFF_FF_FF_FF == mask:
                self._mask = mask
                if self._validate_bits(IP4__ADDRESS_LEN * 8):
                    return

        if isinstance(mask, (memoryview, bytes, bytearray)):
            if len(mask) == 4:
                self._mask = int.from_bytes(mask)
                if self._validate_bits(IP4__ADDRESS_LEN * 8):
                    return

        if isinstance(mask, str) and re.search(r"^\/\d{1,2}$", mask):
            bit_count = int(mask[1:])
            if bit_count in range(33):
                self._mask = int("1" * bit_count + "0" * (32 - bit_count), 2)
                return

        if isinstance(mask, str) and re.search(IP4__REGEX, mask):
            try:
                self._mask = int.from_bytes(socket.inet_aton(mask))
                if self._validate_bits(IP4__ADDRESS_LEN * 8):
                    return
            except OSError:
                pass

        if isinstance(mask, Ip4Mask):
            self._mask = mask._mask
            return

        raise Ip4MaskFormatError(mask)

    @override
    def __repr__(self) -> str:
        """
        Get the IPv4 mask string representation.
        """

        return f"{self.__class__.__name__}('{socket.inet_ntoa(bytes(self))}')"

    @override
    def __bytes__(self) -> bytes:
        """
        Get the IPv4 mask as bytes.
        """

        return self._mask.to_bytes(4)
