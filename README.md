# newgan-validator

This is a Python script that will validate and update the image mappings set up by NewGAN Manager.

It fixes invalid folder mappings such as `SAMed/South American126` to valid ones like `SAMed/SAMed1887` 

*Note: The script will overwrite your config.xml in place by default, so make a backup before running*

## Usage

Download or clone a copy of this code repo and unzip the file if applicable. Open your command line application (such as Terminal on MacOS or PowerShell on Windows) and open the directory containing the code.

Run `python rewrite_xml.py` and enter the path to your Football Manager graphics folder. The script assumes that will contain all the NewGAN folders as well as your `config.xml` file.

The script will validate all entries in the config file and will overwrite the existing file. You can see the changes by restarting the game.
