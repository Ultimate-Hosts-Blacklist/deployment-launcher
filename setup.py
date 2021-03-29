"""
The deployment launcher of the Ultimate Hosts Blacklist project.

License:
::


    MIT License

    Copyright (c) 2019, 2020, 2021 Ultimate-Hosts-Blacklist
    Copyright (c) 2019, 2020, 2021 Nissar Chababy
    Copyright (c) 2019, 2020, 2021 Mitchell Krog

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

from re import compile as comp
from re import sub as substring
from typing import List

from setuptools import setup

NAMESPACE = "ultimate_hosts_blacklist"
MODULE = "deployment_launcher"

PYPI_NAME = substring(r"_", r"-", f"{NAMESPACE}-{MODULE}")


def get_requirements() -> List[str]:
    """
    Extract all requirements from requirements.txt.
    """

    result = set()

    with open("requirements.txt") as file_stream:
        for line in file_stream:
            line = line.strip()

            if line.startswith("#"):
                continue

            if "#" in line:
                line = line[: line.find("#")]

            line = line.strip()

            if not line:
                continue

            result.add(line)

    return list(result)


def get_version():
    """
    Extract the version from ultimate_hosts_blacklist/MODULE/__init__.py
    """

    with open(
        f"ultimate_hosts_blacklist/{MODULE}/__init__.py", encoding="utf-8"
    ) as file_stream:
        to_match = comp(r'__version__\s=\s"(.*)"')

        return to_match.findall(file_stream.read())[0]


def get_long_description():  # pragma: no cover
    """
    Provides the long description.
    """

    with open("README.rst", encoding="utf-8") as file_stream:
        return file_stream.read()


if __name__ == "__main__":
    setup(
        name=PYPI_NAME,
        version=get_version(),
        install_requires=get_requirements(),
        description="The deployment launcher of the Ultimate Hosts Blacklist project.",
        long_description=get_long_description(),
        license="MIT",
        url="https://github.com/Ultimate-Hosts-Blacklist/dev-center/tree/central-repo-updater",
        platforms=["any"],
        packages=[f"ultimate_hosts_blacklist.{MODULE}"],
        keywords=["Ultimate Hosts Blacklist"],
        classifiers=[
            "Environment :: Console",
            "Topic :: Internet",
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
        ],
        entry_points={
            "console_scripts": [
                f"uhb-deployment-launcher=ultimate_hosts_blacklist.{MODULE}.cli:tool",
                f"ultimate-hosts-blacklist-deployment-launcher=ultimate_hosts_blacklist.{MODULE}.cli:tool",
            ]
        },
    )
