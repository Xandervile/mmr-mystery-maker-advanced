MMR Mystery Maker is a Python script (and now standalone .exe, thanks to [PyInstaller](https://pyinstaller.org/en/stable/index.html) - to do for this version!) that generates semi-random "Mystery" settings files for [Majora's Mask Randomizer v1.16.0.12](https://github.com/ZoeyZolotova/mm-rando).

See the [Mystery Settings Document](https://docs.google.com/document/d/1itr0_0H4xHFr2sKhuUdlBxwDGroJu5C74ZKuSIRFvYI/edit?usp=sharing) and the [Category Weights and Hints spreadsheet](https://docs.google.com/spreadsheets/d/14ZggIIteou_-D9oG-CnMEYK8u_s0_E6U5hIgqAkobrs/edit?usp=sharing) to learn more about Mystery settings, courtesy of FifthWhammy!

The original file by FifthWhammy had limitations that, due to it being an early version, I wanted to adapt on and make my own version, especially with the different Win Conditions being weighted, and it spiralled out of control from there.

The script uses categories and weights from the associated weights json, applying them to an input JSON file to generate a new settings file. By default, the script then calls MMR.CLI.exe to generate a new seed using the settings.

The jsons are fully changeable and if you would like to add/change settings, you can change the json and the py script to add/change settings.

To use:
-Download the code as a ZIP file and extract
- Move the Python Script and all json files to your MMR folder (recommended, but you can also set he files manually in the program)
- BEFORE running the program, make sure that MMR is set to AT LEAST output a file (be it a WAD, N64 or a .mmr patch), as well as all visual cosmetic things you would like.
- Load the Python Script, set your weighted chance for each of the Mystery Settings, and randomize!

If you would like to change weights within each setting, open the weights.json associated with the game mode you would like to edit, and change the numbers accordingly.

If you would like to add or change settings, you will need to open the weights.json and add/change the weights and names in there, and then edit the Python script to add your new setting. This can be either adding an item string (see Fairy Shuffling for an example) or a gimmick setting (see Iron Goron).

Command-line operation is still available. Using any command-line option will bypass the options GUI and go straight to generation. Advanced support to be added.

Current options (and their command-line equivalents):

Custom Base MMR Settings File (-i FILE, --input FILE): use FILE as the base settings file

Only Make Settings File (--settings-only): only generate a settings JSON and Mystery spoiler; don't make a seed using MMR.CLI.exe afterward

Number of Seeds (-n N): generate N seeds at a time; -n 5 would generate 5 seeds

Custom Path to MMR.CLI.exe (-r EXE, --randomizer-exe EXE): use EXE to create a seed after making the Mystery settings (useful if your MMR.CLI.exe in a different directory)

--version: command line only--print the current Mystery Maker version number and exit

--help: command line only--print these command line options and exit

For related info and discussion, and to share feedback, visit the #mystery-discussion channel of the MMR Community Discord: https://discord.gg/7jBRhhJ

And if you wish to package the script into an .exe yourself:

- Install Python (https://www.python.org) and then use Python's pip to install PyInstaller (https://pyinstaller.org/en/stable/installation.html).
- Open a PowerShell window or other shell in the same directory as MysteryMaker.py and run:  pyinstaller --onefile .\MysteryMaker.py

Enjoy!

Xandervile
