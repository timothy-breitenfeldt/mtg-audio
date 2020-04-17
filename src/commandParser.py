
import re

from windows import TextWindow


class CommandParser:

    def __init__(self, gamePanel, controller, screenreader):
        self._gamePanel = gamePanel
        self._controller = controller
        self._screenreader = screenreader
        self._commands = {"load": self.loadDeck, "view": self.view, "vw": self.view, "viewinfo": self.viewCardsAndInfo, "vwi": self.viewCardsAndInfo, "move": self.move,
                "mv": self.move, "tap": self.tap, "tp": self.tap, "untap": self.untap, "untp": self.untap, "shuffle": self.shuffle, "shuffl": self.shuffle, "shfl": self.shuffle,
                "sort": self.sort, "srt": self.sort, "cleanup": self.cleanup, "clean": self.cleanup, "cln": self.cleanup, "search": self.search, "play": self.play, "pl": self.play,
                "draw": self.draw, "dr": self.draw, "discard": self.discard, "dsc": self.discard, "ds": self.discard, "mill": self.mill, "mll": self.mill, "ml": self.mill, "attack": self.attack,
                "atk": self.attack, "swap": self.swap, "swp": self.swap, "transform": self.transform, "tran": self.transform, "trans": self.transform, "trnf": self.transform,
                "token": self.createToken, "tk": self.createToken, "addcounter": self.addCounters, "addcounters": self.addCounters, "addcount": self.addCounters,
                "counter+": self.addCounters, "counters+": self.addCounters, "count+": self.addCounters, "subtractcounter": self.subtractCounters,
                "subtractcounters": self.subtractCounters, "subcounter": self.subtractCounters, "subcounters": self.subtractCounters, "subcount": self.subtractCounters,
                "subcounts": self.subtractCounters, "counter-": self.subtractCounters, "counters-": self.subtractCounters, "count-": self.subtractCounters,
                "addplus1counters": self.addPlus1Counters, "addplus1counter": self.addPlus1Counters, "addpluscounters": self.addPlus1Counters,
                "addpluscounter":     self.addPlus1Counters, "plus1counters+": self.addPlus1Counters, "plus1counter+": self.addPlus1Counters, "pluscounters+": self.addPlus1Counters,
                "pluscounter+": self.addPlus1Counters, "subtractplus1counters": self.subtractPlus1Counters, "subtractplus1counter": self.subtractPlus1Counters,
                "subtractpluscounters": self.subtractPlus1Counters, "subtractpluscounter": self.subtractPlus1Counters, "plus1counters-": self.subtractPlus1Counters,
                "plus1counter-": self.subtractPlus1Counters, "pluscounters-": self.subtractPlus1Counters, "pluscounter-": self.subtractPlus1Counters,
                "addminus1counters": self.addMinus1Counters, "addminus1counter": self.addMinus1Counters, "addminuscounters": self.addMinus1Counters,
                "addminuscounter": self.addMinus1Counters, "minus1counters+": self.addMinus1Counters, "minus1counter+": self.addMinus1Counters,
                "minuscounters+": self.addMinus1Counters, "minuscounter+": self.addMinus1Counters, "subtractminus1counters": self.subtractMinus1Counters,
                "subtractminus1counter": self.subtractMinus1Counters, "subtractminuscounters": self.subtractMinus1Counters, "subtractminuscounter": self.subtractMinus1Counters,
                "minus1counters-": self.subtractMinus1Counters, "minus1counter-": self.subtractMinus1Counters, "minuscounters-": self.subtractMinus1Counters,
                "minuscounter-": self.subtractMinus1Counters}
        self._zoneCommands = {"exile": self._controller.player.exile, "exl": self._controller.player.exile, "library": self._controller.player.library, "lib": self._controller.player.library,
                "graveyard": self._controller.player.graveyard, "grave": self._controller.player.graveyard, "grv": self._controller.player.graveyard, "gr": self._controller.player.graveyard,
                "hand": self._controller.player.hand, "hnd": self._controller.player.hand, "creatures": self._controller.player.creatures,"creature": self._controller.player.creatures,
                "crt": self._controller.player.creatures, "cr": self._controller.player.creatures, "lands": self._controller.player.lands, "land": self._controller.player.lands,
                "lnd": self._controller.player.lands, "otherSpells": self._controller.player.otherSpells, "other": self._controller.player.otherSpells, "othr": self._controller.player.otherSpells,
                "oth": self._controller.player.otherSpells}

    @property
    def controller(self):
        return self._controller 

    def validate(self, command):
        try:
            commandOutput = ""

            if command[0] in self._commands:
                func = self._commands[command[0]]
                commandOutput = func(command)
            else:
                raise ValueError("Error: Invalid Command")

            return commandOutput
        except Exception as e:
            raise e

    def _getCardIndex(self, zone, arg):
        try:
            if arg.isdigit():
                index = int(arg) - 1    # subtracts 1 to account for the user friendly base 1 system rather than base 0

                if index < 0 or index >= zone.numberOfCards:
                    raise IndexError("Error, index " + str(index) + " is out of bounds of your " + zone.name)

            else:
                index = zone.search(arg)
                if index == -1:
                    raise LookupError("Error trying to locate " + arg + " in your " + zone.name)

            return index
        except Exception as e:
            raise e

    def loadDeck(self, command):
        try:
            if len(command) != 2 or command[0] != "load":
                raise ValueError("Error: invalid number of arguments for load, must be in format: \"load [deckName.txt]\"")

            filename = command[1]
            self._gamePanel.output("loading " + filename)
            self._controller.loadDeck(filename)
            return "deck loaded"
        except Exception as e:
            raise e

    def view(self, command):
        try:
            if len(command) > 3:
                raise ValueError("Error: invalid number of arguments for view, must be in format: \"view [zone] *[card]\"")
            if len(command) == 1:
                return self._controller.viewBattlefield()

            cardStr = ""
            index = 0;
            zone = None

            if command[1] in self._zoneCommands:
                if len(command) == 2:
                    zone = self._zoneCommands[command[1]]
                    return self._controller.viewCardNames(zone)

                # The command contains three arguments.
                zone = self._zoneCommands[command[1]]
                index = self._getCardIndex(zone, command[2])

                card = zone.getCard(index)
                cardStr = self._controller.viewCard(zone, index)
                window = TextWindow(self._gamePanel, "MTG " + card.cardName, self._screenreader, cardStr)
                window.Show()
                return "viewed " + card.cardName
            else:
                return"Error: invalid zone"
        except Exception as e:
            raise e

    def viewCardsAndInfo(self, command):
        try:
            if len(command) > 3:
                raise ValueError("Error: invalid number of arguments for view, must be in format: \"view [zone] *[card]\"")
            if len(command) == 1:
                return self._controller.viewBattlefieldWithInfo()

            cardStr = ""
            index = 0;
            zone = None

            if command[1] in self._zoneCommands:
                if len(command) == 2:
                    zone = self._zoneCommands[command[1]]
                    return self._controller.viewCardsAndInfo(zone)

                # The command contains three arguments.
                zone = self._zoneCommands[command[1]]
                index = self._getCardIndex(zone, command[2])

                card = zone.getCard(index)
                cardStr = card.__str__()
                window = TextWindow(self._gamePanel, "MTG " + card.cardName, self._screenreader, cardStr)
                window.Show()
                return "viewed " + card.cardName
            else:
                return"Error: invalid zone"
        except Exception as e:
            raise e

    def move(self, command):
        try:
            if len(command) < 3:
                raise ValueError("Error: invalid number of arguments for move, must be in format: \"move [startingZone] *[card] *[card] ... [zoneDestination]\"")
            if command[1] not in self._zoneCommands:
                raise ValueError("Error: Invalid starting zone")

            sourceZone = self._zoneCommands[command[1]]
            destinationZone = None 
            indicies = []

            if command[2] in self._zoneCommands:
                destinationZone = self._zoneCommands[command[2]]
                self._controller.moveZone(sourceZone, destinationZone)
                return "Moved the cards in " + sourceZone.name + " to " + destinationZone.name

            for argIndex in range(2, len(command)):
                argument = command[argIndex]

                if argument in self._zoneCommands:
                    destinationZone = self._zoneCommands[argument]
                else:
                    index = self._getCardIndex(sourceZone, argument)
                    indicies.append(index)

            if destinationZone is None:
                raise ValueError("Error: Invalid destination zone")

            self._controller.moveCards(sourceZone, indicies, destinationZone)
            return "moved cards from " + sourceZone.name + " to " + destinationZone.name
        except Exception as e:
            raise e

    def tap(self, command):
        try:
            if len(command) == 1:
                self._controller.tapBattlefield()
                return "Tapped battlefield"
            if command[1] not in self._zoneCommands:
                raise ValueError("Error: Invalid zone")

            zone = self._zoneCommands[command[1]]
            indicies  = []
            card = None

            if len(command) == 2:
                self._controller.tapZone(zone)
                return "Tapped all cards in your " + zone.name

            for argIndex in range(2, len(command)):
                argument = command[argIndex]
                index = self._getCardIndex(zone, argument)
                indicies.append(index)

            self._controller.tapCards(zone, indicies)
            return "Tapped cards in your " + zone.name
        except Exception as e:
            raise e

    def untap(self, command):
        try:
            if len(command) == 1:
                self._controller.untapBattlefield()
                return "Untapped battlefield"
            if command[1] not in self._zoneCommands:
                raise ValueError("Error: Invalid zone")

            zone = self._zoneCommands[command[1]]
            indicies  = []
            card = None

            if len(command) == 2:
                self._controller.untapZone(zone)
                return "Untapped all cards in your " + zone.name

            for argIndex in range(2, len(command)):
                argument = command[argIndex]
                index = self._getCardIndex(zone, argument)
                indicies.append(index)

            self._controller.untapCards(zone, indicies)
            return "Untapped cards in your " + zone.name
        except Exception as e:
            raise e

    def shuffle(self, command):
        try:
            if len(command) > 2:
                raise ValueError("Error: invalid number of arguments for shuffle, must be in format: \"shuffle *[zone]\"")

            zone = None

            if len(command) == 1:
                zone = self._controller.player.library
            elif command[1] in self._zoneCommands:
                zone = self._zoneCommands[command[1]]

            if zone is None:
                raise ValueError("Error: invalid zone")
            if zone.isEmpty():
                return "Nothing to shuffle"

            self._controller.shuffleZone(zone)
            return "Shuffled " + zone.name
        except Exception as e:
            raise e

    def sort(self, command):
        try:
            if len(command) < 2:
                raise ValueError("Error: invalid number of arguments for sort, must be in format: \"sort [zone] *[properties]...\"")

            zone = None 

            if command[1] in self._zoneCommands:
                zone = self._zoneCommands[command[1]]
            else:
                raise ValueError("Error, invalid zone")

            if zone.isEmpty():
                return "zone is empty"

            if len(command) == 2:
                self._controller.sortZone(zone, ["cmc", "type", "manaCost"])
                return "Sorted " + zone.name + " by converted mana cost, card type, and by mana cost"

            propertyCommands = {"manaCost": "manaCost", "mc": "manaCost", "color": "manaCost", "convertedManaCost": "cmc", "cmc": "cmc", "type": "type", "text": "text",
                    "power": "power", "toughness": "toughness", "set": "setName", "block": "block", "cardName": "cardName", "name": "cardName"}
            sortBy = []

            for index in range(2, len(command)):
                if command[index] in propertyCommands:
                    sortBy.append(propertyCommands[command[index]])
                else:
                    raise ValueError("Error: " + command[index] + " is not a recognized card property")

            self._controller.sortZone(zone, sortBy)
            return "Sorted " + zone.name
        except Exception as e:
            raise e

    def cleanup(self, command):
        if len(command) > 1:
            return "Error: invalid number of arguments for cleanup, must be in format: \"cleanup\""
        if self._controller.player.library.deckName == "":
            return "Error: nothing to clean up"

        self._controller.cleanup()
        return "Reset all zones"

    def search(self, command):
        try:
            if len(command) < 2:
                raise ValueError("Error: invalid number of arguments for search, must be in format: \"search *[arguments]\"")

            cardsStr = ""
            startingIndex = 0
            searchParameters = []
            propertyCommands = {"manacost": "cardManaCost", "mc": "cardManaCost", "color": "cardManaCost", "convertedmanacost": "cardCmc", "cmc": "cardCmc",
                    "type": "cardType", "text": "cardtext", "power": "cardPower", "toughness": "cardToughness", "set": "setName", "block": "blockName",
                    "watermark": "cardWatermark", "water": "cardWatermark", "wm": "cardWatermark"}

            if "=" not in command[1]:
                # Start processing search parameters at command[2] because the first argument is a name
                startingIndex = 2
                searchParameters.append(("cardName", command[1]))
            else:
                startingIndex = 1

            for index in range(startingIndex, len(command)):
                commandArgument = command[index]

                if "=" in commandArgument:
                    flag, value = commandArgument.split("=")
                    flag = flag.strip(" \n\t").lower()
                    value = value.strip(" \n\t").lower()

                    if flag in propertyCommands:
                        searchParameters.append((propertyCommands[flag], value))
                    else:
                        raise ValueError("Error: " + flag + " is not a card property. Check spelling and try again.")

                else:
                    raise ValueError("Error: invalid format for search, arguments must  b in format:\npropertyName=value")

            self._gamePanel.output("Searching...")

            cardsStr = self._controller.searchDatabase(searchParameters)
            window = TextWindow(self._gamePanel, "MTG Search Results", self._screenreader, cardsStr)
            window.Show()
            return "Search Complete"
        except Exception as e:
            raise e

    def play(self, command):
        try:
            if len(command) < 2:
                raise ValueError("Error: invalid number of arguments for play, must be in format: \"play [cards] ... *[destinationZone]\"")
            if self._controller.player.hand.isEmpty():
                raise ValueError("hand is empty")

            zone = None
            indicies = []
            hand = self._controller.player.hand
            text = ""

            for argIndex in range(1, len(command)):
                argument = command[argIndex]

                if argument in self._zoneCommands:
                    zone = self._zoneCommands[argument]
                else:
                    index = self._getCardIndex(hand, argument)
                    indicies.append(index)

            if zone is None:
                text += self._controller.playCardsAutoPlacement(hand, indicies)
            else:
                text = self._controller.playCardsInZone(indicies, zone)

            return text
        except Exception as e:
            raise e

    def draw(self, command):
        try:
            if len(command) > 2:
                raise ValueError("Error: invalid number of arguments for draw, must be in format: \"draw *[numberOfCards]\"")
    
            if len(command) == 1:
                cardName = self._controller.drawCards(1)
                return "Drew " + cardName
            elif len(command) == 2:
                if command[1].isdigit():
                    quantity = int(command[1])
                    cardNames = self._controller.drawCards(quantity)
                    return "Drew " + cardNames
                else:
                    raise ValueError("Error: invalid argument for draw, quantity must be a number")
        except Exception as e:
            raise e

    def discard(self, command):
        try:
            if len(command) < 2:
                raise ValueError("Error, invalid format for discard. must be in format: \"discard [cards] ...\"")

            indicies = []
            hand = self._controller.player.hand

            for argIndex in range(1, len(command)):
                argument = command[argIndex]
                index = self._getCardIndex(hand, argument)
                indicies.append(index)

            cards = self._controller.discardCards(indicies)
            return "Discarded " + cards
        except Exception as e:
            raise e

    def mill(self, command):
        try:
            if len(command) > 2:
                raise ValueError("Error: invalid number of arguments for mill, must be in format: \"mill *[numberOfCards]\"")
            if self._controller.player.library.isEmpty():
                raise ValueError("no cards left in library")

            if len(command) == 1:
                cardName = self._controller.millCards(1)
                return "Milled " + cardName
            elif len(command) == 2:
                if command[1].isdigit():
                    quantity = int(command[1])
                    cardNames = self._controller.millCards(quantity)
                    return "Milled " + cardNames
                else:
                    raise ValueError("Error: invalid argument for mill, quantity must be a number")
        except Exception as e:
            raise e

    def attack(self, command):
        try:
            if self._controller.player.creatures.isEmpty():
                raise ValueError("Creatures is empty")
            if len(command) == 1:
                self._controller.attackWithAllCreatures()
                return "Attacked with everything"

            creatures = self._controller.player.creatures
            indicies = []

            for argIndex in range(1, len(command)):
                argument = command[argIndex]
                index = self._getCardIndex(creatures, argument)
                indicies.append(index)

            cardNames = self._controller.attackWithCreatures(indicies)
            return "Attacked with " + cardNames
        except Exception as e:
            raise e

    def swap(self, command):
        try:
            if len(command) != 3 and len(command) != 4:
                raise ValueError("Error: invalid number of arguments for swap, must be in format: \"swap [zone] *[zone2] *[card1] *[card2]\"")

            zone = None
            zone2 = None
            index1 = -1
            index2 = -1

            if command[1] in self._zoneCommands:
                zone = self._zoneCommands[command[1]]
            else:
                raise ValueError(command[1] + " is not a valid zone")

            if len(command) == 3:
                if command[2] in self._zoneCommands:
                    zone2 = self._zoneCommands[command[2]]
                else:
                    raise ValueError(command[2] + " is not a valid zone")

                self.controller.swapZones(zone, zone2)
                print(zone.name + " after swap: " + str(zone.cardContainer))
                print(zone2.name + " after swap: " + str(zone2.cardContainer))
                return "Swapped all the cards in " + zone.name + " with the cards in " + zone2.name
            elif len(command) == 4:
                if not command[2].isdigit():
                    raise ValueError("index 1 is not a number.")
                if not command[3].isdigit():
                    raise ValueError("index 2 is not a number.")

                index1 = self._getCardIndex(zone, command[2])
                index2 = self._getCardIndex(zone, command[3])
                self.controller.swapCards(zone, index1, index2)
                return "Swapped " + zone.getCard(index1).cardName + " with " + zone.getCard(index2).cardName + " in your " + zone.name

        except Exception as e:
            raise e

    def transform(self, command):
        try:
            if len(command) != 3:
                raise ValueError("invalid number of arguments for transform, must be in format: \"transform [zone] [card]\"")

            zone = None 
            index = None

            if command [1] in self._zoneCommands:
                zone = self._zoneCommands[command[1]]
            else:
                raise ValueError(command[1] + " is an invalid zone.")

            index = self._getCardIndex(zone, command[2])
            card = zone.getCard(index)

            if card.transformation is None:
                raise ValueError("This card can not transform.")

            text = "Transformed " + card.cardName + " into " + card.transformation.cardName + "."
            self.controller.transform(zone, index)
            return text
        except Exception as e:
            raise e

    def createToken(self, command):
        try:
            if len(command) < 3 or len(command) > 6:
                raise ValueError("invalid number of arguments for token, must be in format: "
                        "\"token [zone: creatures|lands|other] [cardName] *[type=tokenType] *[pt=power/toughness *[text=tokenText]\"")

            zone = None 
            type = ""
            cardName = ""
            power = ""
            toughness = ""
            text = ""

            if command [1] in self._zoneCommands:
                zone = self._zoneCommands[command[1]]
            else:
                raise ValueError(command[1] + " is an invalid zone.")

            cardName = command[2]

            for c in range(3, len(command)):
                property = command[c].split("=")

                if len(property) != 2:
                    raise ValueError("Invalid sintax for token, you must format properties like this: pt=power/toughness, type=type, or text=text.")

                propertyName = property[0]
                propertyValue = property[1]

                if propertyName == "type":
                    type = propertyValue
                elif propertyName == "pt":
                    if re.match("\d/\d", propertyValue) is None:
                        raise ValueError("Power and toughness must be in format p/t.")

                    temp = propertyValue.split("/")
                    power = str(temp[0])
                    toughness = str(temp[1])
                elif propertyName == "text":
                    text = propertyValue

            if type == "":
                type = "token"

            self.controller.createToken(zone, cardName, type, power, toughness, text)
            return "Created " + cardName + ", and placed it in " + zone.name
        except Exception as e:
            raise e

    def addCounters(self, command):
        try:
            if len(command) != 4:
                raise ValueError("invalid number of arguments for addcounters, must be in format: \"addcounters [zone] [card] [counters]\"")

            zone = None 
            index = None
            counters = None

            if command [1] in self._zoneCommands:
                zone = self._zoneCommands[command[1]]
            else:
                raise ValueError(command[1] + " is an invalid zone.")

            index = self._getCardIndex(zone, command[2])
            card = zone.getCard(index)

            if not command[3].isdigit():
                raise ValueError("Invalid argument for counters.")

            counters = int(command[3])

            if counters < 0:
                raise ValueError("Can not add negative counters.")

            self.controller.addCounters(zone, index, counters)
            text = "Added " + str(counters) + " counters to " + card.cardName + ". It now has " + str(card.counters) + " counters."
            return text
        except Exception as e:
            raise e

    def subtractCounters(self, command):
        try:
            if len(command) != 4:
                raise ValueError("invalid number of arguments for subtractcounters, must be in format: \"subtractcounters [zone] [card] [counters]\"")

            zone = None 
            index = None
            counters = None

            if command [1] in self._zoneCommands:
                zone = self._zoneCommands[command[1]]
            else:
                raise ValueError(command[1] + " is an invalid zone.")

            index = self._getCardIndex(zone, command[2])
            card = zone.getCard(index)

            if not command[3].isdigit():
                raise ValueError("Invalid argument for counters.")

            counters = int(command[3])

            if counters < 0:
                raise ValueError("Can not subtract negative counters.")
            if card.counters   - counters < 0:
                raise ValueError("There are not that many counters left on " + card.cardName)

            self.controller.subtractCounters(zone, index, counters)
            text = "Removed " + str(counters) + " counters from " + card.cardName + ". It now has " + str(card.counters) + " counters."
            return text
        except Exception as e:
            raise e

    def addPlus1Counters(self, command):
        try:
            if len(command) != 4:
                raise ValueError("invalid number of arguments for addplus1counters, must be in format: \"addplus1counters [zone] [card] [plus 1 counters]\"")

            zone = None 
            index = None
            plus1Counters = None

            if command [1] in self._zoneCommands:
                zone = self._zoneCommands[command[1]]
            else:
                raise ValueError(command[1] + " is an invalid zone.")

            index = self._getCardIndex(zone, command[2])
            card = zone.getCard(index)

            if not command[3].isdigit():
                raise ValueError("Invalid argument for plus 1 Counters.")

            plus1Counters = int(command[3])

            if plus1Counters < 0:
                raise ValueError("Can not add negative plus 1 counters.")

            self.controller.addPlus1Counters(zone, index, plus1Counters)
            text = "Added " + str(plus1Counters) + " plus 1 counters to " + card.cardName + ". It now has " + str(card.plus1Counters) + " plus 1 counters."
            return text
        except Exception as e:
            raise e

    def subtractPlus1Counters(self, command):
        try:
            if len(command) != 4:
                raise ValueError("invalid number of arguments for subtractplus1counters, must be in format: \"subtractplus1counters [zone] [card] [plus 1 counters]\"")

            zone = None 
            index = None
            plus1Counters = None

            if command [1] in self._zoneCommands:
                zone = self._zoneCommands[command[1]]
            else:
                raise ValueError(command[1] + " is an invalid zone.")

            index = self._getCardIndex(zone, command[2])
            card = zone.getCard(index)

            if not command[3].isdigit():
                raise ValueError("Invalid argument for plus 1 counters.")

            plus1Counters = int(command[3])

            if plus1Counters < 0:
                raise ValueError("Can not subtract negative plus 1 counters.")
            if card.plus1Counters   - plus1Counters < 0:
                raise ValueError("There are not that many plus 1 counters left on " + card.cardName)

            self.controller.subtractPlus1Counters(zone, index, plus1Counters)
            text = "Removed " + str(plus1Counters) + " plus 1 counters from " + card.cardName + ". It now has " + str(card.plus1Counters) + " plus 1 counters."
            return text
        except Exception as e:
            raise e

    def addMinus1Counters(self, command):
        try:
            if len(command) != 4:
                raise ValueError("invalid number of arguments for addminus1counters, must be in format: \"addminus1counters [zone] [card] [minus 1 counters]\"")

            zone = None 
            index = None
            minus1Counters = None

            if command [1] in self._zoneCommands:
                zone = self._zoneCommands[command[1]]
            else:
                raise ValueError(command[1] + " is an invalid zone.")

            index = self._getCardIndex(zone, command[2])
            card = zone.getCard(index)

            if not command[3].isdigit():
                raise ValueError("Invalid argument for minus 1 Counters.")

            minus1Counters = int(command[3])

            if minus1Counters < 0:
                raise ValueError("Can not add negative minus 1 counters.")

            self.controller.addMinus1Counters(zone, index, minus1Counters)
            text = "Added " + str(minus1Counters) + " minus 1 counters to " + card.cardName + ". It now has " + str(card.minus1Counters) + " minus 1 counters."
            return text
        except Exception as e:
            raise e

    def subtractMinus1Counters(self, command):
        try:
            if len(command) != 4:
                raise ValueError("invalid number of arguments for subtractminus1counters, must be in format: \"subtractminus1counters [zone] [card] [minus 1 counters]\"")

            zone = None 
            index = None
            minus1Counters = None

            if command [1] in self._zoneCommands:
                zone = self._zoneCommands[command[1]]
            else:
                raise ValueError(command[1] + " is an invalid zone.")

            index = self._getCardIndex(zone, command[2])
            card = zone.getCard(index)

            if not command[3].isdigit():
                raise ValueError("Invalid argument for minus 1 counters.")

            minus1Counters = int(command[3])

            if minus1Counters < 0:
                raise ValueError("Can not subtract negative minus 1 counters.")
            if card.minus1Counters   - minus1Counters < 0:
                raise ValueError("There are not that many minus 1 counters left on " + card.cardName)

            self.controller.subtractMinus1Counters(zone, index, minus1Counters)
            text = "Removed " + str(minus1Counters) + " minus 1 counters from " + card.cardName + ". It now has " + str(card.minus1Counters) + " minus 1 counters."
            return text
        except Exception as e:
            raise e
