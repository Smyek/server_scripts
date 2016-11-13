from ftpmanager import FTP
from random import randint
from os import listdir

class SICUploader:
    def __init__(self):
        self.ftp = FTP()
        self._sourcepath = "O:/smorozhenoe/cicecream/server/"
        self._serverpath = "/home/sicecream_vk/"
        self._serverTESTpath = "/home/sicecream_vk/test/"

    def console(self):
        pass

    def upload_script(self, is_test=True):
        datafiles = ["data/" + f for f in listdir(self._sourcepath + "data/")]
        filelist = ["generation.py"] + datafiles
        path = self._serverTESTpath if is_test else self._serverpath
        if is_test:
            self.ssh_make_beta_folders()

        print("uploading to " + path)
        for proj_file in filelist:
            print(self._sourcepath + proj_file, " >>> " , path + proj_file)
            self.ftp.upload(self._sourcepath + proj_file, path + proj_file)

    def ssh_make_beta_folders(self):
        folders = ["test", "test/data"]
        for folder in folders:
            self.ssh_run_command("mkdir %s%s" % (self._serverpath, folder))

    def ssh_run_beta(self):
        command = "cd %s && python2.7 generation.py" % (self._serverTESTpath)

    def ssh_clear_beta(self):
        command = "rm -rf %s" % (self._serverTESTpath)
        self.ssh_run_command(command)

    def ssh_run_command(self, command):
        stdin, stdout, stderr = self.ftp.sshclient.exec_command(command)
        data = stdout.read() + stderr.read()

    def confirmation_release(self):
        pass_generated = "".join([randint(0,9) for i in range(3)])
        confirm = input("Enter %s to procced with release: ")
        if pass_generated == confirm:
            return True
        return False


if __name__ == "__main__":
    sic_uploader = SICUploader()
    sic_uploader.ssh_clear_beta()
    sic_uploader.ftp.close_connection()