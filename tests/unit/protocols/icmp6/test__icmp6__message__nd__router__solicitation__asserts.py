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
This module contains tests for the ICMPv6 ND Router Solicitation message assembler & parser
argument asserts.

tests/unit/protocols/icmp6/test__icmp6__message__nd__router_solicitation__asserts.py

ver 3.0.0
"""

from testslide import TestCase

from pytcp.lib.int_checks import UINT_16__MAX, UINT_16__MIN
from pytcp.protocols.icmp6.message.nd.icmp6_nd_message__router_solicitation import (
    Icmp6NdRouterSolicitationCode,
    Icmp6NdRouterSolicitationMessage,
)
from pytcp.protocols.icmp6.message.nd.option.icmp6_nd_options import (
    Icmp6NdOptions,
)


class TestIcmp6MessageNdRouterSolicitationAsserts(TestCase):
    """
    The ICMPv6 ND Router Solicitation message assembler & parser argument
    constructors assert tests.
    """

    def setUp(self) -> None:
        """
        Create the default arguments for the ICMPv6 ND Router Solicitation message
        constructor.
        """

        self._message_args = {
            "code": Icmp6NdRouterSolicitationCode.DEFAULT,
            "cksum": 0,
            "options": Icmp6NdOptions(),
        }

    def test__icmp6__message__nd__router_solicitation__code__not_Icmp6NdRouterSolicitationCode(
        self,
    ) -> None:
        """
        Ensure the ICMPv6 ND message constructor raises an exception when the
        provided 'code' argument is not an Icmp6NdRouterSolicitationCode.
        """

        self._message_args["code"] = value = (
            "not an Icmp6NdRouterSolicitationCode"
        )

        with self.assertRaises(AssertionError) as error:
            Icmp6NdRouterSolicitationMessage(**self._message_args)  # type: ignore

        self.assertEqual(
            str(error.exception),
            f"The 'code' field must be an Icmp6NdRouterSolicitationCode. Got: {type(value)!r}",
        )

    def test__icmp6__message__nd__router_solicitation__cksum__under_min(
        self,
    ) -> None:
        """
        Ensure the ICMPv6 ND Router Solicitation message assembler constructor
        raises an exception when the provided 'cksum' argument is lower than
        the minimum supported value.
        """

        self._message_args["cksum"] = value = UINT_16__MIN - 1

        with self.assertRaises(AssertionError) as error:
            Icmp6NdRouterSolicitationMessage(**self._message_args)  # type: ignore

        self.assertEqual(
            str(error.exception),
            f"The 'cksum' field must be a 16-bit unsigned integer. Got: {value!r}",
        )

    def test__icmp6__message__nd__router_solicitation__cksum__over_max(
        self,
    ) -> None:
        """
        Ensure the ICMPv6 ND Router Solicitation message assembler constructor
        raises an exception when the provided 'cksum' argument is higher than
        the maximum supported value.
        """

        self._message_args["cksum"] = value = UINT_16__MAX + 1

        with self.assertRaises(AssertionError) as error:
            Icmp6NdRouterSolicitationMessage(**self._message_args)  # type: ignore

        self.assertEqual(
            str(error.exception),
            f"The 'cksum' field must be a 16-bit unsigned integer. Got: {value!r}",
        )

    def test__icmp6__message__nd__router_solicitation__options__not_Icmp6NdOptions(
        self,
    ) -> None:
        """
        Ensure the ICMPv6 ND message constructor raises an exception when the
        provided 'options' argument is not an Icmp6NdOptions.
        """

        self._message_args["options"] = value = "not an Icmp6NdOptions"

        with self.assertRaises(AssertionError) as error:
            Icmp6NdRouterSolicitationMessage(**self._message_args)  # type: ignore

        self.assertEqual(
            str(error.exception),
            f"The 'options' field must be an Icmp6NdOptions. Got: {type(value)!r}",
        )
