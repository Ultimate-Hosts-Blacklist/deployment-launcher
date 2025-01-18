"""
The deployment launcher of the Ultimate Hosts Blacklist project.

This is the module that provides the command line interface.

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 Ultimate-Hosts-Blacklist Contributors
    Copyright (c) 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 Nissar Chababy - @funilrys
    Copyright (c) 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024 Mitchell Krog - @mitchellkrogza

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import argparse
import logging

import colorama

from ultimate_hosts_blacklist.deployment_launcher import __version__
from ultimate_hosts_blacklist.deployment_launcher.orchester import Orchestration


def tool() -> None:
    """
    Provides the CLI.
    """

    colorama.init(autoreset=True)

    parser = argparse.ArgumentParser(
        description="The deployment launcher of the Ultimate Hosts Blacklist project.",
        epilog=f"Crafted with {colorama.Fore.RED}♥{colorama.Fore.RESET} by "
        f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}Nissar Chababy (Funilrys)",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="Activates the debug mode.",
    )

    parser.add_argument(
        "-v",
        "--version",
        help="Show the version end exits.",
        action="version",
        version="%(prog)s " + __version__,
    )

    args = parser.parse_args()

    if args.debug:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    logging.basicConfig(
        format="[%(asctime)s::%(levelname)s] %(message)s", level=logging_level
    )

    logging.info("Launcher version: %s", __version__)

    Orchestration(debug=args.debug).start()
