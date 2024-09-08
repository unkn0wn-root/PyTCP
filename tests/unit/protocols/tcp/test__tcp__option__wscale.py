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
Module contains tests for the TCP Wscale (Window Scale) option code.

tests/unit/protocols/tcp/test__tcp__option__wscale.py

ver 3.0.2
"""


from typing import Any

from parameterized import parameterized_class  # type: ignore
from testslide import TestCase

from pytcp.lib.int_checks import UINT_8__MIN
from pytcp.protocols.tcp.options.tcp_option import TcpOptionType
from pytcp.protocols.tcp.options.tcp_option__wscale import (
    TCP__OPTION__WSCALE__MAX_VALUE,
    TcpOptionWscale,
)
from pytcp.protocols.tcp.tcp__errors import TcpIntegrityError


class TestTcpOptionWscaleAsserts(TestCase):
    """
    The TCP Wscale option constructor argument assert tests.
    """

    def setUp(self) -> None:
        """
        Create the default arguments for the TCP Wscale option constructor.
        """

        self._args: list[Any] = [0]
        self._kwargs: dict[str, Any] = {}

    def test__tcp__option__wscale__wscale__under_min(self) -> None:
        """
        Ensure the TCP Wscale option constructor raises an exception when the
        provided 'wscale' argument is lower than the minimum supported value.
        """

        self._args[0] = value = UINT_8__MIN - 1

        with self.assertRaises(AssertionError) as error:
            TcpOptionWscale(*self._args, **self._kwargs)

        self.assertEqual(
            str(error.exception),
            "The 'wscale' field must be a 8-bit unsigned integer less than "
            f"or equal to {TCP__OPTION__WSCALE__MAX_VALUE}. Got: {value}",
        )

    def test__tcp__option__wscale__wscale__over_max(self) -> None:
        """
        Ensure the TCP Wscale option constructor raises an exception when the
        provided 'wscale' argument is higher than the maximum supported value.
        """

        self._args[0] = value = TCP__OPTION__WSCALE__MAX_VALUE + 1

        with self.assertRaises(AssertionError) as error:
            TcpOptionWscale(*self._args, **self._kwargs)

        self.assertEqual(
            str(error.exception),
            "The 'wscale' field must be a 8-bit unsigned integer less than "
            f"or equal to {TCP__OPTION__WSCALE__MAX_VALUE}. Got: {value}",
        )


@parameterized_class(
    [
        {
            "_description": "The TCP Wscale option.",
            "_args": [14],
            "_kwargs": {},
            "_results": {
                "__len__": 3,
                "__str__": "wscale 14",
                "__repr__": "TcpOptionWscale(wscale=14)",
                "__bytes__": b"\x03\x03\x0e",
                "wscale": 14,
            },
        },
    ]
)
class TestTcpOptionWscaleAssembler(TestCase):
    """
    The TCP Wscale option assembler tests.
    """

    _description: str
    _args: list[Any]
    _kwargs: dict[str, Any]
    _results: dict[str, Any]

    def setUp(self) -> None:
        """
        Initialize the TCP Wscale option object with testcase arguments.
        """

        self._option = TcpOptionWscale(*self._args, **self._kwargs)

    def test__tcp__option__wscale__len(self) -> None:
        """
        Ensure the TCP Wscale option '__len__()' method returns a correct
        value.
        """

        self.assertEqual(
            len(self._option),
            self._results["__len__"],
        )

    def test__tcp__option__wscale__str(self) -> None:
        """
        Ensure the TCP Wscale option '__str__()' method returns a correct
        value.
        """

        self.assertEqual(
            str(self._option),
            self._results["__str__"],
        )

    def test__tcp__option__wscale__repr(self) -> None:
        """
        Ensure the TCP Wscale option '__repr__()' method returns a correct
        value.
        """

        self.assertEqual(
            repr(self._option),
            self._results["__repr__"],
        )

    def test__tcp__option__wscale__bytes(self) -> None:
        """
        Ensure the TCP Wscale option '__bytes__()' method returns a correct
        value.
        """

        self.assertEqual(
            bytes(self._option),
            self._results["__bytes__"],
        )

    def test__tcp__option__wscale__wscale(self) -> None:
        """
        Ensure the TCP Wscale option 'wscale' field contains a correct value.
        """

        self.assertEqual(
            self._option.wscale,
            self._results["wscale"],
        )


@parameterized_class(
    [
        {
            "_description": "The TCP Wscale option.",
            "_args": [b"\x03\x03\x0e" + b"ZH0PA"],
            "_kwargs": {},
            "_results": {
                "option": TcpOptionWscale(wscale=14),
            },
        },
        {
            "_description": "The TCP Wscale option (maximum value correction).",
            "_args": [b"\x03\x03\xff" + b"ZH0PA"],
            "_kwargs": {},
            "_results": {
                "option": TcpOptionWscale(wscale=14),
            },
        },
        {
            "_description": "The TCP Wscale option minimum length assert.",
            "_args": [b"\x03"],
            "_kwargs": {},
            "_results": {
                "error": AssertionError,
                "error_message": (
                    "The minimum length of the TCP Wscale option must be 2 "
                    "bytes. Got: 1"
                ),
            },
        },
        {
            "_description": "The TCP Wscale option incorrect 'type' field assert.",
            "_args": [b"\xff\03\x0e"],
            "_kwargs": {},
            "_results": {
                "error": AssertionError,
                "error_message": (
                    f"The TCP Wscale option type must be {TcpOptionType.WSCALE!r}. "
                    f"Got: {TcpOptionType.from_int(255)!r}"
                ),
            },
        },
        {
            "_description": "The TCP Wscale option length integrity check (I).",
            "_args": [b"\x03\02\x0e"],
            "_kwargs": {},
            "_results": {
                "error": TcpIntegrityError,
                "error_message": (
                    "[INTEGRITY ERROR][TCP] The TCP Wscale option length must be "
                    "3 bytes. Got: 2"
                ),
            },
        },
        {
            "_description": "The TCP Wscale option length integrity check (II).",
            "_args": [b"\x03\03"],
            "_kwargs": {},
            "_results": {
                "error": TcpIntegrityError,
                "error_message": (
                    "[INTEGRITY ERROR][TCP] The TCP Wscale option length must "
                    "be less than or equal to the length of provided bytes "
                    "(2). Got: 3"
                ),
            },
        },
    ]
)
class TestTcpOptionWscaleParser(TestCase):
    """
    The TCP Wscale option parser tests.
    """

    _description: str
    _args: list[Any]
    _kwargs: dict[str, Any]
    _results: dict[str, Any]

    def test__tcp__option__wscale__from_bytes(self) -> None:
        """
        Ensure the TCP Wscale option parser creates the proper option
        object or throws assertion error.
        """

        if "option" in self._results:
            option = TcpOptionWscale.from_bytes(*self._args, **self._kwargs)

            self.assertEqual(
                option,
                self._results["option"],
            )

        if "error" in self._results:
            with self.assertRaises(self._results["error"]) as error:
                TcpOptionWscale.from_bytes(*self._args, **self._kwargs)

            self.assertEqual(
                str(error.exception),
                self._results["error_message"],
            )
