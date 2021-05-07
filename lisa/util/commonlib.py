from assertpy import assert_that

from pathlib import Path

from lisa import Environment, Node
from lisa.executable import CustomScript, CustomScriptBuilder
from lisa.tools import rpm, wget

def install_lis_rpms(
        address: str, port: int, log: Optional[Logger] = None, timeout: int = 300) -> bool:
        rpm_tool = self.node.tools[Rpm]

        pass