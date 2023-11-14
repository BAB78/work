def configure_syslog(ip, username, password, enable_password):
    try:
        # Establish an SSH connection to configure syslog
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)

        # Command list to generate a 2048-bit RSA key for SSH
        command_list = [
            'configure terminal',
            'crypto key generate rsa modulus 2048',  # Generating a 2048-bit RSA key
            'end',
            'write memory'
        ]

        # Execute commands only if the SSH connection is active
        if ssh.get_transport() is not None and ssh.get_transport().is_active():
            for command in command_list:
                ssh.exec_command(command)

            ssh.close()
            print(f"RSA key (2048-bit) generated successfully for SSH on {ip}")
        else:
            print("SSH connection is not active.")
    except Exception as e:
        print(f"Failed to generate RSA key: {e}")
