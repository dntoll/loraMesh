from ftplib import FTP
from os import walk
import secrets
import threading
import telnetlib


class Telnet:
    def __init__(self, clientIP, username, password, command):
        HOST = clientIP
        user = username
        password = password

        try:
            with telnetlib.Telnet(HOST, 23) as tn:
                print("telnet reset...", flush=True)
                tn.read_until(b"Login as: ")
                tn.write(user.encode('ascii') + b"\r\n")
                if password:
                    tn.read_until(b"Password:", timeout=1)
                    tn.write(password.encode('ascii') + b"\r\n")

                tn.read_until(b">>>", timeout=1)
                tn.write(command + b"\r\n")
                tn.close()
                print("telnet closed", flush=True)
        except:
            print("Something went wrong telnetting to " +clientIP )


class FTPPusher:
    def __init__(self, clientIP, username, password):
        self.clientID = clientIP
        self.username = username
        self.password = password

        t = threading.Thread(target=FTPPusher.push, args=(self, self), daemon=False)
        t.start() 

    def _pushAllPyFiles(ftp, dirpath, filenames):
        for fileName in filenames:
            if ".py" in fileName:
                disallowedFiles = ["test_", "release_"]
                doIncludeFile = True
                for notAllowed in disallowedFiles:
                    if notAllowed in fileName:
                        doIncludeFile = False

                if doIncludeFile:
                    completePath = dirpath + "\\" + fileName
                    with open(completePath, "rb") as fp:
                        ftp.storbinary("STOR " + fileName, fp)
                    print("Wrote: " + completePath + " to device ", flush=True)

    def push(this, that):
        try:
            with FTP(this.clientID, timeout=10) as ftp:
                mypath = "."
                ftp.login(user=this.username, passwd=this.password)
                ftp.cwd('flash')

                for (dirpath, dirnames, filenames) in walk(mypath):
                    disallowedFolders = [".\.git", "__pycache__", "simulator", ".pytest_cache"]

                    doIncludeFolder = True
                    for notAllowed in disallowedFolders:
                        if notAllowed in dirpath:
                            doIncludeFolder = False

                    if doIncludeFolder:
                        print("Dirpath:" + dirpath)
                        if "." == dirpath:
                            FTPPusher._pushAllPyFiles(ftp, dirpath, filenames)
                        elif ".\\" in dirpath: #dont push .git
                            dirName = dirpath[2:]
                            onDeviceDirName = 'flash' + "/" + dirName

                            ftp.cwd("..") # step out of flash
                            try:
                                ftp.mkd(onDeviceDirName)
                                print("mkdir " + onDeviceDirName)
                            except:
                                print("dir exists")

                            ftp.cwd(onDeviceDirName)
                            FTPPusher._pushAllPyFiles(ftp, dirpath, filenames)
                            ftp.cwd("..") #step out to flash
                ftp.close()
            a = Telnet(this.clientID,this.username, this.password, b"machine.reset()")
        except:
            print("FTP Exception on client " + this.clientID)
        
        
            




for client in secrets.clients:
    print("Connecting to " + client, flush=True)
    f = FTPPusher(client, secrets.userName, secrets.passwd)
