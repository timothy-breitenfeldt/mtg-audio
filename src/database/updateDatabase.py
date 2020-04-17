"""	
  This module is meant to pull in the cards from the magic the gathering database, and break down the values return by MTGSDK, 
  to be able to insert those values into my local sqlite3 database
"""


import sqlite3
from sqlite3 import OperationalError

import os
import time
import sys

from mtgsdk import Card
from mtgsdk import Set


class DatabaseUpdater:

    def __init__(self):
        self.filePathCardID = "resources/cardID.txt"
        self.filePathSetCounter = "resources/setCounter.txt"
        self.filePathSets = "resources/sets.txt"
        self.dbFile = "mtg.db"
        self.numberOfCards = 0
        self.numberOfSets = 0

    def update(self):
        if not os.path.isfile("mtg.db"):
            raise OperationalError("mtg  database file does not exist, run buildDatabase.exe to recreate the database")

        print("Comparing online database to local database...")

        self.numberOfCards = self.getLastId()
        self.numberOfSets = self.readSetCounter()
        onlineSets = self.readSetsFromOnline()
        localSets = self.readSetsFromFile()
        sets = self.compareSetLists(onlineSets, localSets)
        connection = self.createConnection()
        memory = connection.cursor()
        cards = []

        if len(sets) > 0:
            print("Missing sets:")
            for s in sets:
                print(s[1])
            print()
        else:
            print("Database is already up to date")
            input("Press enter to continue:")
            sys.exit()

        for i, set in enumerate(sets):
            try:
                print("searching for", set[1])
                cards = Card.where(set=set[0]).all()
                self.insertSet(set, memory)
            except OperationalError:
                raise OperationalError("Error accessing database")

            print("gathered cards for ", set[1], "set")

            for card in cards:
                cardProperties = self.getCardProperties(card, self.numberOfCards, set[0])
                self.insertCard(cardProperties, memory)
                self.numberOfCards += 1    # increment the id used for each card 

            connection.commit()
            self.numberOfSets += 1    # increment the self.numberOfSets used to keep track of which set of the total we are on 
            print(set[1], "complete,", (i+1), "of", len(sets))
            print(self.numberOfCards)
            self.setNewId(self.numberOfCards)
            self.writeSetCounter(self.numberOfSets)

            # this is used to space out the requests since it will throw an error if the program grabs all the card at once
            if self.numberOfSets % 10 == 0:
                time.sleep(30)

    def getLastId(self):
        with open(self.filePathCardID, "r") as file:
            id = file.read()

        return int(id)

    def setNewId(self, id):
        with open(self.filePathCardID, "w") as file:
            file.write(str(id))

    def writeSetCounter(self, counter):
        with open(self.filePathSetCounter, "w") as file:
            file.write(str(counter))

    def readSetCounter(self):
        with open(self.filePathSetCounter, "r") as file:
            counter = file.read()

        return int(counter)

    def writeInAllSets(self):
        try:
            sets = Set.where().all()
        except:
            raise Exception("Error in connection to database")

        setNames = ""

        for set in sets:
            setNames += set.code + "|" + set.name + "|"

            if set.block is not None:
                setNames += set.block + "\n"
            else:
                setNames += "\n"

        setNames = setNames.rstrip("\n")

        with open(self.filePathSets, "w") as file:
                file.write(setNames)

    def readSetsFromOnline(self):
        try:
            setObjects = Set.where().all()
        except OperationalError:
            raise OperationalError("Error in connection to database")

        sets = []
        setInfo = []

        for set in setObjects:
            setInfo = [set.code, set.name.replace(u"\u2014", "-").replace(u"\u2022", "*")]

            if set.block is None:
                setInfo.append("")
            else:
                setInfo.append(set.block)

            sets.append(setInfo)

        return sets

    def readSetsFromFile(self):
        sets= []

        with open(self.filePathSets, "r") as file:
            for line in file:
                set = line.strip(" \n\t\r").split("|")
                set[1] = set[1].replace(u"\u2014", "-").replace(u"\u2022", "*")
                set[2] = set[2].replace(u"\u2014", "-").replace(u"\u2022", "*")
                sets.append(set)

        return sets

    def compareSetLists(self, l1, l2):
        differences = []

        for s1 in l1:
            found = False

            for s2 in l2:
                if s1 == s2:
                    found = True

            if not found:
                differences.append(s1)

        return differences

    def getCardProperties(self, card, id, setID):
        names = self.joinList(card.names)
        colors = self.joinList(card.colors)
        color_identity = self.joinList(card.color_identity)
        supertypes = self.joinList(card.supertypes)
        subtypes = self.joinList(card.subtypes)
        printings = self.joinList(card.printings)
        legalities = self.formatLegalities(card.legalities)
        rulings = self.formatRulings(card.rulings)
        c = (id, card.name, names, card.mana_cost, card.cmc, colors, color_identity, card.type, supertypes, subtypes, card.rarity, card.text, card.flavor, card.power,
                card.toughness,card.loyalty, rulings, legalities, card.watermark, printings, setID)

        return c

    def joinList(self, cardProperty):
        if cardProperty != None:
            return "|".join(cardProperty)
            return cardProperty

    def formatLegalities(self, legalities):
        if legalities == None:
            return legalities

        legalitiesStr = ""
        legalitiesLength = len(legalities)

        for index in range(legalitiesLength):
            legalitiesStr += legalities[index]["format"] + ": " + legalities[index]["legality"]

            if (index +1) != legalitiesLength:
                legalitiesStr += "\n"

        return legalitiesStr

    def formatRulings(self, rulings):
        if rulings == None:
            return rulings

        rulingsStr = ""

        rulingsLength = len(rulings)

        for index in range(rulingsLength):
            rulingsStr += rulings[index]["date"] + ": " + rulings[index]["text"]

            if (index + 1) != rulingsLength:
                rulingsStr += "\n"

        return rulingsStr

    def createConnection(self):
        try:
            connection = sqlite3.connect(self.dbFile)
            return connection
        except Error as e:
            raise Exception("Unable to connect to database")

    def insertSet(self, set, cur):
        sql = "INSERT INTO mtgSet VALUES("
        setProperties = tuple(set)
        setPropertiesLength = len(setProperties)

        for index in range(setPropertiesLength):
            sql += "?"

            if (index + 1) != setPropertiesLength:
                sql += ","

        sql += ");"
        cur.execute(sql, setProperties)

    def insertCard(self, cardProperties, cur):
        sql = "INSERT INTO mtgCard VALUES("
        cardPropertiesLength = len(cardProperties)

        for index in range(cardPropertiesLength):
            sql += "?"

            if (index + 1) != cardPropertiesLength:
                sql += ","

        sql += ");"
        cur.execute(sql, cardProperties)



if __name__ == "__main__":
    updater = DatabaseUpdater()

    updater.update()
    updater.writeInAllSets()
    input("Press enter to continue:")
