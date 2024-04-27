from mu_calculus.formula import PropositionalVariable, Conjunction, Lfp
from mu_calculus.visitors import get_subformulae

x = PropositionalVariable('x')
y = PropositionalVariable('y')
phi1 = Lfp(x, Conjunction(x, y))
phi2 = Lfp(x, Conjunction(x, y))
print(phi1)
print(set(map(str, get_subformulae(phi1))))