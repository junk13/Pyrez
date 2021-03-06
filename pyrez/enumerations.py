from enum import Enum, IntFlag

class BaseEnum(Enum):
    def __str__(self):
        return str(self.value) # return str(self.name)

class ResponseFormat(BaseEnum):
    JSON = "json"
    XML = "xml"

class LanguageCode(IntFlag): # LanguageCode(5) == LanguageCode lang =(LanguageCode) 5;
    English = 1
    German = 2
    French = 3
    Chinese = 5
    Spanish = 7
    Spanish_Latin_America = 9
    Portuguese = 10
    Russian = 11
    Polish = 12
    Turkish = 13

class Endpoint(BaseEnum):
    HAND_OF_THE_GODS_PC = "http://api.handofthegods.com/handofthegodsapi.svc"
    PALADINS_PC = "http://api.paladins.com/paladinsapi.svc"
    PALADINS_PS4 = "http://api.ps4.paladins.com/paladinsapi.svc"
    PALADINS_XBOX = "http://api.xbox.paladins.com/paladinsapi.svc"
    PALADINS_STRIKE_MOBILE = "http://api.paladinsstrike.com/paladinsstrike.svc"
    REALM_ROYALE_PC = "http://api.realmroyale.com/realmapi.svc"
    REALM_ROYALE_PS4 = "http://api.ps4.realmroyale.com/realmapi.svc"
    REALM_ROYALE_XBOX = "http://api.xbox.realmroyale.com/realmapi.svc"
    SMITE_PC = "http://api.smitegame.com/smiteapi.svc"
    SMITE_PS4 = "http://api.ps4.smitegame.com/smiteapi.svc"
    SMITE_XBOX = "http://api.xbox.smitegame.com/smiteapi.svc"

class Platform(BaseEnum):
    MOBILE = "MOBILE"
    NINTENDO_SWITCH = "SWITCH"
    PC = "PC"
    PS4 = "PS4"
    XBOX = "XBOX"

class Classes(BaseEnum):
    Warrior = 2285
    Hunter = 2493
    Mage = 2494
    Engineer = 2495
    Assassin = 2496

class Champions(Enum):
    Androxus = 2205
    Ash = 2404
    Barik = 2073
    Bomb_King = 2281
    Buck = 2147
    Cassie = 2092
    Dredge = 2495
    Drogoz = 2277
    Evie = 2094
    Fernando = 2071
    Furia = 2491
    Grohk = 2093
    Grover = 2254
    Inara = 2348
    Jenos = 2431
    Khan = 2479
    Kinessa = 2249
    Koga = 2493
    Lex = 2362
    Lian = 2417
    Maeve = 2338
    Makoa = 2288
    Mal_Damba = 2303
    Moji = 2481
    Pip = 2056
    Ruckus = 2149
    Seris = 2372
    Sha_Lin = 2307
    Skye = 2057
    Strix = 2438
    Talus = 2472
    Terminus = 2477
    Torvald = 2322
    Tyra = 2314
    Viktor = 2285
    Vivian = 2480
    Willo = 2393
    Ying = 2267
    Zhin = 2420
    
    def getId(self):
        return int(self.value)
    def getIconUrl(self):
        return "https://web2.hirez.com/paladins/champion-icons/{0}.jpg".format(self.name.lower().replace('_', '-'))
    def __str__(self):
        return str(self.name.replace("_", " "))

class Gods(Enum):
    Achilles = 3492
    Agni = 1737
    Ah_Muzen_Cab = 1956
    Ah_Puch = 2056
    Amaterasu = 2110
    Anhur = 1773
    Anubis = 1668
    Ao_Kuang = 2034
    Aphrodite = 1898
    Apollo = 1899
    Arachne = 1699
    Ares = 1782
    Artemis = 1748
    Artio = 3336
    Athena = 1919
    Awilix = 2037
    Bacchus = 1809
    Bakasura = 1755
    Baron_Samedi = 3518
    Bastet = 1678
    Bellona = 2047
    Cabrakan = 2008
    Camazotz = 2189
    Cerberus = 3419
    Cernunnos = 2268
    Chaac = 1966
    Change = 1921 # Chang'e
    Chernobog = 3509
    Chiron = 2075
    Chronos = 1920
    Cu_Chulainn = 2319
    Cupid = 1778
    Da_Ji = 2270
    Discordia = 3377
    Erlang_Shen = 2138
    Fafnir = 2136
    Fenrir = 1843
    Freya = 1784
    Ganesha = 2269
    Geb = 1978
    Guan_Yu = 1763
    Hachiman = 3344
    Hades = 1676
    He_Bo = 1674
    Hel = 1718
    Hera = 3558
    Hercules = 1848
    Hou_Yi = 2040
    Hun_Batz = 1673
    Isis = 1918
    Izanami = 2179
    Janus = 1999
    Jing_Wei = 2122
    Kali = 1649
    Khepri = 2066
    Kukulkan = 1677
    Kumbhakarna = 1993
    Kuzenbo = 2260
    Loki = 1797
    Medusa = 2051
    Mercury = 1941
    Ne_Zha = 1915
    Neith = 1872
    Nemesis = 1980
    Nike = 2214
    Nox = 2036
    Nu_Wa = 1958
    Odin = 1669
    Osiris = 2000
    Pele = 3543
    Poseidon = 1881
    Ra = 1698
    Raijin = 2113
    Rama = 2002
    Ratatoskr = 2063
    Ravana = 2065
    Scylla = 1988
    Serqet = 2005
    Skadi = 2107
    Sobek = 1747
    Sol = 2074
    Sun_Wukong = 1944
    Susano = 2123
    Sylvanus = 2030
    Terra = 2147
    Thanatos = 1943
    The_Morrigan = 2226
    Thor = 1779
    Thoth = 2203
    Tyr = 1924
    Ullr = 1991
    Vamana = 1723
    Vulcan = 1869
    Xbalanque = 1864
    Xing_Tian = 2072
    Ymir = 1670
    Zeus = 1672
    Zhong_Kui = 1926
    def getId(self):
        return int(self.value)
    def getCardUrl(self):
        return "https://web2.hirez.com/smite/god-cards/{0}.jpg".format(self.name.lower().replace('_', '-'))
    def getIconUrl(self):
        return "https://web2.hirez.com/smite/god-icons/{0}.jpg".format(self.name.lower().replace('_', '-'))
    def __str__(self):
        return str(self.name.replace('_', ' '))

class ItemType(IntFlag):
    Unknown = 0
    Defense = 1
    Utility = 2
    Healing = 3
    Damage = 4

class PortalId(Enum):
    HiRez = 1
    Steam = 5
    PS4 = 9
    Xbox = 10
    Switch = 22

class Status(Enum):
    Offline = 0
    In_Lobby = 1
    God_Selection = 2
    In_Game = 3
    Online = 4
    Not_Found = 5
    def __str__(self):
        return str(self.name.replace("_", " "))
class Tier(Enum):
    Unranked = 0 # Qualifying
    Bronze_V = 1
    Bronze_IV = 2
    Bronze_III = 3
    Bronze_II = 4
    Bronze_I = 5
    Silver_V = 6
    Silver_IV = 7
    Silver_III = 8
    Silver_II = 9
    Silver_I = 10
    Gold_V = 11
    Gold_IV = 12
    Gold_III = 13
    Gold_II = 14
    Gold_I = 15
    Platinum_V = 16
    Platinum_IV = 17
    Platinum_III = 18
    Platinum_II = 19
    Platinum_I = 20
    Diamond_V = 21
    Diamond_IV = 22
    Diamond_III = 23
    Diamond_II = 24
    Diamond_I = 25
    Master = 26
    Grandmaster = 27

    def __str__(self):
        return str(self.name.replace("_", " "))

class RealmRoyaleQueue(BaseEnum):
    Duo = 475
    Solo = 474
    Squad = 476
class SmiteQueue(BaseEnum):
    Conquest_5v5 = 423
    Novice_Queue = 424
    Conquest = 426
    Practice = 427
    Conquest_Challenge = 429 #Conquest_Ranked = 430
    Domination = 433
    MOTD = 434
    Arena_Queue = 435
    Basic_Tutorial = 436
    Arena_Challenge = 438
    Domination_Challenge = 439
    Joust_1v1_Ranked = 440
    Joust_Challenge = 441
    Arena_Practice_Easy = 443
    Jungle_Practice = 444
    Assault = 445
    Assault_Challenge = 446
    Joust_Queue_3v3 = 448
    Joust_3v3_Ranked = 450
    Conquest_Ranked = 451 # ConquestLeague
    Arena_League = 452
    Assault_vs_AI_Medium = 454
    Joust_vs_AI_Medium = 456
    Arena_vs_AI_Easy = 457
    Conquest_Practice_Easy = 458
    Siege_4v4 = 459
    Siege_Challenge = 460
    Conquest_vs_AI_Medium = 461
    Arena_Tutorial = 462
    Conquest_Tutorial = 463
    Joust_Practice_Easy = 464
    Clash = 466
    Clash_Challenge = 467
    Arena_vs_AI_Medium = 468
    Clash_vs_AI_Medium = 469
    Clash_Practice_Easy = 470
    Clash_Tutorial = 471
    Arena_Practice_Medium = 472
    Joust_Practice_Medium = 473
    Joust_vs_AI_Easy = 474
    Conquest_Practice_Medium = 475
    Conquest_vs_AI_Easy = 476
    Clash_Practice_Medium = 477
    Clash_vs_AI_Easy = 478
    Assault_Practice_Easy = 479
    Assault_Practice_Medium = 480
    Assault_vs_AI_Easy = 481
    Adventure_Horde = 495
    Adventure_Joust = 499
    Adventure_CH10 = 500
    def __str__(self):
        return str(self.name.replace("_", " "))

class PaladinsQueue(BaseEnum):
    Custom_Siege_Stone_Keep = 423
    Live_Casual = 424#LIVE_Siege
    Live_Pratice_Siege = 425
    Challenge_Match = 426
    Practice = 427
    Live_Competitive = 428
    zzRETIRED = 429
    Custom_Siege_Timber_Mill = 430
    Custom_Siege_Fish_Market = 431
    Custom_Siege_Frozen_Guard = 432
    Custom_Siege_Frog_Isle = 433
    Shooting_Range = 434
    Perf_Capture_Map = 435
    Tencent_Alpha_Test_Queue_Coop = 436
    Payload = 437
    Custom_Siege_Jaguar_Falls = 438
    Custom_Siege_Ice_Mines = 439
    Custom_Siege_Serpeant_Beach = 440
    Challenge_TP = 441
    Challenge_FP = 442
    Challenge_IP = 443
    Tutorial = 444
    Live_Test_Maps = 445
    PvE_Hands_That_Bind = 446
    WIPPvE_Los_Pollos_Fernandos = 447
    WIPPvE_High_Rollers = 448
    PvE_HnS = 449
    WIPPvE_Leap_Frogs = 450
    PvE_Survival = 451
    Live_Onslaught = 452
    Live_Pratice_Onslaught = 453
    Custom_Onslaught_Snowfall_Junction = 454
    Custom_Onslaught_Primal_Court = 455
    Custom_Siege_Brightmarsh = 458
    Custom_Siege_Splitstone_Quarry = 459
    Custom_Onslaught_Foreman_Rise = 462
    Custom_Onslaught_Magistrate_Archives = 464
    Classic_Siege = 465
    Custom_Team_Deathmatch_Trade_District = 468
    Live_Team_DeathMatch = 469
    Live_Pratice_Team_Deathmatch = 470
    Custom_Team_Deathmatch_Foreman_Rise = 471
    Custom_Team_Deathmatch_Magistrate_Archives = 472
    Custom_Siege_Ascension_Peak = 473
    Live_Battlegrounds_Solo = 474
    Live_Battlegrounds_Duo = 475
    Live_Battlegrounds_Quad = 476
    Live_Event_Ascension_Peak = 477 # LIVE HH(Event)
    Live_Event_Rise_Of_Furia = 478 # LIVE HH(Event)
    Custom_Team_Deathmatch_Abyss = 479
    Custom_Team_Deathmatch_Throne = 480
    Custom_Onslaught_Marauders_Port = 483
    Multi_Queue = 999
    def __str__(self):
        return str(self.name.replace("_", " "))
