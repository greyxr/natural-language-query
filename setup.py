TABLES = {}

TABLES['faction'] = (
    "CREATE TABLE faction ("
    "Faction VARCHAR(30),"
    "RankNumber TINYINT UNSIGNED NOT NULL,"
    "RankName VARCHAR(30),"
    "Primary Key (Faction, RankNumber),"
    "CHECK (RankNumber <= 9)"
    ");"
)

TABLES['npc'] = (
    "CREATE TABLE npc ("
    "ID VARCHAR(30) PRIMARY KEY,"
    "NpcName VARCHAR(30) NOT NULL,"
    "NpcLevel INT UNSIGNED NOT NULL,"
    "Faction VARCHAR(30),"
    "RankNumber TINYINT UNSIGNED NOT NULL,"
    "Class VARCHAR(30),"
    "Race VARCHAR(30) NOT NULL,"
    "FOREIGN KEY (Faction, RankNumber) REFERENCES Faction(Faction, RankNumber)"
    ");"
)

TABLES['merchant'] = (
    "CREATE TABLE merchant ("
    "MerchantName VARCHAR(30) PRIMARY KEY,"
    "AvailableGold INT UNSIGNED,"
    "Location VARCHAR(300),"
    "Faction VARCHAR(30),"
    "RankNumber TINYINT UNSIGNED NOT NULL,"
    "FOREIGN KEY (Faction, RankNumber) REFERENCES Faction(Faction, RankNumber)"
    ");"
)

TABLES['merchant_types'] = (
    "CREATE TABLE merchant_types ("
    "MerchantName VARCHAR(30),"
    "ItemType ENUM('Alchemy','Ingredient','Apparatus','Weapon','Armor','Clothing','Book','Misc','Enchanting', 'Assassin Service', 'Healer Service', 'Wise Woman Service', 'Food', 'Drink', 'Priest Service', 'Battlemage Service', 'Caravaner', 'Drillmaster Service', 'Mage Service', 'Monk Service', 'Savant Service', 'Nightblade Service', 'Sorcerer Service', 'Thief Service') NOT NULL,"
    "PRIMARY KEY (MerchantName, ItemType),"
    "FOREIGN KEY (MerchantName) REFERENCES Merchant(MerchantName)"
    ");"
)

TABLES['items'] = (
    "CREATE TABLE items ("
    "ID VARCHAR(30) PRIMARY KEY,"
    "ItemName VARCHAR(30) NOT NULL,"
    "ItemType ENUM('Alchemy','Ingredient','Apparatus','Weapon','Armor','Clothing','Books','Misc') NOT NULL,"
    "ItemWeight FLOAT(10,2),"
    "ItemValue INT UNSIGNED"
    ");"
)