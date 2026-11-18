"""
scan_numbers.py - int_lit and flo_lit (TD D, states 335-385), including a
negative literal written as ~ directly followed by a digit
(TD B: 253 --zero--> 335, 253 --nonzero--> 337), written as one if / elif
branch per state.

Whole part : 335 (zero) or 337, 339, ..., 371 (1st to 18th digit)
             final state = state + 1 on val_delim
Period     : --period--> 373
Fraction   : 374, 376, ..., 384 (1st to 6th digit)
             final state = state + 1 on val_delim

The lexer only counts digits; whether the value fits in Number is not checked
here.
"""

from .definitions import DELIM, zero, nonzero, numbers
from .emit import accept_literal, number_delimiter_error
from .tokens import INT_LIT, FLO_LIT
from . import errors as E


def scan_number(src, tokens, errors):
    start = src.pos
    state = 0
    path = [0]
    while True:
        c = src.peek()
        if state == 0:                # start
            if c == "~":
                state = 253
            elif c in zero:
                state = 335
            elif c in nonzero:
                state = 337
            else:
                return
        elif state == 253:            # ~
            if c in zero:
                state = 335
            elif c in nonzero:
                state = 337
            else:
                return
        elif state == 335:            # 0
            if c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 336, INT_LIT)
                return
            elif c in numbers:
                # no arrow on a digit after 0 (no leading zeros).  Report the
                # 0; the next digit is scanned again from state 0.
                errors.append(E.leading_zero(src, start, src.slice(start)))
                return
            else:
                number_delimiter_error(src, errors, start, 335, "Number literal", "val_delim")
                return
        elif state == 337:    # 1 digit
            if c in numbers:
                state = 339
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 338, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 337, "Number literal", "val_delim")
                return
        elif state == 339:    # 2 digits
            if c in numbers:
                state = 341
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 340, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 339, "Number literal", "val_delim")
                return
        elif state == 341:    # 3 digits
            if c in numbers:
                state = 343
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 342, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 341, "Number literal", "val_delim")
                return
        elif state == 343:    # 4 digits
            if c in numbers:
                state = 345
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 344, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 343, "Number literal", "val_delim")
                return
        elif state == 345:    # 5 digits
            if c in numbers:
                state = 347
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 346, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 345, "Number literal", "val_delim")
                return
        elif state == 347:    # 6 digits
            if c in numbers:
                state = 349
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 348, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 347, "Number literal", "val_delim")
                return
        elif state == 349:    # 7 digits
            if c in numbers:
                state = 351
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 350, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 349, "Number literal", "val_delim")
                return
        elif state == 351:    # 8 digits
            if c in numbers:
                state = 353
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 352, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 351, "Number literal", "val_delim")
                return
        elif state == 353:    # 9 digits
            if c in numbers:
                state = 355
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 354, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 353, "Number literal", "val_delim")
                return
        elif state == 355:    # 10 digits
            if c in numbers:
                state = 357
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 356, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 355, "Number literal", "val_delim")
                return
        elif state == 357:    # 11 digits
            if c in numbers:
                state = 359
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 358, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 357, "Number literal", "val_delim")
                return
        elif state == 359:    # 12 digits
            if c in numbers:
                state = 361
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 360, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 359, "Number literal", "val_delim")
                return
        elif state == 361:    # 13 digits
            if c in numbers:
                state = 363
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 362, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 361, "Number literal", "val_delim")
                return
        elif state == 363:    # 14 digits
            if c in numbers:
                state = 365
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 364, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 363, "Number literal", "val_delim")
                return
        elif state == 365:    # 15 digits
            if c in numbers:
                state = 367
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 366, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 365, "Number literal", "val_delim")
                return
        elif state == 367:    # 16 digits
            if c in numbers:
                state = 369
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 368, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 367, "Number literal", "val_delim")
                return
        elif state == 369:    # 17 digits
            if c in numbers:
                state = 371
            elif c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 370, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 369, "Number literal", "val_delim")
                return
        elif state == 371:    # 18 digits
            if c == ".":
                state = 373
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 372, INT_LIT)
                return
            elif c in numbers:
                # 19th digit: no arrow leaves 371 on a digit.  Report the 18
                # digits read so far; the 19th is scanned again from state 0.
                errors.append(E.too_many_int_digits(src, start, src.slice(start)))
                return
            else:
                number_delimiter_error(src, errors, start, 371, "Number literal", "val_delim")
                return
        elif state == 373:    # period
            if c in numbers:
                state = 374
            else:
                errors.append(E.missing_fraction(src, start, src.pos, src.slice(start)))
                return
        elif state == 374:    # 1 fractional digit
            if c in numbers:
                state = 376
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 375, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 374, "Rational literal", "val_delim")
                return
        elif state == 376:    # 2 fractional digits
            if c in numbers:
                state = 378
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 377, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 376, "Rational literal", "val_delim")
                return
        elif state == 378:    # 3 fractional digits
            if c in numbers:
                state = 380
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 379, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 378, "Rational literal", "val_delim")
                return
        elif state == 380:    # 4 fractional digits
            if c in numbers:
                state = 382
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 381, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 380, "Rational literal", "val_delim")
                return
        elif state == 382:    # 5 fractional digits
            if c in numbers:
                state = 384
            elif c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 383, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 382, "Rational literal", "val_delim")
                return
        elif state == 384:    # 6 fractional digits
            if c in DELIM["val_delim"]:
                accept_literal(src, tokens, start, path, 385, FLO_LIT)
                return
            elif c in numbers:
                # 7th fractional digit: no arrow leaves 384.  Report what was
                # read so far; the extra digit is scanned again from state 0.
                errors.append(E.too_many_frac_digits(src, start, src.slice(start)))
                return
            else:
                number_delimiter_error(src, errors, start, 384, "Rational literal", "val_delim")
                return
        src.advance()
        path.append(state)
