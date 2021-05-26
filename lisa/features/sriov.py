# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from typing import Any

from lisa.feature import Feature
from lisa.platform_ import Platform
from lisa.sut_orchestrator.azure.common import get_network_client
from lisa.util import SkippedException
from lisa.util.logger import get_logger

FEATURE_NAME_SRIOV = "Sriov"


class Sriov(Feature):
    def __init__(self, node: Any, platform: Any) -> None:
        super().__init__(node, platform)
        self._log = get_logger("feature", self.name(), self._node.log)

    @classmethod
    def name(cls) -> str:
        return FEATURE_NAME_SRIOV

    def _is_supported(self) -> bool:
        raise NotImplementedError()

    def check_support(self) -> None:
        if not self._is_supported():
            raise SkippedException("Sriov is not supported.")

    def enable(self) -> bool:
        return self.disable_enable_sriov(self._platform, True)

    def disable(self) -> bool:
        return self.disable_enable_sriov(self._platform, False)

    def disable_enable_sriov(self, platform: Platform, enable: bool) -> bool:
        network_client = get_network_client(platform)
        network_interfaces = network_client.network_interfaces.list(
            self._resource_group_name
        )
        flag = True
        for nic in network_interfaces:
            updated_nic = network_client.network_interfaces.get(
                self._resource_group_name, nic.name
            )
            if updated_nic.enable_accelerated_networking == enable:
                self._log.debug(
                    f"network interface {nic.name} accelerated networking default "
                    "status is consistent with set status, no need to update."
                )
            else:
                updated_nic.enable_accelerated_networking = enable
                network_client.network_interfaces.begin_create_or_update(
                    self._resource_group_name, updated_nic.name, updated_nic
                )
                updated_nic = network_client.network_interfaces.get(
                    self._resource_group_name, nic.name
                )
                if updated_nic.enable_accelerated_networking != enable:
                    flag = False
        return flag
