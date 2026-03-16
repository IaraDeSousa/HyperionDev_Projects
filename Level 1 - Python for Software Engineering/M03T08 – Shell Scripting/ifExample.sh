# Creating folders in shell scripting but with if-statements.

#!/bin/bash   

if [ -d new_folder ]; then # Using -d checks for folders (directories)
    mkdir if_folder
    echo "new_folder found, if_folder created!"
fi

if [ -d if_folder ]; then
    mkdir hyperionDev
    echo "if_folder found, hyperionDev folder created!"
else
    mkdir new-projects
    echo "if_folder not found, new folder new-projects created!"
fi
