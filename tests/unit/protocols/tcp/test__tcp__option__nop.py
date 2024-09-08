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
Module contains tests for the TCP Nop (No Operation) option code.

tests/unit/protocols/tcp/test__tcp__option__nop.py

ver 3.0.2
"""


from typing import Any

from parameterized import parameterized_class  # type: ignore
from testslide import TestCase

from pytcp.protocols.tcp.options.tcp_option import TcpOptionType
from pytcp.protocols.tcp.options.tcp_option__nop import (
    TCP__OPTION__NOP__LEN,
    TcpOptionNop,
)


class TestTcpOptionNopAsserts(TestCase):
    """
    The TCP Nop option constructor argument assert tests.
    """

    # Currently the TCP Nop option does not have any constructor
    # argument asserts.


@parameterized_class(
    [
        {
            "_description": "The TCP Nop option.",
            "_args": [],
            "_kwargs": {},
            "_results": {
                "__len__": 1,
                "__str__": "nop",
                "__repr__": "TcpOptionNop()",
                "__bytes__": b"\x01",
                "type": TcpOptionType.NOP,
                "len": TCP__OPTION__NOP__LEN,
            },
        },
    ]
)
class TestTcpOptionNopAssembler(TestCase):
    """
    The TCP Nop option assembler tests.
    """

    _description: str
    _args: list[Any]
    _kwargs: dict[str, Any]
    _results: dict[str, Any]

    def setUp(self) -> None:
        """
        Initialize the TCP Nop option object with testcase arguments.
        """

        self._option = TcpOptionNop(*self._args, **self._kwargs)

    def test__tcp__option__nop__len(self) -> None:
        """
        Ensure the TCP Nop option '__len__()' method returns a correct
        value.
        """

        self.assertEqual(
            len(self._option),
            self._results["__len__"],
        )

    def test__tcp__option__nop__str(self) -> None:
        """
        Ensure the TCP Nop option '__str__()' method returns a correct
        value.
        """

        self.assertEqual(
            str(self._option),
            self._results["__str__"],
        )

    def test__tcp__option__nop__repr(self) -> None:
        """
        Ensure the TCP Nop option '__repr__()' method returns a correct
        value.
        """

        self.assertEqual(
            repr(self._option),
            self._results["__repr__"],
        )

    def test__tcp__option__nop__bytes(self) -> None:
        """
        Ensure the TCP Nop option '__bytes__()' method returns a correct
        value.
        """

        self.assertEqual(
            bytes(self._option),
            self._results["__bytes__"],
        )

    def test__tcp__option__nop__type(self) -> None:
        """
        Ensure the TCP Nop option 'type' field contains a correct value.
        """

        self.assertEqual(
            self._option.type,
            self._results["type"],
        )

    def test__tcp__option__nop__length(self) -> None:
        """
        Ensure the TCP Nop option 'len' field contains a correct value.
        """

        self.assertEqual(
            self._option.len,
            self._results["len"],
        )


@parameterized_class(
    [
        {
            "_description": "The TCP Nop option.",
            "_args": [b"\x01" + b"ZH0PA"],
            "_kwargs": {},
            "_results": {
                "option": TcpOptionNop(),
            },
        },
        {
            "_description": "The TCP Nop option minimum length assert.",
            "_args": [b""],
            "_kwargs": {},
            "_results": {
                "error": AssertionError,
                "error_message": (
                    "The minimum length of the TCP Nop option must be 1 "
                    "byte. Got: 0"
                ),
            },
        },
        {
            "_description": "The TCP Nop option incorrect 'type' field assert.",
            "_args": [b"\xff"],
            "_kwargs": {},
            "_results": {
                "error": AssertionError,
                "error_message": (
                    f"The TCP Nop option type must be {TcpOptionType.NOP!r}. "
                    f"Got: {TcpOptionType.from_int(255)!r}"
                ),
            },
        },
    ]
)
class TestTcpOptionNopParser(TestCase):
    """
    The TCP Nop option parser tests.
    """

    _description: str
    _args: list[Any]
    _kwargs: dict[str, Any]
    _results: dict[str, Any]

    def test__tcp__option__nop__from_bytes(self) -> None:
        """
        Ensure the TCP Nop option parser creates the proper option object
        or throws assertion error.
        """

        if "option" in self._results:
            option = TcpOptionNop.from_bytes(*self._args, **self._kwargs)

            self.assertEqual(
                option,
                self._results["option"],
            )

        if "error" in self._results:
            with self.assertRaises(self._results["error"]) as error:
                TcpOptionNop.from_bytes(*self._args, **self._kwargs)

            self.assertEqual(
                str(error.exception),
                self._results["error_message"],
            )
