"""
Descarga el youtube downloader
ya dependiendo si existe o no.
si existe se descarga entero, sino se ejecuta el propio programa
y se lanza su comando de actualizacion.

Creo... no me acuerdo muy bien lo que hace esta mierda, pero en principio
es esto
"""

import requests
import os
from github import Github
from datetime import datetime
import logging
import subprocess

# Define directories and paths
currentDate = datetime.now().strftime('%Y%m%d')
#paths
currentDir = os.path.abspath(os.getcwd()) # path to current directory
assetsDir = os.path.join(currentDir, 'assets') # path to assets directory
binariesDirPath = os.path.join(assetsDir, 'bin') # path to binaries directory
tempDir = os.path.join(assetsDir, 'Temp') # path to temp directory
logDir = os.path.join(assetsDir, 'logs') # path to logs directory


#related to yt-dlp
repoName = "yt-dlp/yt-dlp"
ytlpExeName = 'yt-dlp.exe'
ytlpExePath = os.path.join(binariesDirPath, ytlpExeName) #path to yt-dlp.exe


#list of directories
directories = [assetsDir, binariesDirPath, tempDir, logDir]
for directory in directories:
    if not os.path.exists(directory):
        os.mkdir(directory)

# Set up logging
log_file = os.path.join(logDir, 'log_yt-dlp_updater.txt')
if os.path.exists(log_file):
    os.remove(log_file)  # Delete previous log if it exists

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def download_latest_release_zip(repo_name, asset_name, file_path, github_token):
    """
    Downloads the latest release zip of a given asset from a specified GitHub repository.
    """
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    latest_release = repo.get_latest_release()

    download_url = None
    for asset in latest_release.get_assets():
        if asset.name == asset_name:
            download_url = asset.browser_download_url
            break
    else:
        logging.info(f"Asset {asset_name} not found, exiting.")
        return False

    response = requests.get(download_url, stream=True)
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    logging.info(f"Downloaded {asset_name} to {file_path}")

    return True

tokenGithub = None

#check if yt-dlp.exe exist in binaries directory
if not os.path.exists(ytlpExePath):
    logging.info(f"yt-dlp.exe not found, downloading...")
    download_latest_release_zip(repoName, ytlpExeName, ytlpExePath, tokenGithub)
else:
    # Perform an update check of yt-dlp.exe -U and redirect output to the log file
    logging.info("yt-dlp.exe found, checking for updates...")
    with open(log_file, "a") as log_file_handle:
        process = subprocess.Popen([ytlpExePath, "--update-to nightly"], stdout=log_file_handle, stderr=subprocess.STDOUT, text=True)
        process.wait()
        #close the log file
    log_file_handle.close()
