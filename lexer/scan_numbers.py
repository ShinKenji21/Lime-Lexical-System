"""
scan_numbers.py - int_lit and flo_lit (TD C, states 331-405), including a
negative literal written as ~ directly followed by a digit
(TD B: 220 --zero--> 331, 220 --nonzero--> 333), written as one if / elif
branch per state.

Whole part : 331 (zero) or 333, 335, ..., 369 (1st to 19th digit)
             final state = state + 1 on delim_int
Period     : --period--> 371
Fraction   : 372, 374, ..., 404 (1st to 17th digit)
             final state = state + 1 on delim_flo

The lexer only counts digits; whether the value fits in Number is not checked
here.
"""

from .definitions import DELIM, zero, nonzero, numbers, id_chars
from .emit import accept_literal, absorb, number_delimiter_error
from .tokens import INT_LIT, FLO_LIT
from . import errors as E


def scan_number(src, tokens, errors):
    start = src.pos
    state = 0
    path = [0]
    while True:
        c = src.peek()
        if state == 0:                          # start
            if c == "~":
                state = 220
            elif c in zero:
                state = 331
            elif c in nonzero:
                state = 333
            else:
                return
        elif state == 220:                      # ~
            if c in zero:
                state = 331
            elif c in nonzero:
                state = 333
            else:
                return
        elif state == 331:                      # 0
            if c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 332, INT_LIT)
                return
            elif c in numbers:
                # no arrow on a digit after 0 (no leading zeros)
                absorb(src, numbers | id_chars)
                errors.append(E.leading_zero(src, start, src.slice(start)))
                return
            else:
                number_delimiter_error(src, errors, start, 331, "Number literal", "delim_int")
                return
        elif state == 333:                      # 1 digit
            if c in numbers:
                state = 335
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 334, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 333, "Number literal", "delim_int")
                return
        elif state == 335:                      # 2 digits
            if c in numbers:
                state = 337
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 336, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 335, "Number literal", "delim_int")
                return
        elif state == 337:                      # 3 digits
            if c in numbers:
                state = 339
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 338, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 337, "Number literal", "delim_int")
                return
        elif state == 339:                      # 4 digits
            if c in numbers:
                state = 341
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 340, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 339, "Number literal", "delim_int")
                return
        elif state == 341:                      # 5 digits
            if c in numbers:
                state = 343
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 342, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 341, "Number literal", "delim_int")
                return
        elif state == 343:                      # 6 digits
            if c in numbers:
                state = 345
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 344, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 343, "Number literal", "delim_int")
                return
        elif state == 345:                      # 7 digits
            if c in numbers:
                state = 347
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 346, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 345, "Number literal", "delim_int")
                return
        elif state == 347:                      # 8 digits
            if c in numbers:
                state = 349
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 348, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 347, "Number literal", "delim_int")
                return
        elif state == 349:                      # 9 digits
            if c in numbers:
                state = 351
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 350, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 349, "Number literal", "delim_int")
                return
        elif state == 351:                      # 10 digits
            if c in numbers:
                state = 353
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 352, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 351, "Number literal", "delim_int")
                return
        elif state == 353:                      # 11 digits
            if c in numbers:
                state = 355
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 354, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 353, "Number literal", "delim_int")
                return
        elif state == 355:                      # 12 digits
            if c in numbers:
                state = 357
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 356, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 355, "Number literal", "delim_int")
                return
        elif state == 357:                      # 13 digits
            if c in numbers:
                state = 359
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 358, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 357, "Number literal", "delim_int")
                return
        elif state == 359:                      # 14 digits
            if c in numbers:
                state = 361
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 360, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 359, "Number literal", "delim_int")
                return
        elif state == 361:                      # 15 digits
            if c in numbers:
                state = 363
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 362, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 361, "Number literal", "delim_int")
                return
        elif state == 363:                      # 16 digits
            if c in numbers:
                state = 365
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 364, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 363, "Number literal", "delim_int")
                return
        elif state == 365:                      # 17 digits
            if c in numbers:
                state = 367
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 366, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 365, "Number literal", "delim_int")
                return
        elif state == 367:                      # 18 digits
            if c in numbers:
                state = 369
            elif c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 368, INT_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 367, "Number literal", "delim_int")
                return
        elif state == 369:                      # 19 digits
            if c == ".":
                state = 371
            elif c in DELIM["delim_int"]:
                accept_literal(src, tokens, start, path, 370, INT_LIT)
                return
            elif c in numbers:
                # 20th digit: no arrow leaves 369 on a digit.
                absorb(src, numbers | {"."})
                errors.append(E.too_many_int_digits(src, start, src.slice(start)))
                return
            else:
                number_delimiter_error(src, errors, start, 369, "Number literal", "delim_int")
                return
        elif state == 371:                      # period
            if c in numbers:
                state = 372
            else:
                errors.append(E.missing_fraction(src, start, src.pos, src.slice(start)))
                return
        elif state == 372:                      # 1 fractional digit
            if c in numbers:
                state = 374
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 373, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 372, "Rational literal", "delim_flo")
                return
        elif state == 374:                      # 2 fractional digits
            if c in numbers:
                state = 376
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 375, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 374, "Rational literal", "delim_flo")
                return
        elif state == 376:                      # 3 fractional digits
            if c in numbers:
                state = 378
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 377, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 376, "Rational literal", "delim_flo")
                return
        elif state == 378:                      # 4 fractional digits
            if c in numbers:
                state = 380
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 379, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 378, "Rational literal", "delim_flo")
                return
        elif state == 380:                      # 5 fractional digits
            if c in numbers:
                state = 382
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 381, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 380, "Rational literal", "delim_flo")
                return
        elif state == 382:                      # 6 fractional digits
            if c in numbers:
                state = 384
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 383, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 382, "Rational literal", "delim_flo")
                return
        elif state == 384:                      # 7 fractional digits
            if c in numbers:
                state = 386
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 385, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 384, "Rational literal", "delim_flo")
                return
        elif state == 386:                      # 8 fractional digits
            if c in numbers:
                state = 388
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 387, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 386, "Rational literal", "delim_flo")
                return
        elif state == 388:                      # 9 fractional digits
            if c in numbers:
                state = 390
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 389, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 388, "Rational literal", "delim_flo")
                return
        elif state == 390:                      # 10 fractional digits
            if c in numbers:
                state = 392
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 391, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 390, "Rational literal", "delim_flo")
                return
        elif state == 392:                      # 11 fractional digits
            if c in numbers:
                state = 394
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 393, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 392, "Rational literal", "delim_flo")
                return
        elif state == 394:                      # 12 fractional digits
            if c in numbers:
                state = 396
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 395, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 394, "Rational literal", "delim_flo")
                return
        elif state == 396:                      # 13 fractional digits
            if c in numbers:
                state = 398
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 397, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 396, "Rational literal", "delim_flo")
                return
        elif state == 398:                      # 14 fractional digits
            if c in numbers:
                state = 400
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 399, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 398, "Rational literal", "delim_flo")
                return
        elif state == 400:                      # 15 fractional digits
            if c in numbers:
                state = 402
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 401, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 400, "Rational literal", "delim_flo")
                return
        elif state == 402:                      # 16 fractional digits
            if c in numbers:
                state = 404
            elif c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 403, FLO_LIT)
                return
            else:
                number_delimiter_error(src, errors, start, 402, "Rational literal", "delim_flo")
                return
        elif state == 404:                      # 17 fractional digits
            if c in DELIM["delim_flo"]:
                accept_literal(src, tokens, start, path, 405, FLO_LIT)
                return
            elif c in numbers:
                # 18th fractional digit: no arrow leaves 404.
                absorb(src, numbers)
                errors.append(E.too_many_frac_digits(src, start, src.slice(start)))
                return
            else:
                number_delimiter_error(src, errors, start, 404, "Rational literal", "delim_flo")
                return
        src.advance()
        path.append(state)
