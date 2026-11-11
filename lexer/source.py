"""
source.py - the program text being scanned, read one character at a time.

CR LF is read as one newline (Regular Definitions: newline).  Line and column
numbers start at 1.
"""


class Source:
    def __init__(self, text):
        text = text.replace("\r\n", "\n")
        self.text = text
        self.n = len(text)
        self.pos = 0
        self.line_starts = [0]
        for i, c in enumerate(text):
            if c == "\n":
                self.line_starts.append(i + 1)

    def peek(self, n=0):
        """Character n places ahead of the current one; "" means EOF."""
        p = self.pos + n
        if 0 <= p < self.n:
            return self.text[p]
        return ""

    def advance(self):
        """Consume and return the current character ("" at EOF)."""
        c = self.peek()
        if c != "":
            self.pos += 1
        return c

    def at_end(self):
        return self.pos >= self.n

    def slice(self, start, end=None):
        return self.text[start:self.pos if end is None else end]

    def loc(self, p):
        """Position -> (line, col), by binary search over line_starts."""
        lo, hi = 0, len(self.line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.line_starts[mid] <= p:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1, p - self.line_starts[lo] + 1

    @property
    def line(self):
        return self.loc(self.pos)[0]

    @property
    def col(self):
        return self.loc(self.pos)[1]
