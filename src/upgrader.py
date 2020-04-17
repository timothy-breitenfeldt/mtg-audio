
import urllib.error
import os
import subprocess
import time
import platform

from updateUtil import UpdateUtil

def main():
    updateUtil = UpdateUtil()

    try:
        print("Checking for updates...")

        if not updateUtil.checkIfUpToDate():
            print(f"There is a new update, version {updateUtil.serverVersionNumber}")
            update(updateUtil)
            input("Press enter to continue.")
            updateUtil.startProcess("mtg", os.getcwd())
        else:
            print("No new updates.")
            input("Press enter to continue.")
    except urllib.error.URLError as e:
        print("There was a problem trying to update, please check your internet connection and try again.")
        input("Press enter to continue.")
    except urllib.error.HTTPError:
        print("There was a problem trying to update, the web server is down or has been moved.")
        input("Press enter to continue.")
    except FileNotFoundError as e:
        print("Unable to find file, please try again.")
        print("Cleaning up...")
        updateUtil.removeDirectory(os.path.join(updateUtil.tempDirectory, updateUtil.directoryName))
        updateUtil.removeFile(os.path.join(updateUtil.tempDirectory, f"{updateUtil.directoryName}.zip"))
        input("Press enter to continue.")
    except FileExistsError:
        print("Unable to rename folder, on startup, the updater won't be updated.")
        input("Press enter to continue.")

def update(updateUtil):
    updateUtil.removeDirectory(os.path.join(updateUtil.tempDirectory, updateUtil.directoryName))
    updateUtil.removeDirectory(os.path.join(updateUtil.tempDirectory, updateUtil.updatedDirectoryName))
    updateUtil.removeFile(os.path.join(updateUtil.tempDirectory, f"{updateUtil.directoryName}.zip"))

    print("Downloading files...")
    updateUtil.downloadFiles(f"{updateUtil.directoryName}.zip", updateUtil.tempDirectory, updateUtil.downloadUrl)
    print("Successfully downloaded files.")

    print("Unzipping...")
    updateUtil.unzipFile(f"{updateUtil.directoryName}.zip", updateUtil.tempDirectory)
    print("Successfully unzipped folder.")

    print("Updating files...")
    print("Moving files...")
    updateUtil.killProcesses(["mtg"])

    if os.path.isdir("decks"):
        updateUtil.removeDirectory(os.path.join(updateUtil.tempDirectory, updateUtil.directoryName, "decks"))
        updateUtil.removeDirectoryContents(".", excludes=["decks", "upgrader"])
    else:
        updateUtil.removeDirectoryContents(".")

    updateUtil.moveDirectoryContents(os.path.join(updateUtil.tempDirectory, updateUtil.directoryName), ".", excludes=["upgrader"])
    print("Done moving.")
    print("Cleaning...")
    updateUtil.removeFile(os.path.join(updateUtil.tempDirectory, f"{updateUtil.directoryName}.zip"))
    os.rename(os.path.join(updateUtil.tempDirectory, updateUtil.directoryName), os.path.join(updateUtil.tempDirectory, updateUtil.updatedDirectoryName))

if __name__ == "__main__":
    main()
