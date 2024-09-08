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
Module contains IP host base class.

pytcp/lib/net_addr/ip_host.py

ver 3.0.2
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from .ip_address import IpAddress
    from .ip_network import IpNetwork


class IpHostOrigin(Enum):
    """
    IP host address origin enumeration.
    """


A = TypeVar("A", bound="IpAddress")
N = TypeVar("N", bound="IpNetwork")
O = TypeVar("O", bound="IpHostOrigin")


class IpHost(ABC, Generic[A, N, O]):
    """
    IP host support base class.
    """

    _address: A
    _network: N
    _version: int
    _gateway: A | None
    _origin: O
    _expiration_time: int

    def __str__(self) -> str:
        """
        Get the IP host address log string.
        """

        return str(self._address) + "/" + str(len(self._network.mask))

    def __repr__(self) -> str:
        """
        Get the IP host address string representation.
        """

        return f"{self.__class__.__name__}('{str(self)}')"

    def __eq__(self, other: object) -> bool:
        """
        Compare the IP host address with another object.
        """

        return repr(self) == repr(other)

    def __hash__(self) -> int:
        """
        Get the IP host address hash.
        """

        return hash(repr(self))

    @abstractmethod
    def _validate_gateway(self, address: A | None, /) -> None:
        """
        Validate the IPv4 host address gateway.
        """

        raise NotImplementedError

    @property
    def version(self) -> int:
        """
        Get the IP host address version.
        """

        return self._version

    @property
    def is_ip6(self) -> bool:
        """
        Check if the IP host address version is 6.
        """

        return self._version == 6

    @property
    def is_ip4(self) -> bool:
        """
        Check if the IP host address version is 4.
        """

        return self._version == 4

    @property
    def address(self) -> A:
        """
        Get the IP host address '_address' attribute.
        """

        return self._address

    @property
    def network(self) -> N:
        """
        Get the IP host address '_network' attribute.
        """

        return self._network

    @property
    def origin(self) -> O:
        """
        Get the IPv4 host address '_origin' attribute.
        """

        return self._origin

    @origin.setter
    def origin(self, origin: O, /) -> None:
        """
        Set the IPv4 host address '_origin' attribute.
        """

        self._origin = origin

    @property
    def expiration_time(self) -> int:
        """
        Get the IPv4 host address '_expiration_time' attribute.
        """

        return self._expiration_time

    @expiration_time.setter
    def expiration_time(self, time: int, /) -> None:
        """
        Set the IPv4 host address '_expiration_time' attribute.
        """

        self._expiration_time = time

    @property
    def gateway(self) -> A | None:
        """
        Get the IPv4 host address '_gateway' attribute.
        """

        return self._gateway

    @gateway.setter
    def gateway(self, address: A | None, /) -> None:
        """
        Set the IPv4 host address '_gateway' attribute.
        """

        self._validate_gateway(address)

        self._gateway = address
