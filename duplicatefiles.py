import os
import sys
import time
import hashlib


# Arguments used to run the program
path = "" # Absolute path to the directory
delete = False # Sets whether the program will delete the duplicate files or not


def CompareSizes(f1_name, f2_name):
    f1_size = os.stat(f1_name).st_size
    f2_size = os.stat(f2_name).st_size

    return ( f1_size == f2_size )

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

def CompareHashes(f1_name, f2_name):
    f1_sha = GetHash(f1_name)
    f2_sha = GetHash(f2_name)

    return ( f1_sha == f2_sha )


f = [] # This array stores the names of the files in the directory
l = [] # This array will store the names of the duplicate files
buff = [] # This array is a buffer for the loop

# This loop retrieves the names of the files
for (dirpath, dirnames, filenames) in os.walk(path):
    f.extend(filenames)
    break

filesnb = len(f) # Number of files
totalit = ( filesnb*(filesnb-1) ) / 2 # Final number of iterations
count = 0 # Keeps track of the progress (number of iterations done)

initial_time = time.clock() # Time at which the program begins

for i, file1 in enumerate(f):
    buff = [] # We reset the buffer at each loop

    for j, file2 in enumerate(f):
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
        totalit -= (filesnb-i-1)

    # Display of the current progress
    print("Progress : "+str( int( round( float(count)/totalit*100 ) ) )+"%")


# Display of the names of duplicate files
if(len(l) > 0):
    print("\n\nSome duplicate files were found :")
    for index, duo in enumerate(l):
        print("\n\tDuplicate of "+duo[0]+" :")
        print("\t > "+duo[1])
else:
    print("\n\nNo duplicate files were found.")


# Proceeds to the deletion of duplicate files (is delete is True)
if delete and len(l) > 0:
    print("\n")
    for fname in l:
        print("Deleted "+path+fname[1]+".")
        os.remove(path+fname[1])

final_time = time.clock() # Time at which the program ends


# Display of the execution time
print("\nThe program ran in "+str(int(round((final_time - initial_time)*1000)))+"ms.\n")

raw_input("Press a key to exit the program ...")
