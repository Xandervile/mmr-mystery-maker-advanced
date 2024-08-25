MMR Mystery Maker is a Python script (and now standalone .exe, thanks to [PyInstaller](https://pyinstaller.org/en/stable/index.html)) that generates semi-random "Mystery" settings files for [Majora's Mask Randomizer v1.16.0.12](https://github.com/ZoeyZolotova/mm-rando).

See the [Mystery Settings Document](https://docs.google.com/document/d/1itr0_0H4xHFr2sKhuUdlBxwDGroJu5C74ZKuSIRFvYI/edit?usp=sharing) and the [Category Weights and Hints spreadsheet](https://docs.google.com/spreadsheets/d/14ZggIIteou_-D9oG-CnMEYK8u_s0_E6U5hIgqAkobrs/edit?usp=sharing) to learn more about Mystery settings.

The script uses hard-coded categories and weights, applying them to an input JSON file to generate a new settings file. By default, the script then calls MMR.CLI.exe to generate a new seed using the settings.

To use:
- Download the latest Mystery Maker release from the Releases section.
- Extract MysteryMaker.exe and the .json files to the same folder as your MMR install. (You can run Mystery Maker elsewhere, but will have to manually select the base settings file and MMR.CLI.exe.)
- Ensure your desired outputs are on in your MMR settings ("Patch .mmr" is recommended at minimum!), as that's how MMR.CLI.exe decides what to output.
- Run MysteryMaker.exe and an options dialog will open. If it's in the same directory as MMR, you can just click Randomize in the options dialog to generate the seed.
- When finished, check the "output" directory for your seed and Mystery spoiler.

To try the included Remains Shuffle or Fairy Hunt settings, select "Mystery_Remains_Shuffle_base.json" or "Mystery_Fairy_Hunt_base.json" as your settings file!

Command-line operation is still available. Using any command-line option will bypass the options GUI and go straight to generation.

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

FifthWhammy
