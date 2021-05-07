# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from typing import cast, List

from lisa.executable import Tool
from lisa.operating_system import Posix


class Rpm(Tool):
    @property
    def command(self) -> str:
        return "rpm"

    @property
    def can_install(self) -> bool:
        return True

    def _install(self) -> bool:
        posix_os: Posix = cast(Posix, self.node.os)
        posix_os.install_packages("rpm")
        return self._check_exists()

    def install_package(
        self, package_file: str , force_run: bool = False, no_error_log: bool = False
    ) -> None:
        self.initialize()
        run_command = f"-iv {package_file}"
        cmd_result = self.run(
            run_command, force_run=force_run, no_error_log=no_error_log, no_info_log=True
        )
        if (cmd_result.exit_code != 0 or
            package_file not in query_package(self, package_file, true)):
            raise LisaException(
                f"could not install package with '{run_command}', it may caused by"
                f" missing file. stdout: {command_result.stdout}"
            )

    def upgrade_package(
        self, package_file: str , force_run: bool = False, no_error_log: bool = False
    ) -> None:
        self.initialize()
        run_command = f"-Uv {package_file}"
        cmd_result = self.run(
            run_command, force_run=force_run, no_error_log=no_error_log, no_info_log=True
        )
        if (cmd_result.exit_code != 0 or
            package_file not in query_package(self, package_file, true)):
            raise LisaException(
                f"could not install package with '{run_command}', it may caused by"
                f" missing file. stdout: {command_result.stdout}"
            )

    def query_package(
        self, package_file: str = "" , force_run: bool = False, no_error_log: bool = False
    ) -> List[str]:
        self.initialize()
        if package_file:
            run_command = f"-qa | grep {package_file}"
        else:
            run_command = "-qa"
        cmd_result = self.run(
            run_command, force_run=force_run, no_error_log=no_error_log, no_info_log=True
        )
        package_list = []
        if cmd_result.exit_code == 0:
           for row in cmd_result.split('\n'):
               package_list.append(row)
        return package_list