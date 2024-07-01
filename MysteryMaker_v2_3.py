import json
import random
import subprocess
import argparse

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
    
def GenerateMysterySettings(inputFilename, outputSuffix="output"):
    random.seed()

    with open(inputFilename, "r") as read_file:
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
      
    gossipHintsTakenByAlways = 3 + settings["OverrideNumberOfRequiredGossipHints"] + settings["OverrideNumberOfNonRequiredGossipHints"]
    GOSSIP_HINTS_LIMIT = 14

    nonzeroCategories = 0
    NONZERO_CATEGORIES_MINIMUM = 5

    hardOptions = 0
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

    wgtsStartingBossRemains = [70,25,5]
    if (remainsShuffleActive == True):
        wgtsStartingBossRemains = [100,0,0]
    catStartingBossRemains = random.choices(["No change","One","Two"],[70,25,5])
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
                                            "Magic",
                                            "Bomb Bag",
                                            "Blast Mask",
                                            "Empty Bottle",
                                            "Great Fairy's Sword"],
                                           [40,9,9,9,3,4,4,4,5,5,5,3])
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
    if catStartingRandomItem[0] == "Empty Bottle":
        startListString = AddEntryToListString(startListString,0,"100000")
    if catStartingRandomItem[0] == "Great Fairy's Sword":
        startListString = AddEntryToListString(startListString,0,"8000")

    wgtsStartingRandomSong = [30,25,5,5,5,5,5,5,5]
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
        nonzeroCategories += 1

    catCowsanity = random.choices(["No change","Shuffled"],[70,30])
    if catCowsanity[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----------------------------1f-e0000000-------")
        nonzeroCategories += 1

    catStrayFairies = random.choices(["No change",
                                      "Chest fairies + CT",
                                      "All stray fairies"],
                                     [60,30,10])
    if catStrayFairies[0] == "Chest fairies + CT":
        if (fairyHuntActive == False):
            itemListString = AddStringToListString(itemListString,
                                                   "--------------------------3fff83f0-7f003802----------")
        else:
            itemListString = AddEntryToListString(itemListString,10,"2")
            junkListString = RemoveStringFromListString(junkListString,
                                                        "--------------------------3fff83f0-7f003800----------")
    if catStrayFairies[0] == "All stray fairies":
        if (fairyHuntActive == False):
            itemListString = AddStringToListString(itemListString,
                                                   "--------------------------3fffffff-fffffffe----------")
            settings["StrayFairyMode"] = "Default"
        else:
            itemListString = AddEntryToListString(itemListString,10,"2")
            junkListString = RemoveStringFromListString(junkListString,
                                                        "--------------------------3fffffff-fffffffc----------")
    if catStrayFairies[0] != "No change":
        nonzeroCategories += 1

    wgtsEntrancesTemples = [70,30]
    wgtsEntrancesBossRooms = [75,25]
    if catStartingBossRemains[0] != "No change":
        wgtsEntrancesTemples = [40,60]
        wgtsEntrancesBossRooms = [50,50]
    catEntrancesTemples = random.choices(["No change","Shuffled"], wgtsEntrancesTemples)
    if catEntrancesTemples[0] == "Shuffled":
        settings["RandomizeDungeonEntrances"] = True
    catEntrancesBossRooms = random.choices(["No change","Shuffled"], wgtsEntrancesBossRooms)
    if catEntrancesBossRooms[0] == "Shuffled":
        settings["RandomizeBossRooms"] = True

    if catEntrancesTemples[0] != "No change" or catEntrancesBossRooms[0] != "No change":
        nonzeroCategories += 1

    wgtsKeysanityBossKeys = [70,0,15,15]
    if (fairyHuntActive == True):
        wgtsKeysanityBossKeys = [100,0,0,0]
    catKeysanityBossKeys = random.choices(["No change",
                                           "Doors open",
                                           "Shuffled within area",
                                           "Shuffled anywhere"],
                                          wgtsKeysanityBossKeys)
    if catKeysanityBossKeys[0] == "Doors open":
        settings["BossKeyMode"] = "DoorsOpen"
        itemListString = AddStringToListString(itemListString,
                                               "----------------------------------4411000---")
    if catKeysanityBossKeys[0] == "Shuffled within area":
        settings["BossKeyMode"] = "KeepWithinArea, KeepThroughTime"
        itemListString = AddStringToListString(itemListString,
                                               "----------------------------------4411000---")
    if catKeysanityBossKeys[0] == "Shuffled anywhere":
        settings["BossKeyMode"] = "KeepThroughTime"
        itemListString = AddStringToListString(itemListString,
                                               "----------------------------------4411000---")
        settings["OverrideNumberOfRequiredGossipHints"] += 1
        gossipHintsTakenByAlways += 1

    catKeysanitySmallKeys = random.choices(["No change",
                                            "Shuffled within area",
                                            "Shuffled anywhere"],
                                           [60,20,20])
    if catKeysanitySmallKeys[0] == "Shuffled within area":
        settings["SmallKeyMode"] = "KeepWithinArea, KeepThroughTime"
    if catKeysanitySmallKeys[0] == "Shuffled anywhere":
        settings["SmallKeyMode"] = "KeepThroughTime"

    if catKeysanityBossKeys[0] != "No change" or catKeysanitySmallKeys[0] != "No change":
        nonzeroCategories += 1

    catScoopsanity = random.choices(["No change","Shuffled with scoops"],
                                       [75,25])
    if catScoopsanity[0] == "Shuffled with scoops":
        if catSoilsanity[0] == "Shuffled":
            itemListString = AddStringToListString(itemListString,
                                               "---------------------------------fdc0000----")
        else:
            itemListString = AddStringToListString(itemListString,
                                               "---------------------------------ffc0000----")
        settings["OverrideHintPriorities"][1].append("BottleCatchBigPoe")
        nonzeroCategories += 1


    catHitSpots = random.choices(["No change","Shuffled"], [70,30])
    if catHitSpots[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-------1ffffff-ffffffff-fffe0000---8000000-------------------------")
        nonzeroCategories += 1

    catTokensanity = random.choices(["No change","Shuffled"], [80,20])
    if catTokensanity[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "---------------------------1-ffffffff-ffffffe0--------")
        nonzeroCategories += 1

    catCratesAndBarrels = random.choices(["No change","Shuffled"], [70,30])
    if catCratesAndBarrels[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "---------------c0000-2000--3c200--30--1f078-8000008-10000100-20000000------------")
        nonzeroCategories += 1

    catKeatonGrass = random.choices(["No change","Shuffled"], [70,30])
    if catKeatonGrass[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----1f-fffffc00-------------------------------")
        nonzeroCategories += 1

    catGossipFairies = random.choices(["No change","Shuffled"], [100,0])
    if catGossipFairies[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-100000-ffffff00-----------------------------------")
        nonzeroCategories += 1

    catButterflyAndWellFairies = random.choices(["No change","Shuffled"], [80,20])
    if catButterflyAndWellFairies[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "1fe-1fe00000------------------------------------")
        nonzeroCategories += 1

    wgtsLongQuests = [50,15,5,25,5]
    wgtsFrogs = [75,25]
    if catSongsanity[0] != "No change":
        wgtsLongQuests = [50,15,15,15,5]
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
        wgtsFrogs = [50,50]
        gossipHintsTakenByAlways += 1
    if catLongQuests[0] == "All Long Quests":
        hardOptions += 1
    if catLongQuests[0] != "No change":
        nonzeroCategories += 1

    catFrogs = random.choices(["No change","Shuffled"], wgtsFrogs)
    if catFrogs[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "1-e0000000------------------------------------")
        settings["OverrideHintPriorities"][1].append("FrogGreatBayTemple")
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

    wgtsSnowsanity = [90,10]
    if hardOptions >= HARD_OPTIONS_LIMIT:
        wgtsSnowsanity[0] += wgtsSnowsanity[1]
        wgtsSnowsanity[1] = 0
    catSnowsanity = random.choices(["No change","Shuffled"], wgtsSnowsanity)
    if catSnowsanity[0] == "Shuffled":
        itemListString = AddStringToListString(itemListString,
                                               "-----1fc00--------fc0ffff-fc3cf800--c0000----180c006--e00-301c0000-c0000c-------------")
        hardOptions += 1
        nonzeroCategories += 1

    wgtsPotsanity = [75,15,10]
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
        gossipHintsTakenByAlways -= 1
        hardOptions += 1
    if catPotsanity[0] != "No change":
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

    wgtsMinigames = [80,15,5]
    if hardOptions >= HARD_OPTIONS_LIMIT or (gossipHintsTakenByAlways + 3) > GOSSIP_HINTS_LIMIT:
        wgtsMinigames[1] += wgtsMinigames[2]
        wgtsMinigames[2] = 0
    if gossipHintsTakenByAlways >= GOSSIP_HINTS_LIMIT:
        wgtsMinigames[0] += wgtsMinigames[1]
        wgtsMinigames[1] = 0
    catMinigames = random.choices(["No change",
                                    "SwAr/Beav/TCG + Extra",
                                    "All shuffled"],
                                   wgtsMinigames)
    catMinigamesExtra = ["No change"]
    if catMinigames[0] == "SwAr/Beav/TCG + Extra":
        itemListString = AddStringToListString(itemListString,
                                               "-------------------------70000-----------11000000-")
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
        
    wgtsBombersNotebook = [70,20,10]
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
       
    if (remainsShuffleActive == False and fairyHuntActive == False):
        if hardOptions >= HARD_OPTIONS_LIMIT:
            if catStartingBossRemains[0] != "No change":
                catStartingBossRemains[0] = "Two*"
                settings["BossRemainsMode"] = "Blitz2"
            else:
                catStartingBossRemains[0] = "One*"
                settings["BossRemainsMode"] = "Blitz1"
    elif (fairyHuntActive == True):
        if hardOptions >= HARD_OPTIONS_LIMIT:
            if catStartingBossRemains[0] != "No change":
                catStartingBossRemains[0] = "Two"
            else:
                catStartingBossRemains[0] = "One"
        if catStartingBossRemains[0] == "One":
            startListString = AddStringToListString(startListString,
                                                    "e-1c0038-700000--")
        elif catStartingBossRemains[0] == "Two":
            startListString = AddStringToListString(startListString,
                                                    "3e-7c00f8-1f00000--")
    
    settings["CustomItemListString"] = itemListString
    settings["CustomStartingItemListString"] = startListString
    settings["CustomJunkLocationsString"] = junkListString

    outputFilename = inputFilename.removesuffix(".json")
    outputFilename = outputFilename.removesuffix("base")
    outputFilename = "output\\" + outputFilename + outputSuffix + ".json" 

    with open(outputFilename, "w") as write_file:
        json.dump(data,write_file,indent=4)

    spoilerlogFilename = outputFilename.removesuffix(".json")
    spoilerlogFilename = spoilerlogFilename + "_MysterySpoiler.txt"

    with open(spoilerlogFilename, "w") as spoiler_file:
        print("MMR Mystery Maker v2.3 -- Mystery Spoiler Log",file=spoiler_file)
        print("Base settings: ", inputFilename,file=spoiler_file)
        print("  Output file: ", outputFilename,file=spoiler_file)
        if (remainsShuffleActive == True):
            print("Remains Shuffle is active",file=spoiler_file)
        if (fairyHuntActive == True):
            print("Fairy Hunt is active",file=spoiler_file)
        print("=============================================",file=spoiler_file)
        print("               Songsanity: ", catSongsanity[0],file=spoiler_file)    
        if (remainsShuffleActive == False and fairyHuntActive == False):
            print("    Starting Boss Remains: ", catStartingBossRemains[0],file=spoiler_file)
        elif (fairyHuntActive == True):
            startingFairyString = "No change"
            if catStartingBossRemains[0] == "One":
                startingFairyString = "Three from each set"
            elif catStartingBossRemains[0] == "Two":
                startingFairyString = "Five from each set"
            print("   Starting Stray Fairies: ", startingFairyString,file=spoiler_file)
        print("Starting Sword and Shield: ", catStartingSwordShield[0],file=spoiler_file)
        print("     Starting Random Item: ", catStartingRandomItem[0],file=spoiler_file)
        print("     Starting Random Song: ", catStartingRandomSong[0],file=spoiler_file)
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
        if catMinigames[0] == "SwAr/Beav/TCG + Extra":
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
argParser.add_argument("--settings-only", dest="settingsOnly", action="store_true",
                    help="only generate settings; don't roll any seeds")
args = argParser.parse_args()

for i in range(args.numberOfSettingsFiles):
    resultFilename = ''
    while (resultFilename == ''):
        resultFilename = GenerateMysterySettings(args.inputFile,(str)(i+1))
    if (args.settingsOnly == False):
        mmrcl = "MMR.CLI.exe -outputpatch -spoiler -settings " + resultFilename
        subprocess.call(mmrcl)
