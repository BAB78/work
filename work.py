import paramiko
import difflib
import os

# Define variables for the menu options
option_1 = "Telnet"
option_2 = "SSH"
option_3 = "Compare with startup configuration"
option_4 = "Compare with local offline version"
option_5 = "Compare with Cisco device hardening advice"
option_6 = "Configure syslog for event logging and monitoring"
option_7 = "Exit"

# Define the IP address of the device to connect to
ip_address = "192.168.0.1"

# Define the username and password for the device
username = "admin"
password = "password"

# Define the enable password for the device
enable_password = "EnablePassword123"

# Define the path to the hardening advice file
hardening_advice_file = "/path/to/cisco/hardening/advice.txt"

# Define a function for connecting to the device using Telnet
def telnet_connection():
    try:
        telnet = paramiko.Telnet(ip_address, username=username, password=password)
        return telnet
    except Exception as e:
        print(f"Error connecting to {ip_address} via Telnet: {e}")

# Define a function for connecting to the device using SSH
def ssh_connection():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address, username=username, password=password)
        return ssh
    except Exception as e:
        print(f"Error connecting to {ip_address} via SSH: {e}")

# Define a function for comparing configurations
def compare_configurations(config1, config2):
    diff = difflib.ndiff(config1.splitlines(), config2.splitlines())
    return '\n'.join(diff)

# Define a function to get the running configuration
def get_running_configuration(connection):
    try:
        if isinstance(connection, paramiko.Telnet):
            connection.write(b"show running-config\n")
            running_config = connection.read_very_eager().decode("utf-8")
            return running_config
        elif isinstance(connection, paramiko.SSHClient):
            stdin, stdout, stderr = connection.exec_command("show running-config")
            running_config = stdout.read().decode("utf-8")
            return running_config
        else:
            return None
    except Exception as e:
        print(f"Error getting running configuration: {e}")
        return None

# Define a function to get the startup configuration
def get_startup_configuration(connection):
    try:
        if isinstance(connection, paramiko.Telnet):
            connection.write(b"show startup-config\n")
            startup_config = connection.read_very_eager().decode("utf-8")
            return startup_config
        elif isinstance(connection, paramiko.SSHClient):
            stdin, stdout, stderr = connection.exec_command("show startup-config")
            startup_config = stdout.read().decode("utf-8")
            return startup_config
        else:
            return None
    except Exception as e:
        print(f"Error getting startup configuration: {e}")
        return None

# Define a function for comparing the current running configuration with the startup configuration
def compare_with_startup_config():
    telnet = telnet_connection()
    ssh = ssh_connection()
    running_config_telnet = get_running_configuration(telnet)
    running_config_ssh = get_running_configuration(ssh)
    startup_config_telnet = get_startup_configuration(telnet)
    startup_config_ssh = get_startup_configuration(ssh)
    
    diff_telnet = compare_configurations(running_config_telnet, startup_config_telnet)
    diff_ssh = compare_configurations(running_config_ssh, startup_config_ssh)

    print("Telnet Comparison with Startup Configuration:")
    print(diff_telnet)
    print("\nSSH Comparison with Startup Configuration:")
    print(diff_ssh)

# Define a function for comparing the current running configuration with a local offline version
def compare_with_local_offline_version():
    try:
        with open("local_offline_config.txt", "r") as file:
            local_config = file.read()

        telnet = telnet_connection()
        ssh = ssh_connection()
        running_config_telnet = get_running_configuration(telnet)
        running_config_ssh = get_running_configuration(ssh)

        diff_telnet = compare_configurations(running_config_telnet, local_config)
        diff_ssh = compare_configurations(running_config_ssh, local_config)

        print("Telnet Comparison with Local Offline Version:")
        print(diff_telnet)
        print("\nSSH Comparison with Local Offline Version:")
        print(diff_ssh)
    except Exception as e:
        print(f"Error comparing with local offline version: {e}")

# Define a function for comparing the current running configuration with Cisco device hardening advice
def compare_with_hardening_advice():
    try:
        with open(hardening_advice_file, "r") as file:
            advice = file.read()

        telnet = telnet_connection()
        ssh = ssh_connection()
        running_config_telnet = get_running_configuration(telnet)
        running_config_ssh = get_running_configuration(ssh)

        diff_telnet = compare_configurations(running_config_telnet, advice)
        diff_ssh = compare_configurations(running_config_ssh, advice)

        print("Telnet Comparison with Hardening Advice:")
        print(diff_telnet)
        print("\nSSH Comparison with Hardening Advice:")
        print(diff_ssh)
    except FileNotFoundError as e:
        print(f"Error reading hardening advice file: {e}")
    except Exception as e:
        print(f"Error comparing with hardening advice: {e}")

# Define a function for configuring syslog for event logging and monitoring
def configure_syslog():
    try:
        syslog_server_ip = input("Enter the IP of the syslog server: ")
        ssh = ssh_connection()
        stdin, stdout, stderr = ssh.exec_command(f"logging {syslog_server_ip}")
        print("Syslog configuration completed successfully.")
    except Exception as e:
        print(f"Error configuring syslog: {e}")

# Define a function for displaying the menu and executing the selected option
def display_menu():
    while True:
        print("\nMenu:")
        print(f"{option_1}: Telnet")
        print(f"{option_2}: SSH")
        print(f"{option_3}: Compare with startup configuration")
        print(f"{option_4}: Compare with local offline version")
        print(f"{option_5}: Compare with Cisco device hardening advice")
        print(f"{option_6}: Configure syslog for event logging and monitoring")
        print(f"{option_7}: Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == option_1:
            telnet_connection()
        elif choice == option_2:
            ssh_connection()
        elif choice == option_3:
            compare_with_startup_config()
        elif choice == option_4:
            compare_with_local_offline_version()
        elif choice == option_5:
            compare_with_hardening_advice()
        elif choice == option_6:
            configure_syslog()
        elif choice == option_7:
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

# Main execution
display_menu()
