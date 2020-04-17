
import urllib.request
import wget
import zipfile
import shutil
import os
import subprocess
import tempfile
import glob
import platform

import psutil

from version import versionNumber

class UpdateUtil:

    def __init__(self):
        self._serverVersionNumber = ""
        self._localVersionNumber = versionNumber
        self._baseUrl = "http://mtgaudiogame.com"
        self._downloadUrl = f"{self._baseUrl}/downloads"
        self._directoryName = f"mtg{self.serverVersionNumber}"
        self._updatedDirectoryName = f"{self._directoryName}-finish-updating"
        self._tempDirectory = tempfile.gettempdir()

    def downloadFiles(self, filename, tempDirectory, downloadUrl):
        mtgUrl = downloadUrl
    
        if platform.system() == "Windows":
            mtgUrl += f"/windows/{filename}"
        elif platform.system() == "Darwin":
            mtgUrl += f"/mac/{filename}"
    
        wget.download(mtgUrl, out=tempDirectory, bar=self._customProgressOutput)
    
    def _customProgressOutput(self, current, total, width=80):
        if current %5000 == 0 or current == total:
            progressPercentage = int(current / total * 100)
            print(f"Downloading: {progressPercentage}%")
    
    def unzipFile(self, filename, tempDirectory):
        zipHandler = zipfile.ZipFile(tempDirectory + "\\" + filename, "r")
        zipHandler.extractall(tempDirectory + "")
        zipHandler.close()
    
    def killProcesses(self, processesToKill):
        try:
            for process in psutil.process_iter():
                processName = process.name().strip(".exe")
    
                if processName in processesToKill:
                    psutil.Process(process.pid).kill()
        except:
            pass

    def removeFile(self, path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
    
    def removeDirectory(self, path):
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass
    
    def removeDirectoryContents(self, path, excludes=[]):
        files = glob.glob(os.path.join(path, "*"))
        for f in files:
            name = os.path.basename(f)
            name = os.path.splitext(name)[0]
    
            if  name not in excludes:
                if os.path.isfile(f):
                    self.removeFile(f)
                elif os.path.isdir(f):
                    self.removeDirectory(f)
    
    def moveDirectoryContents(self, src, dest, excludes=[]):
        files = glob.glob(os.path.join(src, "*"))
        for f in files:
            name = os.path.basename(f)
            name = os.path.splitext(name)[0]
    
            if name not in excludes:
                shutil.move(f, dest)

    def checkIfUpToDate(self):
        return self.localVersionNumber >= self.serverVersionNumber

    def startProcess(self, exicutableName, path):
        if platform.system() == "Windows":
            subprocess.Popen([f"{exicutableName}"], cwd=path)
        elif platform.system() == "Darwin":
            subprocess.Popen([f"./{exicutableName}"], cwd=path)

    @property
    def serverVersionNumber(self):
        if not self._serverVersionNumber:
            versionUrl = f"{self.downloadUrl}/version.txt"
            response = urllib.request.urlopen(versionUrl)
            result =  response.read()
            response.close()
            self._serverVersionNumber = result.decode("ascii").strip(" \n\r")

        return self._serverVersionNumber

    @property
    def localVersionNumber(self):
        return self._localVersionNumber

    @property
    def baseUrl(self):
        return self._baseUrl

    @property
    def downloadUrl(self):
        return self._downloadUrl

    @property
    def directoryName(self):
        return self._directoryName

    @property
    def updatedDirectoryName(self):
        return self._updatedDirectoryName

    @property
    def tempDirectory(self):
        return self._tempDirectory
