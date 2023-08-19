# Example
# -------
#
#   script arguments demo

import logging
from pyats import aetest
from genie.testbed import load
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):
    # @aetest.subsection
    # def load_testbed(self, testbed):
    #     # Convert pyATS testbed to Genie Testbed
    #     logger.info(
    #         "Converting pyATS testbed to Genie Testbed to support pyATS Library features"
    #     )
    #     testbed = load(testbed)
    #     self.parent.parameters.update(testbed=testbed)

    @aetest.subsection
    def connect(self, testbed):
        """
        establishes connection to all your testbed devices.
        """
        # make sure testbed is provided
        assert testbed, "Testbed is not provided!"

        # connect to all testbed devices
        #   By default ANY error in the CommonSetup will fail the entire test run
        #   Here we catch common exceptions if a device is unavailable to allow test to continue
        try:
            testbed.connect()
        except (TimeoutError, StateMachineError, ConnectionError):
            logger.error("Unable to connect to all devices")


class verify_connected(aetest.Testcase):
    """verify_connected
    Ensure successful connection to all devices in testbed.
    """

    @aetest.test
    def test(self, testbed, steps):
        # Loop over every device in the testbed
        for device_name, device in testbed.devices.items():
            print(type(device))
            with steps.start(
                f"Test Connection Status of {device_name}", continue_=True
            ) as step:
                # Test "connected" status
                if device.connected:
                    logger.info(f"{device_name} connected status: {device.connected}")
                else:
                    logger.error(f"{device_name} connected status: {device.connected}")
                    step.failed()


class cpu(aetest.Testcase):
    """check cpu  consumption"""
    @aetest.setup
    def setup(self, testbed):
        self.processes = {}
        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            if device.os in ("ios", "iosxe", "iosxr", "nxos"):
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(f"getting procceses for {device_name}")
                self.processes[device_name] = device.parse('show processes cpu')

    @aetest.test
    def test(self, testbed, steps):
        for device_name, device in self.processes.items():
            with steps.start(
                f"Looking for CPU Stat on {device_name}", continue_=True
            ) as device_step:
                if device.get("five_min_cpu") > 80:
                    device_step.failed(
                        f'Device {device_name} five min cpu counter is above 80%')
                else:
                    device_step.passed(
                        f'Device {device_name} five min cpu counter is below 80%')

class memory(aetest.Testcase):
    """check cpu  consumption"""
    @aetest.setup
    def setup(self, testbed):
        self.processes = {}
        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            if device.os in ("ios", "iosxe", "iosxr", "nxos"):
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(f"getting procceses for {device_name}")
                self.processes[device_name] = device.parse('show memory statistics')

    @aetest.test
    def test(self, testbed, steps):
        for device_name, device in self.processes.items():
            with steps.start(
                f"Looking for Memory Stat on {device_name}", continue_=True
            ) as device_step:
                memory_usage_percent = (device['name']['processor']['used'] / device['name']['processor']['total'])*100
                if memory_usage_percent > 80:
                    device_step.failed(
                        f'Device {device_name} memory usage is above 80%')
                else:
                    device_step.passed(
                        f'Device {device_name} memory usage is below 80%')

# main()
if __name__ == "__main__":
    # for stand-alone execution
    import argparse
    from pyats import topology

    parser = argparse.ArgumentParser(description="standalone parser")
    parser.add_argument(
        "--testbed",
        dest="testbed",
        help="testbed YAML file",
        type=topology.loader.load,
        default=None,
    )

    # do the parsing
    args = parser.parse_known_args()[0]

    aetest.main(testbed=args.testbed)
