"""
The deployment launcher of the Ultimate Hosts Blacklist project.

This is the module that provides everything related to our outputs.

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

import importlib.resources
import os

CURRENT_DIRECTORY: str = os.getcwd()

MAX_FILE_SIZE_IN_BYTES: int = 5_242_880

TEMPLATE_DIRNAME: str = "templates"

HOSTS_DENY_TEMPLATE_FILENAME: str = "hostsdeny.template"
SUPER_HOSTS_DENY_TEMPLATE_FILENAME: str = "superhostsdeny.template"
UNIX_HOSTS_TEMPLATE_FILENAME: str = "hosts.template"
WINDOWS_HOSTS_TEMPLATE_FILENAME: str = "hosts.windows.template"
README_TEMPLATE_FILENAME: str = "README_template.md"


if os.path.isdir(os.path.join(CURRENT_DIRECTORY, TEMPLATE_DIRNAME)):
    TEMPLATE_DIR = os.path.join(CURRENT_DIRECTORY, TEMPLATE_DIRNAME)
else:
    with importlib.resources.path(
        f"ultimate_hosts_blacklist.deployment_launcher.data.{TEMPLATE_DIRNAME}",
        "__init__.py",
    ) as file_path:
        TEMPLATE_DIR = os.path.dirname(str(file_path))

DOTTED_DIRNAME: str = "domains-dotted-format"
INCOMPLETE_DOTTED_FILENAME: str = DOTTED_DIRNAME + "{0}.list"
DOTTED_DIR: str = os.path.join(CURRENT_DIRECTORY, DOTTED_DIRNAME)

PLAIN_DOMAINS_DIRNAME: str = "domains"
INCOMPLETE_PLAIN_FILENAME: str = PLAIN_DOMAINS_DIRNAME + "{0}.list"
DOMAINS_DIR: str = os.path.join(CURRENT_DIRECTORY, PLAIN_DOMAINS_DIRNAME)


PLAIN_IPS_DIRNAME: str = "ips"
INCOMPLETE_IPS_FILENAME: str = PLAIN_IPS_DIRNAME + "{0}.list"
IPS_DIR: str = os.path.join(CURRENT_DIRECTORY, PLAIN_IPS_DIRNAME)

HOSTS_DENY_DIRNAME: str = "hosts.deny"
INCOMPLETE_HOSTS_DENY_FILENAME: str = "hosts{0}.deny"
HOSTS_DENY_DIR: str = os.path.join(CURRENT_DIRECTORY, HOSTS_DENY_DIRNAME)

SUPER_HOSTS_DENY_DIRNAME: str = "superhosts.deny"
INCOMPLETE_SUPER_HOSTS_DENY_FILENAME: str = "superhosts{0}.deny"
SUPER_HOSTS_DENY_DIR: str = os.path.join(CURRENT_DIRECTORY, SUPER_HOSTS_DENY_DIRNAME)


UNIX_HOSTS_DIRNAME: str = "hosts"
INCOMPLETE_UNIX_HOSTS_FILENAME: str = UNIX_HOSTS_DIRNAME + "{0}"
UNIX_HOSTS_DIR: str = os.path.join(CURRENT_DIRECTORY, UNIX_HOSTS_DIRNAME)


WINDOWS_HOSTS_DIRNAME: str = "hosts.windows"
INCOMPLETE_WINDOWS_HOSTS_FILENAME: str = "hosts{0}.windows"
WINDOWS_HOSTS_DIR: str = os.path.join(CURRENT_DIRECTORY, WINDOWS_HOSTS_DIRNAME)

README_FILENAME: str = "README.md"
