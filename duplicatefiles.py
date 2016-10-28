import os
import sys
import time
import hashlib
import operator

# This will enable the script to work on different platforms
from sys import platform as _platform

clear = 'clear'
if _platform == "win32" and 'TERM' not in os.environ: # Windows
    clear = 'cls'

os.system(clear) # Let's clean the screen before proceding
_rows, _columns = os.popen('stty size', 'r').read().split() # Size of console

    # BEGINNING OF FUNCTIONS #

# Function used to print a message
def message(mess):
    print("\033[1;34m"+mess+"\033[0;39m")

# Function used to print an error message
def errorMessage(mess):
    print("\033[1;31m"+mess+"\033[0;39m")

# Function used to print a confirmation message
def confirmationMessage(mess):
    print("\033[1;32m"+mess+"\033[0;39m")

# Function used to print an informative message
def informativeMessage(mess):
    print("\033[1;35m"+mess+"\033[0;39m")

# Checks whether two files (by their absolute path) have the same size
def CompareSizes(f1_name, f2_name):
    f1_size = os.stat(f1_name).st_size
    f2_size = os.stat(f2_name).st_size
    return ( f1_size == f2_size )

# Retrieves the sha1 of a file (by its absolute path)
def GetHash(file_name):
    sha1 = hashlib.sha1()

    with open(file_name, 'rb') as f:
        while True:
            data = f.read(1024) # Reading data chunks of 1kb
            if not data:
                break
            sha1.update(data)

    f.close()
    return sha1.hexdigest()

# Checks whether two files (by their absolute path) have the sha1 hashes
def CompareHashes(f1_name, f2_name):
    f1_sha = GetHash(f1_name)
    f2_sha = GetHash(f2_name)

    return ( f1_sha == f2_sha )

def pager(text, num_lines = 25):
    for index, line in enumerate(text.splitlines()):
        if index % num_lines == 0 and index:
            inp = input( "\t\033[1;33m> Hit <Enter> to view the next page\033[0;39m\r".rjust(int(_columns)+8, ' '))
            if inp.lower() == 'q':
                break
            sys.stdout.flush()
            sys.stdout.write("\x1b[1A\x1b[2K"+line+"\n")
        else:
            print(line)

    # END OF FUNCTIONS #

# Setting up the variables used to run the script
if len(sys.argv) < 2:
    errorMessage("The script requires an absolute path to run.")
    errorMessage("Correct usage : python duplicatefiles.py path delete=[true,false].")
    exit(1)

path = "" # Absolute path to the directory
delete = False # Sets whether the script will delete the duplicate files or not

if len(sys.argv) >= 2: # It seems that a path has been specified : let's check it
    path = sys.argv[1]
    if not os.path.exists(path): # In case the path does not exist
        errorMessage("The specified path ("+path+") does not seem to exist.")
        exit(2)

if len(sys.argv) >= 3: # It seems that a deletion argument has been provided
    delete = ( sys.argv[2].lower() == "true" )

# Let's confirm the user's choice
print("The script will retrieve the duplicate files at \033[0;33m"+path+"\033[0;39m.")
print("It will show the list of duplicate files at the end.\n")

if delete:
    print("You wish to \033[1;7;31mdelete\033[0;39m the duplicate files at : \033[0;33m"+path+"\033[0;39m.")
    print("The deletion happens at the end of the script and has to be confirmed.")
else:
    print("You wish to \033[1;7;32mkeep\033[0;39m the duplicate files at : \033[0;33m"+path+"\033[0;39m.")

check_deletion = input("Proceed (y/n) ? ")

if check_deletion.lower() != "y":
    message("\nThe script will now exit without doing anything.")
    exit(3)
else:
    informativeMessage("\nStarting the script ...\n")

f = [] # This array stores the names of the files in the directory
l = [] # This array will store the names of the duplicate files
buff = [] # This array is a buffer for the loop

# This loop retrieves the names of the files
for root, dirs, files in os.walk(path):
    files = [f for f in files if not f[0] == '.']
    dirs[:] = [d for d in dirs if not d[0] == '.']
    f.extend(files)
    break

filesnb = len(f) # Number of files
totality = ( filesnb*(filesnb-1) ) / 2 # Final number of iterations
count = 0 # Keeps track of the progress (number of iterations done)

initial_time = time.clock() # Time at which the script begins

for i, file1 in enumerate(f):
    buff = [] # We reset the buffer at each loop

    for j, file2 in enumerate(f):
        # Display of the current progress
        sys.stdout.write("\r\x1b[K"+"\033[1mProgress :\033[0m "+str( "{:.2f}".format( float(count)/totality*100 ) )+"%")
        sys.stdout.flush()

        if i >= j: # We skip the checks that have already happened
            continue

        count += 1
        f1_name = path+file1
        f2_name = path+file2

        # First check : comparison of the sizes
        if not CompareSizes(f1_name, f2_name):
            continue

        # Second check : comparison of the hashes
        if CompareHashes(f1_name, f2_name):
            l.append( (file1, file2) )
            buff.append(file2)

    # We remove the names of duplicate files from the files array
    for rem in buff:
        f.remove(rem)
        filesnb = len(f)
        totality -= (filesnb-i-1)

print()
l.sort(key=operator.itemgetter(0), reverse=True) # Just a little bit of sorting

# Display of the names of duplicate files
dupes_list = ""
if(len(l) > 0):
    if(len(l) != 1):
        confirmationMessage("\nSome duplicate files were found. Here's the full list.")
    else:
        confirmationMessage("\nA duplicate file was found.")

    for index, duo in enumerate(l):
        if(len(l) != 1):
            dupes_list += "\n\033[1;34mDuplicate file number "+str(index+1)+" :\033[0;39m"
        dupes_list += "\n - "+duo[0]
        dupes_list += "\n - "+duo[1]
    pager(dupes_list, int(_rows))
    print()
else:
    message("\nNo duplicate files were found.")

# Let's be sure about the user's choice
if delete and len(l) > 0:
    print("\033[1mReminder :\033[0;39m you wished to \033[1;7;31mdelete\033[0;39m the duplicate files.")
    errorMessage("THIS ACTION IS NOT REVERSIBLE.")
    check_deletion = input("Are you sure you want to proceed (y/n) ? ")
    print()

    # Proceeds to the deletion of duplicate files (is delete is True)
    if check_deletion.lower() == "y":
        for fname in l:
            print("\033[1;31mDeleted\033[0;39m "+path+fname[1])
            os.remove(path+fname[1])
        confirmationMessage("\nThe duplicate files were deleted.")
    else:
        message("\nThe script will now exit without doing anything.")

final_time = time.clock() # Time at which the script ends

# Display of the execution time
informativeMessage("The script ran in "+str(int(round((final_time - initial_time)*1000)))+"ms.")
