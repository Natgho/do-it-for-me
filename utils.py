# Created by SezerBozkir<admin@sezerbozkir.com> at 10/18/2020
import paramiko
from paramiko import AutoAddPolicy


# paramiko.util.log_to_file('paramiko.log')

class SSHClient:
    def __init__(self,
                 ip="192.168.1.113",
                 username="root",
                 password="1",
                 current_location='management'):
        self.ip = ip
        self.username = username
        self.password = password
        self.current_location = current_location

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(hostname=ip,
                            username=username,
                            password=password)
        self.sftp: paramiko.SFTPClient = self.client.open_sftp()
        try:
            self.sftp.stat(self.current_location)
        except IOError as exception:
            print(f"/root/{current_location} is not found. File creating.")
            self.sftp.chdir('/root')
            self.sftp.mkdir(self.current_location)
        self.sftp.chdir("/root/" + self.current_location)
        self.check_and_install_docker()

    def send_command(self, command, show_output=True):
        response = ""
        stdin, stdout, stderr = self.client.exec_command(f"cd /root/{self.current_location}; {command}",
                                                         get_pty=True)
        for line in iter(stdout.readline, ""):
            if show_output:
                print(line, end="")
            response += line

        return response

    def check_and_install_docker(self):
        print("Docker status start to checking...")
        result = self.send_command("docker -v", show_output=False)
        if "Docker version" not in result:
            print("Docker is not installed. Installation started.")
            self.send_command("curl -fsSL https://get.docker.com -o get-docker.sh")
            self.send_command("sh get-docker.sh")
        result = self.send_command("docker-compose -v", show_output=False)
        if "docker-compose version " not in result:
            print("Docker-compose is not installed. Installation started.")
            self.send_command(
                """curl -L "https://github.com/docker/compose/releases/download/1.27.4/""" +
                """docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose""")
            self.send_command("chmod +x /usr/local/bin/docker-compose")
        print("Docker and/or docker-compose installed successfully.")

    def change_current_directory(self, directory):
        self.current_location = directory
        self.sftp.chdir("/root/" + directory)

    def create_directory(self, directory):
        self.sftp.mkdir(self.current_location + "/" + directory)
