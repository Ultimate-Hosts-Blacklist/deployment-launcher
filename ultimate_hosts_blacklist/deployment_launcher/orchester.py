"""
The deployment launcher of the Ultimate Hosts Blacklist project.

This is the module that process the orchestration.

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

import concurrent.futures
import contextlib
import heapq
import logging
import os
import secrets
import tempfile
import time
from typing import Dict, Generator, List, Optional, Tuple

import PyFunceble.facility
import PyFunceble.storage
from github import Github
from PyFunceble.checker.syntax.domain import DomainSyntaxChecker
from PyFunceble.checker.syntax.ip import IPSyntaxChecker
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.cli.continuous_integration.exceptions import StopExecution
from PyFunceble.cli.continuous_integration.utils import ci_object
from PyFunceble.cli.processes.file_sorter import FileSorterProcessesManager
from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.helpers.exceptions import UnableToDownload
from PyFunceble.helpers.file import FileHelper
from ultimate_hosts_blacklist.whitelist.core import Core as WhitelistCore

from ultimate_hosts_blacklist.deployment_launcher import deployer, generator
from ultimate_hosts_blacklist.deployment_launcher.defaults import hubgit, infrastructure


class Orchestration:
    """
    Orchester our workflow.
    """

    ci_engine: Optional[ContinuousIntegrationBase] = None
    github_api: Optional[Github] = None

    temp_dirs: Dict[str, tempfile.TemporaryDirectory] = dict()
    temp_files: Dict[str, tempfile.NamedTemporaryFile] = dict()

    commit_message: Optional[str] = None
    debug: Optional[bool] = None

    def __init__(self, *, debug: bool = False) -> None:
        self.commit_message = f"[{infrastructure.VERSION}]"
        self.debug = debug

        self.ci_engine = ci_object(
            commit_message=self.commit_message,
            end_commit_message=self.commit_message,
        )

        self.ci_engine.commit_message = self.commit_message
        self.ci_engine.end_commit_message = self.commit_message

        if self.ci_engine.authorized:
            self.ci_engine.init()

        self.github_api = Github(hubgit.GITHUB_TOKEN)

        self.temp_dirs = {
            "ip": tempfile.TemporaryDirectory(),
            "domain": tempfile.TemporaryDirectory(),
            "info": tempfile.TemporaryDirectory(),
        }

        self.temp_files = {
            "ip": tempfile.NamedTemporaryFile("w", delete=False),
            "domain": tempfile.NamedTemporaryFile("w", delete=False),
        }

        logging.info("Temporary IP directory: %r", self.temp_dirs["ip"].name)
        logging.info("Temporary domain directory: %r", self.temp_dirs["domain"].name)
        logging.info("Temporary IP file: %r", self.temp_files["ip"].name)
        logging.info("Temporary domain file: %r", self.temp_files["domain"].name)

    def __del__(self) -> None:
        for directory in self.temp_dirs.values():
            directory.cleanup()

        for file in self.temp_files.values():
            FileHelper(file.name).delete()

    def get_repositories(self) -> Generator[None, str, None]:
        """
        Provides a single repository name.
        """

        for repository in self.github_api.get_organization(
            hubgit.ORG_SLUG_NAME
        ).get_repos():
            if repository.name in infrastructure.REPOSITORIES_TO_IGNORE:
                continue
            yield repository.name

    @staticmethod
    def fetch_data(repo_name: str, info_dir: str) -> Tuple[str]:
        """
        Fetches the data of the given input source.
        """

        logging.info("Let's fetch the data behind %r", repo_name)

        url_base = hubgit.PARTIAL_RAW_URL % repo_name

        info_url = url_base + "info.json"
        domain_url = url_base + "domains.list"
        clean_url = url_base + "clean.list"
        ip_url = url_base + "ip.list"
        whitelisted_url = url_base + "whitelisted.list"

        domain_found = False
        clean_found = False
        ip_found = False
        whitelisted_found = False

        ip_file_to_deliver = None
        domain_file_to_deliver = None

        download_info_file = os.path.join(info_dir, secrets.token_hex(8))
        downloaded_ip_file = tempfile.NamedTemporaryFile("r", delete=False)
        downloaded_domain_file = tempfile.NamedTemporaryFile("r", delete=False)
        downloaded_clean_file = tempfile.NamedTemporaryFile("r", delete=False)
        downloaded_whitelisted_file = tempfile.NamedTemporaryFile("r", delete=False)

        output_ip_file = tempfile.NamedTemporaryFile("w", delete=False)
        output_domain_file = tempfile.NamedTemporaryFile("w", delete=False)

        try:
            logging.info(
                "[%r] Started to download %r into %r",
                repo_name,
                info_url,
                download_info_file,
            )

            DownloadHelper(info_url).download_text(destination=download_info_file)

            logging.info(
                "[%r] Finished to download %r into %r",
                repo_name,
                info_url,
                download_info_file,
            )
        except UnableToDownload:
            logging.critical(
                "[%r] Could not download %r into %r. Reason: Not found.",
                repo_name,
                info_url,
                download_info_file,
            )

        try:
            logging.info(
                "[%r] Started to download %r into %r",
                repo_name,
                domain_url,
                downloaded_domain_file.name,
            )

            DownloadHelper(domain_url).download_text(
                destination=downloaded_domain_file.name
            )

            logging.info(
                "[%r] Finished to download %r into %r",
                repo_name,
                domain_url,
                downloaded_domain_file.name,
            )
            domain_found = True
        except UnableToDownload:
            logging.critical(
                "[%r] Could not download %r into %r. Reason: Not found.",
                repo_name,
                domain_url,
                downloaded_domain_file.name,
            )

        try:
            logging.info(
                "[%r] Started to download %r into %r",
                repo_name,
                clean_url,
                downloaded_clean_file.name,
            )

            DownloadHelper(clean_url).download_text(
                destination=downloaded_clean_file.name
            )

            logging.info(
                "[%r] Finished to download %r into %r",
                repo_name,
                clean_url,
                downloaded_clean_file.name,
            )
            clean_found = True
        except UnableToDownload:
            logging.critical(
                "[%r] Could not download %r into %r. Reason: Not found.",
                repo_name,
                clean_url,
                downloaded_clean_file.name,
            )

        try:
            logging.info(
                "[%r] Started to download %r into %r",
                repo_name,
                ip_url,
                downloaded_ip_file.name,
            )

            DownloadHelper(ip_url).download_text(destination=downloaded_ip_file.name)

            logging.info(
                "[%r] Finished to download %r into %r",
                repo_name,
                ip_url,
                downloaded_ip_file.name,
            )
            ip_found = True
        except UnableToDownload:
            logging.critical(
                "[%r] Could not download %r into %r. Reason: Not found.",
                repo_name,
                ip_url,
                downloaded_ip_file.name,
            )

        try:
            logging.info(
                "[%r] Started to download %r into %r",
                repo_name,
                whitelisted_url,
                downloaded_whitelisted_file.name,
            )

            DownloadHelper(whitelisted_url).download_text(
                destination=downloaded_whitelisted_file.name
            )

            logging.info(
                "[%r] Finished to download %r into %r",
                repo_name,
                whitelisted_url,
                downloaded_whitelisted_file.name,
            )
            whitelisted_found = True
        except UnableToDownload:
            logging.critical(
                "[%r] Could not download %r into %r. Reason: Not found.",
                repo_name,
                whitelisted_url,
                downloaded_whitelisted_file.name,
            )

        downloaded_domain_file.seek(0)
        downloaded_clean_file.seek(0)
        downloaded_ip_file.seek(0)
        downloaded_whitelisted_file.seek(0)

        if whitelisted_found:
            domain_file_to_read = (
                domain_file_to_deliver
            ) = downloaded_whitelisted_file.name
        elif clean_found:
            domain_file_to_read = domain_file_to_deliver = downloaded_clean_file.name
        elif domain_found:
            domain_file_to_read = domain_file_to_deliver = downloaded_domain_file.name
        else:
            domain_file_to_read = domain_file_to_deliver = None

        if ip_found:
            ip_file_to_read = ip_file_to_deliver = downloaded_ip_file.name
        else:
            ip_file_to_read = ip_file_to_deliver = None

        logging.info(
            "[%r] Using %r as (domain) file to read and deliver.",
            repo_name,
            domain_file_to_read,
        )
        logging.info(
            "[%r] Using %r as (ip) file to read and deliver.",
            repo_name,
            domain_file_to_read,
        )

        if domain_file_to_read:
            logging.info(
                "[%r] Starting to whitelist content of %r",
                repo_name,
                domain_file_to_read,
            )

            WhitelistCore(
                output_file=domain_file_to_read,
                use_official=True,
            ).filter(file=domain_file_to_read, already_formatted=True)

            logging.info(
                "[%r] Finished to whitelist content of %r",
                repo_name,
                domain_file_to_read,
            )

            logging.info(
                "[%r] Starting to filter content of %r", repo_name, domain_file_to_read
            )
            with open(domain_file_to_read, "r", encoding="utf-8") as file_stream:
                for line in file_stream:
                    if not line.strip():
                        continue

                    if DomainSyntaxChecker(line.strip()).is_valid():
                        output_domain_file.write(line)
                    elif IPSyntaxChecker(line.strip()).is_valid():
                        output_ip_file.write(line)

            logging.info(
                "[%r] Finished to filter content of %r", repo_name, domain_file_to_read
            )

        if ip_file_to_read:
            logging.info(
                "[%r] Starting to whitelist content of %r", repo_name, ip_file_to_read
            )

            WhitelistCore(
                output_file=ip_file_to_read,
                use_official=True,
            ).filter(file=ip_file_to_read, already_formatted=True)

            logging.info(
                "[%r] Finished to whitelist content of %r", repo_name, ip_file_to_read
            )

            logging.info(
                "[%r] Starting to filter content of %r", repo_name, ip_file_to_read
            )

            with open(ip_file_to_read, "r", encoding="utf-8") as file_stream:
                for line in file_stream:
                    if not line.strip():
                        continue

                    if DomainSyntaxChecker(line.strip()).is_valid():
                        output_domain_file.write(line)
                    elif IPSyntaxChecker(line.strip()).is_valid():
                        output_ip_file.write(line)

            logging.info(
                "[%r] Finished to filter content of %r", repo_name, ip_file_to_read
            )

        downloaded_ip_file.close()
        downloaded_domain_file.close()
        downloaded_clean_file.close()
        downloaded_whitelisted_file.close()

        if downloaded_ip_file.name != ip_file_to_deliver:
            FileHelper(downloaded_ip_file.name).delete()

        if downloaded_domain_file.name != domain_file_to_deliver:
            FileHelper(downloaded_domain_file.name).delete()

        if downloaded_whitelisted_file.name != domain_file_to_deliver:
            FileHelper(downloaded_whitelisted_file.name).delete()

        if downloaded_clean_file.name != domain_file_to_deliver:
            FileHelper(downloaded_clean_file.name).delete()

        output_domain_file.seek(0)
        output_ip_file.seek(0)

        output_domain_file.seek(0)
        output_ip_file.seek(0)

        return output_domain_file.name, output_ip_file.name

    def fetch_and_get_files(self) -> List[Tuple[str, str]]:
        """
        Starts the fetching of all files and return them.
        """

        result_files = list()

        with concurrent.futures.ProcessPoolExecutor(max_workers=None) as executor:
            submitted_tasks: List[concurrent.futures.Future] = list()

            for repo_name in self.get_repositories():
                task = executor.submit(
                    self.fetch_data, repo_name, self.temp_dirs["info"].name
                )

                submitted_tasks.append(task)

            for task in concurrent.futures.as_completed(submitted_tasks):
                if task.exception():
                    raise task.exception()

                result_files.append(task.result())

                continue

        return result_files

    def merge_fetched_filed(
        self, fetched_files: List[Tuple[str, str]]
    ) -> Tuple[List[str], List[str]]:
        """
        Sorts the fetched files and respectively returns the list file containing the
        domains and the one with the IPS.
        """

        with contextlib.ExitStack() as stack:
            domain_files = [stack.enter_context(open(x)) for x, _ in fetched_files]
            ip_files = [stack.enter_context(open(y)) for _, y in fetched_files]

            self.temp_files["domain"].seek(0)
            self.temp_files["domain"].writelines(heapq.merge(*domain_files))
            self.temp_files["domain"].seek(0)

            self.temp_files["ip"].seek(0)
            self.temp_files["ip"].writelines(heapq.merge(*ip_files))
            self.temp_files["ip"].seek(0)

            return domain_files, ip_files

    def sort_unique_files(self) -> None:
        """
        Sorts our final unique files.
        """

        local_temp_dir = tempfile.TemporaryDirectory()
        PyFunceble.storage.CONFIG_DIRECTORY = local_temp_dir.name

        PyFunceble.facility.ConfigLoader.set_merge_upstream(True).set_custom_config(
            {
                "debug": {"level": "debug", "active": self.debug},
                "cli_testing": {
                    "ci": {
                        "commit_message": self.commit_message,
                        "end_commit_message": self.commit_message,
                    }
                },
            }
        ).start()

        logging.info("Started to sort files.")
        sorter_process = FileSorterProcessesManager(
            daemon=True,
            max_worker=3,
            generate_input_queue=True,
            generate_output_queue=False,
        )

        files = [self.temp_files["domain"].name, self.temp_files["ip"].name]

        for file in files:
            sorter_process.add_to_input_queue(
                {"file": file, "write_header": False, "remove_duplicates": True},
                worker_name="uhb_controller",
            )
            logging.info("Added %s into the sorting queue.", file)

        sorter_process.start()
        sorter_process.send_stop_signal(worker_name="uhb_controller")
        sorter_process.wait()
        logging.info("Finished to sort files.")

        local_temp_dir.cleanup()

    def generate_files(self) -> None:
        """
        Generates our output files.
        """

        domains_file = self.temp_files["domain"].name
        ip_file = self.temp_files["ip"].name

        generator.dotted(domains_file, ip_file)
        generator.plain_text_domain(domains_file)
        generator.plain_text_ip(ip_file)
        generator.hosts_deny(ip_file)
        generator.superhosts_deny(domains_file, ip_file)
        generator.unix_hosts(domains_file)
        generator.windows_hosts(domains_file)
        generator.readme_md(
            domains_files=(domains_file,),
            ip_files=(ip_file,),
            info_files=[
                os.path.join(self.temp_dirs["info"].name, x)
                for x in os.listdir(self.temp_dirs["info"].name)
            ],
        )

    def start(self) -> "Orchestration":
        """
        Starts the orchestration of the system.
        """

        try:
            _ = self.ci_engine.bypass()
            fetched_files = self.fetch_and_get_files()

            domain_files, ip_files = self.merge_fetched_filed(fetched_files)

            for file in domain_files:
                self.temp_files[secrets.token_hex(6)] = file

            for file in ip_files:
                self.temp_files[secrets.token_hex(6)] = file

            self.sort_unique_files()
            self.generate_files()

            if self.ci_engine.authorized:
                deployer.github(self.ci_engine)
                time.sleep(60)
                deployer.hosts_ubuntu101_co_za()
        except StopExecution:
            logging.info("Stopping because release has been already done.")
