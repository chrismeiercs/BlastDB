from ftplib import FTP
import fnmatch
import os
import tarfile

DB_DIR_NAME = "blastdb"
DOWNLOAD_DIR_NAME = "blastdb-downloads/"
BACKUP_DIR_NAME = 'blastdb-backup'
FTP_DIR_NAME = 'blast/db'
PATTERN = 'blast/db/nr*.tar.gz'

print "Making backup of current blast database"
'''Change directory name for back up'''
os.rename(DB_DIR_NAME, BACKUP_DIR_NAME)

print "Creating directories for new db and downloads"
'''Create new directory for updated db and downloads'''
os.mkdir(DB_DIR_NAME)
os.mkdir(DOWNLOAD_DIR_NAME)


print "Connecting to NCBI via FTP"
ftp = FTP('ftp.ncbi.nlm.nih.gov')
ftp.login()
print "Connected to NCBI via FTP"

list_of_files = ftp.nlst(FTP_DIR_NAME)

matches = fnmatch.filter(list_of_files, PATTERN)

print "Downloading refseq protein files"
print "There are {} files to retrieve".format(len(list_of_files))
#Add a count?
for match in matches:
	print "Downloading {}".format(match)
	'''with open(DOWNLOAD_DIR_NAME+match, "wb") as match_file:
	    ftp.retrbinary('RETR {}'.format(match), match_file.write)'''

ftp.close()
print "Safely disconnected from NCBI"

print "Extracing db files"
'''Extract the files'''
for root, dirs, file in os.walk(DOWNLOAD_DIR_NAME):
	print "Extracting {}".format(file)
	tar = tarfile.open(file)
	tar.extractall(DB_DIR_NAME)
	tar.close()

'''Clean up'''
print "Begin clean up"
#Remove downloads
print "Removing download directory"
os.remove(DOWNLOAD_DIR_NAME)
#remove backup
print "Removing backup of previous db version"
os.remove(BACKUP_DIR_NAME)
