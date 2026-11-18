"""
scan_words.py - reserved words (TD A, states 0-209) and identifiers
(TD C, states 275-334), written as one if / elif branch per state.

Reserved words: every state checks the current character against the arrows
that leave it.  If no arrow matches before the word is fully spelled, or the
word is spelled but a letter/digit/_ follows (Tester, Varying, TrueStory), the
same characters are read again with the identifier diagram (Identifiers
Rule 5: only the exact spelling is reserved).
"""

from .definitions import DELIM, letters, id_chars
from .emit import accept_word, word_delimiter_error, accept_id
from . import errors as E


def scan_word(src, tokens, errors):
    start = src.pos
    state = 0
    path = [0]
    while True:
        c = src.peek()
        if state == 0:        # start
            if c == "A":
                state = 1
            elif c == "B":
                state = 17
            elif c == "C":
                state = 33
            elif c == "F":
                state = 39
            elif c == "H":
                state = 50
            elif c == "I":
                state = 58
            elif c == "L":
                state = 65
            elif c == "M":
                state = 72
            elif c == "N":
                state = 76
            elif c == "O":
                state = 86
            elif c == "P":
                state = 89
            elif c == "R":
                state = 101
            elif c == "S":
                state = 124
            elif c == "T":
                state = 140
            elif c == "U":
                state = 187
            elif c == "V":
                state = 200
            elif c == "W":
                state = 205
            else:
                break
        elif state == 1:      # "A"
            if c == "b":
                state = 2
            elif c == "n":
                state = 8
            elif c == "p":
                state = 11
            else:
                break
        elif state == 2:      # "Ab"
            if c == "s":
                state = 3
            else:
                break
        elif state == 3:      # "Abs"
            if c == "o":
                state = 4
            else:
                break
        elif state == 4:      # "Abso"
            if c == "r":
                state = 5
            else:
                break
        elif state == 5:      # "Absor"
            if c == "b":
                state = 6
            else:
                break
        elif state == 6:      # "Absorb"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 7, "Absorb")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Absorbx
            else:
                word_delimiter_error(src, errors, start, 6, "Absorb", "method_delim")
                return
        elif state == 8:      # "An"
            if c == "d":
                state = 9
            else:
                break
        elif state == 9:      # "And"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 10, "And")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Andx
            else:
                word_delimiter_error(src, errors, start, 9, "And", "method_delim")
                return
        elif state == 11:     # "Ap"
            if c == "p":
                state = 12
            else:
                break
        elif state == 12:     # "App"
            if c == "e":
                state = 13
            else:
                break
        elif state == 13:     # "Appe"
            if c == "n":
                state = 14
            else:
                break
        elif state == 14:     # "Appen"
            if c == "d":
                state = 15
            else:
                break
        elif state == 15:     # "Append"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 16, "Append")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Appendx
            else:
                word_delimiter_error(src, errors, start, 15, "Append", "method_delim")
                return
        elif state == 17:     # "B"
            if c == "a":
                state = 18
            elif c == "l":
                state = 24
            else:
                break
        elif state == 18:     # "Ba"
            if c == "s":
                state = 19
            else:
                break
        elif state == 19:     # "Bas"
            if c == "k":
                state = 20
            else:
                break
        elif state == 20:     # "Bask"
            if c == "e":
                state = 21
            else:
                break
        elif state == 21:     # "Baske"
            if c == "t":
                state = 22
            else:
                break
        elif state == 22:     # "Basket"
            if c in DELIM["bask_delim"]:
                accept_word(src, tokens, start, path, 23, "Basket")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Basketx
            else:
                word_delimiter_error(src, errors, start, 22, "Basket", "bask_delim")
                return
        elif state == 24:     # "Bl"
            if c == "a":
                state = 25
            elif c == "e":
                state = 29
            else:
                break
        elif state == 25:     # "Bla"
            if c == "n":
                state = 26
            else:
                break
        elif state == 26:     # "Blan"
            if c == "d":
                state = 27
            else:
                break
        elif state == 27:     # "Bland"
            if c in DELIM["block_delim"]:
                accept_word(src, tokens, start, path, 28, "Bland")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Blandx
            else:
                word_delimiter_error(src, errors, start, 27, "Bland", "block_delim")
                return
        elif state == 29:     # "Ble"
            if c == "n":
                state = 30
            else:
                break
        elif state == 30:     # "Blen"
            if c == "d":
                state = 31
            else:
                break
        elif state == 31:     # "Blend"
            if c in DELIM["token_delim"]:
                accept_word(src, tokens, start, path, 32, "Blend")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Blendx
            else:
                word_delimiter_error(src, errors, start, 31, "Blend", "token_delim")
                return
        elif state == 33:     # "C"
            if c == "l":
                state = 34
            else:
                break
        elif state == 34:     # "Cl"
            if c == "e":
                state = 35
            else:
                break
        elif state == 35:     # "Cle"
            if c == "a":
                state = 36
            else:
                break
        elif state == 36:     # "Clea"
            if c == "r":
                state = 37
            else:
                break
        elif state == 37:     # "Clear"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 38, "Clear")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Clearx
            else:
                word_delimiter_error(src, errors, start, 37, "Clear", "method_delim")
                return
        elif state == 39:     # "F"
            if c == "a":
                state = 40
            else:
                break
        elif state == 40:     # "Fa"
            if c == "c":
                state = 41
            elif c == "l":
                state = 46
            else:
                break
        elif state == 41:     # "Fac"
            if c == "t":
                state = 42
            else:
                break
        elif state == 42:     # "Fact"
            if c == "o":
                state = 43
            else:
                break
        elif state == 43:     # "Facto"
            if c == "r":
                state = 44
            else:
                break
        elif state == 44:     # "Factor"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 45, "Factor")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Factorx
            else:
                word_delimiter_error(src, errors, start, 44, "Factor", "method_delim")
                return
        elif state == 46:     # "Fal"
            if c == "s":
                state = 47
            else:
                break
        elif state == 47:     # "Fals"
            if c == "e":
                state = 48
            else:
                break
        elif state == 48:     # "False"
            if c in DELIM["val_delim"]:
                accept_word(src, tokens, start, path, 49, "False")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Falsex
            else:
                word_delimiter_error(src, errors, start, 48, "False", "val_delim")
                return
        elif state == 50:     # "H"
            if c == "a":
                state = 51
            else:
                break
        elif state == 51:     # "Ha"
            if c == "r":
                state = 52
            else:
                break
        elif state == 52:     # "Har"
            if c == "v":
                state = 53
            else:
                break
        elif state == 53:     # "Harv"
            if c == "e":
                state = 54
            else:
                break
        elif state == 54:     # "Harve"
            if c == "s":
                state = 55
            else:
                break
        elif state == 55:     # "Harves"
            if c == "t":
                state = 56
            else:
                break
        elif state == 56:     # "Harvest"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 57, "Harvest")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Harvestx
            else:
                word_delimiter_error(src, errors, start, 56, "Harvest", "method_delim")
                return
        elif state == 58:     # "I"
            if c == "n":
                state = 59
            else:
                break
        elif state == 59:     # "In"
            if c == "s":
                state = 60
            else:
                break
        elif state == 60:     # "Ins"
            if c == "e":
                state = 61
            else:
                break
        elif state == 61:     # "Inse"
            if c == "r":
                state = 62
            else:
                break
        elif state == 62:     # "Inser"
            if c == "t":
                state = 63
            else:
                break
        elif state == 63:     # "Insert"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 64, "Insert")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Insertx
            else:
                word_delimiter_error(src, errors, start, 63, "Insert", "method_delim")
                return
        elif state == 65:     # "L"
            if c == "e":
                state = 66
            else:
                break
        elif state == 66:     # "Le"
            if c == "n":
                state = 67
            else:
                break
        elif state == 67:     # "Len"
            if c == "g":
                state = 68
            else:
                break
        elif state == 68:     # "Leng"
            if c == "t":
                state = 69
            else:
                break
        elif state == 69:     # "Lengt"
            if c == "h":
                state = 70
            else:
                break
        elif state == 70:     # "Length"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 71, "Length")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Lengthx
            else:
                word_delimiter_error(src, errors, start, 70, "Length", "method_delim")
                return
        elif state == 72:     # "M"
            if c == "i":
                state = 73
            else:
                break
        elif state == 73:     # "Mi"
            if c == "x":
                state = 74
            else:
                break
        elif state == 74:     # "Mix"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 75, "Mix")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Mixx
            else:
                word_delimiter_error(src, errors, start, 74, "Mix", "method_delim")
                return
        elif state == 76:     # "N"
            if c == "o":
                state = 77
            elif c == "u":
                state = 80
            else:
                break
        elif state == 77:     # "No"
            if c == "t":
                state = 78
            else:
                break
        elif state == 78:     # "Not"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 79, "Not")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Notx
            else:
                word_delimiter_error(src, errors, start, 78, "Not", "method_delim")
                return
        elif state == 80:     # "Nu"
            if c == "m":
                state = 81
            else:
                break
        elif state == 81:     # "Num"
            if c == "b":
                state = 82
            else:
                break
        elif state == 82:     # "Numb"
            if c == "e":
                state = 83
            else:
                break
        elif state == 83:     # "Numbe"
            if c == "r":
                state = 84
            else:
                break
        elif state == 84:     # "Number"
            if c in DELIM["type_delim"]:
                accept_word(src, tokens, start, path, 85, "Number")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Numberx
            else:
                word_delimiter_error(src, errors, start, 84, "Number", "type_delim")
                return
        elif state == 86:     # "O"
            if c == "r":
                state = 87
            else:
                break
        elif state == 87:     # "Or"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 88, "Or")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Orx
            else:
                word_delimiter_error(src, errors, start, 87, "Or", "method_delim")
                return
        elif state == 89:     # "P"
            if c == "o":
                state = 90
            elif c == "r":
                state = 94
            else:
                break
        elif state == 90:     # "Po"
            if c == "u":
                state = 91
            else:
                break
        elif state == 91:     # "Pou"
            if c == "r":
                state = 92
            else:
                break
        elif state == 92:     # "Pour"
            if c in DELIM["block_delim"]:
                accept_word(src, tokens, start, path, 93, "Pour")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Pourx
            else:
                word_delimiter_error(src, errors, start, 92, "Pour", "block_delim")
                return
        elif state == 94:     # "Pr"
            if c == "o":
                state = 95
            else:
                break
        elif state == 95:     # "Pro"
            if c == "d":
                state = 96
            else:
                break
        elif state == 96:     # "Prod"
            if c == "u":
                state = 97
            else:
                break
        elif state == 97:     # "Produ"
            if c == "c":
                state = 98
            else:
                break
        elif state == 98:     # "Produc"
            if c == "e":
                state = 99
            else:
                break
        elif state == 99:     # "Produce"
            if c in DELIM["prod_delim"]:
                accept_word(src, tokens, start, path, 100, "Produce")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Producex
            else:
                word_delimiter_error(src, errors, start, 99, "Produce", "prod_delim")
                return
        elif state == 101:    # "R"
            if c == "a":
                state = 102
            elif c == "e":
                state = 110
            else:
                break
        elif state == 102:    # "Ra"
            if c == "t":
                state = 103
            else:
                break
        elif state == 103:    # "Rat"
            if c == "i":
                state = 104
            else:
                break
        elif state == 104:    # "Rati"
            if c == "o":
                state = 105
            else:
                break
        elif state == 105:    # "Ratio"
            if c == "n":
                state = 106
            else:
                break
        elif state == 106:    # "Ration"
            if c == "a":
                state = 107
            else:
                break
        elif state == 107:    # "Rationa"
            if c == "l":
                state = 108
            else:
                break
        elif state == 108:    # "Rational"
            if c in DELIM["type_delim"]:
                accept_word(src, tokens, start, path, 109, "Rational")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Rationalx
            else:
                word_delimiter_error(src, errors, start, 108, "Rational", "type_delim")
                return
        elif state == 110:    # "Re"
            if c == "a":
                state = 111
            elif c == "c":
                state = 114
            elif c == "m":
                state = 119
            else:
                break
        elif state == 111:    # "Rea"
            if c == "p":
                state = 112
            else:
                break
        elif state == 112:    # "Reap"
            if c in DELIM["stmt_delim"]:
                accept_word(src, tokens, start, path, 113, "Reap")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Reapx
            else:
                word_delimiter_error(src, errors, start, 112, "Reap", "stmt_delim")
                return
        elif state == 114:    # "Rec"
            if c == "i":
                state = 115
            else:
                break
        elif state == 115:    # "Reci"
            if c == "p":
                state = 116
            else:
                break
        elif state == 116:    # "Recip"
            if c == "e":
                state = 117
            else:
                break
        elif state == 117:    # "Recipe"
            if c in DELIM["token_delim"]:
                accept_word(src, tokens, start, path, 118, "Recipe")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Recipex
            else:
                word_delimiter_error(src, errors, start, 117, "Recipe", "token_delim")
                return
        elif state == 119:    # "Rem"
            if c == "o":
                state = 120
            else:
                break
        elif state == 120:    # "Remo"
            if c == "v":
                state = 121
            else:
                break
        elif state == 121:    # "Remov"
            if c == "e":
                state = 122
            else:
                break
        elif state == 122:    # "Remove"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 123, "Remove")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Removex
            else:
                word_delimiter_error(src, errors, start, 122, "Remove", "method_delim")
                return
        elif state == 124:    # "S"
            if c == "a":
                state = 125
            elif c == "q":
                state = 129
            elif c == "t":
                state = 136
            else:
                break
        elif state == 125:    # "Sa"
            if c == "m":
                state = 126
            else:
                break
        elif state == 126:    # "Sam"
            if c == "e":
                state = 127
            else:
                break
        elif state == 127:    # "Same"
            if c in DELIM["token_delim"]:
                accept_word(src, tokens, start, path, 128, "Same")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Samex
            else:
                word_delimiter_error(src, errors, start, 127, "Same", "token_delim")
                return
        elif state == 129:    # "Sq"
            if c == "u":
                state = 130
            else:
                break
        elif state == 130:    # "Squ"
            if c == "e":
                state = 131
            else:
                break
        elif state == 131:    # "Sque"
            if c == "e":
                state = 132
            else:
                break
        elif state == 132:    # "Squee"
            if c == "z":
                state = 133
            else:
                break
        elif state == 133:    # "Squeez"
            if c == "e":
                state = 134
            else:
                break
        elif state == 134:    # "Squeeze"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 135, "Squeeze")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Squeezex
            else:
                word_delimiter_error(src, errors, start, 134, "Squeeze", "method_delim")
                return
        elif state == 136:    # "St"
            if c == "i":
                state = 137
            else:
                break
        elif state == 137:    # "Sti"
            if c == "r":
                state = 138
            else:
                break
        elif state == 138:    # "Stir"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 139, "Stir")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Stirx
            else:
                word_delimiter_error(src, errors, start, 138, "Stir", "method_delim")
                return
        elif state == 140:    # "T"
            if c == "a":
                state = 141
            elif c == "e":
                state = 146
            elif c == "o":
                state = 150
            elif c == "r":
                state = 178
            else:
                break
        elif state == 141:    # "Ta"
            if c == "s":
                state = 142
            else:
                break
        elif state == 142:    # "Tas"
            if c == "t":
                state = 143
            else:
                break
        elif state == 143:    # "Tast"
            if c == "e":
                state = 144
            else:
                break
        elif state == 144:    # "Taste"
            if c in DELIM["block_delim"]:
                accept_word(src, tokens, start, path, 145, "Taste")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Tastex
            else:
                word_delimiter_error(src, errors, start, 144, "Taste", "block_delim")
                return
        elif state == 146:    # "Te"
            if c == "s":
                state = 147
            else:
                break
        elif state == 147:    # "Tes"
            if c == "t":
                state = 148
            else:
                break
        elif state == 148:    # "Test"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 149, "Test")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Testx
            else:
                word_delimiter_error(src, errors, start, 148, "Test", "method_delim")
                return
        elif state == 150:    # "To"
            if c == "N":
                state = 151
            elif c == "R":
                state = 158
            elif c == "T":
                state = 167
            elif c == "W":
                state = 173
            else:
                break
        elif state == 151:    # "ToN"
            if c == "u":
                state = 152
            else:
                break
        elif state == 152:    # "ToNu"
            if c == "m":
                state = 153
            else:
                break
        elif state == 153:    # "ToNum"
            if c == "b":
                state = 154
            else:
                break
        elif state == 154:    # "ToNumb"
            if c == "e":
                state = 155
            else:
                break
        elif state == 155:    # "ToNumbe"
            if c == "r":
                state = 156
            else:
                break
        elif state == 156:    # "ToNumber"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 157, "ToNumber")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. ToNumberx
            else:
                word_delimiter_error(src, errors, start, 156, "ToNumber", "method_delim")
                return
        elif state == 158:    # "ToR"
            if c == "a":
                state = 159
            else:
                break
        elif state == 159:    # "ToRa"
            if c == "t":
                state = 160
            else:
                break
        elif state == 160:    # "ToRat"
            if c == "i":
                state = 161
            else:
                break
        elif state == 161:    # "ToRati"
            if c == "o":
                state = 162
            else:
                break
        elif state == 162:    # "ToRatio"
            if c == "n":
                state = 163
            else:
                break
        elif state == 163:    # "ToRation"
            if c == "a":
                state = 164
            else:
                break
        elif state == 164:    # "ToRationa"
            if c == "l":
                state = 165
            else:
                break
        elif state == 165:    # "ToRational"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 166, "ToRational")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. ToRationalx
            else:
                word_delimiter_error(src, errors, start, 165, "ToRational", "method_delim")
                return
        elif state == 167:    # "ToT"
            if c == "r":
                state = 168
            else:
                break
        elif state == 168:    # "ToTr"
            if c == "u":
                state = 169
            else:
                break
        elif state == 169:    # "ToTru"
            if c == "t":
                state = 170
            else:
                break
        elif state == 170:    # "ToTrut"
            if c == "h":
                state = 171
            else:
                break
        elif state == 171:    # "ToTruth"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 172, "ToTruth")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. ToTruthx
            else:
                word_delimiter_error(src, errors, start, 171, "ToTruth", "method_delim")
                return
        elif state == 173:    # "ToW"
            if c == "o":
                state = 174
            else:
                break
        elif state == 174:    # "ToWo"
            if c == "r":
                state = 175
            else:
                break
        elif state == 175:    # "ToWor"
            if c == "d":
                state = 176
            else:
                break
        elif state == 176:    # "ToWord"
            if c in DELIM["method_delim"]:
                accept_word(src, tokens, start, path, 177, "ToWord")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. ToWordx
            else:
                word_delimiter_error(src, errors, start, 176, "ToWord", "method_delim")
                return
        elif state == 178:    # "Tr"
            if c == "u":
                state = 179
            elif c == "y":
                state = 185
            else:
                break
        elif state == 179:    # "Tru"
            if c == "e":
                state = 180
            elif c == "t":
                state = 182
            else:
                break
        elif state == 180:    # "True"
            if c in DELIM["val_delim"]:
                accept_word(src, tokens, start, path, 181, "True")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Truex
            else:
                word_delimiter_error(src, errors, start, 180, "True", "val_delim")
                return
        elif state == 182:    # "Trut"
            if c == "h":
                state = 183
            else:
                break
        elif state == 183:    # "Truth"
            if c in DELIM["type_delim"]:
                accept_word(src, tokens, start, path, 184, "Truth")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Truthx
            else:
                word_delimiter_error(src, errors, start, 183, "Truth", "type_delim")
                return
        elif state == 185:    # "Try"
            if c in DELIM["token_delim"]:
                accept_word(src, tokens, start, path, 186, "Try")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Tryx
            else:
                word_delimiter_error(src, errors, start, 185, "Try", "token_delim")
                return
        elif state == 187:    # "U"
            if c == "n":
                state = 188
            elif c == "p":
                state = 194
            else:
                break
        elif state == 188:    # "Un"
            if c == "r":
                state = 189
            else:
                break
        elif state == 189:    # "Unr"
            if c == "i":
                state = 190
            else:
                break
        elif state == 190:    # "Unri"
            if c == "p":
                state = 191
            else:
                break
        elif state == 191:    # "Unrip"
            if c == "e":
                state = 192
            else:
                break
        elif state == 192:    # "Unripe"
            if c in DELIM["block_delim"]:
                accept_word(src, tokens, start, path, 193, "Unripe")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Unripex
            else:
                word_delimiter_error(src, errors, start, 192, "Unripe", "block_delim")
                return
        elif state == 194:    # "Up"
            if c == "r":
                state = 195
            else:
                break
        elif state == 195:    # "Upr"
            if c == "o":
                state = 196
            else:
                break
        elif state == 196:    # "Upro"
            if c == "o":
                state = 197
            else:
                break
        elif state == 197:    # "Uproo"
            if c == "t":
                state = 198
            else:
                break
        elif state == 198:    # "Uproot"
            if c in DELIM["stmt_delim"]:
                accept_word(src, tokens, start, path, 199, "Uproot")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Uprootx
            else:
                word_delimiter_error(src, errors, start, 198, "Uproot", "stmt_delim")
                return
        elif state == 200:    # "V"
            if c == "a":
                state = 201
            else:
                break
        elif state == 201:    # "Va"
            if c == "r":
                state = 202
            else:
                break
        elif state == 202:    # "Var"
            if c == "y":
                state = 203
            else:
                break
        elif state == 203:    # "Vary"
            if c in DELIM["token_delim"]:
                accept_word(src, tokens, start, path, 204, "Vary")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Varyx
            else:
                word_delimiter_error(src, errors, start, 203, "Vary", "token_delim")
                return
        elif state == 205:    # "W"
            if c == "o":
                state = 206
            else:
                break
        elif state == 206:    # "Wo"
            if c == "r":
                state = 207
            else:
                break
        elif state == 207:    # "Wor"
            if c == "d":
                state = 208
            else:
                break
        elif state == 208:    # "Word"
            if c in DELIM["type_delim"]:
                accept_word(src, tokens, start, path, 209, "Word")
                return
            elif c in id_chars:
                break                         # longer identifier, e.g. Wordx
            else:
                word_delimiter_error(src, errors, start, 208, "Word", "type_delim")
                return
        src.advance()
        path.append(state)

    # Not a reserved word: read the same characters again as an identifier.
    src.pos = start
    scan_identifier(src, tokens, errors)


def scan_identifier(src, tokens, errors):
    start = src.pos
    state = 0
    path = [0]
    while True:
        c = src.peek()
        if state == 0:                # start
            if c in letters:
                state = 275
            else:
                return
        elif state == 275:    # 1 character
            if c in id_chars:
                state = 277
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 276)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 275))
                return
        elif state == 277:    # 2 characters
            if c in id_chars:
                state = 279
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 278)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 277))
                return
        elif state == 279:    # 3 characters
            if c in id_chars:
                state = 281
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 280)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 279))
                return
        elif state == 281:    # 4 characters
            if c in id_chars:
                state = 283
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 282)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 281))
                return
        elif state == 283:    # 5 characters
            if c in id_chars:
                state = 285
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 284)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 283))
                return
        elif state == 285:    # 6 characters
            if c in id_chars:
                state = 287
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 286)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 285))
                return
        elif state == 287:    # 7 characters
            if c in id_chars:
                state = 289
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 288)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 287))
                return
        elif state == 289:    # 8 characters
            if c in id_chars:
                state = 291
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 290)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 289))
                return
        elif state == 291:    # 9 characters
            if c in id_chars:
                state = 293
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 292)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 291))
                return
        elif state == 293:    # 10 characters
            if c in id_chars:
                state = 295
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 294)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 293))
                return
        elif state == 295:    # 11 characters
            if c in id_chars:
                state = 297
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 296)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 295))
                return
        elif state == 297:    # 12 characters
            if c in id_chars:
                state = 299
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 298)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 297))
                return
        elif state == 299:    # 13 characters
            if c in id_chars:
                state = 301
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 300)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 299))
                return
        elif state == 301:    # 14 characters
            if c in id_chars:
                state = 303
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 302)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 301))
                return
        elif state == 303:    # 15 characters
            if c in id_chars:
                state = 305
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 304)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 303))
                return
        elif state == 305:    # 16 characters
            if c in id_chars:
                state = 307
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 306)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 305))
                return
        elif state == 307:    # 17 characters
            if c in id_chars:
                state = 309
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 308)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 307))
                return
        elif state == 309:    # 18 characters
            if c in id_chars:
                state = 311
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 310)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 309))
                return
        elif state == 311:    # 19 characters
            if c in id_chars:
                state = 313
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 312)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 311))
                return
        elif state == 313:    # 20 characters
            if c in id_chars:
                state = 315
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 314)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 313))
                return
        elif state == 315:    # 21 characters
            if c in id_chars:
                state = 317
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 316)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 315))
                return
        elif state == 317:    # 22 characters
            if c in id_chars:
                state = 319
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 318)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 317))
                return
        elif state == 319:    # 23 characters
            if c in id_chars:
                state = 321
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 320)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 319))
                return
        elif state == 321:    # 24 characters
            if c in id_chars:
                state = 323
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 322)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 321))
                return
        elif state == 323:    # 25 characters
            if c in id_chars:
                state = 325
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 324)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 323))
                return
        elif state == 325:    # 26 characters
            if c in id_chars:
                state = 327
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 326)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 325))
                return
        elif state == 327:    # 27 characters
            if c in id_chars:
                state = 329
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 328)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 327))
                return
        elif state == 329:    # 28 characters
            if c in id_chars:
                state = 331
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 330)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 329))
                return
        elif state == 331:    # 29 characters
            if c in id_chars:
                state = 333
            elif c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 332)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 331))
                return
        elif state == 333:    # 30 characters
            if c in DELIM["id_delim"]:
                accept_id(src, tokens, start, path, 334)
                return
            elif c in id_chars:
                # 31st character: no arrow leaves 333.  Report the 30 characters
                # read so far; the 31st is scanned again from state 0.
                errors.append(E.identifier_too_long(src, start, src.slice(start)))
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "id_delim", 333))
                return
        src.advance()
        path.append(state)


def scan_underscore(src, tokens, errors):
    """No arrow leaves state 0 on '_': report the '_' alone and go back to
    state 0 at the next character (e.g. _name -> error on _, then name)."""
    start = src.pos
    src.advance()
    errors.append(E.underscore_start(src, start, src.slice(start)))
