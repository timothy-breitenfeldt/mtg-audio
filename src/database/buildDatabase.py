
import sqlite3
import os
import time
from urllib.error import URLError

from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import MtgException


class DatabaseBuilder:

    def __init__(self):
        self.filePathCardID = "resources/cardID.txt"
        self.filePathSetCounter = "resources/setCounter.txt"
        self.filePathSets = "resources/sets.txt"
        self.dbFile = "mtg.db"
        self.numberOfCards = 0
        self.setCounter = 0

    def build(self):
        if os.path.isfile("mtg.db"):
            print("Removing existing database...")
            os.remove("mtg.db")

        self.setNewId(1)
        self.writeSetCounter(1)

        self.numberOfCards = 1

        connection = self.createSqliteConnection()
        print("Creating new database...")
        self.createNewDatabase(connection)
        sets = self.readInSets()
        cards = []

        for set in sets:
            cards = self.requestCards(set, connection, 0)

            if cards is None:
                print("the online API has denied to many requests, please try again in a little bit.")
                break 

            print("gathered cards for ", set[1], "set")

            for card in cards:
                cardProperties = self.getCardProperties(card, self.numberOfCards, set[0])
                self.insertCard(cardProperties, connection)
                self.numberOfCards += 1    # increment the id used for each card 

            connection.commit()
            self.setCounter += 1    # increment the self.setCounter used to keep track of which set of the total we are on 
            print(set[1], "complete,", self.setCounter, "of", len(sets))
            print(self.numberOfCards)
            self.setNewId(self.numberOfCards)
            self.writeSetCounter(self.setCounter)

            # this is used to space out the requests to the database
            if self.setCounter % 10 == 0:
                time.sleep(30)

        connection.close()    

    def createNewDatabase(self, connection):
        with open("mtg.sql") as file:
            connection.executescript(file.read())

    def requestCards(self, set, connection, timesCalled):
        try:
            if timesCalled == 0:
                set[1] = set[1].replace("\u2019", "\"").replace("\u2018", "\"");

            print("Searching for ", set[1])
            cards = Card.where(set=set[0]).all()
            self.insertSet(set, connection)
            return cards
        except (MtgException, URLError) as e:
            timesCalled += 1

            if timesCalled <= 10:
                print("API denied request, attempting to make request again for the " + str(timesCalled) + " time.")
                time.sleep(40)
                self.requestCards(set, connection, timesCalled)
            else:
                return None

    def setNewId(self, id):
        with open(self.filePathCardID, "w") as file:
            file.write(str(id))

    def writeSetCounter(self, counter):
        with open(self.filePathSetCounter, "w") as file:
            file.write(str(counter))

    def readSetCounter(self):
        with open(self.filePathSetCounter, "r") as file:
            counter = file.read()

        return int(counter) + 1

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

    def readInSets(self):
        sets= []

        with open(self.filePathSets, "r") as file:
            for line in file:
                set = line.strip(" \n\t\r").split("|")
                set[1] = set[1].replace(u"\u2014", "-").replace(u"\u2022", "*")
                set[2] = set[2].replace(u"\u2014", "-").replace(u"\u2022", "*")
                sets.append(set)

        return sets

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

    def createSqliteConnection(self):
        try:
            connection = sqlite3.connect(self.dbFile)
            return connection
        except Error as e:
            raise Exception("Unable to connect to database")

    def insertSet(self, set, connection):
        sql = "INSERT INTO mtgSet VALUES("
        setProperties = tuple(set)
        setPropertiesLength = len(setProperties)

        for index in range(setPropertiesLength):
            sql += "?"

            if (index + 1) != setPropertiesLength:
                sql += ","

        sql += ");"
        connection.executemany(sql, [setProperties])

    def insertCard(self, cardProperties, connection):
        sql = "INSERT INTO mtgCard VALUES("
        cardPropertiesLength = len(cardProperties)

        for index in range(cardPropertiesLength):
            sql += "?"

            if (index + 1) != cardPropertiesLength:
                sql += ","

        sql += ");"
        connection.executemany(sql, [cardProperties])


if __name__ == "__main__":
    builder = DatabaseBuilder()

    builder.writeInAllSets()
    builder.build()
    input("press enter to continue:")
