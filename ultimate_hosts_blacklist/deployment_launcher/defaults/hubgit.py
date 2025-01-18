"""
The deployment launcher of the Ultimate Hosts Blacklist project.

This is the module that provides everything related to the way we interact of
GitHub.

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 Ultimate-Hosts-Blacklist Contributors
    Copyright (c) 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 Nissar Chababy - @funilrys

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

USERNAME: str = "ultimate-hosts-blacklist-bot"

if "GITHUB_TOKEN" in os.environ:
    GITHUB_TOKEN: str = os.environ["GITHUB_TOKEN"]
else:
    GITHUB_TOKEN: str = None

ORG_SLUG_NAME: str = "Ultimate-Hosts-Blacklist"

RAW_URL_BASE: str = "https://raw.githubusercontent.com"
PARTIAL_RAW_URL: str = f"{RAW_URL_BASE}/{ORG_SLUG_NAME}/%s/master/"

IGNORE_REPO_RAW_URL: str = (PARTIAL_RAW_URL + "deployment/ignore-repo") % "dev-center"
