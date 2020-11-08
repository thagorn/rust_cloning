import sys
from result import Result
from constants import *

class Clone:
    def __init__(self, clone_array, creation = None):
        self.creation = creation
        self.genes = tuple(clone_array)
        self.string_repr = self._str_repr()
        self.hash = hash(self.string_repr)
        self.undefined = self._has_undefined()

    @classmethod
    def fromString(cls, clone_string):
        return cls(cls._create_clone(clone_string))

    @staticmethod
    def _create_clone(clone_string):
        clone_string = clone_string.strip().upper()
        if len(clone_string) != 6:
            sys.exit("LENGTH ERROR: {0}".format(clone_string))
        for char in clone_string:
            if char not in VALID_GENES:
                sys.exit("INVALID CHARACTER: {0} IN CLONE: {1}".format(char, clone_string))
        return [char for char in clone_string]

    def __str__(self):
        return self.string_repr

    def __eq__(self, other):
        if other == None:
            return False
        return self.hash == other.hash

    def __hash__(self):
        return self.hash

    def _str_repr(self):
        return ''.join(self.genes)

    def _has_undefined(self):
        for gene in self.genes:
            if gene == UNDEFINED_GREEN or gene == UNDEFINED_RED:
                return True
        return False

    def is_undefined(self):
        """ Return True if any genes of this clone are undefined"""
        return self.undefined

    def is_equivalent(self, other):
        return self.yield_count() == other.yield_count() and \
                self.growth_count() == other.growth_count()

    def yield_count(self):
        return sum(y == YIELD for y in self.genes)
    
    def growth_count(self):
        return sum(g == GROWTH for g in self.genes)

    def get_genes(self):
        return self.genes

    def get_box(self):
        return self.creation

    def get_result(self):
        return Result(self, self.creation)

    def score(self):
        score = 0
        for gene in self.genes:
            if gene == GROWTH:
                score += 5
            if gene == YIELD:
                score += 5
        return score

