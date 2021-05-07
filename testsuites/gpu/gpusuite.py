from assertpy import assert_that

from pathlib import Path

from lisa import Environment, Node, TestCaseMetadata, TestSuite, TestSuiteMetadata
from lisa.executable import CustomScript, CustomScriptBuilder
from lisa.testsuite import simple_requirement
from lisa.util import commonlib
from lisa.tools import Lscpu, Lsvmbus

@TestSuiteMetadata(
    area="gpu",
    category="functional",
    description="""
    This test suite runs the gpu test cases.
    """,
    tags=[],
)
class gpu(TestSuite):

    unsupported_distro = ["CLEARLINUX", "COREOS"]
    grid_supported_sku = ["Standard_NV"]
    cuda_supported_sku = ["Standard_NC", "Standard_ND"]
        
    @TestCaseMetadata(
        description="""
            This test case verfies kernel support for gpu drivers.

            Steps:
            1. Install the GPU drivers on the VM.
            2. Verifies if gpu drivers can be loaded successfully.
        """,
        requirement=simple_requirement(
            environment_status=EnvironmentStatus.Deployed,
        ),
    )
    def gpu_validate_gpudriver(self, environment: Environment, node: Node) -> None:
        # validate if distro is supported for GPU
        if not validate_gpu_support(self, node):
            raise SkippedException("distro not supported")

        if any(map((node.AzureNodeSchema.vm_size).__contains__, grid_supported_sku)):
            self.log.info(
                f"The VM {node.AzureNodeSchema.vm_size}"
                f" instance is with GRID device driver."
            )
            install_result = validate_grid_install(self, node)

        elif any(map((node.AzureNodeSchema.vm_size).__contains__, cuda_supported_sku)):
            self.log.info(
                f"The VM {node.AzureNodeSchema.vm_size}"
                f" instance is with CUDA device driver."
            )
            validate_cuda_install(self, node)

        else:
            raise SkippedException("Azure VM size not supported.")


    # Helper functions

    # TODO: validate the test params against GPU support test matrix
    # when test matrix is available.
    def validate_gpu_support(self, node: Node) -> bool:
        for distro in unsupported_distro:
            if distro in node.os._get_detect_string(node):
                self._log.info(f"{distro} is not supported! Test skipped")
                return False
        return True

    # For CentOS and RedHat, it is required to install LIS RPMs.
    if (
            "REDHAT" in node.os._get_detect_string(node) or
            "CENTOS" in node.os._get_detect_string(node)
        ):
        lis_rpm = install_lis_rpms(
            node.public_address, node.public_port, log=self.log, timeout=self.TIME_OUT)

    def validate_grid_install(self, node: Node) -> bool: 
        pass

    def validate_cuda_install() -> bool:
        pass

    def validate_gpu_adapter(self, node: Node) -> bool:
        pass


        