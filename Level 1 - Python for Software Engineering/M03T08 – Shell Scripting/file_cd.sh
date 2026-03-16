# Creating and deleting folders using shell scripting.

#!/bin/bash   

mkdir Folder1 # Changed to use relative instead of absolute paths
mkdir Folder2
mkdir Folder3

cd Folder1
mkdir Folder1/FolderA
mkdir Folder1/FolderB
mkdir Folder1/FolderC

rmdir Folder2 # Using rmdir as there are no files inside.
rmdir Folder3