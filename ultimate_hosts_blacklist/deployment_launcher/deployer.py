"""
The deployment launcher of the Ultimate Hosts Blacklist project.

This is the module that provides or trigger the deployment.

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

import logging

import requests
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.cli.continuous_integration.exceptions import StopExecution

from ultimate_hosts_blacklist.deployment_launcher.defaults import infrastructure


def github(ci_engine: ContinuousIntegrationBase) -> None:
    """
    Deploy to our central GitHub repository.
    """

    try:
        logging.info("Started deployment to GitHub.")
        ci_engine.apply_end_commit()
        logging.info("Finished deployment to GitHub.")
    except StopExecution:
        pass


def hosts_ubuntu101_co_za() -> None:
    """
    Trigger the deployment tool behind our domain.
    """

    logging.info("Started deployment request to our mirror.")
    requests.get(
        infrastructure.DOMAIN_DEPLOYMENT_LINK,
        headers={"User-Agent": "Ultimate-Hosts-Blacklist/central-repo-updaters"},
    )
    logging.info("Finished deployment request to our mirror.")
