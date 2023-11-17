# Function to compare with hardening advice 
def compare_with_hardening_advice():
  print("Comparing running config with hardening advice...")
  
  with open('hardening_advice.txt', 'r') as f:
    hardening_advice = f.read()

  running_config = get_running_config()

  diff = difflib.unified_diff(running_config.splitlines(), hardening_advice.splitlines())

  print('\n'.join(diff))

# Function to configure syslog
def configure_syslog(ip, username, passwd, enable_pwd):
  print("Configuring syslog...")

  tn.write(b'logging 192.168.1.100\n')  
  tn.write(b'logging buffered debugging\n')

  tn.write(b'wr\n')

  print("Syslog configured successfully.")

# Helper function
def get_running_config():
  return telnet_session(ip, username, passwd, enable_pwd, 'show run') 

# Existing functions...

# In display_menu()

elif choice == '5':
  compare_with_hardening_advice()

elif choice == '6':
  configure_syslog(ip, username, password, enable_password)

# Rest of display_menu()...
