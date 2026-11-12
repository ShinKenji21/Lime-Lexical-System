"""
scan_words.py - reserved words (TD A, states 0-205) and identifiers
(TD C, states 271-330), written as one if / elif branch per state.

Reserved words: every state checks the current character against the arrows
that leave it.  If no arrow matches before the word is fully spelled, or the
word is spelled but a letter/digit/_ follows (Tester, Varying, Orange), the
same characters are read again with the identifier diagram (Identifiers
Rule 6).
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
                state = 97
            elif c == "S":
                state = 120
            elif c == "T":
                state = 136
            elif c == "U":
                state = 183
            elif c == "V":
                state = 196
            elif c == "W":
                state = 201
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
            if c in DELIM["delim_func"]:
                accept_word(src, tokens, start, path, 7, "Absorb")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Absorbx
            else:
                word_delimiter_error(src, errors, start, 6, "Absorb", "delim_func")
                return
        elif state == 8:      # "An"
            if c == "d":
                state = 9
            else:
                break
        elif state == 9:      # "And"
            if c in DELIM["delim_ctrl"]:
                accept_word(src, tokens, start, path, 10, "And")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Andx
            else:
                word_delimiter_error(src, errors, start, 9, "And", "delim_ctrl")
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
            if c in DELIM["delim_func"]:
                accept_word(src, tokens, start, path, 16, "Append")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Appendx
            else:
                word_delimiter_error(src, errors, start, 15, "Append", "delim_func")
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
            if c in DELIM["delim_bask"]:
                accept_word(src, tokens, start, path, 23, "Basket")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Basketx
            else:
                word_delimiter_error(src, errors, start, 22, "Basket", "delim_bask")
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
            if c in DELIM["delim_blan"]:
                accept_word(src, tokens, start, path, 28, "Bland")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Blandx
            else:
                word_delimiter_error(src, errors, start, 27, "Bland", "delim_blan")
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
            if c in DELIM["delim_decl"]:
                accept_word(src, tokens, start, path, 32, "Blend")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Blendx
            else:
                word_delimiter_error(src, errors, start, 31, "Blend", "delim_decl")
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
            if c in DELIM["delim_func"]:
                accept_word(src, tokens, start, path, 38, "Clear")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Clearx
            else:
                word_delimiter_error(src, errors, start, 37, "Clear", "delim_func")
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
            if c in DELIM["delim_ctrl"]:
                accept_word(src, tokens, start, path, 45, "Factor")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Factorx
            else:
                word_delimiter_error(src, errors, start, 44, "Factor", "delim_ctrl")
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
            if c in DELIM["delim_bool"]:
                accept_word(src, tokens, start, path, 49, "False")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Falsex
            else:
                word_delimiter_error(src, errors, start, 48, "False", "delim_bool")
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
            if c in DELIM["delim_ctrl"]:
                accept_word(src, tokens, start, path, 57, "Harvest")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Harvestx
            else:
                word_delimiter_error(src, errors, start, 56, "Harvest", "delim_ctrl")
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
            if c in DELIM["delim_func"]:
                accept_word(src, tokens, start, path, 64, "Insert")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Insertx
            else:
                word_delimiter_error(src, errors, start, 63, "Insert", "delim_func")
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
            if c in DELIM["delim_func"]:
                accept_word(src, tokens, start, path, 71, "Length")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Lengthx
            else:
                word_delimiter_error(src, errors, start, 70, "Length", "delim_func")
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
            if c in DELIM["delim_ctrl"]:
                accept_word(src, tokens, start, path, 75, "Mix")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Mixx
            else:
                word_delimiter_error(src, errors, start, 74, "Mix", "delim_ctrl")
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
            if c in DELIM["delim_ctrl"]:
                accept_word(src, tokens, start, path, 79, "Not")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Notx
            else:
                word_delimiter_error(src, errors, start, 78, "Not", "delim_ctrl")
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
            if c in DELIM["delim_type"]:
                accept_word(src, tokens, start, path, 85, "Number")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Numberx
            else:
                word_delimiter_error(src, errors, start, 84, "Number", "delim_type")
                return
        elif state == 86:     # "O"
            if c == "r":
                state = 87
            else:
                break
        elif state == 87:     # "Or"
            if c in DELIM["delim_ctrl"]:
                accept_word(src, tokens, start, path, 88, "Or")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Orx
            else:
                word_delimiter_error(src, errors, start, 87, "Or", "delim_ctrl")
                return
        elif state == 89:     # "P"
            if c == "r":
                state = 90
            else:
                break
        elif state == 90:     # "Pr"
            if c == "o":
                state = 91
            else:
                break
        elif state == 91:     # "Pro"
            if c == "d":
                state = 92
            else:
                break
        elif state == 92:     # "Prod"
            if c == "u":
                state = 93
            else:
                break
        elif state == 93:     # "Produ"
            if c == "c":
                state = 94
            else:
                break
        elif state == 94:     # "Produc"
            if c == "e":
                state = 95
            else:
                break
        elif state == 95:     # "Produce"
            if c in DELIM["delim_prod"]:
                accept_word(src, tokens, start, path, 96, "Produce")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Producex
            else:
                word_delimiter_error(src, errors, start, 95, "Produce", "delim_prod")
                return
        elif state == 97:     # "R"
            if c == "a":
                state = 98
            elif c == "e":
                state = 106
            else:
                break
        elif state == 98:     # "Ra"
            if c == "t":
                state = 99
            else:
                break
        elif state == 99:     # "Rat"
            if c == "i":
                state = 100
            else:
                break
        elif state == 100:    # "Rati"
            if c == "o":
                state = 101
            else:
                break
        elif state == 101:    # "Ratio"
            if c == "n":
                state = 102
            else:
                break
        elif state == 102:    # "Ration"
            if c == "a":
                state = 103
            else:
                break
        elif state == 103:    # "Rationa"
            if c == "l":
                state = 104
            else:
                break
        elif state == 104:    # "Rational"
            if c in DELIM["delim_type"]:
                accept_word(src, tokens, start, path, 105, "Rational")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Rationalx
            else:
                word_delimiter_error(src, errors, start, 104, "Rational", "delim_type")
                return
        elif state == 106:    # "Re"
            if c == "a":
                state = 107
            elif c == "c":
                state = 110
            elif c == "m":
                state = 115
            else:
                break
        elif state == 107:    # "Rea"
            if c == "p":
                state = 108
            else:
                break
        elif state == 108:    # "Reap"
            if c in DELIM["delim_reup"]:
                accept_word(src, tokens, start, path, 109, "Reap")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Reapx
            else:
                word_delimiter_error(src, errors, start, 108, "Reap", "delim_reup")
                return
        elif state == 110:    # "Rec"
            if c == "i":
                state = 111
            else:
                break
        elif state == 111:    # "Reci"
            if c == "p":
                state = 112
            else:
                break
        elif state == 112:    # "Recip"
            if c == "e":
                state = 113
            else:
                break
        elif state == 113:    # "Recipe"
            if c in DELIM["delim_decl"]:
                accept_word(src, tokens, start, path, 114, "Recipe")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Recipex
            else:
                word_delimiter_error(src, errors, start, 113, "Recipe", "delim_decl")
                return
        elif state == 115:    # "Rem"
            if c == "o":
                state = 116
            else:
                break
        elif state == 116:    # "Remo"
            if c == "v":
                state = 117
            else:
                break
        elif state == 117:    # "Remov"
            if c == "e":
                state = 118
            else:
                break
        elif state == 118:    # "Remove"
            if c in DELIM["delim_func"]:
                accept_word(src, tokens, start, path, 119, "Remove")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Removex
            else:
                word_delimiter_error(src, errors, start, 118, "Remove", "delim_func")
                return
        elif state == 120:    # "S"
            if c == "a":
                state = 121
            elif c == "q":
                state = 125
            elif c == "t":
                state = 132
            else:
                break
        elif state == 121:    # "Sa"
            if c == "m":
                state = 122
            else:
                break
        elif state == 122:    # "Sam"
            if c == "e":
                state = 123
            else:
                break
        elif state == 123:    # "Same"
            if c in DELIM["delim_decl"]:
                accept_word(src, tokens, start, path, 124, "Same")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Samex
            else:
                word_delimiter_error(src, errors, start, 123, "Same", "delim_decl")
                return
        elif state == 125:    # "Sq"
            if c == "u":
                state = 126
            else:
                break
        elif state == 126:    # "Squ"
            if c == "e":
                state = 127
            else:
                break
        elif state == 127:    # "Sque"
            if c == "e":
                state = 128
            else:
                break
        elif state == 128:    # "Squee"
            if c == "z":
                state = 129
            else:
                break
        elif state == 129:    # "Squeez"
            if c == "e":
                state = 130
            else:
                break
        elif state == 130:    # "Squeeze"
            if c in DELIM["delim_func"]:
                accept_word(src, tokens, start, path, 131, "Squeeze")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Squeezex
            else:
                word_delimiter_error(src, errors, start, 130, "Squeeze", "delim_func")
                return
        elif state == 132:    # "St"
            if c == "i":
                state = 133
            else:
                break
        elif state == 133:    # "Sti"
            if c == "r":
                state = 134
            else:
                break
        elif state == 134:    # "Stir"
            if c in DELIM["delim_ctrl"]:
                accept_word(src, tokens, start, path, 135, "Stir")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Stirx
            else:
                word_delimiter_error(src, errors, start, 134, "Stir", "delim_ctrl")
                return
        elif state == 136:    # "T"
            if c == "a":
                state = 137
            elif c == "e":
                state = 142
            elif c == "o":
                state = 146
            elif c == "r":
                state = 174
            else:
                break
        elif state == 137:    # "Ta"
            if c == "s":
                state = 138
            else:
                break
        elif state == 138:    # "Tas"
            if c == "t":
                state = 139
            else:
                break
        elif state == 139:    # "Tast"
            if c == "e":
                state = 140
            else:
                break
        elif state == 140:    # "Taste"
            if c in DELIM["delim_taun"]:
                accept_word(src, tokens, start, path, 141, "Taste")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Tastex
            else:
                word_delimiter_error(src, errors, start, 140, "Taste", "delim_taun")
                return
        elif state == 142:    # "Te"
            if c == "s":
                state = 143
            else:
                break
        elif state == 143:    # "Tes"
            if c == "t":
                state = 144
            else:
                break
        elif state == 144:    # "Test"
            if c in DELIM["delim_ctrl"]:
                accept_word(src, tokens, start, path, 145, "Test")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Testx
            else:
                word_delimiter_error(src, errors, start, 144, "Test", "delim_ctrl")
                return
        elif state == 146:    # "To"
            if c == "N":
                state = 147
            elif c == "R":
                state = 154
            elif c == "T":
                state = 163
            elif c == "W":
                state = 169
            else:
                break
        elif state == 147:    # "ToN"
            if c == "u":
                state = 148
            else:
                break
        elif state == 148:    # "ToNu"
            if c == "m":
                state = 149
            else:
                break
        elif state == 149:    # "ToNum"
            if c == "b":
                state = 150
            else:
                break
        elif state == 150:    # "ToNumb"
            if c == "e":
                state = 151
            else:
                break
        elif state == 151:    # "ToNumbe"
            if c == "r":
                state = 152
            else:
                break
        elif state == 152:    # "ToNumber"
            if c in DELIM["delim_func"]:
                accept_word(src, tokens, start, path, 153, "ToNumber")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. ToNumberx
            else:
                word_delimiter_error(src, errors, start, 152, "ToNumber", "delim_func")
                return
        elif state == 154:    # "ToR"
            if c == "a":
                state = 155
            else:
                break
        elif state == 155:    # "ToRa"
            if c == "t":
                state = 156
            else:
                break
        elif state == 156:    # "ToRat"
            if c == "i":
                state = 157
            else:
                break
        elif state == 157:    # "ToRati"
            if c == "o":
                state = 158
            else:
                break
        elif state == 158:    # "ToRatio"
            if c == "n":
                state = 159
            else:
                break
        elif state == 159:    # "ToRation"
            if c == "a":
                state = 160
            else:
                break
        elif state == 160:    # "ToRationa"
            if c == "l":
                state = 161
            else:
                break
        elif state == 161:    # "ToRational"
            if c in DELIM["delim_func"]:
                accept_word(src, tokens, start, path, 162, "ToRational")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. ToRationalx
            else:
                word_delimiter_error(src, errors, start, 161, "ToRational", "delim_func")
                return
        elif state == 163:    # "ToT"
            if c == "r":
                state = 164
            else:
                break
        elif state == 164:    # "ToTr"
            if c == "u":
                state = 165
            else:
                break
        elif state == 165:    # "ToTru"
            if c == "t":
                state = 166
            else:
                break
        elif state == 166:    # "ToTrut"
            if c == "h":
                state = 167
            else:
                break
        elif state == 167:    # "ToTruth"
            if c in DELIM["delim_func"]:
                accept_word(src, tokens, start, path, 168, "ToTruth")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. ToTruthx
            else:
                word_delimiter_error(src, errors, start, 167, "ToTruth", "delim_func")
                return
        elif state == 169:    # "ToW"
            if c == "o":
                state = 170
            else:
                break
        elif state == 170:    # "ToWo"
            if c == "r":
                state = 171
            else:
                break
        elif state == 171:    # "ToWor"
            if c == "d":
                state = 172
            else:
                break
        elif state == 172:    # "ToWord"
            if c in DELIM["delim_func"]:
                accept_word(src, tokens, start, path, 173, "ToWord")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. ToWordx
            else:
                word_delimiter_error(src, errors, start, 172, "ToWord", "delim_func")
                return
        elif state == 174:    # "Tr"
            if c == "u":
                state = 175
            elif c == "y":
                state = 181
            else:
                break
        elif state == 175:    # "Tru"
            if c == "e":
                state = 176
            elif c == "t":
                state = 178
            else:
                break
        elif state == 176:    # "True"
            if c in DELIM["delim_bool"]:
                accept_word(src, tokens, start, path, 177, "True")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Truex
            else:
                word_delimiter_error(src, errors, start, 176, "True", "delim_bool")
                return
        elif state == 178:    # "Trut"
            if c == "h":
                state = 179
            else:
                break
        elif state == 179:    # "Truth"
            if c in DELIM["delim_type"]:
                accept_word(src, tokens, start, path, 180, "Truth")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Truthx
            else:
                word_delimiter_error(src, errors, start, 179, "Truth", "delim_type")
                return
        elif state == 181:    # "Try"
            if c in DELIM["delim_ctrl"]:
                accept_word(src, tokens, start, path, 182, "Try")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Tryx
            else:
                word_delimiter_error(src, errors, start, 181, "Try", "delim_ctrl")
                return
        elif state == 183:    # "U"
            if c == "n":
                state = 184
            elif c == "p":
                state = 190
            else:
                break
        elif state == 184:    # "Un"
            if c == "r":
                state = 185
            else:
                break
        elif state == 185:    # "Unr"
            if c == "i":
                state = 186
            else:
                break
        elif state == 186:    # "Unri"
            if c == "p":
                state = 187
            else:
                break
        elif state == 187:    # "Unrip"
            if c == "e":
                state = 188
            else:
                break
        elif state == 188:    # "Unripe"
            if c in DELIM["delim_taun"]:
                accept_word(src, tokens, start, path, 189, "Unripe")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Unripex
            else:
                word_delimiter_error(src, errors, start, 188, "Unripe", "delim_taun")
                return
        elif state == 190:    # "Up"
            if c == "r":
                state = 191
            else:
                break
        elif state == 191:    # "Upr"
            if c == "o":
                state = 192
            else:
                break
        elif state == 192:    # "Upro"
            if c == "o":
                state = 193
            else:
                break
        elif state == 193:    # "Uproo"
            if c == "t":
                state = 194
            else:
                break
        elif state == 194:    # "Uproot"
            if c in DELIM["delim_reup"]:
                accept_word(src, tokens, start, path, 195, "Uproot")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Uprootx
            else:
                word_delimiter_error(src, errors, start, 194, "Uproot", "delim_reup")
                return
        elif state == 196:    # "V"
            if c == "a":
                state = 197
            else:
                break
        elif state == 197:    # "Va"
            if c == "r":
                state = 198
            else:
                break
        elif state == 198:    # "Var"
            if c == "y":
                state = 199
            else:
                break
        elif state == 199:    # "Vary"
            if c in DELIM["delim_decl"]:
                accept_word(src, tokens, start, path, 200, "Vary")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Varyx
            else:
                word_delimiter_error(src, errors, start, 199, "Vary", "delim_decl")
                return
        elif state == 201:    # "W"
            if c == "o":
                state = 202
            else:
                break
        elif state == 202:    # "Wo"
            if c == "r":
                state = 203
            else:
                break
        elif state == 203:    # "Wor"
            if c == "d":
                state = 204
            else:
                break
        elif state == 204:    # "Word"
            if c in DELIM["delim_type"]:
                accept_word(src, tokens, start, path, 205, "Word")
                return
            elif c in id_chars:
                break                      # longer identifier, e.g. Wordx
            else:
                word_delimiter_error(src, errors, start, 204, "Word", "delim_type")
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
        if state == 0:
            if c in letters:
                state = 271
            else:
                return
        elif state == 271:                         # 1 character
            if c in id_chars:
                state = 273
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 272)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 271))
                return
        elif state == 273:                         # 2 characters
            if c in id_chars:
                state = 275
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 274)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 273))
                return
        elif state == 275:                         # 3 characters
            if c in id_chars:
                state = 277
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 276)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 275))
                return
        elif state == 277:                         # 4 characters
            if c in id_chars:
                state = 279
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 278)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 277))
                return
        elif state == 279:                         # 5 characters
            if c in id_chars:
                state = 281
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 280)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 279))
                return
        elif state == 281:                         # 6 characters
            if c in id_chars:
                state = 283
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 282)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 281))
                return
        elif state == 283:                         # 7 characters
            if c in id_chars:
                state = 285
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 284)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 283))
                return
        elif state == 285:                         # 8 characters
            if c in id_chars:
                state = 287
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 286)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 285))
                return
        elif state == 287:                         # 9 characters
            if c in id_chars:
                state = 289
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 288)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 287))
                return
        elif state == 289:                         # 10 characters
            if c in id_chars:
                state = 291
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 290)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 289))
                return
        elif state == 291:                         # 11 characters
            if c in id_chars:
                state = 293
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 292)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 291))
                return
        elif state == 293:                         # 12 characters
            if c in id_chars:
                state = 295
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 294)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 293))
                return
        elif state == 295:                         # 13 characters
            if c in id_chars:
                state = 297
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 296)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 295))
                return
        elif state == 297:                         # 14 characters
            if c in id_chars:
                state = 299
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 298)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 297))
                return
        elif state == 299:                         # 15 characters
            if c in id_chars:
                state = 301
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 300)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 299))
                return
        elif state == 301:                         # 16 characters
            if c in id_chars:
                state = 303
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 302)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 301))
                return
        elif state == 303:                         # 17 characters
            if c in id_chars:
                state = 305
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 304)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 303))
                return
        elif state == 305:                         # 18 characters
            if c in id_chars:
                state = 307
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 306)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 305))
                return
        elif state == 307:                         # 19 characters
            if c in id_chars:
                state = 309
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 308)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 307))
                return
        elif state == 309:                         # 20 characters
            if c in id_chars:
                state = 311
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 310)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 309))
                return
        elif state == 311:                         # 21 characters
            if c in id_chars:
                state = 313
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 312)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 311))
                return
        elif state == 313:                         # 22 characters
            if c in id_chars:
                state = 315
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 314)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 313))
                return
        elif state == 315:                         # 23 characters
            if c in id_chars:
                state = 317
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 316)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 315))
                return
        elif state == 317:                         # 24 characters
            if c in id_chars:
                state = 319
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 318)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 317))
                return
        elif state == 319:                         # 25 characters
            if c in id_chars:
                state = 321
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 320)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 319))
                return
        elif state == 321:                         # 26 characters
            if c in id_chars:
                state = 323
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 322)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 321))
                return
        elif state == 323:                         # 27 characters
            if c in id_chars:
                state = 325
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 324)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 323))
                return
        elif state == 325:                         # 28 characters
            if c in id_chars:
                state = 327
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 326)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 325))
                return
        elif state == 327:                         # 29 characters
            if c in id_chars:
                state = 329
            elif c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 328)
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 327))
                return
        elif state == 329:                         # 30 characters
            if c in DELIM["delim_id"]:
                accept_id(src, tokens, start, path, 330)
                return
            elif c in id_chars:
                # 31st character: no arrow leaves 329.  Report the 30 characters
                # read so far; the 31st is scanned again from state 0.
                errors.append(E.identifier_too_long(src, start, src.slice(start)))
                return
            else:
                errors.append(E.invalid_delimiter(src, start, src.pos, "Identifier",
                                                  src.slice(start), "delim_id", 329))
                return
        src.advance()
        path.append(state)


def scan_underscore(src, tokens, errors):
    """No arrow leaves state 0 on '_': report the '_' alone and go back to
    state 0 at the next character (e.g. _name -> error on _, then name)."""
    start = src.pos
    src.advance()
    errors.append(E.underscore_start(src, start, src.slice(start)))
