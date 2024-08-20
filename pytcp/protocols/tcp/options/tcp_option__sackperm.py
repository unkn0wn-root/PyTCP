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
This module contains the TCP Sackperm (SACK Permitted) option support code.

pytcp/protocols/tcp/options/tcp_option__sackperm.py

ver 3.0.0
"""


from __future__ import annotations

import struct
from dataclasses import dataclass, field
from typing import override

from pytcp.protocols.tcp.options.tcp_option import TcpOption, TcpOptionType
from pytcp.protocols.tcp.tcp__errors import TcpIntegrityError

# The TCP Sackperm (SACK Permitted) option [RFC 2018].

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |    Type = 4   |   Length = 2  |
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


TCP__OPTION_SACKPERM__LEN = 2


@dataclass(frozen=True, kw_only=True)
class TcpOptionSackperm(TcpOption):
    """
    The TCP Sackperm (SACK Permitted) option support class.
    """

    type: TcpOptionType = field(
        repr=False, init=False, default=TcpOptionType.SACKPERM
    )
    len: int = field(repr=False, init=False, default=TCP__OPTION_SACKPERM__LEN)

    @override
    def __post_init__(self) -> None:
        """
        Validate the TCP Sackperm option fields.
        """

    @override
    def __str__(self) -> str:
        """
        Get the TCP Sackperm option log string.
        """

        return "sackperm"

    @override
    def __bytes__(self) -> bytes:
        """
        Get the TCP Sackperm option as bytes.
        """

        return struct.pack(
            "! BB",
            self.type.value,
            self.len,
        )

    @staticmethod
    def from_bytes(_bytes: bytes) -> TcpOptionSackperm:
        """
        Initialize the TCP Sackperm option from bytes.
        """

        assert len(_bytes) >= 2
        assert _bytes[0] == int(TcpOptionType.SACKPERM)

        if _bytes[1] != TCP__OPTION_SACKPERM__LEN:
            raise TcpIntegrityError("Invalid Sackperm option length (I).")

        # The Sackperm option has no data, so the length should be exactly 2
        # and the option length integrity check (II) here wouldn't function
        # properly as the condition when length field is missing is already
        # being handled assert.

        return TcpOptionSackperm()
