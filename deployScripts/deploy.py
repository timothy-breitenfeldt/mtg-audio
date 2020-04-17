
import os
import zipfile
import configparser
import ftplib

def main():
    serverAddress, username, password, versionPath, applicationPath = getServerSettings("ftp_config.ini")

    if os.path.basename(os.getcwd()) != "mtg-audio":
        os.chdir(os.path.join(".."))

    print("Writing version to file...")
    os.chdir("src")
    versionNumber = readCurrentVersionNumber()
    
    os.chdir(os.path.join("..", "dist"))
    writeVersionFile(versionNumber)

    print("zipping file...")
    removeFile(f"mtg{versionNumber}.zip")
    zipDirectory(f"mtg{versionNumber}", f"mtg{versionNumber}.zip")
    print("done zipping.")

    session = ftplib.FTP(serverAddress, username, password)
    upload(session, applicationPath, f"mtg{versionNumber}.zip")
    upload(session, versionPath, "version.txt")
    session.quit()
    print("Successfully uploaded files")
    removeFile("version.txt")

def readCurrentVersionNumber():
    with open("version.py") as file:
        text = file.readline()
        version = text.split("=")[1]
        version = version.strip(" \n\r\"\'")
        return version

def writeVersionFile(versionNumber):
    with open("version.txt", "w") as file:
        file.write(versionNumber)

def zipDirectory(path, zipFileName):
    zipHandle = zipfile.ZipFile(zipFileName, "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            zipHandle.write(os.path.join(root, file))

def getServerSettings(ftpConfigPath):
    config = configparser.ConfigParser()
    config.read_file(open(ftpConfigPath))
    serverAddress = config["ftp_config"]["server_address"]
    username = config["ftp_config"]["username"]
    password = config["ftp_config"]["password"]
    versionPath = config["ftp_config"]["version_path"]
    applicationPath = config["ftp_config"]["application_path"]
    return (serverAddress, username, password, versionPath, applicationPath)

def deleteFromServer(session, filename):
    try:
        session.delete(filename)
        print("deleted file successfully")
    except:
        print("No file with the name of " + filename)

def transferFile(session, filename):
    with open(filename, "rb") as file:
        session.storbinary("STOR " + filename, file)

def upload(session, path, filename):
    session.cwd(path)
    print(f"deleting {filename}.zip if exists.")
    deleteFromServer(session, filename)
    print(f"Transfering {filename}...")
    transferFile(session, filename)
    print("transfer complete.")

def removeFile(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

main()