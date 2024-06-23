# C9800-Client-Command-Impact

This Python script was initially created to assist in running CLI commands on a Cisco Catalyst 9800 wireless controller, with the primary goal of determining which commands were disruptive to wireless clients. 

The script uses the pyATS library for network automation and the Genie library for parsing CLI outputs. It specifically parses the output of the `show wireless client mac {mac_address} detail` command on a C9800 device. This command provides detailed information about a specific wireless client identified by its MAC address.

By monitoring the 'Join Time' of a wireless client, the script can check if the client's connection was disrupted after applying specific configurations or commands. If the client's 'Join Time' changes, it indicates that the client was disconnected and had to rejoin, suggesting that the applied command was potentially disruptive. This monitoring process allows network administrators to better understand the impact of specific configurations or commands on the connectivity of wireless clients.

The script is especially useful in a testing environment, where its automated and continuous monitoring capabilities can save time and provide more consistent and reliable results compared to manual monitoring.

**Disclaimer:** This script is not officially endorsed or provided by Cisco Systems. It is created and maintained by me. The use of this script is at your own risk. The script is provided "as is" without warranty of any kind, either expressed or implied, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose.

## Features
- **Command Parsing:** The script parses the output of show wireless client mac {mac_address} detail using regex and extracts the client join time.
- **Configuration Application:** It applies a specific configuration (in this example; removing a RADIUS server) on a device.
- **Continuous Checking:** The script continuously checks the client join time until the client is present.
- **Status Verification:** It verifies if the client join time has changed after applying the configuration. If the join time changes, the test fails. If it stays the same, the test passes.

## Usage
1. Load your testbed YAML file.
2. Connect to your device.
3. Instantiate the ShowWirelessClientMacDetail class.
4. Call the cli() method, passing the MAC address of the client whose details you want.
5. The method will return a dictionary with the client join time.
6. You can then use this information as needed, for example, to verify the status of a client after applying a specific configuration.

## Dependencies
This script uses the following Python libraries:

- **re** for regular expressions.
- **time** to introduce delay between multiple checks.
- **pyATS** for network automation.
- **genie.testbed** for loading testbed YAML file.
- **genie.metaparser** and **genie.metaparser.util.schemaengine** for parsing the command output.

To run this script, make sure you have these libraries installed in your Python environment. If not, you can install them using pip:

```
pip install pyats genie
```

## Example 

### Passing Test

As an example of how this script might be used, consider a scenario where we are removing the RADIUS server configuration from the WLC. In this scenario, our wireless client is connected via 802.1X. After running the script and applying the configuration changes, we see the test result as "pass". This indicates that the client did not get disconnected after the removal of the RADIUS server configuration, suggesting that this command was not disruptive to the client;
```
2024-02-20T15:58:31: %AETEST-INFO: Passed reason: Client join time remained the same: 02/20/2024 20:04:37 Central
2024-02-20T15:58:31: %AETEST-INFO: The result of section apply_configuration_and_check_client is => PASSED
2024-02-20T15:58:31: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-20T15:58:31: %AETEST-INFO: |                           Starting section cleanup                           |
2024-02-20T15:58:31: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-20T15:58:42: %AETEST-INFO: The result of section cleanup is => PASSED
2024-02-20T15:58:42: %AETEST-INFO: The result of testcase WirelessClientTest is => PASSED
2024-02-20T15:58:42: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-20T15:58:42: %AETEST-INFO: |                               Detailed Results                               |
2024-02-20T15:58:42: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-20T15:58:42: %AETEST-INFO:  SECTIONS/TESTCASES                                                      RESULT   
2024-02-20T15:58:42: %AETEST-INFO: --------------------------------------------------------------------------------
2024-02-20T15:58:42: %AETEST-INFO: .
2024-02-20T15:58:42: %AETEST-INFO: `-- WirelessClientTest                                                    PASSED
2024-02-20T15:58:42: %AETEST-INFO:     |-- setup                                                             PASSED
2024-02-20T15:58:42: %AETEST-INFO:     |-- apply_configuration_and_check_client                              PASSED
2024-02-20T15:58:42: %AETEST-INFO:     `-- cleanup                                                           PASSED
2024-02-20T15:58:42: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-20T15:58:42: %AETEST-INFO: |                                   Summary                                    |
2024-02-20T15:58:42: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-20T15:58:42: %AETEST-INFO:  Number of ABORTED                                                            0 
2024-02-20T15:58:42: %AETEST-INFO:  Number of BLOCKED                                                            0 
2024-02-20T15:58:42: %AETEST-INFO:  Number of ERRORED                                                            0 
2024-02-20T15:58:42: %AETEST-INFO:  Number of FAILED                                                             0 
2024-02-20T15:58:42: %AETEST-INFO:  Number of PASSED                                                             1 
2024-02-20T15:58:42: %AETEST-INFO:  Number of PASSX                                                              0 
2024-02-20T15:58:42: %AETEST-INFO:  Number of SKIPPED                                                            0 
2024-02-20T15:58:42: %AETEST-INFO:  Total Number                                                                 1 
2024-02-20T15:58:42: %AETEST-INFO:  Success Rate                                                            100.0% 
2024-02-20T15:58:42: %AETEST-INFO: --------------------------------------------------------------------------------
```

### Failing Test

In another scenario, we disable and then enable the wireless policy profile of the AP to which the wireless client is connected. This is a more significant change that directly impacts the wireless environment of the client. After running the script in this scenario, we see the test result as "fail". This indicates that the client did get disconnected after the change, suggesting that disabling and re-enabling the wireless policy profile is disruptive to the client. Hence, network administrators and engineers should be cautious when applying such changes in a live network environment.

```
2024-02-20T17:47:44: %AETEST-ERROR: Failed reason: Client join time changed from 02/20/2024 23:46:58 Central to 02/20/2024 23:47:33 Central
2024-02-20T17:47:44: %AETEST-INFO: The result of section apply_configuration_and_check_client is => FAILED
2024-02-20T17:47:44: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-20T17:47:44: %AETEST-INFO: |                           Starting section cleanup                           |
2024-02-20T17:47:44: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-20T17:47:55: %AETEST-INFO: The result of section cleanup is => PASSED
2024-02-20T17:47:55: %AETEST-INFO: The result of testcase WirelessClientTest is => FAILED
2024-02-20T17:47:55: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-20T17:47:55: %AETEST-INFO: |                               Detailed Results                               |
2024-02-20T17:47:55: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-20T17:47:55: %AETEST-INFO:  SECTIONS/TESTCASES                                                      RESULT   
2024-02-20T17:47:55: %AETEST-INFO: --------------------------------------------------------------------------------
2024-02-20T17:47:55: %AETEST-INFO: .
2024-02-20T17:47:55: %AETEST-INFO: `-- WirelessClientTest                                                    FAILED
2024-02-20T17:47:55: %AETEST-INFO:     |-- setup                                                             PASSED
2024-02-20T17:47:55: %AETEST-INFO:     |-- apply_configuration_and_check_client                              FAILED
2024-02-20T17:47:55: %AETEST-INFO:     `-- cleanup                                                           PASSED
2024-02-20T17:47:55: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-20T17:47:55: %AETEST-INFO: |                                   Summary                                    |
2024-02-20T17:47:55: %AETEST-INFO: +------------------------------------------------------------------------------+
2024-02-20T17:47:55: %AETEST-INFO:  Number of ABORTED                                                            0 
2024-02-20T17:47:55: %AETEST-INFO:  Number of BLOCKED                                                            0 
2024-02-20T17:47:55: %AETEST-INFO:  Number of ERRORED                                                            0 
2024-02-20T17:47:55: %AETEST-INFO:  Number of FAILED                                                             1 
2024-02-20T17:47:55: %AETEST-INFO:  Number of PASSED                                                             0 
2024-02-20T17:47:55: %AETEST-INFO:  Number of PASSX                                                              0 
2024-02-20T17:47:55: %AETEST-INFO:  Number of SKIPPED                                                            0 
2024-02-20T17:47:55: %AETEST-INFO:  Total Number                                                                 1 
2024-02-20T17:47:55: %AETEST-INFO:  Success Rate                                                              0.0% 
2024-02-20T17:47:55: %AETEST-INFO: --------------------------------------------------------------------------------
```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

