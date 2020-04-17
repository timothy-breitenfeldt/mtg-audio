
from sqlite3 import connect
from sqlite3 import OperationalError
from urllib.request import pathname2url

from game.cards import Card


class DatabaseManager:

    def __init__(self):
        self._databasePath = "database/mtg.db"
        self._connection = None
        self._sql = ""
        self._variables = []

    def connect(self):
        try:
            dbURI = "file:{}?mode=ro".format(pathname2url(self._databasePath))
            self._connection = connect(dbURI, uri=True)
        except OperationalError as oe:
            raise OperationalError("Unable to find database")

    def close(self):
        self._connection.close()

    def searchForCards(self, queryData):
        cursor = self._connection.cursor()
        results = []
        tempList = []  # Used for storing the query data variables to pass into execute to avoid concatenation for preventing SQL injections.
        sql = ("SELECT cardName, cardManaCost, cardCmc, cardType, cardSupertypes, cardSubtypes, cardRarity, cardText, cardFlavor, cardPower, cardToughness, "
                "cardLoyalty, cardRulings, cardWatermark, cardPrintings, setName, blockName, cardNames FROM mtgCard NATURAL JOIN mtgSet WHERE ")

        for index in range(len(queryData)):
            dataName = queryData[index][0]
            value = queryData[index][1].strip(" \t")
            sql = self._processDataOperators(sql, tempList, dataName, value)

            if (index + 1) != len(queryData):
                sql += "and "

        sql += "GROUP BY cardName;"

        rows = cursor.execute(sql, tempList).fetchall()
        frontName = ""
        backName = ""

        for r in rows:
            cardName = r[0]
            
            if any(c.cardName == cardName for c in results):
                continue

            mtgCard = self._parseCard(r, cursor)
            results.append(mtgCard)

        return results

    def searchByCardName(self, cardName):
        cursor = self._connection.cursor()
        sql = ("SELECT cardName, cardManaCost, cardCmc, cardType, cardSupertypes, cardSubtypes, cardRarity, cardText, cardFlavor, cardPower, "
                "cardToughness, cardLoyalty, cardRulings, cardWatermark, cardPrintings, setName, blockName, cardNames FROM mtgCard NATURAL JOIN mtgSet "
                "WHERE cardName LIKE ? GROUP BY cardName;")

        cursor.execute(sql, (cardName,))
        r = cursor.fetchone()

        if r is None:
            return None

        mtgCard = self._parseCard(r, cursor)
        return mtgCard

    def _processDataOperators(self, sql, tempList, dataName, value):
        # split value on the | to check for or operators that may be splitting up multiple values and loop through all of the values.
        dataValues = value.split("|")

        if len(dataValues) > 1:
            sql += "("

        for valueIndex in range(len(dataValues)):
            data = dataValues[valueIndex].strip(" \t")

            # check the dataName for if it is one of the four properties that is an integer.
            if dataName == "cardCmc" or dataName == "cardPower" or dataName == "cardToughness" or dataName == "cardLoyalty":
                sql += dataName + " == ?"
                tempList.append(int(data))
            elif dataName == "cardManaCost":
                for letterIndex in range(len(data)):
                    sql += dataName + " LIKE ? "
                    tempList.append("%" + data[letterIndex] + "%")

                    if (letterIndex + 1) < len(data):
                        sql += "and "

            else:
                sql  += dataName + " LIKE ?"

                # Check if the data is not surrounded by brackets, which signifys wildcards to be place after all words.
                # IF only one of the brackets is included, throw an error, and if both brackets are included at beginning and end, strip the brackets and continue on
                # allowing for exact text to be searched for.
                if not data.startswith("[") and not data.endswith("]"):
                    data = "%" + data + "%"

                    if " " in data:
                        data = data.replace(" ", "% ")
                elif data.startswith("[") and data.endswith("]"):
                    data = data.strip("[]")
                else:
                    raise ValueError("Value " + data + " is missing a bracket")

                tempList.append(data)

            if (valueIndex + 1) != len(dataValues):
                sql += "or "

        if len(dataValues) > 1:
            sql = sql.strip(" ") + ")"

        return sql

    def _parseCard(self, r, cursor):
        # Assosiate list items to readable variables.
        (name, manacost, cmc, type, supertypes, subtypes, rarity, text, flavor, power, toughness,
                loyalty, rulings, watermark, printings, setname, blockname, names) = r

        printings = self._searchSetsForPrintings(printings, cursor)
        mtgCard = Card(name, manacost, cmc, type, supertypes, subtypes, rarity, text, flavor, power, toughness,
                loyalty, rulings, watermark, printings, setname, blockname)

        # Check for transformation and other related cards
        if names is not None and names != "":
            temp = names.split("|")  # Split the names of the card.
            frontName = temp[0]
            backName = temp[1]

            if backName.lower() == mtgCard.cardName.lower():
                mtgCard.frontFacing = False

            if len(temp) == 2:
                mtgCard = self._getTransformation(mtgCard, frontName, backName, cursor)
            else:
                if mtgCard.frontFacing:
                    mtgCard.relatedCards.append(temp[2])
                    mtgCard = self._getTransformation(mtgCard, frontName, backName, cursor)
                else:
                    del temp[temp.index(mtgCard.cardName)]
                    mtgCard.relatedCards.extend(temp)

        return mtgCard

    def _getTransformation(self, mtgCard, frontName, backName, cursor):
        t = self._searchForTransformation(mtgCard, frontName, backName, cursor)

        if t is None:
            raise TypeError("Error, transformation for " + frontName + " into " + backName + " can not be found in the database")

        mtgCard.transformation = t

        if not mtgCard.frontFacing:
            mtgCard = mtgCard.transformation

        return mtgCard

    def _searchSetsForPrintings(self, printings, cursor):
        sql = "SELECT setName FROM mtgSet WHERE setID IN ("
        sets = printings.split("|")

        for counter in range(len(sets)):
            sql += "?"

            if counter != len(sets)-1:
                sql += ", "

        sql += ");"
        cursor.execute(sql, sets)
        sets = cursor.fetchall()
        sets = [y for x in sets for y in x]
        return ", ".join(sets)

    def _searchForTransformation(self, card, frontName, backName, cursor):
        cardBack = None;
        sql = ("SELECT cardName, cardManaCost, cardCmc, cardType, cardSupertypes, cardSubtypes, cardRarity, cardText, cardFlavor, cardPower, "
                "cardToughness, cardLoyalty, cardRulings, cardWatermark, cardPrintings, setName, blockName, cardNames FROM mtgCard NATURAL JOIN mtgSet "
                "WHERE cardName LIKE ? GROUP BY cardName;")
        nameToSearchBy = None

        # Check if we are looking at the back of the card, if so we need to search for the front.
        if card.frontFacing == False:
            nameToSearchBy = frontName
        else:
            nameToSearchBy = backName

        cursor.execute(sql, (nameToSearchBy,))
        r = cursor.fetchone()

        if r is not None:
            # Assosiate list items to readable variables.
            (name, manacost, cmc, type, supertypes, subtypes, rarity, text, flavor, power, toughness,
                    loyalty, rulings, watermark, printings, setname, blockname, names) = r

            printings = self._searchSetsForPrintings(printings, cursor)
            cardBack = Card(name, manacost, cmc, type, supertypes, subtypes, rarity, text, flavor, power, toughness,
                    loyalty, rulings, watermark, printings, setname, blockname, card, frontFacing=False)

        return cardBack



if __name__ == "__main__":
    db = DatabaseManager()
    db.connect()
    c = db.searchByCardName("thing in the ice")
    db.close()

    print(c)
