BODY_PARTS_COLOR_MAP_IDS = set(tuple(range(100,127)))

COLOR_MAP_INSTANCES = {
    0: (226., 226., 226.), #(174., 199., 232.),
    1: (120., 94., 240.), #purple 
    2: (254., 97., 0.), #orange
    3: (255., 176., 0.), #yellow
    4: (100., 143., 255.), #blue
    5: (220., 38., 127.), #pink
    6: (0., 255., 255.),
    7: (255., 204., 153.),
    8: (255., 102., 0.),
    9: (0., 128., 128.),
    10: (153., 153., 255.),
}

MERGED_BODY_PART_COLORS = {
    0:  (226., 226., 226.),
    1:  (158.0, 143.0, 20.0),  #rightHand
    2:  (243.0, 115.0, 68.0),  #rightUpLeg
    3:  (228.0, 162.0, 227.0), #leftArm
    4:  (210.0, 78.0, 142.0),  #head
    5:  (152.0, 78.0, 163.0),  #leftLeg
    6:  (76.0, 134.0, 26.0),   #leftFoot
    7:  (100.0, 143.0, 255.0), #torso
    8:  (129.0, 0.0, 50.0),    #rightFoot
    9:  (255., 176., 0.),      #rightArm
    10: (192.0, 100.0, 119.0), #leftHand
    11: (149.0, 192.0, 228.0), #rightLeg 
    12: (243.0, 232.0, 88.0),  #leftForeArm
    13: (90., 64., 210.),      #rightForeArm
    14: (152.0, 200.0, 156.0), #leftUpLeg
    15: (129.0, 103.0, 106.0), #hips
}

LABEL_LIST = ["background", "rightHand", "rightUpLeg", "leftArm", "head", "leftEye", "rightEye", "leftLeg", 
                "leftToeBase", "leftFoot", "spine1", "spine2", "leftShoulder", "rightShoulder", 
                "rightFoot", "rightArm", "leftHandIndex1", "rightLeg", "rightHandIndex1",
                "leftForeArm", "rightForeArm", "neck", "rightToeBase", "spine", "leftUpLeg", 
                "leftHand", "hips"]

MERGED_LABEL_LIST = {
            0: "background",
            1: "rightHand",
            2: "rightUpLeg",
            3: "leftArm",
            4: "head",
            5: "leftLeg",
            6: "leftFoot",
            7: "torso",
            8: "rightFoot",
            9: "rightArm",
            10: "leftHand",
            11: "rightLeg",
            12: "leftForeArm",
            13: "rightForeArm",
            14: "leftUpLeg",
            15: "hips"}


COLOR_MAP_W_BODY_PARTS = { 
            0: (0., 0., 0.),
            # body parts
            100: (35., 69., 100.), # rightHand
            101: (73., 196., 37.), # rightUpLeg
            102: (121., 25., 252.), # leftArm
            103: (96., 237., 31.), # head
            104: (55., 40., 93.), # leftEye
            105: (75., 180., 125.), # rightEye
            106: (165., 38., 65.), # leftLeg
            107: (63., 75., 77.), # leftToeBase
            108: (27., 255., 80.), # leftFoot
            109: (82., 110., 90.), # spine1
            110: (87., 54., 10.), # spine2
            111: (210., 200., 110.), # leftShoulder
            112: (217., 212., 76.), # rightShoulder
            113: (254., 176., 234.), # rightFoot 
            114: (111., 140., 56.), # rightArm
            115: (83., 15., 157.), # leftHandIndex1
            116: (98., 255., 160.), # rightLeg
            117: (153., 170., 17.), # rightHandIndex1
            118: (54., 82., 122.), # leftForeArm
            119: (10., 19., 94.), # rightForeArm
            120: (1., 147., 72.), # neck
            121: (47., 210., 21.), # rightToeBase
            122: (174., 22., 133.), # spine
            123: (98., 58., 83.), # leftUpLeg
            124: (222., 25., 45.), # leftHand
            125: (75., 233., 65.), # hips
        }


COLOR_MAP = { # scannet colors followed by body parts colors
    -1: (255., 255., 255.),
    0:  (226., 226., 226.),
    1: (174., 199., 232.),
    2: (152., 223., 138.),
    3: (31., 119., 180.),
    4: (255., 187., 120.),
    5: (188., 189., 34.),
    6: (140., 86., 75.),
    7: (255., 152., 150.),
    8: (214., 39., 40.),
    9: (197., 176., 213.),
    10: (148., 103., 189.),
    11: (196., 156., 148.),
    12: (23., 190., 207.),
    14: (247., 182., 210.),
    15: (66., 188., 102.),
    16: (219., 219., 141.),
    17: (140., 57., 197.),
    18: (202., 185., 52.),
    19: (51., 176., 203.),
    20: (200., 54., 131.),
    21: (92., 193., 61.),
    22: (78., 71., 183.),
    23: (172., 114., 82.),
    24: (255., 127., 14.),
    25: (91., 163., 138.),
    26: (153., 98., 156.),
    27: (140., 153., 101.),
    28: (158., 218., 229.),
    29: (100., 125., 154.),
    30: (178., 127., 135.),
    31: (120., 185., 128.),
    32: (146., 111., 194.),
    33: (44., 160., 44.),
    34: (112., 128., 144.),
    35: (96., 207., 209.),
    36: (227., 119., 194.),
    37: (213., 92., 176.),
    38: (94., 106., 211.),
    39: (82., 84., 163.),
    40: (100., 85., 144.),
    41: (0., 0., 255.), #artificial human
    # body parts
    100: (35., 69., 100.), # rightHand
    101: (73., 196., 37.), # rightUpLeg
    102: (121., 25., 252.), # leftArm
    103: (96., 237., 31.), # head
    104: (55., 40., 93.), # leftEye
    105: (75., 180., 125.), # rightEye
    106: (165., 38., 65.), # leftLeg
    107: (63., 75., 77.), # leftToeBase
    108: (27., 255., 80.), # leftFoot
    109: (82., 110., 90.), # spine1
    110: (87., 54., 10.), # spine2
    111: (210., 200., 110.), # leftShoulder
    112: (217., 212., 76.), # rightShoulder
    113: (254., 176., 234.), # rightFoot 
    114: (111., 140., 56.), # rightArm
    115: (83., 15., 157.), # leftHandIndex1
    116: (98., 255., 160.), # rightLeg
    117: (153., 170., 17.), # rightHandIndex1
    118: (54., 82., 122.), # leftForeArm
    119: (10., 19., 94.), # rightForeArm
    120: (1., 147., 72.), # neck
    121: (47., 210., 21.), # rightToeBase
    122: (174., 22., 133.), # spine
    123: (98., 58., 83.), # leftUpLeg
    124: (222., 25., 45.), # leftHand
    125: (75., 233., 65.), # hips
}