# Created by SezerBozkir<admin@sezerbozkir.com> at 10/18/2020
import yaml


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
    # server = SSHClient()
    # sonuc = server.send_command('pwd', show_output=False)
    mysql = {"version": "3",
             "services": {
                 "mysql": {
                     "container_name": "traveler_app_db",
                     "restart": "always",
                     "image": "mysql:latest",
                     "ports": [
                         "3306:3306"
                     ],
                     "environment": {
                         "MYSQL_ROOT_PASSWORD": "burayi_degistir"  # TODO make it dynamic
                     },
                     "volumes": [
                         "/root/management/mysql/data:/var/lib/mysql"  # TODO make it dynamic
                     ]
                 },
                 "app": {
                     "depends_on": ["mysql"],
                     "image": "phpmyadmin/phpmyadmin",
                     "container_name": "phpmyadmin",  # TODO make it dynamic
                     "restart": "always",
                     "ports": ["3307:80"],
                     "environment": {
                         "PMA_HOST": "mysql"
                     }
                 }
             }
             }
    with open("sample.yaml", "w") as file:
        output = yaml.dump(mysql, file)
