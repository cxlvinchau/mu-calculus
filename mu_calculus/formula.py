import abc
from typing import List

class Formula(abc.ABC):

    def accept_visitor(self, visitor, pre_order: bool = True):
        pass


class Top(abc.ABC):

    def __str__():
        return 'T'

    def accept_visitor(self, visitor, pre_order: bool = True):
        return visitor.visit_top()

    def __eq__(self, other):
        return isinstance(other, Top)

    def __hash__(self):
        return hash('top')


class Bottom(abc.ABC):

    def __str__():
        return 'B'

    def accept_visitor(self, visitor, pre_order: bool = True):
        return visitor.visit_bottom()

    def __eq__(self, other):
        return isinstance(other, Bottom)

    def __hash__(self):
        return hash('bot')


class PropositionalVariable(Formula):

    def __init__(self, name: str, is_negated: bool = False):
        self._name = name
        self._is_negated = is_negated

    @property
    def name(self):
        return self._name

    @property
    def is_negated(self):
        return self._is_negated

    def __str__(self):
        if self.is_negated:
            return f'¬{self.name}'
        return self.name

    def accept_visitor(self, visitor, pre_order: bool = True):
        return visitor.visit_propositional_variable(self)

    def __eq__(self, other):
        return isinstance(other, PropositionalVariable) and other.name == self.name and other.is_negated == self.is_negated

    def __hash__(self):
        return hash(self.name) + hash(self.is_negated)


class Negation(Formula):

    def __init__(self, formula: Formula):
        self._formula = formula

    def __str__(self):
        return f'¬({self._formula})'

    @property
    def formula(self):
        return self._formula

    def accept_visitor(self, visitor, pre_order: bool = True):
        if pre_order:
            visitor.visit_negation(self)
            self._formula.accept_visitor(visitor, pre_order=pre_order)
        else:
            self._formula.accept_visitor(visitor, pre_order=pre_order)
            visitor.visit_negation(self)

    def __eq__(self, other):
        return isinstance(other, Negation) and other.formula == self.formula

    def __hash__(self):
        return -1 * hash(self.formula)


class Conjunction(Formula):

    def __init__(self, *formulae):
        self._formulae = formulae

    def __str__(self):
        return ' ∧ '.join(map(lambda f: f'{f}', self._formulae))

    def accept_visitor(self, visitor, pre_order: bool = True):
        if pre_order:
            visitor.visit_conjunction(self)
            for formula in self._formulae:
                formula.accept_visitor(visitor, pre_order=pre_order)
        else:
            for formula in self._formulae:
                formula.accept_visitor(visitor)
            visitor.visit_conjunction(self, pre_order=pre_order)

    @property
    def formulae(self):
        return self._formulae

    def __eq__(self, other):
        return isinstance(other, Conjunction) and other.formulae == self.formulae

    def __hash__(self):
        return sum(map(hash, self.formulae)) + hash('conjunction')


class Disjunction(Formula):

    def __init__(self, *formulae):
        self._formulae = formulae

    def __str__(self):
        return ' ∨ '.join(map(lambda f: f'{f}', self._formulae))

    def accept_visitor(self, visitor, pre_order: bool = True):
        if pre_order:
            visitor.visit_disjunction(self)
            for formula in self._formulae:
                formula.accept_visitor(visitor, pre_order=pre_order)
        else:
            for formula in self._formulae:
                formula.accept_visitor(visitor, pre_order=pre_order)     
            visitor.visit_disjunction(self)

    @property
    def formulae(self):
        return self._formulae

    def __eq__(self, other):
        return isinstance(other, Disjunction) and other.formulae == self.formulae

    def __hash__(self):
        return sum(map(hash, self.formulae)) + hash('disjunction')


class Box(Formula):

    def __init__(self, formula: Formula):
        self._formula = formula

    def __str__(self):
        return f'☐({self._formula})'

    def accept_visitor(self, visitor, pre_order: bool = True):
        if pre_order:
            visitor.visit_box(self)
            self._formula.accept_visitor(visitor, pre_order=pre_order)
        else:
            self._formula.accept_visitor(visitor, pre_order=pre_order)
            visitor.visit_box(self)

    @property
    def formula(self):
        return self.formula

    def __eq__(self, other):
        return isinstance(other, Box) and other.formula == self.formula

    def __hash__(self):
        return hash(self._formula) + hash('box')


class Diamond(Formula):

    def __init__(self, formula: Formula):
        self._formula = formula

    def __str__(self):
        return f'♢{self._formula}'

    def accept_visitor(self, visitor, pre_order: bool = True):
        if pre_order:
            visitor.visit_diamond(self)
            self._formula.accept_visitor(visitor, pre_order=pre_order)
        else:
            self._formula.accept_visitor(visitor, pre_order=pre_order)
            visitor.visit_diamond(self)

    def __eq__(self, other):
        return isinstance(other, Diamond) and other.formula == self.formula

    def __hash__(self):
        return hash(self._formula) + hash('diamond')


class Lfp(Formula):

    def __init__(self, variable: PropositionalVariable, formula: Formula):
        self._variable = variable
        self._formula = formula

    def __str__(self):
        return f'μ {self._variable}.({self._formula})'

    def accept_visitor(self, visitor, pre_order: bool = True):
        if pre_order:
            visitor.visit_lfp(self)
            self._formula.accept_visitor(visitor)
        else:
            self._formula.accept_visitor(visitor)
            visitor.visit_lfp(self)

    @property
    def variable(self):
        return self._variable

    @property
    def formula(self):
        return self._formula

    def __eq__(self, other):
        return isinstance(other, Lfp) and other.variable == self.variable and other.formula == self.formula

    def __hash__(self):
        return hash(self.formula) + hash(self.variable) + hash('lfp')


class Gfp(Formula):

    def __init__(self, variable: PropositionalVariable, formula: Formula):
        self._variable = variable
        self._formula = formula

    def __str__(self):
        return f'ν {self._variable}.({self._formula})'

    def accept_visitor(self, visitor):
        if pre_order:
            visitor.visit_gfp(self)
            self._formula.accept_visitor(visitor)
        else:
            self._formula.accept_visitor(visitor)
            visitor.visit_gfp(self)

    @property
    def variable(self):
        return self._variable

    @property
    def formula(self):
        return self._formula

    def __eq__(self, other):
        return isinstance(other, Gfp) and other.variable == self.variable and other.formula == self.formula

    def __hash__(self):
        return hash(self.formula) + hash(self.variable) + hash('gfp')