
import os
import time

import shutil

def main():
    if os.path.basename(os.getcwd()) != "mtg-audio":
        os.chdir(os.path.join(".."))

    currentVersionNumber = _readCurrentVersionNumber("src")
    versionNumber = getVersionNumber(currentVersionNumber)
    print("Writing version number to version.py")
    _writeNewVersion("src", versionNumber)

    print("Removing existing dist folder")
    removeDirectory("dist")

    print("Building exicutables...")
    distPath = os.path.join("dist", f"mtg{versionNumber}")
    os.system(f"pyinstaller --distpath {distPath} {os.path.join('src', 'upgrader.spec')}")
    os.system(f"pyinstaller --distpath {os.path.join(distPath, 'database')} {os.path.join('src', 'database', 'buildDatabase.spec')}")
    os.system(f"pyinstaller --distpath {distPath} {os.path.join('src', 'mtg.spec')}")

    print("Copy readme to src/dist.")
    shutil.copyfile(os.path.join("src", "readme.html"), os.path.join(distPath, "readme.html"))
    print("create decks and copy in default deck.")
    os.mkdir(os.path.join(distPath, "decks"))
    shutil.copyfile(os.path.join("src", "decks", "dinosaur(RWG).txt"), os.path.join(distPath, "decks", "dinosaur(RWG).txt"))

    print("Copy database files...")
    shutil.copyfile(os.path.join("src", "database", "mtg.sql"), os.path.join(distPath, "database", "mtg.sql"))
    shutil.copyfile(os.path.join("src", "database", "mtg.db"), os.path.join(distPath, "database", "mtg.db"))
    shutil.copytree(os.path.join("src", "database", "resources"), os.path.join(distPath, "database", "resources"))
    print("done.")

def getVersionNumber(currentVersionNumber):
    newVersionNumber = ""
    
    while True:
        print(f"Version is currently {currentVersionNumber}")
        newVersionNumber = input("Enter a version number")
        isOk = False
        
        if newVersionNumber.strip(" ") == "":
            continue

        while not isOk:
            answer = input(f"Is {newVersionNumber} ok?")
        
            if answer.lower() == "y" or answer.lower() == "yes":
                isOk = True
            elif answer.lower() == "n" or answer.lower() == "no":
                break

        if isOk:
            break

    return newVersionNumber

def _readCurrentVersionNumber(path):
    with open(os.path.join(path, "version.py")) as file:
        text = file.readline()
        version = text.split("=")[1]
        version = version.strip(" \n\r\"\'")
        return version

def _writeNewVersion(path, versionNumber):
    with open(os.path.join(path, "version.py"), "w") as file:
        file.write(f"versionNumber='{versionNumber}'")

def removeDirectory(path):
    try:
        shutil.rmtree(path)

        # insure that the folder is deleted, if not wait 
        while os.path.isdir("dist"):
            time.sleep(0.1)
    except FileNotFoundError:
        pass

main()