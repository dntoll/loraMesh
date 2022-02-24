from ftplib import FTP
from os import walk
from MeshTestConsole import secrets
import threading
import telnetlib


class Telnet:
    def __init__(self, clientIP, username, password, command):
        HOST = clientIP
        user = username
        password = password

        try:
            with telnetlib.Telnet(HOST, 23) as tn:
                print("telnet >>>" + str(command), flush=True)
                tn.read_until(b"Login as: ")
                tn.write(user.encode('ascii') + b"\r\n")
                if password:
                    tn.read_until(b"Password:", timeout=1)
                    tn.write(password.encode('ascii') + b"\r\n")

                tn.read_until(b">>>", timeout=1)
                tn.write(command + b"\r\n")
                tn.read_until(b">>>", timeout=1)
                tn.close()
                print("telnet closed", flush=True)
        except Exception as e:
            print(e)
            print("Something went wrong telnet ing to " +clientIP )


class FTPPusher:
    def __init__(self, clientIP, username, password):
        self.clientID = clientIP
        self.username = username
        self.password = password

        t = threading.Thread(target=FTPPusher.push, args=(self, self), daemon=False)
        t.start() 

    def _pushAllPyFiles(ftp, localSubFolder, filenames):
        print("_pushAllPyFiles" + localSubFolder)
        for fileName in filenames:
            if ".py" in fileName:
                disallowedFiles = ["test_", "release_", "sim_"]
                doIncludeFile = True
                for notAllowed in disallowedFiles:
                    if notAllowed in fileName:
                        doIncludeFile = False

                if doIncludeFile:
                    completePath = localSubFolder + "\\" + fileName
                    with open(completePath, "rb") as fp:
                        ftp.storbinary("STOR " + fileName, fp)
                    print("Wrote: " + completePath + " to device ", flush=True)

    def push(this, that):
        try:
            a = Telnet(this.clientID,this.username, this.password, b"import ftpdeploy; ftpdeploy.cleandirectory()")
            FTPPusher.pushFolders(this)
            a = Telnet(this.clientID,this.username, this.password, b"import machine; machine.reset()")
        except:
            print("FTP Exception on client " + this.clientID)
    
    def pushFolders(this):
        with FTP(this.clientID, timeout=10) as ftp:
            localBasePath = ".\\MeshTestConsole"
            ftp.login(user=this.username, passwd=this.password)
            ftp.cwd('flash')

            for (localSubFolder, dirnames, filenames) in walk(localBasePath):
                disallowedFolders = [".git", "__pycache__", ".pytest_cache"]
                

                doIncludeFolder = True
                for notAllowed in disallowedFolders:
                    if notAllowed in localSubFolder:
                        doIncludeFolder = False

                if doIncludeFolder:
                    print("Local directory path:" + localSubFolder, flush=True)
                    if localBasePath == localSubFolder:
                        #these end up in Flash
                        FTPPusher._pushAllPyFiles(ftp, localSubFolder, filenames)
                    elif localBasePath + "\\" in localSubFolder: #dont push .git
                        dirName = localSubFolder[len(localBasePath)+1:]
                        onDeviceDirName = 'flash' + "/" + dirName
                        print("onDeviceDirName " + onDeviceDirName, flush=True)
                        ftp.cwd("..") # step out of flash
                        try:
                            ftp.mkd(onDeviceDirName)
                            print("mkdir " + onDeviceDirName)
                        except:
                            print("dir exists")
                        print("cwd")
                        ftp.cwd(onDeviceDirName)
                        print("after" + localSubFolder, flush=True)
                        FTPPusher._pushAllPyFiles(ftp, localSubFolder, filenames)
                        print("pushed")
                        ftp.cwd("..") #step out to flash
            ftp.close()
        
            




for client in secrets.clients:
    print("Connecting to " + client, flush=True)
    f = FTPPusher(client, secrets.userName, secrets.passwd)
