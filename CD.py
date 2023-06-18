import os
# Read in the file
with open('CDVERSION.tmp', 'r') as cdfile :
  cdfiledata = cdfile.read()
with open('DoElvUIClient.py', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('LocalDoElvUIClientVersion = None', 'LocalDoElvUIClientVersion = ' + cdfiledata)

# Write the file out again
with open('DoElvUIClient.py', 'w') as file:
  file.write(filedata)