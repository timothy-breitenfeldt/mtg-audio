/*
  Mtg Database
  This database contains card and set information for the magic the gathering card game 
*/

CREATE TABLE UserSetting (
  "userSettingUsername" TEXT
);

INSERT INTO UserSetting VALUES("x");


CREATE TABLE mtgSet (
  "setID" TEXT NOT NULL,
  "setName" TEXT NOT NULL,
  "blockName" TEXT NOT NULL,
  PRIMARY KEY(setID)
);


CREATE TABLE mtgCard (
  "cardID" INT NOT NULL,
  "cardName" TEXT NOT NULL,
  "cardNames" TEXT NULL,
  "cardManaCost" TEXT NULL,
  "cardCmc" INT NULL,
  "cardColors" TEXT NULL,
  "cardColorIdentity" TEXT NULL,
  "cardType" TEXT NULL,
  "cardSupertypes" TEXT NULL,
  "cardSubtypes" TEXT NULL,
  "cardRarity" TEXT NULL,
  "cardText" TEXT NULL,
  "cardFlavor" TEXT NULL,
  "cardPower" INT NULL,
  "cardToughness" INT NULL,
  "cardLoyalty" INT NULL,
  "cardRulings" TEXT NULL,
  "cardLegalities" TEXT NULL,
  "cardWatermark" TEXT NULL,
  "cardPrintings" TEXT NULL,
  "setID" TEXT NULL,
  FOREIGN KEY(setID) REFERENCES mtgSet(setID),
  PRIMARY KEY(cardID)
);
