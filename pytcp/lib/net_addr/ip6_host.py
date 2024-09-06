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
Module contains IPv6 host support class.

pytcp/lib/net_addr/ip6_host.py

ver 3.0.2
"""


from __future__ import annotations

import time
from enum import auto
from typing import override

from pytcp.lib.net_addr.mac_address import MacAddress

from .errors import (
    Ip6AddressFormatError,
    Ip6HostFormatError,
    Ip6HostGatewayError,
    Ip6HostSanityError,
    Ip6MaskFormatError,
)
from .ip6_address import Ip6Address
from .ip6_mask import Ip6Mask
from .ip6_network import Ip6Network
from .ip_host import IpHost, IpHostOrigin


class Ip6HostOrigin(IpHostOrigin):
    """
    IPv4 address origin enumeration.
    """

    STATIC = auto()
    ND = auto()
    DHCP = auto()
    UNKNOWN = auto()


class Ip6Host(IpHost[Ip6Address, Ip6Network, Ip6HostOrigin]):
    """
    IPv6 host support class.
    """

    _version: int = 6
    _gateway: Ip6Address | None = None
    _origin: Ip6HostOrigin
    _expiration_time: int

    def __init__(
        self,
        host: (
            Ip6Host
            | tuple[Ip6Address, Ip6Network]
            | tuple[Ip6Address, Ip6Mask]
            | str
        ),
        /,
        *,
        gateway: Ip6Address | None = None,
        origin: Ip6HostOrigin | None = None,
        expiration_time: int | None = None,
    ) -> None:
        """
        Get the IPv6 host address log string.
        """

        self._gateway = gateway
        self._origin = origin or Ip6HostOrigin.UNKNOWN
        self._expiration_time = expiration_time or 0

        if self._origin in {Ip6HostOrigin.ND, Ip6HostOrigin.DHCP}:
            assert self._expiration_time >= int(time.time())
        else:
            assert self._expiration_time == 0

        if isinstance(host, tuple):
            if len(host) == 2:
                if isinstance(host[0], Ip6Address) and isinstance(
                    host[1], Ip6Network
                ):
                    self._address = host[0]
                    self._network = host[1]
                    if self._address not in self._network:
                        raise Ip6HostSanityError(host)
                    self._validate_gateway(gateway)
                    return
                if isinstance(host[0], Ip6Address) and isinstance(
                    host[1], Ip6Mask
                ):
                    self._address = host[0]
                    self._network = Ip6Network((host[0], host[1]))
                    return

        if isinstance(host, str):
            try:
                address, _ = host.split("/")
                self._address = Ip6Address(address)
                self._network = Ip6Network(host)
                return
            except (ValueError, Ip6AddressFormatError, Ip6MaskFormatError):
                pass

        if isinstance(host, Ip6Host):
            assert (
                gateway is None
            ), f"Gateway cannot be set when copying host. Got: {gateway!r}"
            assert (
                origin is None
            ), f"Origin cannot be set when copying host. Got: {origin!r}"
            assert (
                expiration_time is None
            ), f"Expiration time cannot be set when copying host. Got: {expiration_time!r}"
            self._address = host.address
            self._network = host.network
            self._gateway = host.gateway
            self._origin = host.origin
            self._expiration_time = host.expiration_time
            return

        raise Ip6HostFormatError(host)

    @override
    def _validate_gateway(self, address: Ip6Address | None, /) -> None:
        """
        Validate the IPv6 host address gateway.
        """

        if address is not None and (
            address not in Ip6Network("fe80::/10")
            or address == self._network.address
            or address == self._address
        ):
            raise Ip6HostGatewayError(address)

    @staticmethod
    def from_eui64(
        *, mac_address: MacAddress, ip6_network: Ip6Network
    ) -> Ip6Host:
        """
        Create IPv6 EUI64 host address.
        """

        assert len(ip6_network.mask) == 64, (
            "The IPv6 EUI64 network address mask must be /64. "
            f"Got: {ip6_network.mask}"
        )

        interface_id = (
            ((int(mac_address) & 0xFFFFFF000000) << 16)
            | int(mac_address) & 0xFFFFFF
            | 0xFFFE000000
        ) ^ 0x0200000000000000

        return Ip6Host(
            (
                Ip6Address(int(ip6_network.address) | interface_id),
                Ip6Mask("/64"),
            )
        )
