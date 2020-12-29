# Created by SezerBozkir<admin@sezerbozkir.com> at 10/18/2020
import paramiko
from paramiko import AutoAddPolicy
import yaml
import sub_utils.constants


# paramiko.util.log_to_file('paramiko.log')

class SSHClient:
    def __init__(self,
                 ip="192.168.1.113",
                 username="root",
                 password="1",
                 current_location='management'):
        self._ip = ip
        self._username = username
        self._password = password
        self._current_location = current_location

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(hostname=ip,
                            username=username,
                            password=password)
        self._sftp: paramiko.SFTPClient = self.client.open_sftp()

        if not self.sftp_exist(self._current_location):
            print(f"/root/{current_location} is not found. File creating.")
            self._sftp.chdir('/root')
            self._sftp.mkdir(self._current_location)

        self._sftp.chdir("/root/" + self._current_location)
        # self.check_and_install_docker()
        self._compose_yaml = sub_utils.constants.compose_baseline

    def send_command(self, command, show_output=True):
        response = ""
        stdin, stdout, stderr = self.client.exec_command(f"cd /root/{self._current_location}; {command}",
                                                         get_pty=True)
        for line in iter(stdout.readline, ""):
            if show_output:
                print(line, end="")
            response += line

        return response

    def check_and_install_docker(self):
        exist = True
        print("Docker status start to checking...")
        result = self.send_command("docker -v", show_output=False)
        if "Docker version" not in result:
            print("Docker is not installed. Installation started.")
            self.send_command("curl -fsSL https://get.docker.com -o get-docker.sh")
            self.send_command("sh get-docker.sh")
            exist = False
        result = self.send_command("docker-compose -v", show_output=False)
        if "docker-compose version " not in result:
            print("Docker-compose is not installed. Installation started.")
            self.send_command(
                """curl -L "https://github.com/docker/compose/releases/download/1.27.4/""" +
                """docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose""")
            self.send_command("chmod +x /usr/local/bin/docker-compose")
            exist = False
        if exist:
            print("Docker and/or docker-compose already exist.Installation process skipping.")
        else:
            print("Docker and/or docker-compose installed successfully.")

    def change_current_directory(self, directory):
        self._current_location = directory
        self._sftp.chdir("/root/" + directory)

    def _create_directory(self, directory):
        self._sftp.mkdir(self._current_location + "/" + directory)

    def sftp_exist(self, path):
        try:
            self._sftp.stat(path)
            return True
        except FileNotFoundError:
            return False

    def create_yaml(self):
        try:
            with open("docker-compose.yml", "w") as file:
                yaml.dump(self._compose_yaml, file, sort_keys=False)
        except Exception as e:
            print("Error while create docker-compose.yml", e)

    def add_service(self, service: str):
        if service.lower() == 'mysql':
            self._compose_yaml['services'].update(sub_utils.constants.mysql)
        elif service.lower() == 'redis':
            print("Coming soon")
        else:
            print("This service not implemented yet.")

    def remove_service(self, service):
        if service in self._compose_yaml['services'].keys():
            for service_name in sub_utils.constants.mysql.keys():
                del self._compose_yaml['services'][service_name]
        else:
            print("Service not found")

    def __del__(self):
        print("Connection closed.")
        self.client.close()
