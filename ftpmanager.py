import paramiko
import time


class FTP:
    def __init__(self):
        self.host_port = ("192.168.1.100", 22)
        self.username = "root"
        self.try_connect()

        #self.connection_timeout()

    def try_connect(self):
        self.transport = paramiko.Transport(self.host_port)
        pswd = input('Password:')

        self.transport.connect(username=self.username, password=pswd)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        self.ssh_autoconnect(pswd)


    def ssh_autoconnect(self, pswd):
        self.sshclient = paramiko.SSHClient()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshclient.connect(hostname=self.host_port[0], username=self.username, password=pswd, port=self.host_port[1])

    def close_connection(self):
        self.sftp.close()
        self.transport.close()
        self.sshclient.close()

    def connection_timeout(self):
        time_secs = 15
        time.sleep(time_secs)
        self.close_connection()
        print("Connection closed after %s seconds idle." % time_secs)

    def download(self, filepath, localpath):
        self.sftp.get(filepath, localpath)
        #print("File successfully downloaded")

    def upload(self, localpath, filepath):
        self.sftp.put(localpath, filepath)
        #print("File successfully uploaded")


if __name__ == "__main__":
    ftp = FTP()
    #ftp.upload("test.txt", "/home/sicecream_vk/test.txt")
    ftp.close_connection()