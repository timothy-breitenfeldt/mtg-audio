
class Card:

    def __init__(self, cardName, manaCost, cmc, type, superTypes, subTypes, rarity, text, flavor, power, toughness, loyalty, rulings, watermark, printings, setName, blockName,
            transformation=None, frontFacing=True):
        self._cardName = self._scrubData(cardName)
        self._manaCost = self._scrubData(manaCost)
        self._manaCost = self._manaCost.replace("{", "").replace("}", "")
        self._cmc = self._scrubData(cmc)
        self._type = self._scrubData(type)
        self._superTypes = self._scrubData(superTypes)
        self._subTypes = self._scrubData(subTypes)
        self._rarity = self._scrubData(rarity)
        self._text = self._scrubData(text)
        self._flavor = self._scrubData(flavor)
        self._power = self._scrubData(power)
        self._toughness = self._scrubData(toughness)
        self._loyalty = self._scrubData(loyalty)
        self._rulings = self._scrubData(rulings)
        self._watermark = self._scrubData(watermark)
        self._printings = self._scrubData(printings)
        self._setName = self._scrubData(setName)
        self._blockName = self._scrubData(blockName)
        self._transformation = transformation
        self._relatedCards = []
        self._frontFacing = frontFacing
        self._tapped = ""
        self._counters = 0
        self._plus1Counters = 0
        self._minus1Counters = 0

    def _scrubData(self, data):
        if data is None:
            data = ""
        else:
            data = str(data).replace(u"\u2014", "-").replace("\u2212", "-").replace(u"\u2022", "*")

            # insure that the data given is a string, and strip all unicode symbols from the string that won't print on a windows commandline shell by converting to askii.
            data = str(data).encode("ascii", "ignore")
            data = data.decode()

        return data

    def clone(self):
        back = None
        front = Card(self._cardName, self._manaCost, self._cmc, self._type, self._superTypes, self._subTypes, self._rarity, self._text, self._flavor, self._power, self._toughness,
                self._loyalty, self._rulings, self._watermark, self._printings, self._setName, self._blockName, None, self._frontFacing)

        if self._transformation is not None:
            back = Card(self._transformation.cardName, self._transformation.manaCost, self._transformation.cmc, self._transformation.type, self._transformation.superTypes,
                    self._transformation.subTypes, self._transformation.rarity, self._transformation.text, self._transformation.flavor, self._transformation.power,
                    self._transformation.toughness, self._transformation.loyalty, self._transformation.rulings, self._transformation.watermark, self._transformation.printings,
                    self._transformation.setName, self._transformation.blockName, front, self._transformation.frontFacing)
            front.transformation = back

        return front

    @property
    def cardName(self):
        return self._cardName

    @property
    def manaCost(self):
        return self._manaCost

    @property
    def cmc(self):
        return self._cmc

    @property
    def type(self):
        return self._type

    @property
    def superTypes(self):
        return self._superTypes

    @property
    def subTypes(self):
        return self._subTypes

    @property
    def rarity(self):
        return self._rarity

    @property
    def text(self):
        return self._text

    @property
    def flavor(self):
        return self._flavor

    @property
    def power(self):
        return self._power

    @property
    def toughness(self):
        return self._toughness

    @property
    def loyalty(self):
        return self._loyalty

    @property
    def rulings(self):
        return self._rulings

    @property
    def watermark(self):
        return self._watermark

    @property
    def printings(self):
        return self._printings

    @property
    def setName(self):
        return self._setName

    @property
    def blockName(self):
        return self._blockName

    @property
    def transformation(self):
        return self._transformation

    @property
    def relatedCards(self):
        return self._relatedCards

    @property
    def tapped(self):
        return self._tapped

    @property
    def frontFacing(self):
        return self._frontFacing

    @property
    def powerAndToughness(self):
        pt = ""

        if self.power and self.toughness:
            pt = "(" + self.power + "/" + self.toughness + ")"

        return pt

    @property
    def counters(self):
        return self._counters 

    @property
    def plus1Counters(self):
        return self._plus1Counters 

    @property
    def minus1Counters(self):
        return self._minus1Counters

    @transformation.setter
    def transformation(self, card):
        self._transformation = card

    @tapped.setter
    def tapped(self, tapStatus):
        if tapStatus != "tapped" and tapStatus != "":
            raise ValueError("Error tapStatus must be either \"tapped\" or \"\"")

        self._tapped = tapStatus

    @frontFacing.setter
    def frontFacing(self, isFrontFacing):
        if isFrontFacing is None:
            raise ValueError("Error, invalid value for front facing property")

        self._frontFacing = isFrontFacing

    @counters.setter
    def counters(self, counters):
        if counters < 0:
            self._counters = 0
        else:
            self._counters = counters

    @plus1Counters.setter
    def plus1Counters(self, plus1Counters):
        if plus1Counters < 0:
            self._plus1Counters = 0
        else:
            self._plus1Counters = plus1Counters

    @minus1Counters.setter
    def minus1Counters(self, minus1Counters):
        if minus1Counters < 0:
            self._minus1Counters = 0
        else:
            self._minus1Counters = minus1Counters

    def __eq__(self, other):
        if other is None:
            return False
        if type(other) is not type(self):
            return False
        if other._transformation is not None and self._transformation is not None:
            if other._cardName == self._transformation.cardname and other._manaCost == self._transformation.manaCost:
                return True
            if other._transformation.cardName == self._cardname and other._transformation.manaCost == self._manaCost:
                return True

        return other._cardName == self._cardName and other._manaCost == self._manaCost

    def __hash__(self):
        return hash( (self._cardName, self._manaCost) )

    def __str__(self, showTransformation=True):
        text = ("------------------------------\n"
                "" + self.cardName + " " + self.manaCost + "\n" + self.type + "\nText: " + self.powerAndToughness + " " + self.text)

        if self.loyalty != "":
            text += "\nLoyalty: " + self.loyalty

        if self.watermark != "":
            text += "\n" + "watermark: " + self.watermark    

        if showTransformation and self.transformation is not None and self.transformation != "":
            text += "\nTransformation: " + self.transformation.cardName

        if len(self.relatedCards) > 0:
            text += "\nRelated Cards: " + ", ".join(self.relatedCards)

        if self.flavor != "":
            text += "\nFlavor: " + self.flavor

        if self.rulings != "":
            text += "\nRulings: " + self.rulings

        text += "\n" + self.printings

        if self.rarity != "":
            text += "\n(" + self.rarity + ")"

        if showTransformation and self.transformation is not None and self.transformation != "":
            text+= "\n\n" + self.transformation.__str__(showTransformation=False)

        return text

