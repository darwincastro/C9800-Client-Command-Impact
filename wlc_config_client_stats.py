import re
import time
from pyats import aetest
from genie.testbed import load
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Optional

class ShowWirelessClientMacDetailSchema(MetaParser):
    schema = {
        'client_join_time': str,
    }

class ShowWirelessClientMacDetail(ShowWirelessClientMacDetailSchema):
    """Parser for 'show wireless client mac {mac_address} detail'"""

    show_command = 'show wireless client mac {mac_address} detail'

    def cli(self, mac_address="", output=None):
        if output is None:
            cmd = self.show_command.format(mac_address=mac_address)
            output = self.device.execute(cmd)
        else:
            output = output

        parsed_dict = {}
        # Client Join Time:
        p0 = re.compile(r'^Join Time Of Client : (?P<client_join_time>.+)$')

        for line in output.splitlines():
            line = line.strip()

            m = p0.match(line)
            if m:
                parsed_dict['client_join_time'] = m.groupdict()['client_join_time']

        return parsed_dict


class WirelessClientTest(aetest.Testcase):
    @aetest.setup
    def setup(self):
        # Load the testbed YAML file
        self.testbed = load('testbed.yaml')
        # Connect to the device
        self.device = self.testbed.devices['9800-l']
        self.device.connect()
        # Parse the initial client join time
        self.parser = ShowWirelessClientMacDetail(device=self.device)
        self.initial_join_time = self.parser.cli(mac_address="aaaa.bbbb.cccc")['client_join_time']

    @aetest.test
    def apply_configuration_and_check_client(self):
        # Apply the configuration
        self.device.configure([
            'no radius server <name of radius server>',
            'end'
        ])

        # Check the client join time again until client is present
        current_join_time = None
        while not current_join_time:
            try:
                current_join_time = self.parser.cli(mac_address="aaaa.bbbb.cccc")['client_join_time']
            except KeyError:
                time.sleep(10)

        # If the join time has changed, the test fails
        if self.initial_join_time != current_join_time:
            self.failed(f"Client join time changed from {self.initial_join_time} to {current_join_time}")
        else:
            self.passed(f"Client join time remained the same: {self.initial_join_time}")

    @aetest.cleanup
    def cleanup(self):
        # Disconnect from the device
        self.device.disconnect()


if __name__ == '__main__':
    aetest.main()