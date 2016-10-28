# About duplicate-files
This little Python 3 script will help you find duplicate files in a directory (and its subdirectories) on your computer.

It can also help you delete them automatically if you wish to.

The script proceeds in two steps to know whether two file are the same or not :
- First, it compares the files' sizes
- If the first comparison wasn't enough, it proceeds to the comparison of the files' hashes

## Running the script
In order to run the script, you need to have Python 3 installed.

The script requires at least an argument which is the path of the directory you wish to check in for duplicate files. The check for duplicate files will happen recursively within every subdirectories.

You can also pass a second facultative argument that equals ```true``` or ```false``` and will tell the script to delete or not the duplicate files it may find. By default, this argument is set to ```false```. If subdirectories were to be left empty in the process, they are deleted at the end of the script.

```{r, engine='python'}
python duplicatefiles.py PATH DELETION=["TRUE", "FALSE"]
```
