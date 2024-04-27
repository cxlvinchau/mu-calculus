import abc
from mu_calculus.formula import PropositionalVariable, Negation, Conjunction, Disjunction, Box, Diamond, Lfp, Gfp, Top, Bottom, Formula

class FormulaVisitor(abc.ABC):

    @abc.abstractmethod
    def visit_top(self):
        pass

    @abc.abstractmethod
    def visit_bottom(self):
        pass

    @abc.abstractmethod
    def visit_propositional_variable(self, variable: PropositionalVariable):
        pass

    @abc.abstractmethod
    def visit_negation(self, negation: Negation):
        pass

    @abc.abstractmethod
    def visit_conjunction(self, conjunction: Conjunction):
        pass

    @abc.abstractmethod
    def visit_disjunction(self, disjunction: Disjunction):
        pass

    @abc.abstractmethod
    def visit_box(self, box: Box):
        pass

    @abc.abstractmethod
    def visit_diamond(self, diamond: Diamond):
        pass

    @abc.abstractmethod
    def visit_lfp(self, lfp: Lfp):
        pass

    @abc.abstractmethod
    def visit_gfp(self, gfp: Gfp):
        pass


class SubformulaeCollector(FormulaVisitor):

    def __init__(self):
        self._subformulae = set()

    def visit_bottom(self):
        self._subformulae.add(Bottom())

    def visit_top(self):
        self._subformulae.add(Top())

    def visit_propositional_variable(self, variable: PropositionalVariable):
        self._subformulae.add(variable)

    def visit_negation(self, negation: Negation):
        self._subformulae.add(negation)
    
    def visit_conjunction(self, conjunction: Conjunction):
        self._subformulae.add(conjunction)

    def visit_disjunction(self, disjunction: Disjunction):
        self._subformulae.add(disjunction)

    def visit_box(self, box: Box):
        self._subformulae.add(box)

    def visit_diamond(self, diamond: Diamond):
        self._subformulae.add(diamond)

    def visit_lfp(self, lfp: Lfp):
        self._subformulae.add(lfp)

    def visit_gfp(self, gfp: Gfp):
        self._subformulae.add(gfp)

    @property
    def subformulae(self):
        return self._subformulae


def get_subformulae(formula: Formula):
    visitor = SubformulaeCollector()
    formula.accept_visitor(visitor)
    return visitor.subformulae