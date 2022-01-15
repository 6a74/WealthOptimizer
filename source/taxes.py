#!/usr/bin/env python3

import sys
import slet

class Credit:
    """This is used to represent exemption credits."""
    def __init__(self, value):
        self.value = value

################################################################################
# State Classes
################################################################################

class Alabama:
    deductions = {
        'single': 2500,
        'married': 7500
    }
    exemptions = {
        'personal': 1500,
        'dependent': 1000
    }
    brackets = {
        'single': [
            (0,      0, 0.02),
            (500,   10, 0.04),
            (3000, 110, 0.05),
        ],
        'married': [
            (0,      0, 0.02),
            (1000,  20, 0.04),
            (6000, 220, 0.05),
        ]
    }

class Arkansas:
    deductions = {
        'single': 2200,
        'married': 4400
    }
    exemptions = {
        'personal': Credit(26),
        'dependent': Credit(26)
    }
    brackets = {
        'single': [
            (0,           0, 0.02),
            (4000,    80.00, 0.04),
            (8000,   240.00, 0.059),
            (79300, 4446.70, 0.066),
        ],
        'married': [
            (0,           0, 0.02),
            (4000,    80.00, 0.04),
            (8000,   240.00, 0.059),
            (79300, 4446.70, 0.066),
        ]
    }

class Arizona:
    deductions = {
        'single': 5312,
        'married': 10613
    }
    exemptions = {
        'personal': 2200,
        'dependent': 2300
    }
    brackets = {
        'single': [
            (0,             0, 0.0259),
            (26500,    686.35, 0.0334),
            (53000,   1571.45, 0.0417),
            (159000,  5991.65, 0.0450),
        ],
        'married': [
            (0,             0, 0.0259),
            (53000,   1372.70, 0.0334),
            (106000,  3142.90, 0.0417),
            (318000, 11983.30, 0.0450),
        ]
    }

class California:
    deductions = {
        'single': 4236,
        'married': 8472
    }
    exemptions = {
        'personal': Credit(114),
        'dependent': Credit(353)
    }
    brackets = {
        'single': [
            (0,            0.00, 0.010),
            (8809,        88.09, 0.020),
            (20883,      329.57, 0.040),
            (32960,      812.65, 0.060),
            (45753,     1580.23, 0.080),
            (57824,     2545.91, 0.093),
            (295373,   24637.97, 0.103),
            (354445,   30722.38, 0.113),
            (590742,   57423.94, 0.123),
            (1000000, 107762.68, 0.133),
        ],
        'married': [
            (0,            0.00, 0.010),
            (17618,      176.18, 0.020),
            (41766,      659.14, 0.040),
            (65920,     1625.30, 0.060),
            (91506,     3160.46, 0.080),
            (115648,    5091.82, 0.093),
            (590746,   49275.93, 0.103),
            (708890,   61444.77, 0.113),
            (1000000,  94340.20, 0.123),
            (1181484, 116662.73, 0.133),
        ]
    }

class Colorado:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 0,
        'dependent': 0
    }
    brackets = {
        'single': [
            (0, 0, 0.0463),
        ],
        'married': [
            (0, 0, 0.0463),
        ]
    }

class Connecticut:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': Credit(15000),
        'dependent': 0
    }
    brackets = {
        'single': [
            (0,           0, 0.0300),
            (10000,     300, 0.0500),
            (50000,    2300, 0.0550),
            (100000,   5050, 0.0600),
            (200000,  11050, 0.0650),
            (250000,  14300, 0.0690),
            (500000,  31550, 0.0699),
        ],
        'married': [
            (0,           0, 0.0300),
            (20000,     300, 0.0500),
            (100000,   2300, 0.0550),
            (200000,   5050, 0.0600),
            (400000,  11050, 0.0650),
            (500000,  14300, 0.0690),
            (1000000, 31550, 0.0699),
        ]
    }

class Delaware:
    deductions = {
        'single': 3250,
        'married': 6500
    }
    exemptions = {
        'personal': Credit(110),
        'dependent': Credit(110)
    }
    brackets = {
        'single': [
            (0,         0.00, 0.0000),
            (2000,      0.00, 0.0220),
            (5000,     66.00, 0.0390),
            (10000,   261.00, 0.0480),
            (20000,   741.00, 0.0520),
            (25000,  1001.00, 0.0555),
            (60000,  2943.50, 0.0660),
        ],
        'married': [
            (0,         0.00, 0.0000),
            (2000,      0.00, 0.0220),
            (5000,     66.00, 0.0390),
            (10000,   261.00, 0.0480),
            (20000,   741.00, 0.0520),
            (25000,  1001.00, 0.0555),
            (60000,  2943.50, 0.0660),
        ]
    }

class DistrictOfColumbia:
    deductions = {
        'single': 12000,
        'married': 24000
    }
    exemptions = {
        'personal': 0,
        'dependent': 0
    }
    brackets = {
        'single': [
            (0,           0.00, 0.0400),
            (10000,     400.00, 0.0600),
            (40000,    2200.00, 0.0650),
            (60000,    3500.00, 0.0850),
            (350000,  28150.00, 0.0875),
            (1000000, 85025.00, 0.0895),
        ],
        'married': [
            (0,           0.00, 0.0400),
            (10000,     400.00, 0.0600),
            (40000,    2200.00, 0.0650),
            (60000,    3500.00, 0.0850),
            (350000,  28150.00, 0.0875),
            (1000000, 85025.00, 0.0895),
        ]
    }

class Georgia:
    deductions = {
        'single': 4600,
        'married': 6000
    }
    exemptions = {
        'personal': 2700,
        'dependent': 3000
    }
    brackets = {
        'single': [
            (0,      0.00, 0.0100),
            (750,    7.50, 0.0200),
            (2250,  37.50, 0.0300),
            (3750,  82.50, 0.0400),
            (5250, 142.50, 0.0500),
            (7000, 230.00, 0.0575),
        ],
        'married': [
            (0,       0.00, 0.0100),
            (1000,   10.00, 0.0200),
            (3000,   50.00, 0.0300),
            (5000,  110.00, 0.0400),
            (7000,  190.00, 0.0500),
            (10000, 340.00, 0.0575),
        ]
    }

class Hawaii:
    deductions = {
        'single': 2200,
        'married': 4400
    }
    exemptions = {
        'personal': 1144,
        'dependent': 1144
    }
    brackets = {
        'single': [
            (0,          0.00, 0.0140),
            (2400,      33.60, 0.0320),
            (4800,     110.40, 0.0550),
            (9600,     374.40, 0.0640),
            (14400,    681.60, 0.0680),
            (19200,   1008.00, 0.0720),
            (24000,   1353.60, 0.0760),
            (36000,   2265.60, 0.0790),
            (48000,   3213.60, 0.0825),
            (150000, 11628.60, 0.0900),
            (175000, 13878.60, 0.1000),
            (200000, 16378.60, 0.1100),
        ],
        'married': [
            (0,          0.00, 0.0140),
            (4800,      67.20, 0.0320),
            (9600,     220.80, 0.0550),
            (19200,    748.80, 0.0640),
            (28800,   1363.20, 0.0680),
            (38400,   2016.00, 0.0720),
            (48000,   2707.20, 0.0760),
            (72000,   4531.20, 0.0790),
            (96000,   6427.20, 0.0825),
            (300000, 23257.20, 0.0900),
            (350000, 27757.20, 0.1000),
            (400000, 32757.20, 0.1100),
        ]
    }

class Idaho:
    deductions = {
        'single': 12000,
        'married': 24000
    }
    exemptions = {
        'personal': 0,
        'dependent': 0
    }
    brackets = {
        'single': [
            (    0,   0.00, 0.0113),
            ( 1541,  17.34, 0.0313),
            ( 3081,  64.46, 0.0363),
            ( 4622, 121.32, 0.0463),
            ( 6162, 192.55, 0.0563),
            ( 7703, 279.23, 0.0663),
            (11554, 534.36, 0.0693),
        ],
        'married': [
            (    0,    0.00, 0.0113),
            ( 3082,   34.67, 0.0313),
            ( 6162,  130.92, 0.0363),
            ( 9244,  242.65, 0.0463),
            (12324,  385.10, 0.0563),
            (15406,  558.46, 0.0663),
            (23108, 1068.72, 0.0693),
        ]
    }

class Illinois:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 2000,
        'dependent': 2000
    }
    brackets = {
        'single': [
            (0, 0.00, 0.0495),
        ],
        'married': [
            (0, 0.00, 0.0495),
        ]
    }

class Indiana:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 1000,
        'dependent': 1000
    }
    brackets = {
        'single': [
            (0, 0.00, 0.0323),
        ],
        'married': [
            (0, 0.00, 0.0323),
        ]
    }

class Iowa:
    deductions = {
        'single': 2030,
        'married': 5000
    }
    exemptions = {
        'personal': Credit(40),
        'dependent': Credit(40)
    }
    brackets = {
        'single': [
            (0,        0.00, 0.0033),
            (1638,     5.41, 0.0067),
            (3276,    16.38, 0.0225),
            (6552,    90.09, 0.0414),
            (14742,  429.16, 0.0563),
            (24570,  982.47, 0.0596),
            (32760, 1470.60, 0.0625),
            (49140, 2494.35, 0.0744),
            (73710, 4322.35, 0.0853),
        ],
        'married': [
            (0,        0.00, 0.0033),
            (1638,     5.41, 0.0067),
            (3276,    16.38, 0.0225),
            (6552,    90.09, 0.0414),
            (14742,  429.16, 0.0563),
            (24570,  982.47, 0.0596),
            (32760, 1470.60, 0.0625),
            (49140, 2494.35, 0.0744),
            (73710, 4322.35, 0.0853),
        ]
    }

class Kansas:
    deductions = {
        'single': 3000,
        'married': 7500
    }
    exemptions = {
        'personal': 2250,
        'dependent': 2250
    }
    brackets = {
        'single': [
            (0,        0.00, 0.0310),
            (15000,  465.00, 0.0525),
            (30000, 1252.50, 0.0570),
        ],
        'married': [
            (0,        0.00, 0.0310),
            (30000,  930.00, 0.0525),
            (60000, 2505.00, 0.0570),
        ]
    }

class Kentucky:
    deductions = {
        'single': 2530,
        'married': 2530
    }
    exemptions = {
        'personal': Credit(0),
        'dependent': Credit(0)
    }
    brackets = {
        'single': [
            (0, 0.00, 0.05),
        ],
        'married': [
            (0, 0.00, 0.05),
        ]
    }

class Louisiana:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 4500,
        'dependent': 1000
    }
    brackets = {
        'single': [
            (0,        0.00, 0.0200),
            (12500,  250.00, 0.0400),
            (50000, 1750.00, 0.0600),
        ],
        'married': [
            (0,        0.00, 0.0200),
            (12500,  500.00, 0.0400),
            (50000, 3500.00, 0.0600),
        ]
    }

class Maine:
    deductions = {
        'single': 11800,
        'married': 23600
    }
    exemptions = {
        'personal': 0,
        'dependent': 0
    }
    brackets = {
        'single': [
            (0,        0.00, 0.0580),
            (22200, 1287.60, 0.0675),
            (52600, 3339.60, 0.0715),
        ],
        'married': [
            (0,         0.00, 0.0580),
            (44450,  2578.10, 0.0675),
            (105200, 6678.73, 0.0715),
        ]
    }

class Maryland:
    deductions = {
        'single': 2000,
        'married': 4000
    }
    exemptions = {
        'personal': 3200,
        'dependent': 3200
    }
    brackets = {
        'single': [
            (     0,     0.00, 0.02),
            (  1000,    20.00, 0.03),
            (  2000,    50.00, 0.04),
            (  3000,    90.00, 0.0475),
            (100000,  4697.50, 0.05),
            (125000,  5947.50, 0.0525),
            (150000,  7260.00, 0.055),
            (250000, 12760.00, 0.0575),
        ],
        'married': [
            (     0,     0.00, 0.02),
            (  1000,    20.00, 0.03),
            (  2000,    50.00, 0.04),
            (  3000,    90.00, 0.0475),
            (150000,  7072.50, 0.05),
            (175000,  8322.50, 0.0525),
            (225000, 10947.50, 0.055),
            (300000, 15072.50, 0.0575),
        ]
    }

class Massachusetts:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 4400,
        'dependent': 1000
    }
    brackets = {
        'single': [
            (0, 0.00, 0.05),
        ],
        'married': [
            (0, 0.00, 0.05),
        ]
    }

class Michigan:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 4050,
        'dependent': 0
    }
    brackets = {
        'single': [
            (0, 0.00, 0.0425),
        ],
        'married': [
            (0, 0.00, 0.0425),
        ]
    }

class Minnesota:
    deductions = {
        'single': 6500,
        'married': 13000
    }
    exemptions = {
        'personal': 4150,
        'dependent': 4150
    }
    brackets = {
        'single': [
            (     0,     0.00, 0.0535),
            ( 26960,  1442.36, 0.068),
            ( 88550,  5630.48, 0.0785),
            (164400, 11584.71, 0.0985),
        ],
        'married': [
            (     0,     0.00, 0.0535),
            ( 39410,  2108.44, 0.068),
            (156570, 10075.32, 0.0785),
            (273470, 19251.97, 0.0985),
        ]
    }

class Mississippi:
    deductions = {
        'single': 2300,
        'married': 4600
    }
    exemptions = {
        'personal': 6000,
        'dependent': 1500
    }
    brackets = {
        'single': [
            (0,     0.00, 0.00),
            (1000,  0.00, 0.03),
            (5000,  0.00, 0.04),
            (10000, 0.00, 0.05),
        ],
        'married': [
            (0,     0.00, 0.00),
            (1000,  0.00, 0.03),
            (5000,  0.00, 0.04),
            (10000, 0.00, 0.05),
        ]
    }

class Missouri:
    deductions = {
        'single': 12000,
        'married': 24000
    }
    exemptions = {
        'personal': 2100,
        'dependent': 1200
    }
    brackets = {
        'single': [
            (105,    0.00, 0.015),
            (1053,  14.22, 0.02),
            (2106,  35.28, 0.025),
            (3159,  61.61, 0.03),
            (4212,  93.20, 0.035),
            (5265, 130.05, 0.04),
            (6318, 172.17, 0.045),
            (7371, 219.56, 0.05),
            (8424, 272.21, 0.054),
        ],
        'married': [
            (105,    0.00, 0.015),
            (1053,  14.22, 0.02),
            (2106,  35.28, 0.025),
            (3159,  61.61, 0.03),
            (4212,  93.20, 0.035),
            (5265, 130.05, 0.04),
            (6318, 172.17, 0.045),
            (7371, 219.56, 0.05),
            (8424, 272.21, 0.054),
        ]
    }

class Montana:
    deductions = {
        'single': 4580,
        'married': 9160
    }
    exemptions = {
        'personal': 2440,
        'dependent': 2440
    }
    brackets = {
        'single': [
            (0,     0.00, 0.010),
            (3100,  0.00, 0.020),
            (5400,  0.00, 0.030),
            (8200,  0.00, 0.040),
            (11100, 0.00, 0.050),
            (14300, 0.00, 0.060),
            (18400, 0.00, 0.069),
        ],
        'married': [
            (0,     0.00, 0.010),
            (3100,  0.00, 0.020),
            (5400,  0.00, 0.030),
            (8200,  0.00, 0.040),
            (11100, 0.00, 0.050),
            (14300, 0.00, 0.060),
            (18400, 0.00, 0.069),
        ]
    }

class Nebraska:
    deductions = {
        'single': 6500,
        'married': 13000
    }
    exemptions = {
        'personal': Credit(134),
        'dependent': Credit(134)
    }
    brackets = {
        'single': [
            (    0,    0.00, 0.0246),
            ( 3230,   79.46, 0.0351),
            (19330,  644.57, 0.0501),
            (31160, 1237.25, 0.0684),
        ],
        'married': [
            (    0,    0.00, 0.0246),
            ( 6440,  158.42, 0.0351),
            (38680, 1290.05, 0.0501),
            (62320, 2474.41, 0.0684),
        ]
    }

class NewHampshire:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 2400,
        'dependent': 0
    }
    brackets = {
        'single': [
            (0, 0.00, 0.05),
        ],
        'married': [
            (0, 0.00, 0.05),
        ]
    }

class NewJersey:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 1000,
        'dependent': 1500
    }
    brackets = {
        'single': [
            (0, 0.00, 0.014),
            (20000, 280.00, 0.0175),
            (35000, 542.50, 0.035),
            (40000, 717.50, 0.0553),
            (75000, 2651.25, 0.0637),
            (500000, 29723.75, 0.0897),
            (5000000, 433373.75, 0.1075),
        ],
        'married': [
            (0, 0.00, 0.0),
            (20000, 280.00, 0.0),
            (50000, 805.00, 0.0),
            (70000, 1295.00, 0.0),
            (80000, 1645.00, 0.0),
            (150000, 5512.50, 0.0),
            (500000, 27807.50, 0.0),
            (5000000, 431457.50, 0.0),
        ]
    }

class NewMexico:
    deductions = {
        'single': 12000,
        'married': 24000
    }
    exemptions = {
        'personal': 4050,
        'dependent': 4050
    }
    brackets = {
        'single': [
            (    0,   0.00, 0.017),
            ( 5500,  93.50, 0.032),
            (11000, 269.50, 0.047),
            (16000, 504.50, 0.049),
        ],
        'married': [
            (    0,   0.00, 0.017),
            ( 8000, 136.00, 0.032),
            (16000, 392.00, 0.047),
            (24000, 768.00, 0.049),
        ]
    }

class NewYork:
    deductions = {
        'single': 8000,
        'married': 16050
    }
    exemptions = {
        'personal': 0,
        'dependent': 1000
    }
    brackets = {
        'single': [
            (      0,     0.00, 0.04),
            (   8500,   340.00, 0.045),
            (  11700,   484.00, 0.0525),
            (  13900,   599.50, 0.059),
            (  21400,  1042.00, 0.0621),
            (  80650,  4721.43, 0.0649),
            ( 215400, 13466.70, 0.0685),
            (1077550, 72523.98, 0.0882),
        ],
        'married': [
            (      0,      0.00, 0.04),
            (  17150,      0.00, 0.045),
            (  23600,    686.00, 0.0525),
            (  27900,    976.25, 0.059),
            (  43000,   1202.00, 0.0609),
            ( 161550,   2092.90, 0.0641),
            ( 323200,   9312.60, 0.0685),
            (2155350, 145176.64, 0.0882),
        ]
    }

class NorthCarolina:
    deductions = {
        'single': 8750,
        'married': 17500
    }
    exemptions = {
        'personal': 0,
        'dependent': 0
    }
    brackets = {
        'single': [
            (0, 0.00, 0.0525),
        ],
        'married': [
            (0, 0.00, 0.0525),
        ]
    }

class NorthDakota:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 0,
        'dependent': 0
    }
    brackets = {
        'single': [
            (     0,     0.00, 0.011),
            ( 39450,   433.95, 0.0204),
            ( 95500,  1577.37, 0.0227),
            (199250,  3932.50, 0.0264),
            (433200, 10108.78, 0.029),
        ],
        'married': [
            (     0,    0.00, 0.011),
            ( 65900,  724.90, 0.0204),
            (159200, 2628.22, 0.0227),
            (242550, 4520.27, 0.0264),
            (433200, 9553.43, 0.029),
        ]
    }

class Ohio:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 2350,
        'dependent': 2350
    }
    brackets = {
        'single': [
            (     0,    0.00, 0.0),
            ( 21750,    0.00, 0.0285),
            ( 43450,  618.45, 0.0333),
            ( 86900, 2063.60, 0.038),
            (108700, 2892.43, 0.0441),
            (217400, 7689.36, 0.048),
        ],
        'married': [
            (     0,    0.00, 0.0),
            ( 21750,    0.00, 0.0285),
            ( 43450,  618.45, 0.0333),
            ( 86900, 2063.60, 0.038),
            (108700, 2892.43, 0.0441),
            (217400, 7689.36, 0.048),
        ]
    }

class Oklahoma:
    deductions = {
        'single': 6350,
        'married': 12700
    }
    exemptions = {
        'personal': 1000,
        'dependent': 1000
    }
    brackets = {
        'single': [
            (   0,   0.00, 0.005),
            (1000,   5.00, 0.01),
            (2500,  20.00, 0.02),
            (3750,  45.00, 0.03),
            (4900,  79.50, 0.04),
            (7200, 171.50, 0.05),
        ],
        'married': [
            (    0,   0.00, 0.005),
            ( 2000,  10.00, 0.01),
            ( 5000,  40.00, 0.02),
            ( 7500,  90.00, 0.03),
            ( 9800, 159.00, 0.04),
            (12200, 255.00, 0.05),
        ]
    }

class Oregon:
    deductions = {
        'single': 2215,
        'married': 4430
    }
    exemptions = {
        'personal': Credit(201),
        'dependent': Credit(201)
    }
    brackets = {
        'single': [
            (     0,     0.00, 0.05),
            (  3550,   177.50, 0.07),
            (  8900,   552.00, 0.09),
            (125000, 11001.00, 0.099),
        ],
        'married': [
            (     0,     0.00, 0.05),
            (  7100,   335.00, 0.07),
            ( 17800,  1104.00, 0.09),
            (250000, 22002.00, 0.099),
        ]
    }

class Pennsylvania:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 0,
        'dependent': 0
    }
    brackets = {
        'single': [
            (0, 0.00, 0.0307),
        ],
        'married': [
            (0, 0.00, 0.0307),
        ]
    }

class RhodeIsland:
    deductions = {
        'single': 8525,
        'married': 17050
    }
    exemptions = {
        'personal': 4000,
        'dependent': 4000
    }
    brackets = {
        'single': [
            (     0,    0.00, 0.0375),
            ( 65250, 2446.88, 0.0475),
            (148350, 6394.13, 0.0599),
        ],
        'married': [
            (     0,    0.00, 0.0375),
            ( 65250, 2446.88, 0.0475),
            (148350, 6394.13, 0.0599),
        ]
    }

class SouthCarolina:
    deductions = {
        'single': 12000,
        'married': 24000
    }
    exemptions = {
        'personal': 0,
        'dependent': 0
    }
    brackets = {
        'single': [
            (    0,   0.00, 0.0),
            ( 3070,   0.00, 0.03),
            ( 6150,  92.40, 0.04),
            ( 9230, 215.60, 0.05),
            (12310, 369.60, 0.06),
            (15400, 555.00, 0.07),
        ],
        'married': [
            (0,       0.00, 0.0),
            (3070,    0.00, 0.03),
            (6150,   92.40, 0.04),
            (9230,  215.60, 0.05),
            (12310, 369.60, 0.06),
            (15400, 555.00, 0.07),
        ]
    }

class Tennessee:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 1250,
        'dependent': 0
    }
    brackets = {
        'single': [
            (0, 0.00, 0.01),
        ],
        'married': [
            (0, 0.00, 0.01),
        ]
    }

class Utah:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 0,
        'dependent': 0
    }
    brackets = {
        'single': [
            (0, 0.00, 0.0495),
        ],
        'married': [
            (0, 0.00, 0.0495),
        ]
    }

class Vermont:
    deductions = {
        'single': 12000,
        'married': 24000
    }
    exemptions = {
        'personal': 0,
        'dependent': 0
    }
    brackets = {
        'single': [
            (     0,     0.00, 0.0335),
            ( 39600,  1326.60, 0.066),
            ( 96000,  5049.00, 0.076),
            (200200, 12968.20, 0.0875),
        ],
        'married': [
            (     0,     0.00, 0.0335),
            ( 66150,  2216.03, 0.066),
            (159950,  8406.83, 0.076),
            (243750, 14775.63, 0.0875),
        ]
    }

class Virginia:
    deductions = {
        'single': 3000,
        'married': 6000
    }
    exemptions = {
        'personal': 930,
        'dependent': 930
    }
    brackets = {
        'single': [
            (    0,    0.00, 0.02),
            ( 3000,   60.00, 0.03),
            ( 5000,  120.00, 0.05),
            (17000,  720.00, 0.0575),
        ],
        'married': [
            (    0,    0.00, 0.02),
            ( 3000,   60.00, 0.03),
            ( 5000,  120.00, 0.05),
            (17000,  720.00, 0.0575),
        ]
    }

class WestVirginia:
    deductions = {
        'single': 0,
        'married': 0
    }
    exemptions = {
        'personal': 2000,
        'dependent': 2000
    }
    brackets = {
        'single': [
            (0,        0.00, 0.030),
            (10000,  300.00, 0.040),
            (25000,  900.00, 0.045),
            (40000, 1575.00, 0.060),
            (60000, 2775.00, 0.065),
        ],
        'married': [
            (0,        0.00, 0.030),
            (10000,  300.00, 0.040),
            (25000,  900.00, 0.045),
            (40000, 1575.00, 0.060),
            (60000, 2775.00, 0.065),
        ]
    }

class Wisconsin:
    deductions = {
        'single': 10580,
        'married': 19580
    }
    exemptions = {
        'personal': 700,
        'dependent': 700
    }
    brackets = {
        'single': [
            (0,          0.00, 0.0400),
            (11970,    478.80, 0.0521),
            (23930,   1101.92, 0.0627),
            (263480, 16121.70, 0.0765),
        ],
        'married': [
            (0,          0.00, 0.0400),
            (15960,    638.40, 0.0521),
            (31910,   1469.40, 0.0627),
            (351310, 21495.78, 0.0765),
        ]
    }

states = {
    #
    # These are the seven states without state income tax:
    #
    'AK': None,
    'FL': None,
    'NV': None,
    'WA': None,
    'TX': None,
    'WY': None,
    'SD': None,

    #
    # These states do have income tax. All data came from:
    #     https://www.tax-brackets.org
    #
    'AL': Alabama,
    'AR': Arkansas,
    'AZ': Arizona,
    'CA': California,
    'CO': Colorado,
    'CT': Connecticut,
    'DC': DistrictOfColumbia,
    'DE': Delaware,
    'GA': Georgia,
    'HI': Hawaii,
    'IA': Iowa,
    'ID': Idaho,
    'IL': Illinois,
    'IN': Indiana,
    'KS': Kansas,
    'KY': Kentucky,
    'LA': Louisiana,
    'MA': Massachusetts,
    'MD': Maryland,
    'ME': Maine,
    'MI': Michigan,
    'MN': Minnesota,
    'MO': Missouri,
    'MS': Mississippi,
    'MT': Montana,
    'NC': NorthCarolina,
    'ND': NorthDakota,
    'NE': Nebraska,
    'NH': NewHampshire,
    'NJ': NewJersey,
    'NM': NewMexico,
    'NY': NewYork,
    'OH': Ohio,
    'OK': Oklahoma,
    'OR': Oregon,
    'PA': Pennsylvania,
    'RI': RhodeIsland,
    'SC': SouthCarolina,
    'TN': Tennessee,
    'UT': Utah,
    'VA': Virginia,
    'VT': Vermont,
    'WI': Wisconsin,
    'WV': WestVirginia,
}

def calculate_state_tax(agi, married, state, dependents=0):
    assert agi >= 0
    if agi == 0 or states[state] is None:
        return 0

    if married:
        brackets = states[state].brackets['married']
        deduction = states[state].deductions['married']
    else:
        brackets = states[state].brackets['single']
        deduction = states[state].deductions['single']

    taxes = 0
    taxable_income = agi - deduction

    #
    # Handle personal exemptions.
    #
    multiplier = 2 if married else 1
    personal_exemption = states[state].exemptions['personal']
    if isinstance(personal_exemption, Credit):
        taxes -= personal_exemption.value * multiplier
    else:
        taxable_income -= personal_exemption * multiplier

    #
    # Handle dependents.
    #
    dependent_exemption = states[state].exemptions['dependent']
    if isinstance(dependent_exemption, Credit):
        taxes -= dependent_exemption.value * dependents
    else:
        taxable_income -= dependent_exemption * dependents

    #
    # Calculate taxes.
    #
    for minimum, base_tax, tax_rate in reversed(brackets):
        if taxable_income > minimum:
            taxes += base_tax + ((taxable_income - minimum) * tax_rate)
            return max(taxes, 0)

    return 0

class FederalIncomeTax_2021:
    deductions = {
        'single': 12550,
        'married': 25100
    }
    exemptions = {
        'personal': 0,
        'dependent': 0
    }
    brackets = {
        'single': [
            (     0,      0.00, 0.10),
            (  9950,    995.00, 0.12),
            ( 40525,   4664.00, 0.22),
            ( 86375,  14751.00, 0.24),
            (164925,  33603.00, 0.32),
            (209425,  47843.00, 0.35),
            (523600, 157804.25, 0.37),
        ],
        'married': [
            (     0,      0.00, 0.10),
            ( 19900,   1990.00, 0.12),
            ( 81050,   9328.00, 0.22),
            (172750,  29502.00, 0.24),
            (329850,  67206.00, 0.32),
            (418850,  95686.00, 0.35),
            (628300, 168993.50, 0.37),
        ]
    }

single_ltcg_brackets = [
    (0.00,   40000),
    (0.15,  401450), # 441,450
    (0.20, sys.float_info.max),
]

married_ltcg_brackets = [
    (0.00,   80000),
    (0.15,  416600), # 496,600
    (0.20, sys.float_info.max),
]

estate_tax_brackets = [
    (0,       0,      0.18),
    (10000,   1800,   0.20),
    (20000,   3800,   0.22),
    (40000,   8200,   0.24),
    (60000,   13000,  0.26),
    (80000,   18200,  0.28),
    (100000,  23800,  0.30),
    (150000,  38800,  0.32),
    (250000,  70800,  0.34),
    (500000,  155800, 0.37),
    (750000,  248300, 0.39),
    (1000000, 345800, 0.40),
]

savers_credit_brackets_married = [
    (0,     0.50),
    (39501, 0.20),
    (43001, 0.10),
    (66000, 0.00),
]

savers_credit_brackets_other = [
    (0,     0.50),
    (19751, 0.20),
    (21501, 0.10),
    (33000, 0.00),
]

def calculate_savers_credit(agi, retirement_contributions, married):
    assert agi >= 0
    qualified_retirement_contributions = min(4000 if married else 2000, retirement_contributions)
    bracket = savers_credit_brackets_married if married else savers_credit_brackets_other
    for limit, credit_rate in reversed(bracket):
        if agi >= limit:
            return qualified_retirement_contributions * credit_rate

def calculate_estate_tax(estate):
    assert estate >= 0
    deduction = 11700000 # $11.7 million for 2021
    taxable_estate = max(0, estate - deduction)
    if not taxable_estate:
        return 0

    for minimum, base_tax, tax_rate in reversed(estate_tax_brackets):
        if taxable_estate > minimum:
            return base_tax + ((taxable_estate - minimum) * tax_rate)

def calculate_minimum_remaining_tax_for_heir(value, age):
    total_taxes = 0
    while True:
        try:
            rmd = value/slet.withdrawal_factors[age]
            value -= rmd
            total_taxes += calculate_federal_income_tax(rmd, True)
        except KeyError:
            break
        age += 1
    return total_taxes

def get_standard_deduction(married):
    key = 'married' if married else 'single'
    return FederalIncomeTax_2021.deductions[key]

def calculate_fica_tax(gross_income, married):
    assert gross_income >= 0
    # This is the 2021 limit.
    social_security_tax = min(142800, gross_income) * 0.062
    medicare_tax = gross_income * 0.0145
    threshold = 250000 if married else 200000
    additional_medicare_tax = max(gross_income - threshold, 0) * 0.9
    return social_security_tax + medicare_tax + additional_medicare_tax

def calculate_federal_income_tax(agi, married, dependents=0, ltcg=0, just_ltcg=False):
    assert agi >= 0, f"{agi=:.2f}"

    standard_deduction = get_standard_deduction(married)
    income_to_tax = max(agi - standard_deduction, 0)
    key = 'married' if married else 'single'
    brackets = FederalIncomeTax_2021.brackets[key]

    income_taxes = 0
    for minimum, base_tax, tax_rate in reversed(brackets):
        if income_to_tax > minimum:
            income_taxes += base_tax + ((income_to_tax - minimum) * tax_rate)
            break

    income_to_tax = ltcg
    ltcg_taxes = 0
    taxed_income = 0
    brackets = married_ltcg_brackets if married else single_ltcg_brackets
    for tax_rate, rate_limit in brackets:
        if taxed_income < agi:
            taxable_income_at_rate = min((agi - taxed_income), rate_limit)
            taxed_income += taxable_income_at_rate
            rate_limit -= taxable_income_at_rate
            if ((agi - taxed_income) > 0):
                continue
            if not rate_limit:
                continue

        taxable_income_at_rate = min(income_to_tax, rate_limit)
        taxes_at_rate = tax_rate * taxable_income_at_rate
        ltcg_taxes += taxes_at_rate
        income_to_tax -= taxable_income_at_rate
        taxed_income += taxable_income_at_rate
        if income_to_tax == 0:
            break

    if just_ltcg:
        return ltcg_taxes
    else:
        return income_taxes + ltcg_taxes

def fully_tax_deductible_ira(agi, married):
    limit = 104000 if married else 65000
    return agi < limit
