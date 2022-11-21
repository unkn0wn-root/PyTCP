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


#
# examples/udp_echo.py - The 'user space' service UDP Echo (RFC 862).
#
# ver 2.7
#


from __future__ import annotations

import time
from typing import TYPE_CHECKING

import click

from examples.udp_service import UdpService
from pytcp import TcpIpStack
from pytcp.misc.malpi import malpa, malpi, malpka

if TYPE_CHECKING:
    from pytcp.lib.socket import Socket


class UdpEchoService(UdpService):
    """
    UDP Echo service support class.
    """

    def __init__(
        self, *, local_ip_address: str = "0.0.0.0", local_port: int = 7
    ):
        """
        Class constructor.
        """

        super().__init__(
            service_name="Echo",
            local_ip_address=local_ip_address,
            local_port=local_port,
        )

    def service(self, *, listening_socket: Socket) -> None:
        """
        Inbound connection handler.
        """

        while self._run_thread:
            message, remote_address = listening_socket.recvfrom()

            click.echo(
                f"Service UDP Echo: Received {len(message)} bytes from "
                f"{remote_address[0]}, port {remote_address[1]}."
            )

            if b"malpka" in message.strip().lower():
                message = malpka
            elif b"malpa" in message.strip().lower():
                message = malpa
            elif b"malpi" in message.strip().lower():
                message = malpi

            listening_socket.sendto(message, remote_address)

            click.echo(
                f"Service UDP Echo: Echo'ed {len(message)} bytes back to "
                f"{remote_address[0]}, port {remote_address[1]}."
            )


@click.command()
@click.option("--interface", default="tap7")
def cli(*, interface: str) -> None:
    """
    Start PyTCP stack and stop it when user presses Ctrl-C.
    Run the UDP Echo service.
    """

    stack = TcpIpStack(interface)
    service = UdpEchoService()

    try:
        stack.start()
        service.start()
        while True:
            time.sleep(60)

    except KeyboardInterrupt:
        service.stop()
        stack.stop()


if __name__ == "__main__":
    cli()
