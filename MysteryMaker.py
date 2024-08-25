import json
import random
import subprocess
import argparse
import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

MYSTERY_MAKER_VERSION = "v3.0"

def openOptionsGui():
    def guiStartRandomize(*args):
        guiWindow.destroy()

    def guiCloseButton(*args):
        windowForceClosed.set("1")
        guiWindow.destroy()

    def browseForBaseSettingsFile(*args):
        baseSettingsFilePath.set(filedialog.askopenfilename())

    def browseForFairySettingsFile(*args):
        fairySettingsFilePath.set(filedialog.askopenfilename())

    def browseForRemainsSettingsFile(*args):
        remainsSettingsFilePath.set(filedialog.askopenfilename())

    def browseForCommandLineExe(*args):
        mmrCommandLineExePath.set(filedialog.askopenfilename())

    guiWindow = Tk()
    guiWindow.title("MMR Mystery Maker " + MYSTERY_MAKER_VERSION)

    mainframe = ttk.Frame(guiWindow, padding="8 8 4 8")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    guiWindow.columnconfigure(0, weight=1)
    guiWindow.rowconfigure(0, weight=1)

    windowForceClosed = StringVar(value="0")

    baseSettingsFilePath = StringVar(value="Default_Mystery_base.json")
    baseSettingsFilePath_entry = ttk.Entry(mainframe, width=70, textvariable=baseSettingsFilePath)
    baseSettingsFilePath_entry.grid(column=2, row=1, sticky=(W, E))

    fairySettingsFilePath = StringVar(value="Mystery_Fairy_Hunt_base.json")
    fairySettingsFilePath_entry = ttk.Entry(mainframe, width=70, textvariable=fairySettingsFilePath)
    fairySettingsFilePath_entry.grid(column=2, row=2, sticky=(W, E))

    remainsSettingsFilePath = StringVar(value="Mystery_Remains_Shuffle_base.json")
    remainsSettingsFilePath_entry = ttk.Entry(mainframe, width=70, textvariable=remainsSettingsFilePath)
    remainsSettingsFilePath_entry.grid(column=2, row=3, sticky=(W, E))
	
    mmrCommandLineExePath = StringVar(value="MMR.CLI.exe")
    mmrCommandLineExePath_entry = ttk.Entry(mainframe, width=70, textvariable=mmrCommandLineExePath)
    mmrCommandLineExePath_entry.grid(column=2, row=4, sticky=(W, E))
	
    fairyHuntChance = StringVar(value="0")
    fairyHuntChance_spinbox = ttk.Spinbox(mainframe, width=5, from_=0, to=100,textvariable=fairyHuntChance)
    fairyHuntChance_spinbox.grid(column=2, row=5, sticky=W)
	
    remainHuntChance = StringVar(value="0")
    remainHuntChance_spinbox = ttk.Spinbox(mainframe, width=5, from_=0, to=100,textvariable=remainHuntChance)
    remainHuntChance_spinbox.grid(column=2, row=6, sticky=W)

    totalChance = StringVar(value="1")
    totalChance_spinbox = ttk.Spinbox(mainframe, width=5, from_=1, to=100,textvariable=totalChance)
    totalChance_spinbox.grid(column=2, row=7, sticky=W)

    numberToGenerate = StringVar(value="1")
    numberToGenerate_spinbox = ttk.Spinbox(mainframe, width=5, from_=1, to=100,textvariable=numberToGenerate)
    numberToGenerate_spinbox.grid(column=2, row=8, sticky=W)

    makeSettingsOnly = StringVar(value="0")
    makeSettingsOnly_checkbutton = ttk.Checkbutton(mainframe, text="Only make settings file", variable=makeSettingsOnly)
    makeSettingsOnly_checkbutton.grid(column=1, row=9, sticky=E)

    ttk.Button(mainframe, text="Browse...", command=browseForBaseSettingsFile).grid(column=3, row=1, sticky=W)
    ttk.Button(mainframe, text="Browse...", command=browseForFairySettingsFile).grid(column=3, row=2, sticky=W)
    ttk.Button(mainframe, text="Browse...", command=browseForRemainsSettingsFile).grid(column=3, row=3, sticky=W)
    ttk.Button(mainframe, text="Browse...", command=browseForCommandLineExe).grid(column=3, row=4, sticky=W)
    ttk.Button(mainframe, text="Randomize", command=guiStartRandomize).grid(column=3, row=8, sticky=W)

    ttk.Label(mainframe, text="Custom base MMR settings file:").grid(column=1, row=1, sticky=E)
    ttk.Label(mainframe, text="Custom fairy hunt MMR settings file:").grid(column=1, row=2, sticky=E)
    ttk.Label(mainframe, text="Custom remains hunt MMR settings file:").grid(column=1, row=3, sticky=E)
    ttk.Label(mainframe, text="Weight of Fairy Hunt:").grid(column=1, row=5, sticky=E)
    ttk.Label(mainframe, text="Weight of Remain Hunt:").grid(column=1, row=6, sticky=E)
    ttk.Label(mainframe, text="Total Weight:").grid(column=1, row=7, sticky=E)
    ttk.Label(mainframe, text="Custom path to MMR.CLI.exe:").grid(column=1, row=4, sticky=E)
    ttk.Label(mainframe, text="# of seeds:").grid(column=1, row=8, sticky=E)

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
            (int)(totalChance.get()),
            (int)(numberToGenerate.get()),
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
    
def GenerateMysterySettings(inputFilename, fairyFilename, remainsFilename, fairyWeight, remainWeight, totalWeight, outputSuffix="output"):

    random.seed()

    randomFilename = random.choices([fairyFilename, remainsFilename, inputFilename], [fairyWeight, remainWeight, max(totalWeight - remainWeight - fairyWeight, 0)])

    with open(randomFilename[0], "r") as read_file:
        data = json.load(read_file)

    settings = data["GameplaySettings"]
    itemListString = settings["CustomItemListString"]
    startListString = settings["CustomStartingItemListString"]
    junkListString = settings["CustomJunkLocationsString"]

    remainsShuffleActive = False
    fairyHuntActive = False

    if (CheckStringInListString(itemListString,
                                "-----f00000--------------------------------")):
        if ("GreatFairyRewards" in settings["BossRemainsMode"]):
            fairyHuntActive = True
        else:
            remainsShuffleActive = True
      
    gossipHintsTakenByAlways = 4 + settings["OverrideNumberOfRequiredGossipHints"] + settings["OverrideNumberOfNonRequiredGossipHints"]
    GOSSIP_HINTS_LIMIT = 12  # intentionally two less than the 14 gossip slots available

    nonzeroCategories = 0
    NONZERO_CATEGORIES_MINIMUM = 5

    hardOptions = 0
    hardOptionLimitBonus = False
    HARD_OPTIONS_LIMIT = 2

    if (fairyHuntActive == True):
        itemListString = AddStringToListString(itemListString,
                                               "--------------------------3fffffff-fffffffc----------")
        junkListString = AddStringToListString(junkListString,
                                               "--------------------------3fffffff-fffffffc----------")

    catSongsanity = random.choices(["No change","Mix songs with items"],[65,35])
    if catSongsanity[0] == "Mix songs with items":
        settings["AddSongs"] = True
        itemListString = RemoveEntryFromListString(itemListString,3,"1")
        settings["OverrideHintPriorities"][2].append("SongEpona")
        settings["OverrideNumberOfRequiredGossipHints"] += 1
        gossipHintsTakenByAlways += 1
        nonzeroCategories += 1

    wgtsStartingBossRemains = [70,25,10]
    if (remainsShuffleActive or fairyHuntActive):
        wgtsStartingBossRemains = [100,0,0]
    catStartingBossRemains = random.choices(["No change","One","Two"], wgtsStartingBossRemains)
    if catStartingBossRemains[0] == "One" and fairyHuntActive == False:
        settings["BossRemainsMode"] = "Blitz1"
    if catStartingBossRemains[0] == "Two" and fairyHuntActive == False:
        settings["BossRemainsMode"] = "Blitz2"

    catStartingSwordShield = random.choices(["No change","Shuffled"],[75,25])
    if catStartingSwordShield[0] == "Shuffled":
        itemListString = AddEntryToListString(itemListString,7,"4000000")
        itemListString = AddEntryToListString(itemListString,7,"2000000")

    catStartingRandomItem = random.choices(["No change",
                                            "Deku Mask",
                                            "Goron Mask",
                                            "Zora Mask",
                                            "Fierce Deity's Mask",
                                            "Bow",
                                            "Hookshot",
                                            "Bomb Bag",
                                            "Blast Mask",
                                            "Adult's Wallet",
                                            "Empty Bottle (Dampe's)",
                                            "Bunny Hood",
                                            "Great Fairy's Sword",
                                            "Magic"],
                                           [0,10,10,10,10,10,10,5,5,10,10,5,5,0])
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


    wgtsStartingRandomSong = [0,40,10,10,10,10,10,10,0]
    if catSongsanity[0] != "No change":
        wgtsStartingRandomSong[0] = 0
    catStartingRandomSong = random.choices(["No change",
                                            "Epona's Song",
                                            "Song of Healing",
                                            "Song of Storms",
                                            "Sonata of Awakening",
                                            "Goron Lullaby",
                                            "New Wave Bossa Nova",
                                            "Elegy of Emptiness",
                                            "Oath to Order"],
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

    wgtsFierceDeityAnywhere = [55,45]
    if catStartingRandomItem[0] == "Fierce Deity's Mask":
        wgtsFierceDeityAnywhere = [0,100]
    catFierceDeityAnywhere = random.choices(["No change","Active"], wgtsFierceDeityAnywhere)
    if catFierceDeityAnywhere[0] == "Active":
        settings["AllowFierceDeityAnywhere"] = True

    wgtsShopsanityPrices = [70,20,10]
    catShopsanityChecks = random.choices(["No change",
                                          "Late Shopsanity",
                                          "Full Shopsanity"],
                                         [60,20,20])
    if catShopsanityChecks[0] == "Late Shopsanity":
        itemListString = AddStringToListString(itemListString,
                                               "-------------------------3--------3f000----")
        wgtsShopsanityPrices = [50,35,15]
    if catShopsanityChecks[0] == "Full Shopsanity":
        itemListString = AddStringToListString(itemListString,
                                               "-------------------------b03--------3ffff-80000000---")
        wgtsShopsanityPrices = [10,65,25]

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

    catSoilsanity = random.choices(["No change","Shuffled"],[70,30])
    if catSoilsanity[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----------7ff-f0000000-------------------------")
        settings["OverrideHintPriorities"][2].append("CollectableRomaniRanchSoftSoil1")
        nonzeroCategories += 1

    catCowsanity = random.choices(["No change","Shuffled"],[70,30])
    if catCowsanity[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----------------------------1f-e0000000-------")
        settings["OverrideHintPriorities"][1].append("ItemWellCowMilk")
        nonzeroCategories += 1

    wgtsStrayFairies = [0,70,30]
    catStrayFairies = random.choices(["No change",
                                      "Most chest fairies + CT",
                                      "All stray fairies"],
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

    wgtsEntrancesTemples = [55,45]
    wgtsEntrancesBossRooms = [70,30]
    catEntrancesTemples = random.choices(["No change","Shuffled"], wgtsEntrancesTemples)
    if catEntrancesTemples[0] == "Shuffled":
        settings["RandomizeDungeonEntrances"] = True
    catEntrancesBossRooms = random.choices(["No change","Shuffled"], wgtsEntrancesBossRooms)
    if catEntrancesBossRooms[0] == "Shuffled":
        settings["RandomizeBossRooms"] = True

    if catEntrancesTemples[0] != "No change" or catEntrancesBossRooms[0] != "No change":
        nonzeroCategories += 1

    wgtsKeysanityBossKeys = [50,30,20,0,0]
    if (fairyHuntActive == True):
        wgtsKeysanityBossKeys = [100,0,0,0,0]
    if hardOptions >= HARD_OPTIONS_LIMIT:
        wgtsKeysanityBossKeys[1] += wgtsKeysanityBossKeys[2]
        wgtsKeysanityBossKeys[2] = 0
    catKeysanityBossKeys = random.choices(["No change",
                                           "Shuffled within their temple",
                                           "Shuffled within any temple",
                                           "Shuffled within area",
                                           "Shuffled anywhere"],
                                          wgtsKeysanityBossKeys)
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

    catKeysanitySmallKeys = random.choices(["No change",
                                            "Shuffled within their temple",
                                            "Shuffled within any temple",
                                            "Shuffled within area",
                                            "Shuffled anywhere"],
                                           [60,20,20,0,0])
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

    if catKeysanityBossKeys[0] != "No change" or catKeysanitySmallKeys[0] != "No change":
        nonzeroCategories += 1

    catScoopsanity = random.choices(["No change","Shuffled with scoops"],
                                       [75,25])
    if catScoopsanity[0] == "Shuffled with scoops":
        itemListString = AddStringToListString(itemListString,
                                               "---------------------------------fdc0000----")
        settings["OverrideHintPriorities"][1].append("BottleCatchBigPoe")
        nonzeroCategories += 1

    catHitSpots = random.choices(["No change", "One Rupee each", "All Rupees"], [70,25,5])
    if catHitSpots[0] == "One Rupee each":
        itemListString = AddStringToListString(itemListString,
                                               "-------924924-92492492-49240000---8000000-------------------------")
    if catHitSpots[0] == "All Rupees":
        itemListString = AddStringToListString(itemListString,
                                               "-------1ffffff-ffffffff-fffe0000---8000000-------------------------")
    if catHitSpots[0] != "No change":
        nonzeroCategories += 1

    catTokensanity = random.choices(["No change","One house","Both houses"], [80,15,5])
    catTokensanityHouse = ["No change"]
    if catTokensanity[0] == "One house":
        catTokensanityHouse = random.choices(["SSH","OSH"],[1,1])
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

    catCratesAndBarrels = random.choices(["No change","Shuffled"], [70,30])
    if catCratesAndBarrels[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "---------------c0000-2000--3c200--30--1f078-8000008-10000100-20000000------------")
        nonzeroCategories += 1

    catKeatonGrass = random.choices(["No change","Shuffled"], [75,25])
    if catKeatonGrass[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----1f-fffffc00-------------------------------")
        nonzeroCategories += 1

    catGossipFairies = random.choices(["No change","Shuffled"], [100,0])
    if catGossipFairies[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-100000-ffffff00-----------------------------------")
        nonzeroCategories += 1

    catButterflyAndWellFairies = random.choices(["No change","Shuffled"], [75,25])
    if catButterflyAndWellFairies[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "1fe-1fe00000------------------------------------")
        if ("ChestWellLeftPurpleRupee" in settings["OverrideHintPriorities"][2]):
            settings["OverrideHintPriorities"][2].remove("ChestWellLeftPurpleRupee")
        nonzeroCategories += 1

    wgtsLongQuests = [35,20,15,30,0]
    if hardOptions >= HARD_OPTIONS_LIMIT:
        wgtsLongQuests[4] = 0    
    catLongQuests = random.choices(["No change",
                                    "Anju and Kafei",
                                    "Baby Zoras",
                                    "Frog Choir",
                                    "All Long Quests"],
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

    wgtsFrogs = [65,35]
    if hardOptions >= HARD_OPTIONS_LIMIT and (catLongQuests[0] == "Frog Choir" or catLongQuests[0] == "All Long Quests"):
        wgtsFrogs = [100,0]
    catFrogs = random.choices(["No change","Shuffled"], wgtsFrogs)
    if catFrogs[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "1-e0000000------------------------------------")
        settings["OverrideHintPriorities"][1].append("FrogGreatBayTemple")
        settings["OverrideHintPriorities"][2].append("FrogWoodfallTemple")
        if catLongQuests[0] == "Frog Choir" or catLongQuests[0] == "All Long Quests":
            hardOptions += 1
        nonzeroCategories += 1

    wgtsLooseRupees = [60,10,10,10,10]
    if hardOptions >= HARD_OPTIONS_LIMIT:
        wgtsLooseRupees[3] += wgtsLooseRupees[4]
        wgtsLooseRupees[4] = 0
    catLooseRupees = random.choices(["No change",
                                     "Temple Red only",
                                     "All Red",
                                     "All Red and Blue",
                                     "All Red, Blue, and Green"],
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

    wgtsSnowsanity = [85,15,0]
    if hardOptions >= HARD_OPTIONS_LIMIT:
        wgtsSnowsanity[1] += wgtsSnowsanity[2]
        wgtsSnowsanity[2] = 0
    catSnowsanity = random.choices(["No change","Any-day snowballs","All shuffled"], wgtsSnowsanity)
    if catSnowsanity[0] == "Any-day snowballs":
        itemListString = AddStringToListString(itemListString,
                                               "-----1fc00--------fc0ff00-cf800--c0000----180c006--e00-1c0000-c0000c-------------")
    if catSnowsanity[0] == "All shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----1fc00--------fc0ffff-fc3cf800--c0000----180c006--e00-301c0000-c0000c-------------")
        hardOptions += 1
    if catSnowsanity[0] != "No change":
        nonzeroCategories += 1

    wgtsPotsanity = [80,10,10]
    if hardOptions >= HARD_OPTIONS_LIMIT:
        wgtsPotsanity[1] += wgtsPotsanity[2]
        wgtsPotsanity[2] = 0
    catPotsanity = random.choices(["No change",
                                   "Temples and side dungeons",
                                   "All but fairies/owls shuffled"],
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
        gossipHintsTakenByAlways -= 1
        hardOptions += 1
    if catPotsanity[0] != "No change":
        if ("ChestWellLeftPurpleRupee" in settings["OverrideHintPriorities"][2]):
            settings["OverrideHintPriorities"][2].remove("ChestWellLeftPurpleRupee")
        nonzeroCategories += 1

    wgtsPhotosSales = [75,25]
    if gossipHintsTakenByAlways >= GOSSIP_HINTS_LIMIT:
        wgtsPhotosSales[0] += wgtsPhotosSales[1]
        wgtsPhotosSales[1] = 0
    catPhotosSales = random.choices(["No change", "Shuffled"], wgtsPhotosSales)
    if catPhotosSales[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----60000--------------------f8c070------------")
        settings["OverrideHintPriorities"][1].remove("HeartPieceSeaHorse")
        settings["OverrideHintPriorities"][0].append("HeartPieceSeaHorse")
        gossipHintsTakenByAlways += 1
        nonzeroCategories += 1

    wgtsMinigames = [80,20,0]
    if hardOptions >= HARD_OPTIONS_LIMIT or (gossipHintsTakenByAlways + 3) > GOSSIP_HINTS_LIMIT:
        wgtsMinigames[1] += wgtsMinigames[2]
        wgtsMinigames[2] = 0
    if gossipHintsTakenByAlways >= GOSSIP_HINTS_LIMIT:
        wgtsMinigames[0] += wgtsMinigames[1]
        wgtsMinigames[1] = 0
    catMinigames = random.choices(["No change",
                                    "Swamp 2 + Full TCG + Extra",
                                    "All shuffled"],
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
        
    wgtsBombersNotebook = [80,10,10]
    if hardOptions >= HARD_OPTIONS_LIMIT or gossipHintsTakenByAlways >= GOSSIP_HINTS_LIMIT:
        wgtsBombersNotebook[1] += wgtsBombersNotebook[2]
        wgtsBombersNotebook[2] = 0
    catBombersNotebook = random.choices(["No change",
                                         "Meetings only",
                                         "All shuffled"],
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
    
    settings["CustomItemListString"] = itemListString
    settings["CustomStartingItemListString"] = startListString
    settings["CustomJunkLocationsString"] = junkListString

    outputFilename = inputFilename.removesuffix(".json")
    outputFilename = outputFilename.removesuffix("base")
    outputFilename = "output\\" + FilenameOnly(outputFilename) + outputSuffix + ".json" 

    try:
        os.makedirs("output")
    except FileExistsError:
        pass

    with open(outputFilename, "w") as write_file:
        json.dump(data,write_file,indent=4)

    spoilerlogFilename = "MysterySpoiler.txt"

    with open(spoilerlogFilename, "w") as spoiler_file:
        print("MMR Mystery Maker", MYSTERY_MAKER_VERSION,"-- Mystery Spoiler Log",file=spoiler_file)
        print("Base settings: ", FilenameOnly(randomFilename[0]),file=spoiler_file)
        print("  Output file: ", outputFilename,file=spoiler_file)
        print("=============================================",file=spoiler_file)
        if (remainsShuffleActive == True):
            print("              Special Mode:  Remains Shuffle",file=spoiler_file)
            print("",file=spoiler_file)
        if (fairyHuntActive == True):
            print("              Special Mode:  Fairy Hunt",file=spoiler_file)
            print("",file=spoiler_file)
        if (remainsShuffleActive == False and fairyHuntActive == False):
            print("    Starting Boss Remains: ", catStartingBossRemains[0],file=spoiler_file)
        print("Starting Sword and Shield: ", catStartingSwordShield[0],file=spoiler_file)
        print("     Starting Random Item: ", catStartingRandomItem[0],file=spoiler_file)
        print("     Starting Random Song: ", catStartingRandomSong[0],file=spoiler_file)
        print("    Fierce Deity Anywhere: ", catFierceDeityAnywhere[0],file=spoiler_file)
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
argParser.add_argument("-tw", dest="totalChance",type=int,default=0,
                    help="total weight of seed")
args = argParser.parse_args()

if (args.showVersion):
    print("MMR Mystery Maker", MYSTERY_MAKER_VERSION)
    sys.exit()

optionSettingsFile = args.inputFile
optionFairyFile = args.fairyFile
optionRemainsFile = args.remainsFile
optionFairyWeight = args.fairyHuntChance
optionRemainsWeight = args.remainHuntChance
optionTotalWeight = args.totalChance
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
    optionDontMakeSeed = guiResults[9]
    optionFairyWeight = guiResults[5]
    optionRemainsWeight = guiResults[6]
    optionTotalWeight = guiResults[7]

for i in range(optionOutputCount):
    resultFilename = ''
    while (resultFilename == ''):
        resultFilename = GenerateMysterySettings(optionSettingsFile, optionFairyFile, optionRemainsFile, optionFairyWeight, optionRemainsWeight, optionTotalWeight,(str)(i+1))
    if (optionDontMakeSeed == False):
        mmrcl = optionRandomizerExe + " -outputpatch -spoiler -settings " + resultFilename
        subprocess.call(mmrcl)
