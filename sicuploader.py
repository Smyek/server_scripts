from ftpmanager import FTP
from random import randint
from os import listdir
import os
import webbrowser

class SICUploader:
    def __init__(self):
        self.ftp = FTP()
        self._sourcepath = "O:/smorozhenoe/cicecream/server/"
        self._serverpath = "/home/sicecream_vk/"
        self._serverTESTpath = "/home/sicecream_vk/test/"

        self.beta_test_success = False

    def console(self):
        while True:
            print('1: Initiate beta-testing sequence'
                '\n2: Upload beta'
                '\n3: Clear test folder on FTP'
                '\nrls: Release Update'
                '\n0: exit')
            choice = input('>>')
            if choice == '0':
                print('Have a nice day!')
                break
            elif choice == '1':
                self.initiate_test_sequence()
            elif choice == '2':
                self.upload_script()
            elif choice == '3':
                self.ssh_clear_beta()
                print("Test folder on ftp has been removed.")
            elif choice == 'rls':
                self.upload_release()

    def upload_release(self):
        if not self.beta_test_success:
            print("You haven't test an update")
            return False
        if not self.confirmation_release():
            print("Wrong confirmation code!..")
            return False
        print("Uploading release...")
        self.upload_script(is_test=False)
        self.ftp.upload("data/release_config.csv", self._serverpath + "data/config.csv")

    ##pre_process
    def upload_script(self, is_test=True):
        filelist = ["generation.py", "testmodule.py", "utils.py"] + self.dir_files(is_test)
        path = self._serverTESTpath if is_test else self._serverpath
        if is_test:
            self.ssh_make_beta_folders()

        print("uploading to " + path)
        for proj_file in filelist:
            print(self._sourcepath + proj_file, " >>> " , path + proj_file)
            # if os.path.isdir(self._sourcepath + proj_file):
            #     self.ssh_run_command("mkdir %s%s" % (self._serverpath, proj_file))
            self.ftp.upload(self._sourcepath + proj_file, path + proj_file)

    def dir_files(self, is_test):
        result_paths = []
        directories = ["data/", "service/"]
        if is_test: directories.append("data/userdata/")
        for directory in directories:
            directory_paths = [f for f in listdir(self._sourcepath + directory) if not os.path.isdir(self._sourcepath + directory + f)]
            result_paths += [directory + f for f in directory_paths]
        return result_paths

    def ensure_test_config(self):
        with open(self._sourcepath + "data/config.csv", "w", encoding="utf-8") as f:
            f.write("test_mode;True")

    def initiate_test_sequence(self):
        self.ensure_test_config()
        self.ssh_clear_beta()
        self.upload_script()
        self.ssh_run_beta()
        webbrowser.open_new_tab("https://vk.com/wall-125307022")
        self.beta_test_success = True


    ##ssh
    def ssh_make_beta_folders(self):
        folders = ["test", "test/data", "test/data/userdata", "test/service"]
        for folder in folders:
            self.ssh_run_command("mkdir %s%s" % (self._serverpath, folder))

    def ssh_run_beta(self):
        command = "cd %s && python2.7 generation.py" % (self._serverTESTpath)
        print(command)
        self.ssh_run_command(command)

    def ssh_clear_beta(self):
        command = "rm -rf %s" % (self._serverTESTpath)
        self.ssh_run_command(command)

    def ssh_run_command(self, command):
        stdin, stdout, stderr = self.ftp.sshclient.exec_command(command)
        data = stdout.read() + stderr.read()


    ##auxiliary
    def confirmation_release(self):
        pass_generated = "".join([str(randint(0,9)) for i in range(3)])
        confirm = input("Enter %s to proceed with release: " % pass_generated)
        if pass_generated == confirm:
            return True
        return False


if __name__ == "__main__":
    sic_uploader = SICUploader()
    sic_uploader.console()
    sic_uploader.ftp.close_connection()