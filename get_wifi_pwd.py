# Allows us to use system commands
import subprocess
# Allows us to make regular expressions
import re

# Shows us all wifi profiles stored in computer
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()
# Extract profile names using pattern search
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
wifi_list = list()

if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = dict()
        # Show us particular wifi profile info
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()
        # If it does not have a security key that means wifi is open
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name
            # Use key=clear to clear Key Content and get password
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
            # Extract password using pattern matching
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            if password is None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
            wifi_list.append(wifi_profile)

# Display all wifi profiles
for x in range(len(wifi_list)):
    print(wifi_list[x])

