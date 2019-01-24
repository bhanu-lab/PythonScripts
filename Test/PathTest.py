import os
#Path where file are present
path = 'EMailAttachments/'

files = os.listdir(path)
#Printing all the files in Directory
for name in files:
    print(name)
