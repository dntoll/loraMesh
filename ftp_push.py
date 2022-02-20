from ftplib import FTP
from os import walk
import secrets
import threading


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
                    if not ".\.git" in dirpath and not "__pycache__" in dirpath and not "simulator" in dirpath:
                        print("Dirpath:" + dirpath)
                        if "." == dirpath:
                            FTPPusher._pushAllPyFiles(ftp, dirpath, filenames)

                            #ftp.dir()
                        elif ".\\" in dirpath: #dont push .git
                            
                            dirName = dirpath[2:]
                            onDeviceDirName = 'flash' + "/" + dirName
                            print("path: " + onDeviceDirName)

                            ftp.cwd("..") # step out of flash
                            try:
                                ftp.mkd(onDeviceDirName)
                                print("mkdir " + onDeviceDirName)
                            except:
                                print("dir exists")

                            print("cd " + onDeviceDirName)
                            ftp.cwd(onDeviceDirName)
                            FTPPusher._pushAllPyFiles(ftp, dirpath, filenames)
                            ftp.cwd("..") #step out to flash
                ftp.close()
        except:
            print("Exception on client " + this.clientID)
            




for client in secrets.clients:
    print("Connecting to " + client, flush=True)
    f = FTPPusher(client, secrets.userName, secrets.passwd)
