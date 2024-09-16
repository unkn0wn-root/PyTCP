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
Module contains BSD like socket interface for the stack.

pytcp/lib/socket.py

ver 3.0.2
"""


from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from pytcp.lib.name_enum import NameEnum
from pytcp.protocols.enums import IpProto

if TYPE_CHECKING:
    from net_addr import IpAddress


class gaierror(OSError):
    """
    BSD Socket error for compatibility.
    """


class ReceiveTimeout(Exception):
    """
    Timeout of receive operation.
    """


class AddressFamily(NameEnum):
    """
    Address family identifier.
    """

    UNSPECIFIED = 0
    INET4 = 1
    INET6 = 2

    @staticmethod
    def from_ver(ver: int) -> AddressFamily:
        """
        Get the address family from an IP version.
        """

        match ver:
            case 4:
                return AddressFamily.INET4
            case 6:
                return AddressFamily.INET6
            case _:
                return AddressFamily.UNSPECIFIED


class SocketType(NameEnum):
    """
    Socket type identifier.
    """

    UNSPECIFIED = 0
    STREAM = 1
    DGRAM = 2
    RAW = 3


class Socket(ABC):
    """
    Base class for all socket classes. It contains only the methods that are relevant
    for the BSD socket API. The rest of the methods and actual socket logic are
    implemented in the derived classes.
    """

    _address_family: AddressFamily
    _socket_type: SocketType
    _ip_proto: IpProto
    _local_ip_address: IpAddress
    _remote_ip_address: IpAddress
    _local_port: int
    _remote_port: int

    def __str__(self) -> str:
        """
        Get socket log string.
        """

        return (
            f"{self._address_family}/{self._socket_type}/{self._ip_proto}/"
            f"{self._local_ip_address}/{self._local_port}/"
            f"{self._remote_ip_address}/{self._remote_port}"
        )

    def __repr__(self) -> str:
        """
        Get socket string representation.
        """

        return self.__str__()

    # BSD socket API methods.

    @property
    def id(
        self,
    ) -> tuple[
        AddressFamily, SocketType, IpProto, IpAddress, int, IpAddress, int
    ]:
        """
        Get the socket ID.
        """

        return (
            self._address_family,
            self._socket_type,
            self._ip_proto,
            self._local_ip_address,
            self._local_port,
            self._remote_ip_address,
            self._remote_port,
        )

    @property
    def local_ip_address(self) -> IpAddress:
        """
        Get the '_local_ip_address' attribute.
        """

        return self._local_ip_address

    @property
    def remote_ip_address(self) -> IpAddress:
        """
        Get the '_remote_ip_address' attribute.
        """

        return self._remote_ip_address

    @property
    def local_port(self) -> int:
        """
        Get the '_local_port' attribute.
        """

        return self._local_port

    @property
    def remote_port(self) -> int:
        """
        Get the '_remote_port' attribute.
        """

        return self._remote_port

    ###############################
    ##  BSD socket API methods.  ##
    ###############################

    @property
    def family(self) -> AddressFamily:
        """
        Get the '_family' attribute.
        """

        return self._address_family

    @property
    def type(self) -> SocketType:
        """
        Get the '_type' attribute.
        """

        return self._socket_type

    @property
    def proto(self) -> IpProto:
        """
        Get the '_proto' attribute.
        """

        return self._ip_proto

    def getsockname(self) -> tuple[str, int]:
        """
        Get the local address and port.
        """

        return str(self._local_ip_address), self._local_port

    def getpeername(self) -> tuple[str, int]:
        """
        Get the remote address and port.
        """

        return str(self._remote_ip_address), self._local_port

    def bind(
        self,
        address: tuple[str, int],
    ) -> None:
        """
        The 'bind()' socket API method placeholder.
        """

        raise NotImplementedError

    def connect(
        self,
        address: tuple[str, int],
    ) -> None:
        """
        The 'connect()' socket API method placeholder.
        """

        raise NotImplementedError

    def send(
        self,
        data: bytes,
    ) -> int:
        """
        The 'send()' socket API method placeholder.
        """

        raise NotImplementedError

    def recv(
        self,
        bufsize: int | None = None,
        timeout: float | None = None,
    ) -> bytes:
        """
        The 'recv()' socket API method placeholder.
        """

        raise NotImplementedError

    def close(self) -> None:
        """
        The 'close()' socket API placeholder.
        """

        raise NotImplementedError

    def listen(self) -> None:
        """
        The 'listen()' socket API placeholder.
        """

        raise NotImplementedError

    def accept(self) -> tuple[Socket, tuple[str, int]]:
        """
        The 'accept()' socket API placeholder.
        """

        raise NotImplementedError

    def sendto(self, data: bytes, address: tuple[str, int]) -> int:
        """
        The 'sendto()' socket API placeholder.
        """

        raise NotImplementedError

    def recvfrom(
        self,
        bufsize: int | None = None,
        timeout: float | None = None,
    ) -> tuple[bytes, tuple[str, int]]:
        """
        The 'recvfrom()' socket API placeholder.
        """

        raise NotImplementedError
