# accesing to a ftp server
"""
script de python para administrar un ftp
basicamente la hice para las putas series que tienen nombre y numero y tal
ya que paraver desde un nas en un dlna server se mostraba como el culo
es la primera version
"""
import ftplib
import os
import re
import sys

# creating logon credentials
ftpUser = "root"
ftpPass = "root"
ftpHost = "192.168.1.1"


# try the connection
try:
    ftp = ftplib.FTP(ftpHost)
    ftp.login(ftpUser, ftpPass)
    # set working directory
    ftp.cwd(sys.argv[1])
    # get all the files in the directory
    listFiles = ftp.nlst()
    # loop through all the files
    for file in listFiles:
        # saving the fileName as oldName
        oldName = os.path.splitext(file)[0]
        # get the extension of the file
        extension = os.path.splitext(file)[1]
        # capture all the numbers from old file name
        newName = re.findall(r'\d+', oldName)[0]
        # rename the file
        ftp.rename(file, newName + extension)

    # then close the connection after all the work is done
    ftp.quit()
except:
    print("Connection failed")
