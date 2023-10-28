# Display heading
print('')
print('Devices with bad software versions')
print('----------------------------------')

# Set Variable for current version comparison used in Step 4
current_version = 'Version 5.3.1'

# Open the file devices-06.txt for reading and for each device enter the information into a list.
# Read all lines of device information from file
file = open('devices-06.txt', 'r')

for line in file:
    # Put device info into list
    device_info_list = line.strip().split(',')

    # For each device, take the device information and put it into a dictionary
    # with fields for name, os-type, ipaddress, version, username, and password.
    device_info = {}  # Create the inner dictionary of device info
    device_info['name'] = device_info_list[0]
    device_info['ip'] = device_info_list[2]
    device_info['version'] = device_info_list[3]

    # For each device, compare the version to see if it is out of date,
    # using a simple comparison of the string. Display a table of devices
    # whose version does not match the given 'current version' 5.3.1.
    if device_info['version'] != current_version:
        print('Device:', device_info['name'], 'Version:', device_info['version'])

# Close the file
file.close()
