# Created by SezerBozkir<admin@sezerbozkir.com> at 10/18/2020
import yaml
from utils import SSHClient

if __name__ == '__main__':
    # client = paramiko.SSHClient()
    # client.set_missing_host_key_policy(AutoAddPolicy())
    # client.connect('192.168.1.113', username='root', password='1')
    # sftp: paramiko.SFTPClient = client.open_sftp()
    # stdin, stdout, stderr = client.exec_command('ls', get_pty=True)
    # for line in iter(stdout.readline, ""):
    #     print(line, end="")
    # resp = stdout.readlines()
    # print(resp)
    server = SSHClient(ip="192.168.1.113",
                       username="root",
                       password="1",
                       current_location='management')
    # sonuc = server.send_command('pwd', show_output=False)
    server.add_service('mysql')
    server.remove_service('mysql')
    server.create_yaml()
