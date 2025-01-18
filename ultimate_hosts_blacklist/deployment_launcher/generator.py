"""
The deployment launcher of the Ultimate Hosts Blacklist project.

This is the module that provides all sorts of file generator or updater.

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

import json
import logging
import os
from typing import List, Optional

from PyFunceble.helpers.directory import DirectoryHelper
from PyFunceble.helpers.file import FileHelper

from ultimate_hosts_blacklist.deployment_launcher.defaults import (
    infrastructure,
    outputs,
)


def generate_next_file(
    directory_path: str,
    filename: str,
    format_to_apply: str,
    input_files: List[str],
    template: Optional[str] = None,
    endline: Optional[str] = None,
    write_mode: Optional[str] = "lf",
) -> None:
    """
    A general function which write into the next file.

    :param directory_path:
        The path of the directory to write into.
    :param filename:
        The path of the filename.
    :param format_to_apply:
        The format to apply to each line.
    :param input_file:
        The input file to read
    :param template:
        The template to write before starting to write each lines.
    :param endline:
        The last line to write.
    """

    windows_lf = "\r\n"
    unix_lf = "\n"

    if write_mode.lower() == "lf":
        line_ending = unix_lf

        if template:
            template = template.replace(windows_lf, unix_lf)
    elif write_mode.lower() == "crlf":
        line_ending = windows_lf

        if template:
            template = template.replace(unix_lf, windows_lf)
    else:
        raise ValueError("<write_mode> not supported.")

    dir_helper = DirectoryHelper(directory_path)

    if dir_helper.exists():
        for root, _, files in os.walk(directory_path):
            for file in files:
                FileHelper(os.path.join(root, file)).delete()
    else:
        dir_helper.create()

    i = 0
    destination = None
    template_written = False

    for input_file in input_files:
        with open(input_file, "r", encoding="utf-8") as file_stream:
            for line in file_stream:
                line = line.strip()
                destination = os.path.join(directory_path, filename.format(i))

                if not FileHelper(destination).exists():
                    logging.info("Started Generation of %r", destination)

                with open(
                    destination, "a+", encoding="utf-8", newline=line_ending
                ) as destination_file_stream:
                    if i == 0 and template and not template_written:
                        logging.debug("Writting template:\n%s", template)
                        destination_file_stream.write(template)

                        template_written = True

                    destination_file_stream.write(
                        f"{format_to_apply.format(line)}{line_ending}"
                    )

                    if destination_file_stream.tell() >= outputs.MAX_FILE_SIZE_IN_BYTES:
                        logging.info(
                            "Finished Generation of %r",
                            destination,
                        )

                        i += 1
                        continue

    if destination and endline:
        with open(destination, "a+", encoding="utf-8") as destination_file_stream:
            logging.debug("Writting last line:\n%r", endline)
            destination_file_stream.write(endline + "\n")


def dotted(*args: List[str]) -> None:
    """
    Generates the dotted formatted file.

    :param args:
        The files to read and convert.
    """

    generate_next_file(
        outputs.DOTTED_DIR, outputs.INCOMPLETE_DOTTED_FILENAME, ".{0}", args
    )


def plain_text_domain(*args: List[str]) -> None:
    """
    Generates the plain text domain formatted file.

    :param args:
        The files to read and convert.
    """

    generate_next_file(
        outputs.DOMAINS_DIR, outputs.INCOMPLETE_PLAIN_FILENAME, "{0}", args
    )


def plain_text_ip(*args: List[str]) -> None:
    """
    Generates the plain text IP formatted file.

    :param args:
        The files to read and convert.
    """

    generate_next_file(outputs.IPS_DIR, outputs.INCOMPLETE_IPS_FILENAME, "{0}", args)


def hosts_deny(*args: List[str]) -> None:
    """
    Generates the hosts deny file.

    :param args:
        The files to read and convert.
    """

    template_file = os.path.join(
        outputs.TEMPLATE_DIR, outputs.HOSTS_DENY_TEMPLATE_FILENAME
    )

    with open(template_file, "r", encoding="utf-8") as file_stream:
        template = file_stream.read()

    subjects_count = 0

    for file in args:
        with open(file, "r", encoding="utf-8") as file_stream:
            for line in file_stream:
                if not line.strip():
                    continue

                subjects_count += 1

    template = template.replace("%%version%%", infrastructure.VERSION)
    template = template.replace("%%lenIP%%", f"{subjects_count:,d}")

    generate_next_file(
        outputs.HOSTS_DENY_DIR,
        outputs.INCOMPLETE_HOSTS_DENY_FILENAME,
        "ALL: {0}",
        args,
        template=template,
        endline="# ##### END hosts.deny Block List # DO NOT EDIT #####",
    )


def superhosts_deny(*args: List[str]) -> None:
    """
    Generates the superhosts deny file.

    :param args:
        The files to read and convert.
    """

    template_file = os.path.join(
        outputs.TEMPLATE_DIR, outputs.SUPER_HOSTS_DENY_TEMPLATE_FILENAME
    )

    with open(template_file, "r", encoding="utf-8") as file_stream:
        template = file_stream.read()

    subjects_count = 0

    for file in args:
        with open(file, "r", encoding="utf-8") as file_stream:
            for line in file_stream:
                if not line.strip():
                    continue

                subjects_count += 1

    template = template.replace("%%version%%", infrastructure.VERSION)
    template = template.replace("%%lenIPHosts%%", f"{subjects_count:,d}")

    generate_next_file(
        outputs.SUPER_HOSTS_DENY_DIR,
        outputs.INCOMPLETE_SUPER_HOSTS_DENY_FILENAME,
        "ALL: {0}",
        args,
        template=template,
        endline="# ##### END Super hosts.deny Block List # DO NOT EDIT #####",
    )


def unix_hosts(*args: List[str]) -> None:
    """
    Generates the UNIX hosts file.

    :param args:
        The files to read and convert.
    """

    template_file = os.path.join(
        outputs.TEMPLATE_DIR, outputs.UNIX_HOSTS_TEMPLATE_FILENAME
    )

    with open(template_file, "r", encoding="utf-8") as file_stream:
        template = file_stream.read()

    subjects_count = 0

    for file in args:
        with open(file, "r", encoding="utf-8") as file_stream:
            for line in file_stream:
                if not line.strip():
                    continue

                subjects_count += 1

    template = template.replace("%%version%%", infrastructure.VERSION)
    template = template.replace("%%lenHosts%%", f"{subjects_count:,d}")

    generate_next_file(
        outputs.UNIX_HOSTS_DIR,
        outputs.INCOMPLETE_UNIX_HOSTS_FILENAME,
        "0.0.0.0 {0}",
        args,
        template=template,
        endline="# END HOSTS LIST ### DO NOT EDIT THIS LINE AT ALL ###",
    )


def windows_hosts(*args: List[str]) -> None:
    """
    Generates the Windows hosts file.

    :param args:
        The files to read and convert.
    """

    template_file = os.path.join(
        outputs.TEMPLATE_DIR, outputs.WINDOWS_HOSTS_TEMPLATE_FILENAME
    )

    with open(template_file, "r", encoding="utf-8") as file_stream:
        template = file_stream.read()

    subjects_count = 0

    for file in args:
        with open(file, "r", encoding="utf-8") as file_stream:
            for line in file_stream:
                if not line.strip():
                    continue

                subjects_count += 1

    template = template.replace("%%version%%", infrastructure.VERSION)
    template = template.replace("%%lenHosts%%", f"{subjects_count:,d}")

    generate_next_file(
        outputs.WINDOWS_HOSTS_DIR,
        outputs.INCOMPLETE_WINDOWS_HOSTS_FILENAME,
        "127.0.0.1 {0}",
        args,
        template=template,
        endline="# END HOSTS LIST ### DO NOT EDIT THIS LINE AT ALL ###",
        write_mode="crlf",
    )


def readme_md(
    *, domains_files: List[str], ip_files: List[str], info_files: List[str]
) -> None:
    """
    Generates the Windows hosts file.

    :param args:
        The files to read and convert.
    """

    destination = os.path.join(outputs.CURRENT_DIRECTORY, outputs.README_FILENAME)
    template_file = os.path.join(outputs.TEMPLATE_DIR, outputs.README_TEMPLATE_FILENAME)

    logging.info("Started Generation of %r", destination)

    with open(template_file, "r", encoding="utf-8") as file_stream:
        template = file_stream.read()

    domains_count = 0
    ips_count = 0

    for file in domains_files:
        with open(file, "r", encoding="utf-8") as file_stream:
            for line in file_stream:
                if not line.strip():
                    continue

                domains_count += 1

    for file in ip_files:
        with open(file, "r", encoding="utf-8") as file_stream:
            for line in file_stream:
                if not line.strip():
                    continue

                ips_count += 1

    data = []

    for file in info_files:
        with open(file, encoding="utf-8") as file_stream:
            try:
                data.append(json.loads(file_stream.read()))
            except json.decoder.JSONDecodeError:
                logging.critical("Could not decode (info.json): %s", file)

    data = list(sorted(data, key=lambda x: x["name"].lower()))

    single_format = "| %(name)s | [Link](https://github.com/Ultimate-Hosts-Blacklist/%(name)s) | [Link](%(raw_link)s) |"  # noqa: E501

    filtered_data = [single_format % x for x in data]

    template = template.replace("%%version%%", infrastructure.VERSION)
    template = template.replace("%%lenHosts%%", f"{domains_count:,d}")
    template = template.replace("%%lenIPs%%", f"{ips_count:,d}")
    template = template.replace("%%lenHostsIPs%%", f"{domains_count + ips_count:,d}")
    template = template.replace("%%credit-table%%", "\n".join(filtered_data))

    with open(destination, "w", encoding="utf-8") as file_stream:
        file_stream.write(template + "\n")
