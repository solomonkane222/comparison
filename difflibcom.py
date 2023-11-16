import re
from netmiko import ConnectHandler
import getpass
import difflib

def compare_configurations(running_config_file, startup_config_file):
    #This will compare the running and startup configurations
    with open(running_config_file, 'r') as running_file, open(startup_config_file, 'r') as startup_file:
        running_lines = running_file.readlines()
        startup_lines = startup_file.readlines()

    #Importing difflib. This will be used to find differences in files.
    differ = difflib.Differ()
    diff = list(differ.compare(startup_lines , running_lines ))

    # Create a comparison_results file and save the differences
    with open('comparison_results.txt', 'w') as results_file:
        results_file.write('Differences between running and startup configurations:\n')
        for line in diff:
            if line.startswith('  '):
                continue  # Skip lines that are identical in both configurations
            elif line.startswith('- '):
                results_file.write(f'Removed: {line[2:]}\n')
            elif line.startswith('+ '):
                results_file.write(f'Added: {line[2:]}\n')

    return 'comparison_results.txt'

def compare_configurations2(running_config_file, devices_file):
    # Compare the running and startup configurations
    devices_file_txt = 'devices-05.txt'
    with open(running_config_file, 'r') as running_file, open(devices_file_txt, 'r') as devices_file:
        running_lines = running_file.readlines()
        devices_lines = devices_file.readlines()

    differ = difflib.Differ()
    diff = list(differ.compare(devices_lines , running_lines ))

    # Create a comparison_results file and save the differences
    with open('comparison_results2.txt', 'w') as results_file2:
        results_file2.write('Differences between devices and running configurations:\n')
        for line in diff:
            if line.startswith('  '):
                continue  # Skip lines that are identical in both configurations
            elif line.startswith('- '):
                results_file2.write(f'Removed: {line[2:]}\n')
            elif line.startswith('+ '):
                results_file2.write(f'Added: {line[2:]}\n')

    return 'comparison_results2.txt'

# Define device parameters
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': getpass.getpass('Enter Username: '),  # Use getpass for username input, username = prne
    'password': getpass.getpass('Enter Device Password: '),  # Use getpass for password input, password = cisco123!
    'secret': getpass.getpass('Enter Secret Phrase for the Device: '),  # class123! = secret phrase
}

# Connect to the device
try:
    connection = ConnectHandler(**device)
except Exception as e:
    print(f'Failed to connect to {device["ip"]}: {e}')
    exit()

# Enter enable mode
connection.enable()

#This will configure the hostname to 'Router3'.
config_commands = ['hostname Router3']
output = connection.send_config_set(config_commands)

#This will save the running configuration to a file locally and automatically. 
running_config_file = 'running_config.txt'
running_config = connection.send_command('show running-config')
with open(running_config_file, 'w') as output_file:
    output_file.write(running_config)

# This will save the startup configuration to a file locally and automatically. 
startup_config_file = 'startup_config.txt'
startup_config = connection.send_command('show startup-config')
with open(startup_config_file, 'w') as output_file:
    output_file.write(startup_config)

#The running and startup configurations will be compared and saved.
results_file = compare_configurations(running_config_file, startup_config_file)

results_file2 = compare_configurations2(running_config_file, 'devices-05.txt')

# Display a success message - for a successful connection.
print('------------------------------------------------------')
print('')
print(f'Successfully connected to IP address: {device["ip"]}')
print(f'Username: {device["username"]}')
print('Password: ********')  # Masking the password for security
print(f'Hostname: Router3')
print(f'Running Configuration saved to: {running_config_file}')
print(f'Startup Configuration saved to: {startup_config_file}')
print(f'Comparison results saved to: {results_file}')
print(f'Comparison results saved to: {results_file2}')
print('')
print('------------------------------------------------------')

# Disconnect from the device
connection.disconnect()
