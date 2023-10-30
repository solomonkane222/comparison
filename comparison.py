import re
from netmiko import ConnectHandler
import getpass 

# Define device parameters
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': getpass.getpass('Enter Username (e.g., prne): '),  # Use getpass for username input
    'password': getpass.getpass('Enter Password (e.g., cisco123!): '),  # Use getpass for password input
    'secret': 'class123!', #class123! = secret password
}

# Connect to the device
try:
    connection = ConnectHandler(**device)
except Exception as e:
    print(f'Failed to connect to {device["ip"]}: {e}')
    exit()

# Enter enable mode
connection.enable()

# Configuring the hostname to Router3
config_commands = ['hostname Router3']
output = connection.send_config_set(config_commands)

# Save the running configuration to a file
running_config_file = 'running_config.txt'
running_config = connection.send_command('show running-config')
with open(running_config_file, 'w') as output_file:
    output_file.write(running_config)

# Save the startup configuration to a file
startup_config_file = 'startup_config.txt'
startup_config = connection.send_command('show startup-config')
with open(startup_config_file, 'w') as output_file:
    output_file.write(startup_config)

# Compare the running and startup configurations
with open(running_config_file, 'r') as running_file, open(startup_config_file, 'r') as startup_file:
    running_lines = running_file.readlines()
    startup_lines = startup_file.readlines()

# Compare line by line or use difflib to find differences

# Display a success message - for a successful connection.
print('------------------------------------------------------')
print('')
print(f'Successfully connected to IP address: {device["ip"]}')
print(f'Username: {device["username"]}')
print('Password: ********')  # Masking the password for security
print('Hostname: Router3')
print(f'Running Configuration saved to: {running_config_file}')
print(f'Startup Configuration saved to: {startup_config_file}')
print('')
print('------------------------------------------------------')

# Disconnect from the device
connection.disconnect()
