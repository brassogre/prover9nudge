
import clause

class Proof:
    """A Proof is a collection of clauses, possibly with additional information"""

    def __init__(self):
        #  dictionary: keys are integers (consecutive)
        #             values are dicts again
        #  d[i]['clause'] = clause.Clause
        self.clause_dict = {}

    def max_clause_index(self):
        if self.clause_dict == {}: return 0
        else: return max(self.clause_dict.keys())

    def add_clause(self, c):
        if isinstance(c, clause.Clause):
            self.clause_list.append(c)
        elif isinstance(c, str):
            self.clause_list.append(clause.Clause(c))

