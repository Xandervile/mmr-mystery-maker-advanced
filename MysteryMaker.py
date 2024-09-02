import json
import random
import subprocess
import argparse
import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

MYSTERY_MAKER_VERSION = "v3.0 Adv."

generator_dir = os.path.dirname(os.path.abspath(__file__))

weight_folder = os.path.join(generator_dir, "mystery")

def openOptionsGui():
    def guiStartRandomize(*args):
        guiWindow.destroy()

    def guiCloseButton(*args):
        windowForceClosed.set("1")
        guiWindow.destroy()

    def browseForBaseSettingsFile(*args):
        baseSettingsFilePath.set(filedialog.askopenfilename(initialdir=weight_folder))

    def browseForFairySettingsFile(*args):
        fairySettingsFilePath.set(filedialog.askopenfilename(initialdir=weight_folder))

    def browseForRemainsSettingsFile(*args):
        remainsSettingsFilePath.set(filedialog.askopenfilename(initialdir=weight_folder))

    def browseForBaseWeightsFile(*args):
        baseWeightsFilePath.set(filedialog.askopenfilename(initialdir=weight_folder))

    def browseForFairyWeightsFile(*args):
        fairyWeightsFilePath.set(filedialog.askopenfilename(initialdir=weight_folder))

    def browseForRemainsWeightsFile(*args):
        remainsWeightsFilePath.set(filedialog.askopenfilename(initialdir=weight_folder))

    def browseForCommandLineExe(*args):
        mmrCommandLineExePath.set(filedialog.askopenfilename(initialdir=generator_dir))

    guiWindow = Tk()
    guiWindow.title("MMR Mystery Maker " + MYSTERY_MAKER_VERSION)

    mainframe = ttk.Frame(guiWindow, padding="8 8 4 8")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    guiWindow.columnconfigure(0, weight=1)
    guiWindow.rowconfigure(0, weight=1)

    windowForceClosed = StringVar(value="0")

    baseSettingsFilePath = StringVar(value="mystery\\Default_Mystery_base.json")
    baseSettingsFilePath_entry = ttk.Entry(mainframe, width=70, textvariable=baseSettingsFilePath)
    baseSettingsFilePath_entry.grid(column=3, row=1, sticky=(W, E), columnspan=2)

    fairySettingsFilePath = StringVar(value="mystery\\Mystery_Fairy_Hunt_base.json")
    fairySettingsFilePath_entry = ttk.Entry(mainframe, width=70, textvariable=fairySettingsFilePath)
    fairySettingsFilePath_entry.grid(column=3, row=3, sticky=(W, E), columnspan=2)

    remainsSettingsFilePath = StringVar(value="mystery\\Mystery_Remains_Shuffle_base.json")
    remainsSettingsFilePath_entry = ttk.Entry(mainframe, width=70, textvariable=remainsSettingsFilePath)
    remainsSettingsFilePath_entry.grid(column=3, row=5, sticky=(W, E), columnspan=2)
	
    mmrCommandLineExePath = StringVar(value="MMR.CLI.exe")
    mmrCommandLineExePath_entry = ttk.Entry(mainframe, width=70, textvariable=mmrCommandLineExePath)
    mmrCommandLineExePath_entry.grid(column=3, row=7, sticky=(W, E), columnspan=2)
	
    fairyHuntChance = StringVar(value="10")
    fairyHuntChance_spinbox = ttk.Spinbox(mainframe, width=5, from_=0, to=100000,textvariable=fairyHuntChance)
    fairyHuntChance_spinbox.grid(column=2, row=4, sticky=E)
	
    remainHuntChance = StringVar(value="15")
    remainHuntChance_spinbox = ttk.Spinbox(mainframe, width=5, from_=0, to=100000,textvariable=remainHuntChance)
    remainHuntChance_spinbox.grid(column=2, row=6, sticky=E)

    baseChance = StringVar(value="75")
    baseChance_spinbox = ttk.Spinbox(mainframe, width=5, from_=1, to=100000,textvariable=baseChance)
    baseChance_spinbox.grid(column=2, row=2, sticky=E)

    baseWeightsFilePath = StringVar(value="mystery\\Default_Mystery_Weights.json")
    baseWeightsFilePath_entry = ttk.Entry(mainframe, width=70, textvariable=baseWeightsFilePath)
    baseWeightsFilePath_entry.grid(column=3, row=2, sticky=(W, E), columnspan=2)

    fairyWeightsFilePath = StringVar(value="mystery\\Mystery_Fairy_Hunt_Weights.json")
    fairyWeightsFilePath_entry = ttk.Entry(mainframe, width=70, textvariable=fairyWeightsFilePath)
    fairyWeightsFilePath_entry.grid(column=3, row=4, sticky=(W, E), columnspan=2)

    remainsWeightsFilePath = StringVar(value="mystery\\Mystery_Remains_Shuffle_Weights.json")
    remainsWeightsFilePath_entry = ttk.Entry(mainframe, width=70, textvariable=remainsWeightsFilePath)
    remainsWeightsFilePath_entry.grid(column=3, row=6, sticky=(W, E), columnspan=2)

    numberToGenerate = StringVar(value="1")
    numberToGenerate_spinbox = ttk.Spinbox(mainframe, width=5, from_=1, to=100,textvariable=numberToGenerate)
    numberToGenerate_spinbox.grid(column=4, row=8, sticky=W)

    makeSettingsOnly = StringVar(value="0")
    makeSettingsOnly_checkbutton = ttk.Checkbutton(mainframe, text="Only make settings file", variable=makeSettingsOnly)
    makeSettingsOnly_checkbutton.grid(column=1, row=8, sticky=E)

    ttk.Label(mainframe, text="Custom base MMR settings file:").grid(column=1, row=1, sticky=E,columnspan = 2)
    ttk.Label(mainframe, text="Custom fairy hunt MMR settings file:").grid(column=1, row=3, sticky=E, columnspan = 2)
    ttk.Label(mainframe, text="Custom remains hunt MMR settings file:").grid(column=1, row=5, sticky=E, columnspan = 2)
    ttk.Button(mainframe, text="Browse...", command=browseForBaseSettingsFile).grid(column=5, row=1, sticky=W)
    ttk.Button(mainframe, text="Browse...", command=browseForFairySettingsFile).grid(column=5, row=3, sticky=W)
    ttk.Button(mainframe, text="Browse...", command=browseForRemainsSettingsFile).grid(column=5, row=5, sticky=W)
    ttk.Button(mainframe, text="Browse...", command=browseForCommandLineExe).grid(column=5, row=7, sticky=W)
    ttk.Button(mainframe, text="Randomize", command=guiStartRandomize).grid(column=5, row=8, sticky=W)
    ttk.Label(mainframe, text="Custom path to MMR.CLI.exe:").grid(column=1, row=7, sticky=E, columnspan = 2)
    ttk.Label(mainframe, text="# of seeds:").grid(column=3, row=8, sticky=E)

    ttk.Label(mainframe, text="Weight of Fairy Hunt:").grid(column=1, row=4, sticky=E)
    ttk.Label(mainframe, text="Weight of Remain Hunt:").grid(column=1, row=6, sticky=E)
    ttk.Label(mainframe, text="Weight of Base Settings:").grid(column=1, row=2, sticky=E)
    ttk.Button(mainframe, text="Browse...", command=browseForBaseWeightsFile).grid(column=5, row=2, sticky=W)
    ttk.Button(mainframe, text="Browse...", command=browseForFairyWeightsFile).grid(column=5, row=4, sticky=W)
    ttk.Button(mainframe, text="Browse...", command=browseForRemainsWeightsFile).grid(column=5, row=6, sticky=W)


    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    baseSettingsFilePath_entry.focus()
    guiWindow.protocol("WM_DELETE_WINDOW", guiCloseButton)
    guiWindow.bind("<Return>", guiStartRandomize)

    guiWindow.mainloop()
    return [(windowForceClosed.get() == "1"),
            baseSettingsFilePath.get(),
            fairySettingsFilePath.get(),
            remainsSettingsFilePath.get(),
            mmrCommandLineExePath.get(),
            (int)(fairyHuntChance.get()),
            (int)(remainHuntChance.get()),
            (int)(baseChance.get()),
            (int)(numberToGenerate.get()),
            baseWeightsFilePath.get(),
            fairyWeightsFilePath.get(),
            remainsWeightsFilePath.get(),
            (makeSettingsOnly.get() == "1")]

def AddEntryToListString(liststring, word, value):
    bitstringWords = liststring.split("-")
    bitstringWords.reverse()
    existingWord = bitstringWords[word]
    if existingWord == '':
        existingWord = '0'
    bitstringWords[word] = hex(int(existingWord,16) | int(value,16))[2:]
    bitstringWords.reverse()
    return "-".join(bitstringWords)

def RemoveEntryFromListString(liststring, word, value):
    bitstringWords = liststring.split("-")
    bitstringWords.reverse()
    existingWord = bitstringWords[word]
    if existingWord == '':
        existingWord = '0'
    if int(existingWord,16) | int(value,16) == int(existingWord,16):
        bitstringWords[word] = hex(int(existingWord,16) - int(value,16))[2:]
    bitstringWords.reverse()
    return "-".join(bitstringWords)

def CheckEntryInListString(liststring, word, value):
    bitstringWords = liststring.split("-")
    bitstringWords.reverse()
    existingWord = bitstringWords[word]
    if existingWord == '':
        existingWord = '0'
    if int(existingWord,16) | int(value,16) == int(existingWord,16):
        return True
    else:
        return False

def AddStringToListString(liststring, newstring):
    liststringWords = liststring.split("-")
    newstringWords = newstring.split("-")
    for i in range(min([len(liststringWords),len(newstringWords)])):
        if (liststringWords[i] != '' or newstringWords[i] != ''):
            if liststringWords[i] == '':
                liststringWords[i] = '0'
            if newstringWords[i] == '':
                newstringWords[i] = '0'
            liststringWords[i] = hex(int(liststringWords[i],16) |
                                     int(newstringWords[i],16))[2:]
            if liststringWords[i] == '0':
                liststringWords[i] = ''
    return "-".join(liststringWords)

def RemoveStringFromListString(liststring, newstring):
    liststringWords = liststring.split("-")
    newstringWords = newstring.split("-")
    for i in range(min([len(liststringWords),len(newstringWords)])):
        if (liststringWords[i] != '' or newstringWords[i] != ''):
            if liststringWords[i] == '':
                liststringWords[i] = '0'
            if newstringWords[i] == '':
                newstringWords[i] = '0'
            liststringWords[i] = hex((int(liststringWords[i],16) ^
                                     int(newstringWords[i],16)) &
                                     int(liststringWords[i],16))[2:]
            if liststringWords[i] == '0':
                liststringWords[i] = ''
    return "-".join(liststringWords)

def CheckStringInListString(liststring, newstring):
    liststringWords = liststring.split("-")
    newstringWords = newstring.split("-")
    for i in range(min([len(liststringWords),len(newstringWords)])):
        if (liststringWords[i] != '' or newstringWords[i] != ''):
            if liststringWords[i] == '':
                liststringWords[i] = '0'
            if newstringWords[i] == '':
                newstringWords[i] = '0'
            if (int(liststringWords[i],16) | int(newstringWords[i],16)) != int(liststringWords[i],16):
                return False
    return True

def FilenameOnly(pathstring):
    filename = pathstring[(pathstring.rfind("/") + 1):]
    filename = filename[(filename.rfind("\\") + 1):]
    return filename
    
def GenerateMysterySettings(inputFilename, fairyFilename, remainsFilename, fairyWeight, remainWeight, baseWeight, baseWeightfile, fairyWeightfile, remainsWeightfile, outputSuffix="output"):

    random.seed()

    randomFilename = random.choices([fairyFilename, remainsFilename, inputFilename], [fairyWeight, remainWeight, baseWeight])

    if randomFilename[0] == fairyFilename:
        weightFilename = fairyWeightfile
    elif randomFilename[0] == remainsFilename:
        weightFilename = remainsWeightfile
    else:
        weightFilename = baseWeightfile



    with open(randomFilename[0], "r") as read_file:
        data = json.load(read_file)

    settings = data["GameplaySettings"]
    itemListString = settings["CustomItemListString"]
    startListString = settings["CustomStartingItemListString"]
    junkListString = settings["CustomJunkLocationsString"]


    with open(weightFilename, "r") as read_file:
        weights = json.load(read_file)

    settingsweights = weights["GameplaySettings"]

    remainsShuffleActive = False
    fairyHuntActive = False

    if (CheckStringInListString(itemListString,
                                "-----f00000--------------------------------")):
        if ("GreatFairyRewards" in settings["BossRemainsMode"] or "Fairies" in settings["VictoryMode"]):
            fairyHuntActive = True
        else:
            if not (CheckStringInListString(startListString, "3e0000-------")):
                remainsShuffleActive = True
      
    gossipHintsTakenByAlways = 4 + settings["OverrideNumberOfRequiredGossipHints"] + settings["OverrideNumberOfNonRequiredGossipHints"]
    GOSSIP_HINTS_LIMIT = 12  # intentionally two less than the 14 gossip slots available

    nonzeroCategories = 0
    NONZERO_CATEGORIES_MINIMUM = settingsweights["MinimumNonZeroCategories"]

    hardOptions = 0
    hardOptionLimitBonus = settingsweights["HardOptionLimitBonus"]
    HARD_OPTIONS_LIMIT = settingsweights["HardOptionsLimit"]

    if (fairyHuntActive == True):
        itemListString = AddStringToListString(itemListString,
                                               "--------------------------3fffffff-fffffffc----------")
        junkListString = AddStringToListString(junkListString,
                                               "--------------------------3fffffff-fffffffc----------")

    catTrapEnabled = random.choices(settingsweights["TrapAmount"][0], settingsweights["TrapAmount"][1])
    settings["TrapAmount"] = catTrapEnabled[0]
    if catTrapEnabled[0] != "None":
        settings["TrapQuirks"] = True
        settings["TrapWeights"] = settingsweights["TrapWeights"]

    catEnemyShuffle = random.choices(settingsweights["RandomizeEnemies"][0], settingsweights["RandomizeEnemies"][1])
    if catEnemyShuffle[0] == "Shuffled":
        settings["RandomizeEnemies"] = True
        
    catCharacterModel = random.choices(settingsweights["Character"][0], settingsweights["Character"][1])
    settings["Character"] = catCharacterModel[0]

    catGiantMaskAnywhere = random.choices(settingsweights["GiantMaskAnywhere"][0], settingsweights["GiantMaskAnywhere"][1])
    if catGiantMaskAnywhere[0] == "Active":
        settings["GiantMaskAnywhere"] = True

    catIronGoron = random.choices(settingsweights["IronGoron"][0], settingsweights["IronGoron"][1])
    if catIronGoron[0] == "Enabled":
        settings["IronGoron"] = True

    catClimbSurfaces = random.choices(settingsweights["ClimbMostSurfaces"][0], settingsweights["ClimbMostSurfaces"][1])
    if catClimbSurfaces[0] == "Enabled":
        settings["ClimbMostSurfaces"] = True

    catDekuHopping = random.choices(settingsweights["ContinuousDekuHopping"][0], settingsweights["ContinuousDekuHopping"][1])
    if catDekuHopping[0] == "Enabled":
        settings["ContinuousDekuHopping"] = True

    catHookshotAnySurface = random.choices(settingsweights["HookshotAnySurface"][0], settingsweights["HookshotAnySurface"][1])
    if catHookshotAnySurface[0] == "Enabled":
        settings["HookshotAnySurface"] = True

    catSunsSongEnabled = random.choices(settingsweights["EnableSunsSong"][0], settingsweights["EnableSunsSong"][1])
    if catSunsSongEnabled[0] == "Enabled":
        settings["EnableSunsSong"] = True

    catDamageEffect = random.choices(settingsweights["DamageEffect"][0], settingsweights["DamageEffect"][1])
    settings["DamageEffect"] = catDamageEffect[0]

    catDamageMode = random.choices(settingsweights["DamageMode"][0], settingsweights["DamageMode"][1])
    settings["DamageMode"] = catDamageMode[0]

    catMovementMode = random.choices(settingsweights["MovementMode"][0], settingsweights["MovementMode"][1])
    settings["MovementMode"] = catMovementMode[0]

    catFloorType = random.choices(settingsweights["FloorType"][0], settingsweights["FloorType"][1])
    settings["FloorType"] = catFloorType[0]

    catClockSpeed = random.choices(settingsweights["ClockSpeed"][0], settingsweights["ClockSpeed"][1])
    settings["ClockSpeed"] = catClockSpeed[0]

    catSongsanity = random.choices(settingsweights["AddSongs"][0],settingsweights["AddSongs"][1])
    if catSongsanity[0] == "Mix songs with items":
        settings["AddSongs"] = True
        itemListString = RemoveEntryFromListString(itemListString,3,"1")
        settings["OverrideHintPriorities"][2].append("SongEpona")
        settings["OverrideNumberOfRequiredGossipHints"] += 1
        gossipHintsTakenByAlways += 1
        nonzeroCategories += 1

    catStartingBossRemains = random.choices(settingsweights["StartingBossRemains"][0], settingsweights["StartingBossRemains"][1])
    if catStartingBossRemains[0] == "One" and fairyHuntActive == False:
        settings["BossRemainsMode"] = "Blitz1"
    if catStartingBossRemains[0] == "Two" and fairyHuntActive == False:
        settings["BossRemainsMode"] = "Blitz2"

    catStartingSwordShield = random.choices(settingsweights["StartingSwordShield"][0],settingsweights["StartingSwordShield"][1])
    if catStartingSwordShield[0] == "Shuffled":
        itemListString = AddEntryToListString(itemListString,7,"4000000")
        itemListString = AddEntryToListString(itemListString,7,"2000000")

    catStartingRandomItem = random.choices(settingsweights["StartingRandomItems"][0],
                                           settingsweights["StartingRandomItems"][1])
    if catStartingRandomItem[0] == "Deku Mask":
        startListString = AddEntryToListString(startListString,0,"1")
    if catStartingRandomItem[0] == "Goron Mask":
        startListString = AddEntryToListString(startListString,1,"200000")
    if catStartingRandomItem[0] == "Zora Mask":
        startListString = AddEntryToListString(startListString,1,"400000")
    if catStartingRandomItem[0] == "Fierce Deity's Mask":
        startListString = AddEntryToListString(startListString,2,"20000")
    if catStartingRandomItem[0] == "Bow":
        startListString = AddEntryToListString(startListString,0,"2")
    if catStartingRandomItem[0] == "Hookshot":
        startListString = AddEntryToListString(startListString,0,"400")
    if catStartingRandomItem[0] == "Magic":
        startListString = AddEntryToListString(startListString,0,"800")
    if catStartingRandomItem[0] == "Bomb Bag":
        startListString = AddEntryToListString(startListString,0,"20")
    if catStartingRandomItem[0] == "Blast Mask":
        startListString = AddEntryToListString(startListString,1,"8")
    if catStartingRandomItem[0] == "Empty Bottle (Dampe's)":
        startListString = AddEntryToListString(startListString,0,"100000")
    if catStartingRandomItem[0] == "Great Fairy's Sword":
        startListString = AddEntryToListString(startListString,0,"8000")
    if catStartingRandomItem[0] == "Adult's Wallet":
        startListString = AddEntryToListString(startListString,0,"40000000")
    if catStartingRandomItem[0] == "Bunny Hood":
        startListString = AddEntryToListString(startListString,1,"100")

    wgtsStartingRandomSong = settingsweights["StartingRandomSong"][1]
    if catSongsanity[0] != "No change":
        wgtsStartingRandomSong[0] = 0
    catStartingRandomSong = random.choices(settingsweights["StartingRandomSong"][0],
                                           wgtsStartingRandomSong)
    if catStartingRandomSong[0] != "No change":
        if catSongsanity[0] == "No change":
            itemListString = RemoveEntryFromListString(itemListString,3,"4")        
    if catStartingRandomSong[0] == "Epona's Song":
        startListString = AddEntryToListString(startListString,1,"8000000")
    if catStartingRandomSong[0] == "Song of Healing":
        startListString = AddEntryToListString(startListString,1,"2000000")
    if catStartingRandomSong[0] == "Song of Storms":
        startListString = AddEntryToListString(startListString,1,"10000000")
    if catStartingRandomSong[0] == "Sonata of Awakening":
        startListString = AddEntryToListString(startListString,1,"20000000")
    if catStartingRandomSong[0] == "Goron Lullaby":
        startListString = AddEntryToListString(startListString,1,"40000000")
    if catStartingRandomSong[0] == "New Wave Bossa Nova":
        startListString = AddEntryToListString(startListString,1,"80000000")
    if catStartingRandomSong[0] == "Elegy of Emptiness":
        startListString = AddEntryToListString(startListString,2,"1")
    if catStartingRandomSong[0] == "Oath to Order":
        startListString = AddEntryToListString(startListString,2,"2")
        if "MoonAccess" in settingsweights:
            catMoonAccess = random.choices(settingsweights["MoonAccess"][0], settingsweights["MoonAccess"][1])
            if catMoonAccess[0] == "Items Placed":
                itemListString = AddStringToListString(itemListString,
                                                       "------------------------------de0000-------")
                nonzeroCategories += 1


    wgtsFierceDeityAnywhere = settingsweights["AllowFierceDeityAnywhere"][1]
    if catStartingRandomItem[0] == "Fierce Deity's Mask":
        wgtsFierceDeityAnywhere = [0,100]
    catFierceDeityAnywhere = random.choices(settingsweights["AllowFierceDeityAnywhere"][0], wgtsFierceDeityAnywhere)
    if catFierceDeityAnywhere[0] == "Active":
        settings["AllowFierceDeityAnywhere"] = True

    wgtsShopsanityPrices = settingsweights["NoShopsanityPriceShuffle"][1]
    catShopsanityChecks = random.choices(settingsweights["Shopsanity"][0],
                                         settingsweights["Shopsanity"][1])
    if catShopsanityChecks[0] == "Late Shopsanity":
        itemListString = AddStringToListString(itemListString,
                                               "-------------------------3--------3f000----")
        wgtsShopsanityPrices = settingsweights["LateShopsanityPriceShuffle"][1]
    if catShopsanityChecks[0] == "Full Shopsanity":
        itemListString = AddStringToListString(itemListString,
                                               "-------------------------b03--------3ffff-80000000---")
        wgtsShopsanityPrices = settingsweights["FullShopsanityPriceShuffle"][1]

    catShopsanityPrices = random.choices(["No change",
                                          "Shuffle purchase prices",
                                          "Randomize purchase prices"],
                                         wgtsShopsanityPrices)
    if catShopsanityPrices[0] == "Shuffle purchase prices":
        settings["PriceMode"] = "Purchases, ShuffleOnly"
        itemListString = AddEntryToListString(itemListString,1,"1")
    if catShopsanityPrices[0] == "Randomize purchase prices":
        settings["PriceMode"] = "Purchases"
        itemListString = AddEntryToListString(itemListString,1,"1")
        settings["FillWallet"] = True

    if catShopsanityChecks[0] != "No change" or catShopsanityPrices[0] != "No change":
        nonzeroCategories += 1

    catSoilsanity = random.choices(settingsweights["Soilsanity"][0],settingsweights["Soilsanity"][1])
    if catSoilsanity[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----------7ff-f0000000-------------------------")
        settings["OverrideHintPriorities"][2].append("CollectableRomaniRanchSoftSoil1")
        nonzeroCategories += 1

    catCowsanity = random.choices(settingsweights["Cowsanity"][0],settingsweights["Cowsanity"][1])
    if catCowsanity[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----------------------------1f-e0000000-------")
        settings["OverrideHintPriorities"][1].append("ItemWellCowMilk")
        nonzeroCategories += 1

    wgtsStrayFairies = settingsweights["StrayFairysanity"][1]
    catStrayFairies = random.choices(settingsweights["StrayFairysanity"][0],
                                     wgtsStrayFairies)
    if catStrayFairies[0] == "Most chest fairies + CT":
        if (wgtsStrayFairies[0] > 0):
            nonzeroCategories += 1
        if (fairyHuntActive == False):
            itemListString = AddStringToListString(itemListString,
                                                   "--------------------------3fbb83f0-7f003802----------")
        else:
            itemListString = AddEntryToListString(itemListString,10,"2")
            junkListString = RemoveStringFromListString(junkListString,
                                                        "--------------------------3fbb83f0-7f003800----------")
    if catStrayFairies[0] == "All stray fairies":
        nonzeroCategories += 1
        settings["OverrideHintPriorities"][2].append("CollectibleStrayFairyStoneTower8")
        settings["OverrideHintPriorities"][2].append("CollectibleStrayFairyStoneTower4")
        if (fairyHuntActive == False):
            itemListString = AddStringToListString(itemListString,
                                                   "--------------------------3fffffff-fffffffe----------")
            settings["StrayFairyMode"] = "Default"
        else:
            itemListString = AddEntryToListString(itemListString,10,"2")
            junkListString = RemoveStringFromListString(junkListString,
                                                        "--------------------------3fffffff-fffffffc----------")

    catEntrancesTemples = random.choices(settingsweights["RandomizeDungeonEntrances"][0], settingsweights["RandomizeDungeonEntrances"][1])
    if catEntrancesTemples[0] == "Shuffled":
        settings["RandomizeDungeonEntrances"] = True
    catEntrancesBossRooms = random.choices(settingsweights["RandomizeBossRooms"][0], settingsweights["RandomizeBossRooms"][1])
    if catEntrancesBossRooms[0] == "Shuffled":
        settings["RandomizeBossRooms"] = True

    if catEntrancesTemples[0] != "No change" or catEntrancesBossRooms[0] != "No change":
        nonzeroCategories += 1

    wgtsKeysanityBossKeys = settingsweights["BossKeyMode"][1]
    if hardOptions >= HARD_OPTIONS_LIMIT:
        wgtsKeysanityBossKeys[2] += wgtsKeysanityBossKeys[3]
        wgtsKeysanityBossKeys[3] = 0
    catKeysanityBossKeys = random.choices(settingsweights["BossKeyMode"][0],
                                          wgtsKeysanityBossKeys)
    if catKeysanityBossKeys[0] == "Vanilla":
        settings["BossKeyMode"] = "KeepThroughTime"
        itemListString = RemoveStringFromListString(itemListString, "----------------------------------4411000---")
    if catKeysanityBossKeys[0] == "Shuffled within their temple":
        settings["BossKeyMode"] = "KeepWithinArea, KeepWithinTemples, KeepThroughTime"
    if catKeysanityBossKeys[0] == "Shuffled within any temple":
        settings["BossKeyMode"] = "KeepWithinTemples, KeepThroughTime"
        hardOptions += 1
    if catKeysanityBossKeys[0] == "Shuffled within area":
        settings["BossKeyMode"] = "KeepWithinArea, KeepThroughTime"
    if catKeysanityBossKeys[0] == "Shuffled anywhere":
        settings["BossKeyMode"] = "KeepThroughTime"
        settings["OverrideNumberOfRequiredGossipHints"] += 1
        gossipHintsTakenByAlways += 1

    catKeysanitySmallKeys = random.choices(settingsweights["SmallKeyMode"][0], settingsweights["SmallKeyMode"][1])
    if catKeysanitySmallKeys[0] == "Vanilla":
        settings["SmallKeyMode"] = "KeepThroughTime"
        itemListString = RemoveStringFromListString(itemListString, "----------------------------------788e2000---")
    if catKeysanitySmallKeys[0] == "Shuffled within their temple":
        settings["SmallKeyMode"] = "KeepWithinArea, KeepWithinTemples, KeepThroughTime"
    if catKeysanitySmallKeys[0] == "Shuffled within any temple":
        settings["SmallKeyMode"] = "KeepWithinTemples, KeepThroughTime"
        settings["OverrideHintPriorities"][2].remove("ItemIceArrow")
        settings["OverrideHintPriorities"][1].append("ItemIceArrow")
    if catKeysanitySmallKeys[0] == "Shuffled within area":
        settings["SmallKeyMode"] = "KeepWithinArea, KeepThroughTime"
    if catKeysanitySmallKeys[0] == "Shuffled anywhere":
        settings["SmallKeyMode"] = "KeepThroughTime"

    if (catKeysanityBossKeys[0] != "Keysy" and "Vanilla") or (catKeysanitySmallKeys[0] != "Keysy" and "Vanilla"):
        nonzeroCategories += 1

    catScoopsanity = random.choices(settingsweights["Scoopsanity"][0],
                                       settingsweights["Scoopsanity"][1])
    if catScoopsanity[0] == "Shuffled with scoops":
        itemListString = AddStringToListString(itemListString,
                                               "---------------------------------fdc0000----")
        settings["OverrideHintPriorities"][1].append("BottleCatchBigPoe")
        nonzeroCategories += 1

    catHitSpots = random.choices(settingsweights["HitSpotShuffle"][0], settingsweights["HitSpotShuffle"][1])
    if catHitSpots[0] == "One Rupee each":
        itemListString = AddStringToListString(itemListString,
                                               "-------924924-92492492-49240000---8000000-------------------------")
    if catHitSpots[0] == "All Rupees":
        itemListString = AddStringToListString(itemListString,
                                               "-------1ffffff-ffffffff-fffe0000---8000000-------------------------")
    if catHitSpots[0] != "No change":
        nonzeroCategories += 1

    catTokensanity = random.choices(settingsweights["Tokensanity"][0], settingsweights["Tokensanity"][1])
    catTokensanityHouse = ["No change"]
    if catTokensanity[0] == "One house":
        catTokensanityHouse = random.choices(settingsweights["TokenHouse"][0],settingsweights["TokenHouse"][1])
        if catTokensanityHouse[0] == "SSH":
            itemListString = AddStringToListString(itemListString,
                                               "----------------------------7-ffffffe0--------")
        if catTokensanityHouse[0] == "OSH":
            itemListString = AddStringToListString(itemListString,
                                               "---------------------------1-fffffff8---------")
    if catTokensanity[0] == "Both houses":
        itemListString = AddStringToListString(itemListString,
                                               "---------------------------1-ffffffff-ffffffe0--------")
    if catTokensanity[0] != "No change":
        nonzeroCategories += 1

    catCratesAndBarrels = random.choices(settingsweights["CratesandBarrelsShuffle"][0], settingsweights["CratesandBarrelsShuffle"][1])
    if catCratesAndBarrels[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "---------------c0000-2000--3c200--30--1f078-8000008-10000100-20000000------------")
        nonzeroCategories += 1

    catKeatonGrass = random.choices(settingsweights["KeatonGrassShuffle"][0], settingsweights["KeatonGrassShuffle"][1])
    if catKeatonGrass[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----1f-fffffc00-------------------------------")
        nonzeroCategories += 1

    catGossipFairies = random.choices(settingsweights["GossipFairyShuffle"][0], settingsweights["GossipFairyShuffle"][1])
    if catGossipFairies[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-100000-ffffff00-----------------------------------")
        nonzeroCategories += 1
        if "MoonAccess" in settingsweights and catStartingRandomSong[0] == "Oath to Order":
            if catMoonAccess[0] == "Items Placed":
                itemListString = AddStringToListString(itemListString,
                                                       "-fffff------------------------------------")

    catButterflyAndWellFairies = random.choices(settingsweights["ButterflyFairyShuffle"][0], settingsweights["ButterflyFairyShuffle"][1])
    if catButterflyAndWellFairies[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "1fe-1fe00000------------------------------------")
        if ("ChestWellLeftPurpleRupee" in settings["OverrideHintPriorities"][2]):
            settings["OverrideHintPriorities"][2].remove("ChestWellLeftPurpleRupee")
        nonzeroCategories += 1

    wgtsLongQuests = settingsweights["LongQuestShuffle"][1]
    if hardOptions >= HARD_OPTIONS_LIMIT:
        wgtsLongQuests[4] = 0    
    catLongQuests = random.choices(settingsweights["LongQuestShuffle"][0],
                                   wgtsLongQuests)
    if catLongQuests[0] == "Anju and Kafei" or catLongQuests[0] == "All Long Quests":
        junkListString = RemoveEntryFromListString(junkListString,2,"400000")
        settings["OverrideHintPriorities"][0].append("MaskCouple")
        gossipHintsTakenByAlways += 1
    if catLongQuests[0] == "Baby Zoras" or catLongQuests[0] == "All Long Quests":
        junkListString = RemoveEntryFromListString(junkListString,3,"80")
        settings["OverrideHintPriorities"][0].append("SongNewWaveBossaNova")
        gossipHintsTakenByAlways += 1
        if catSongsanity[0] == "No change":
            if catStartingRandomSong[0] == "No change":
                itemListString = RemoveEntryFromListString(itemListString,3,"4")
            else:
                itemListString = RemoveEntryFromListString(itemListString,3,"1")
    if catLongQuests[0] == "Frog Choir" or catLongQuests[0] == "All Long Quests":
        junkListString = RemoveEntryFromListString(junkListString,1,"8000000")
        settings["OverrideHintPriorities"][0].append("HeartPieceChoir")
        gossipHintsTakenByAlways += 1
    if catLongQuests[0] == "All Long Quests":
        hardOptions += 1
    if catLongQuests[0] != "No change":
        nonzeroCategories += 1

    wgtsFrogs = settingsweights["FrogShuffle"][1]
    if hardOptions >= HARD_OPTIONS_LIMIT and (catLongQuests[0] == "Frog Choir" or catLongQuests[0] == "All Long Quests"):
        wgtsFrogs = [100,0]
    catFrogs = random.choices(settingsweights["FrogShuffle"][0], wgtsFrogs)
    if catFrogs[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "1-e0000000------------------------------------")
        settings["OverrideHintPriorities"][1].append("FrogGreatBayTemple")
        settings["OverrideHintPriorities"][2].append("FrogWoodfallTemple")
        if catLongQuests[0] == "Frog Choir" or catLongQuests[0] == "All Long Quests":
            hardOptions += 1
        nonzeroCategories += 1

    wgtsLooseRupees = settingsweights["LooseRupeeShuffle"][1]
    if hardOptions >= HARD_OPTIONS_LIMIT:
        wgtsLooseRupees[3] += wgtsLooseRupees[4]
        wgtsLooseRupees[4] = 0
    catLooseRupees = random.choices(settingsweights["LooseRupeeShuffle"][0],
                                    wgtsLooseRupees)
    if catLooseRupees[0] == "Temple Red only":
        itemListString = AddStringToListString(itemListString,
                                               "---------------6f370f8----------------------")
    if catLooseRupees[0] == "All Red":
        itemListString = AddStringToListString(itemListString,
                                               "----------8100-40000000-7800000---7f37ffe----------------------")
    if catLooseRupees[0] == "All Red and Blue":
        itemListString = AddStringToListString(itemListString,
                                               "---------8410-8103-c0000000-7c7c10c---7f37ffe------f041fff-ffb00183-c3003e00--------------")
    if catLooseRupees[0] == "All Red, Blue, and Green":
        itemListString = AddStringToListString(itemListString,
                                               "---------1ffff-8000ffff-fdef7800-7fffffc---7f37ffe--1e7-fffc2cff-fffffeff-80000000-f041fff-ffb00183-c3003e00--------------")
        settings["OverrideHintPriorities"][0].remove("MaskScents")
        gossipHintsTakenByAlways -= 1
        hardOptions += 1
    if catLooseRupees[0] != "No change":
        nonzeroCategories += 1

    wgtsSnowsanity = settingsweights["Snowsanity"][1]
    if hardOptions >= HARD_OPTIONS_LIMIT:
        wgtsSnowsanity[1] += wgtsSnowsanity[2]
        wgtsSnowsanity[2] = 0
    catSnowsanity = random.choices(settingsweights["Snowsanity"][0], wgtsSnowsanity)
    if catSnowsanity[0] == "Any-day snowballs":
        itemListString = AddStringToListString(itemListString,
                                               "-----1fc00--------fc0ff00-cf800--c0000----180c006--e00-1c0000-c0000c-------------")
    if catSnowsanity[0] == "All shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----1fc00--------fc0ffff-fc3cf800--c0000----180c006--e00-301c0000-c0000c-------------")
        hardOptions += 1
    if catSnowsanity[0] != "No change":
        nonzeroCategories += 1

    wgtsPotsanity = settingsweights["Potsanity"][1]
    if hardOptions >= HARD_OPTIONS_LIMIT:
        wgtsPotsanity[1] += wgtsPotsanity[2]
        wgtsPotsanity[2] = 0
    catPotsanity = random.choices(settingsweights["Potsanity"][0],
                                  wgtsPotsanity)
    if catPotsanity[0] == "Temples and side dungeons":
        itemListString = AddStringToListString(itemListString,
                                               "-----60--c000000------300000-3c10030-e0000000-4000----12001-f0f00000-60004-6-83fde00-------------")
    if catPotsanity[0] == "All but fairies/owls shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----60--c000000-----3-f03f0000-3c107ff-e0000000-20804fff-fffffe18-100--707d2801-f0f3e000-4e0004-e3c186-b3fdef3-dc000000------------")
        itemListString = RemoveEntryFromListString(itemListString, 0, "40000")
        settings["OverrideHintPriorities"][0].remove("ItemBottleGoronRace")
        settings["OverrideHintPriorities"][1].append("CollectableDekuShrineGreyBoulderRoomPot1")
        if "MoonAccess" in settingsweights and catStartingRandomSong[0] == "Oath to Order":
            if catMoonAccess[0] == "Items Placed":
                itemListString = AddStringToListString(itemListString,
                                                       "----------------f000000---------------------")
        gossipHintsTakenByAlways -= 1
        hardOptions += 1
    if catPotsanity[0] != "No change":
        if ("ChestWellLeftPurpleRupee" in settings["OverrideHintPriorities"][2]):
            settings["OverrideHintPriorities"][2].remove("ChestWellLeftPurpleRupee")
        nonzeroCategories += 1

    wgtsPhotosSales = settingsweights["MundaneShuffle"][1]
    if gossipHintsTakenByAlways >= GOSSIP_HINTS_LIMIT:
        wgtsPhotosSales[0] += wgtsPhotosSales[1]
        wgtsPhotosSales[1] = 0
    catPhotosSales = random.choices(settingsweights["MundaneShuffle"][0], wgtsPhotosSales)
    if catPhotosSales[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----60000--------------------f8c070------------")
        settings["OverrideHintPriorities"][1].remove("HeartPieceSeaHorse")
        settings["OverrideHintPriorities"][0].append("HeartPieceSeaHorse")
        gossipHintsTakenByAlways += 1
        nonzeroCategories += 1

    wgtsMinigames = settingsweights["ExtraMiniGameShuffle"][1]
    if hardOptions >= HARD_OPTIONS_LIMIT or (gossipHintsTakenByAlways + 3) > GOSSIP_HINTS_LIMIT:
        wgtsMinigames[1] += wgtsMinigames[2]
        wgtsMinigames[2] = 0
    if gossipHintsTakenByAlways >= GOSSIP_HINTS_LIMIT:
        wgtsMinigames[0] += wgtsMinigames[1]
        wgtsMinigames[1] = 0
    catMinigames = random.choices(settingsweights["ExtraMiniGameShuffle"][0],
                                   wgtsMinigames)
    catMinigamesExtra = ["No change"]
    if catMinigames[0] == "Swamp 2 + Full TCG + Extra":
        itemListString = AddStringToListString(itemListString,
                                               "-------------------------70000-----------1000000-")
        catMinigamesExtra = random.choices(["DPG Three Days", "H&D Three Days", "Town Archery 50"])
    if catMinigamesExtra[0] == "DPG Three Days" or catMinigames[0] == "All shuffled":
        itemListString = AddEntryToListString(itemListString,1,"20000")  
        settings["OverrideHintPriorities"][0].append("MundaneItemDekuPlaygroundPurpleRupee")
        settings["OverrideHintPriorities"][0].append("HeartPieceDekuPlayground")
        gossipHintsTakenByAlways += 1
    if catMinigamesExtra[0] == "H&D Three Days" or catMinigames[0] == "All shuffled":
        itemListString = AddEntryToListString(itemListString,1,"80000")  
        settings["OverrideHintPriorities"][0].append("MundaneItemHoneyAndDarlingPurpleRupee")
        settings["OverrideHintPriorities"][0].append("HeartPieceHoneyAndDarling")
        gossipHintsTakenByAlways += 1
    if catMinigamesExtra[0] == "Town Archery 50" or catMinigames[0] == "All shuffled":
        itemListString = AddEntryToListString(itemListString,1,"40000")  
        settings["OverrideHintPriorities"][0].append("UpgradeBigQuiver")
        settings["OverrideHintPriorities"][0].append("HeartPieceTownArchery")
        gossipHintsTakenByAlways += 1
    if catMinigames[0] == "All shuffled":
        catMinigamesExtra = ["All three"]
        hardOptions += 1
    if catMinigames[0] != "No change":
        nonzeroCategories += 1
        
    wgtsBombersNotebook = settingsweights["NotebookShuffle"][1]
    if hardOptions >= HARD_OPTIONS_LIMIT or gossipHintsTakenByAlways >= GOSSIP_HINTS_LIMIT:
        wgtsBombersNotebook[1] += wgtsBombersNotebook[2]
        wgtsBombersNotebook[2] = 0
    catBombersNotebook = random.choices(settingsweights["NotebookShuffle"][0],
                                        wgtsBombersNotebook)
    if catBombersNotebook[0] == "Meetings only":
        startListString = AddEntryToListString(startListString,0,"400000")
        itemListString = AddStringToListString(itemListString,
                                               "----1fff-fe000000--------------------------------")
        settings["OverrideHintPriorities"][1].append("NotebookMeetKafei")
        settings["OverrideHintPriorities"][2].append("NotebookMeetShiro")
    if catBombersNotebook[0] == "All shuffled":
        startListString = AddEntryToListString(startListString,0,"400000")
        itemListString = AddStringToListString(itemListString,
                                               "---f7f-ffffffff-fe000000--------------------------------")
        if catLongQuests[0] == "Anju and Kafei" or catLongQuests[0] == "All Long Quests":
            itemListString = AddEntryToListString(itemListString,34,"80")
            settings["OverrideHintPriorities"][0].append("NotebookUniteAnjuAndKafei")
        settings["OverrideHintPriorities"][0].append("NotebookEscapeFromSakonSHideout")
        settings["OverrideHintPriorities"][2].append("NotebookPostmansFreedom")
        settings["OverrideHintPriorities"][2].append("MaskPostmanHat")
        settings["OverrideHintPriorities"][1].append("NotebookPurchaseCuriosityShopItem")
        settings["OverrideHintPriorities"][1].append("MaskAllNight")
        settings["OverrideHintPriorities"][2].append("NotebookDeliverPendant")
        settings["OverrideHintPriorities"][2].append("NotebookDeliverLetterToMama")
        settings["OverrideHintPriorities"][2].append("NotebookPromiseAnjuDelivery")
        settings["OverrideHintPriorities"][0].append("NotebookSaveTheCows")
        settings["OverrideHintPriorities"][0].append("NotebookProtectMilkDelivery")
        settings["OverrideHintPriorities"][2].append("NotebookGrogsThanks")
        settings["OverrideHintPriorities"][2].append("NotebookMovingGorman")
        settings["OverrideHintPriorities"][2].append("NotebookPromiseKamaro")
        settings["OverrideHintPriorities"][2].append("NotebookSaveInvisibleSoldier")
        settings["OverrideHintPriorities"][2].append("NotebookMeetShiro")
        if catSongsanity[0] == "Mix songs with items":
            settings["OverrideHintPriorities"][2].append("NotebookPromiseRomani")
        gossipHintsTakenByAlways += 1
        hardOptions += 1
    if catBombersNotebook[0] != "No change":
        nonzeroCategories += 1

    if fairyHuntActive == True:
        wgtsStrayFairyLocations = settingsweights["StrayFairyMode"][1]
        if (hardOptions >= HARD_OPTIONS_LIMIT and settingsweights["FullFairyHardMode"]):
            wgtsStrayFairyLocations[1] += wgtsStrayFairyLocations[0]
            wgtsStrayFairyLocations[0] = 0
        catStrayFairyLocations = random.choices(settingsweights["StrayFairyMode"][0], wgtsStrayFairyLocations)
        if (catStrayFairyLocations[0] == "Anywhere" and settingsweights["FullFairyHardMode"]):
            hardOptions += 1
        if catStrayFairyLocations[0] == "Regional":
            settings["StrayFairyMode"] = "KeepWithinArea"

    if remainsShuffleActive == True:
        catRemainsLocation = random.choices(settingsweights["BossRemainsMode"][0], settingsweights["BossRemainsMode"][1])
        if catRemainsLocation[0] == "Regional":
            settings["BossRemainsMode"] = "KeepWithinArea"

    if nonzeroCategories < NONZERO_CATEGORIES_MINIMUM:
        return ''
       
    if (hardOptionLimitBonus and remainsShuffleActive == False and fairyHuntActive == False):
        if hardOptions >= HARD_OPTIONS_LIMIT:
            if catStartingBossRemains[0] != "No change":
                catStartingBossRemains[0] = "Two*"
                settings["BossRemainsMode"] = "Blitz2"
            else:
                catStartingBossRemains[0] = "One*"
                settings["BossRemainsMode"] = "Blitz1"

    if (hardOptionLimitBonus and fairyHuntActive):
        if hardOptions >= HARD_OPTIONS_LIMIT:
            if catStrayFairyLocations[0] == "Anywhere":
                catStrayFairyLocations[0] = "Anywhere*"
                startListString = AddEntryToListString(startListString, 2, "1f00000")
                startListString = AddEntryToListString(startListString, 3, "7c00f8")
                startListString = AddEntryToListString(startListString, 4, "3e")
            if catStrayFairyLocations[0] == "Regional":
                catStrayFairyLocations[0] = "Regional*"
                startListString = AddEntryToListString(startListString, 2, "700000")
                startListString = AddEntryToListString(startListString, 3, "1c0038")
                startListString = AddEntryToListString(startListString, 4, "e")

    
    settings["CustomItemListString"] = itemListString
    settings["CustomStartingItemListString"] = startListString
    settings["CustomJunkLocationsString"] = junkListString

    outputFilename = "output\\MysterySettings_" + outputSuffix + ".json" 

    try:
        os.makedirs("output")
    except FileExistsError:
        pass

    with open(outputFilename, "w") as write_file:
        json.dump(data,write_file,indent=4)

    spoilerlogFilename = outputFilename.removesuffix(".json")
    spoilerlogFilename = spoilerlogFilename + "_Spoiler.txt"

    with open(spoilerlogFilename, "w") as spoiler_file:
        print("MMR Mystery Maker", MYSTERY_MAKER_VERSION,"-- Mystery Spoiler Log",file=spoiler_file)
        print("Base settings: ", FilenameOnly(randomFilename[0]),file=spoiler_file)
        print("  Weight file: ", FilenameOnly(weightFilename),file=spoiler_file)
        print("  Output file: ", outputFilename,file=spoiler_file)
        print("=============================================",file=spoiler_file)
        if (remainsShuffleActive == True):
            print("             Special Mode:  Remains Shuffle",file=spoiler_file)
            print("        Remains Locations: ", catRemainsLocation[0],file=spoiler_file)
            print("",file=spoiler_file)
        if (fairyHuntActive == True):
            print("             Special Mode:  Fairy Hunt",file=spoiler_file)
            print("          Fairy Locations: ", catStrayFairyLocations[0],file=spoiler_file)
            print("",file=spoiler_file)
        if (remainsShuffleActive == False and fairyHuntActive == False):
            print("    Starting Boss Remains: ", catStartingBossRemains[0],file=spoiler_file)
        print("Starting Sword and Shield: ", catStartingSwordShield[0],file=spoiler_file)
        print("     Starting Random Item: ", catStartingRandomItem[0],file=spoiler_file)
        print("     Starting Random Song: ", catStartingRandomSong[0],file=spoiler_file)
        print("    Fierce Deity Anywhere: ", catFierceDeityAnywhere[0],file=spoiler_file)
        if settingsweights["GiantMaskAnywhere"][1][0] > 0:
            print("      Giant Mask Anywhere: ", catGiantMaskAnywhere[0],file=spoiler_file)
        if settingsweights["EnableSunsSong"][1][0] > 0:
            print("                Suns Song: ", catSunsSongEnabled[0],file=spoiler_file)
        if settingsweights["ContinuousDekuHopping"][1][0] > 0:
            print("  Continuous Deku Hopping: ", catDekuHopping[0], file=spoiler_file)
        if settingsweights["IronGoron"][1][0] > 0:
            print("               Iron Goron: ", catIronGoron[0],file=spoiler_file)
        if settingsweights["ClimbMostSurfaces"][1][0] > 0:
            print("      Climb Most Surfaces: ", catClimbSurfaces[0],file=spoiler_file)
        if settingsweights["HookshotAnySurface"][1][0] > 0:
            print("     Hookshot Any Surface: ", catHookshotAnySurface[0], file=spoiler_file)
        if sum(settingsweights["Character"][1]) - settingsweights["Character"][1][0] > 0:
            print("          Character Model: ", catCharacterModel[0],file=spoiler_file)
        if sum(settingsweights["TrapAmount"][1]) - settingsweights["TrapAmount"][1][0] > 0:
            print("              Trap Amount: ", catTrapEnabled[0],file=spoiler_file)
        if sum(settingsweights["DamageMode"][1]) - settingsweights["DamageMode"][1][0] > 0:
            print("              Damage Mode: ", catDamageMode[0],file=spoiler_file)
        if sum(settingsweights["DamageEffect"][1]) - settingsweights["DamageEffect"][1][0] > 0:
            print("            Damage Effect: ", catDamageEffect[0],file=spoiler_file)
        if sum(settingsweights["MovementMode"][1]) - settingsweights["MovementMode"][1][0] > 0:
            print("            Movement Mode: ", catMovementMode[0],file=spoiler_file)
        if sum(settingsweights["FloorType"][1]) - settingsweights["FloorType"][1][0] > 0:
            print("               Floor Type: ", catFloorType[0],file=spoiler_file)
        if sum(settingsweights["ClockSpeed"][1]) - settingsweights["ClockSpeed"][1][0] > 0:
            print("              Clock Speed: ", catClockSpeed[0],file=spoiler_file)
        if "MoonAccess" in settingsweights and catStartingRandomSong[0] == "Oath to Order":
            print("              Moon Access: ", catMoonAccess[0],file=spoiler_file)
        print("",file=spoiler_file)
        print("               Songsanity: ", catSongsanity[0],file=spoiler_file) 
        print("       Shopsanity: Checks: ", catShopsanityChecks[0],file=spoiler_file)
        print("       Shopsanity: Prices: ", catShopsanityPrices[0],file=spoiler_file)
        print("               Soilsanity: ", catSoilsanity[0],file=spoiler_file)
        print("                Cowsanity: ", catCowsanity[0],file=spoiler_file)
        print("            Stray Fairies: ", catStrayFairies[0],file=spoiler_file)
        print("       Entrances: Temples: ", catEntrancesTemples[0],file=spoiler_file)
        print("    Entrances: Boss Rooms: ", catEntrancesBossRooms[0],file=spoiler_file)
        print("     Keysanity: Boss Keys: ", catKeysanityBossKeys[0],file=spoiler_file)
        print("    Keysanity: Small Keys: ", catKeysanitySmallKeys[0],file=spoiler_file)
        print("              Scoopsanity: ", catScoopsanity[0],file=spoiler_file)
        print("                Hit Spots: ", catHitSpots[0],file=spoiler_file)
        if catTokensanity[0] == "One house":
            print("              Tokensanity: ", catTokensanity[0], "--", catTokensanityHouse[0],file=spoiler_file)
        else:
            print("              Tokensanity: ", catTokensanity[0],file=spoiler_file)
        print("       Crates and Barrels: ", catCratesAndBarrels[0],file=spoiler_file)
        print("             Keaton Grass: ", catKeatonGrass[0],file=spoiler_file)
        print("   Butterfly/Well Fairies: ", catButterflyAndWellFairies[0],file=spoiler_file)
        print("              Long Quests: ", catLongQuests[0],file=spoiler_file)
        print("                    Frogs: ", catFrogs[0],file=spoiler_file)
        print("             Loose Rupees: ", catLooseRupees[0],file=spoiler_file)
        print("               Snowsanity: ", catSnowsanity[0],file=spoiler_file)
        print("                Potsanity: ", catPotsanity[0],file=spoiler_file)
        print("Photos/Sales/Small Favors: ", catPhotosSales[0],file=spoiler_file)
        if catMinigames[0] == "Swamp 2 + Full TCG + Extra":
            print("                Minigames: ", catMinigames[0], "--", catMinigamesExtra[0],file=spoiler_file)
        else:
            print("                Minigames: ", catMinigames[0],file=spoiler_file)
        print("        Bombers' Notebook: ", catBombersNotebook[0],file=spoiler_file)
        if settingsweights["RandomizeEnemies"][1][1] > 0:
            print("            Enemy Shuffle: ", catEnemyShuffle[0],file=spoiler_file)
        print("---------------------------------------------",file=spoiler_file)
        print("  Gossip slots for always: ",gossipHintsTakenByAlways,file=spoiler_file)
        print("        Hard options used: ",hardOptions,file=spoiler_file)
        print("       Nonzero categories: ",nonzeroCategories,file=spoiler_file)

    return outputFilename

argParser = argparse.ArgumentParser(description="Randomly generates Mystery settings files for MMR and runs MMR.CLI to roll seeds with them.")
argParser.add_argument("-n", dest="numberOfSettingsFiles",type=int,default=1,
                    help="create multiple settings/seeds at once")
argParser.add_argument("-i", "--input", dest="inputFile",default="Default_Mystery_base.json",
                    help="base MMR settings file")
argParser.add_argument("-f", "--finput", dest="fairyFile",default="Mystery_Fairy_Hunt_base.json",
                    help="Fairy Hunt MMR settings file")
argParser.add_argument("-rh", "--rhinput", dest="remainsFile",default="Mystery_Remains_Shuffle_base.json",
                    help="Remains Hunt MMR settings file")
argParser.add_argument("-r", "--randomizer-exe", dest="randomizerExe",default="MMR.CLI.exe",
                    help="MMR command-line executable")   
argParser.add_argument("--settings-only", dest="settingsOnly", action="store_true",
                    help="only generate settings; don't roll any seeds")
argParser.add_argument("--version", dest="showVersion", action="store_true",
                    help="print version number and exit")
argParser.add_argument("-fw", dest="fairyHuntChance",type=int,default=0,
                    help="weight of fairy hunt seed")
argParser.add_argument("-rw", dest="remainHuntChance",type=int,default=0,
                    help="weight of remain hunt seed")
argParser.add_argument("-bw", dest="baseChance",type=int,default=0,
                    help="weight of base settings")
args = argParser.parse_args()

if (args.showVersion):
    print("MMR Mystery Maker", MYSTERY_MAKER_VERSION)
    sys.exit()

optionSettingsFile = args.inputFile
optionFairyFile = args.fairyFile
optionRemainsFile = args.remainsFile
optionFairyWeight = args.fairyHuntChance
optionRemainsWeight = args.remainHuntChance
optionBaseWeight = args.baseChance
optionRandomizerExe = args.randomizerExe
optionOutputCount = args.numberOfSettingsFiles
optionDontMakeSeed = args.settingsOnly

if (len(sys.argv) == 1):
    guiResults = openOptionsGui()
    if (guiResults[0]):
        sys.exit()
    optionSettingsFile = guiResults[1]
    optionFairyFile = guiResults[2]
    optionRemainsFile = guiResults[3]
    optionRandomizerExe = guiResults[4]
    optionOutputCount = guiResults[8]
    optionDontMakeSeed = guiResults[12]
    optionFairyWeight = guiResults[5]
    optionRemainsWeight = guiResults[6]
    optionBaseWeight = guiResults[7]
    optionBaseWeightsFile = guiResults[9]
    optionFairyWeightsFile = guiResults[10]
    optionRemainsWeightsFile = guiResults[11]

for i in range(optionOutputCount):
    resultFilename = ''
    while (resultFilename == ''):
        resultFilename = GenerateMysterySettings(optionSettingsFile, optionFairyFile, optionRemainsFile, optionFairyWeight, optionRemainsWeight, optionBaseWeight, optionBaseWeightsFile, optionFairyWeightsFile, optionRemainsWeightsFile, (str)(i+1))
    if (optionDontMakeSeed == False):
        mmrcl = optionRandomizerExe + " -outputpatch -spoiler -settings " + resultFilename
        subprocess.call(mmrcl)
