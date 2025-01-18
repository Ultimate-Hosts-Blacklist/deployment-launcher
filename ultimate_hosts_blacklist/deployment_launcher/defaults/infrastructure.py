"""
The deployment launcher of the Ultimate Hosts Blacklist project.

This is the module that provides everything related to our infrastructure.

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

import os
from datetime import datetime
from typing import List

from PyFunceble.helpers.download import DownloadHelper

from .hubgit import IGNORE_REPO_RAW_URL

CURRENT_DATETIME: datetime = datetime.utcnow()

REPOSITORIES_TO_IGNORE: List[str] = [
    x.strip()
    for x in DownloadHelper(IGNORE_REPO_RAW_URL).download_text().splitlines()
    if x and not x.strip().startswith("#")
]

for index, line in enumerate(REPOSITORIES_TO_IGNORE):
    if "#" in line:
        line = line[: line.find("#")].strip()

        REPOSITORIES_TO_IGNORE[index] = line


if "GITHUB_RUN_NUMBER" in os.environ:
    VERSION: str = (
        f"V2.{os.environ['GITHUB_RUN_NUMBER']}."
        f"{CURRENT_DATETIME.strftime('%Y')}."
        f"{CURRENT_DATETIME.strftime('%m')}."
        f"{CURRENT_DATETIME.strftime('%d')}"
    )
else:
    VERSION = (
        f"V2."
        f"{CURRENT_DATETIME.strftime('%Y')}."
        f"{CURRENT_DATETIME.strftime('%m')}."
        f"{CURRENT_DATETIME.strftime('%d')}"
    )

DOMAIN_DEPLOYMENT_LINK: str = "https://hosts.ubuntu101.co.za/update_hosts.php"
