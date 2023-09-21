"""
Script que realiza la descarga del software de ffmpeg
programa necesario para poder convetir los videos mp4 a mp3

Esta hardcodeado, si alguien lee esto que haga lo que le de la gana.
ya que lo hice so lo por joder y aburrimiento. La repo donde se descarga 
el software es BtbN/FFmpeg-Builds y de ahi solo se extrae el fichero ffprobe.exe y ffmpeg.exe

Solo lo descargaría tras haber pasado 7 dias de antiguedad, por eso decia algunas mierdas 
estan hardcodeadas
"""


import requests
import os
import zipfile
from github import Github
from datetime import datetime
import logging
import re

# Define directories and paths
currentDate = datetime.now().strftime('%Y%m%d')
#paths
currentDir = os.path.abspath(os.getcwd()) # path to current directory
assetsDir = os.path.join(currentDir, 'assets') # path to assets directory
binariesDirPath = os.path.join(assetsDir, 'bin') # path to binaries directory
tempDir = os.path.join(assetsDir, 'Temp') # path to temp directory
logDir = os.path.join(assetsDir, 'logs') # path to logs directory

#related to ffmpeg
repoName = "BtbN/FFmpeg-Builds"
zipName = "ffmpeg.zip"
ffmpegExeName = 'ffmpeg.exe'
ffmprobeExeName = 'ffprobe.exe'
zipPath = os.path.join(tempDir, zipName) #path to zip file
ffmpegExePath = os.path.join(binariesDirPath, ffmpegExeName) #path to ffmpeg.exe
assetName = "ffmpeg-master-latest-win64-gpl.zip"
assetNameRegex = re.compile(r"ffmpeg-master-.+-win64-gpl.zip")
daysUpToDate = 7 #number of days to consider the file up to date

#list of directories
directories = [assetsDir, binariesDirPath, tempDir, logDir]
for directory in directories:
    if not os.path.exists(directory):
        os.mkdir(directory)

# Set up logging
log_file = os.path.join(logDir, 'log_ffmp_updater.txt')
if os.path.exists(log_file):
    os.remove(log_file)  # Delete previous log if it exists

logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def is_file_up_to_date(file_path, current_date, days):
    """
    Check if the file is updated within the specified number of days.
    """
    if not os.path.exists(file_path):
        return False

    last_modified = os.path.getmtime(file_path)
    last_modified_date = datetime.fromtimestamp(last_modified).strftime('%Y%m%d')
    date_difference = int(current_date) - int(last_modified_date)

    return date_difference <= int(days)


def download_latest_release_zip(repo_name, asset_name, zip_path, github_token):
    """
    Downloads the latest release zip of a given asset from a specified GitHub repository.
    """
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    latest_release = repo.get_latest_release()

    download_url = None
    for asset in latest_release.get_assets():
        if asset.name == asset_name:
            logging.info(f"Asset: {asset.name}")
            download_url = asset.browser_download_url
            break
    else:
        logging.info(f"Asset {asset_name} not found, exiting.")
        return False

    response = requests.get(download_url, stream=True)
    with open(zip_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    logging.info(f"Downloaded {asset_name} to {zip_path}")

    return True


def extract_executable_from_zip(zip_path, exe_name, target_dir):
    """
    Extracts the specified executable from the downloaded ZIP file and saves it to the target directory.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for archivo_en_zip in zip_ref.namelist():
            if archivo_en_zip.endswith(exe_name):
                with zip_ref.open(archivo_en_zip) as source, open(os.path.join(target_dir, exe_name), 'wb') as target:
                    target.write(source.read())
                logging.info(f"{exe_name} has been extracted to {target_dir}")
                break
        else:
            logging.info(f"{exe_name} not found in the ZIP.")
            return False


# Personal Access Token for Github
tokenGithub = None


# checking existence or latest modification date of ffmpeg.exe
if is_file_up_to_date(ffmpegExePath, currentDate, daysUpToDate) and is_file_up_to_date(ffmprobeExeName, currentDate, daysUpToDate):
    logging.info("ffmpeg  and ffmprobe are up to date, exiting.")
    exit(0)
else:
    # if both files are not up to date, download the latest release and extract the executables
    if download_latest_release_zip(repoName, assetName, zipPath, tokenGithub):
        extract_executable_from_zip(zipPath, ffmpegExeName, binariesDirPath)
        extract_executable_from_zip(zipPath, ffmprobeExeName, binariesDirPath)
    else:
        logging.info("Download failed, exiting.")
        exit(1)
