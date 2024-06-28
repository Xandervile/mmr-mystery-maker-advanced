MMR Mystery Maker is a Python script that generates semi-random "Mystery" settings files for Majora's Mask Randomizer v1.16.0.10 (https://github.com/ZoeyZolotova/mm-rando).

The script uses hard-coded categories and weights, applying them to an input JSON file to generate a new settings file. By default, the script then calls MMR.CLI.exe to generate a new seed using the settings.

Install Python (https://www.python.org) in order to use this script. This version was developed and tested on Python 3.12.3, but any later version should be fine.

To use:
- Place MysteryMaker_v2_0.py and Default_Mystery_base.json in the same folder as your MMR 1.16.0.10 install.
- Ensure your desired outputs are on in your MMR settings ("Patch .mmr" is recommended at minimum!), as that's how MMR.CLI.EXE decides what to output.
- Run MysteryMaker_v2_0.py. When finished, check the "output" directory for your seed and Mystery spoiler.

Current command-line options:

--settings-only: only generate a settings JSON and mystery spoiler; don't run MMR.CLI afterward

-n: generate N seeds at a time

-i, --input: specify a different base settings file

To try the included Remains Shuffle or Fairy Hunt settings, try adding "-i Mystery_Remains_Shuffle_base.json" or "-i Mystery_Fairy_Hunt_base.json" to the command line!

For related info and discussion, and to share feedback, visit the #mystery-discussion channel of the MMR Community Discord: https://discord.gg/7jBRhhJ

Enjoy!

FifthWhammy
