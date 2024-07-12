from mu_calculus.formula import Variable, Conjunction, Lfp, AP, Disjunction, Diamond, Gfp
from mu_calculus.model_checker import global_model_checking
from mu_calculus.transition_system import TransitionSystem
from mu_calculus.visitors import get_subformulae

ts = TransitionSystem(
    {0, 1, 2, 3, 4, 5, 6},
    {(0, 1), (1, 2), (2, 3), (3, 2), (1, 4), (4, 5), (5, 6), (6, 6)},
    {2: {"a"}, 4: {"b"}, 5: {"a"}, 6: {"c"}})

with open('ts.dot', 'w') as f:
    f.write(ts.to_dot())

phi1 = Gfp(Variable("Y"), Lfp(Variable('X'), Conjunction(Disjunction(AP("a"), Diamond(Variable("X"))), Diamond(Variable("Y")))))
phi2 = Gfp(Variable("Y"), Lfp(Variable('X'), Disjunction(Conjunction(AP("a"), Diamond(Variable("Y"))), Diamond(Variable("X")))))
phi3 = Lfp(Variable("X"), Disjunction(AP("b"), Diamond(Variable("X"))))

for phi in [phi1, phi2, phi3]:
    print(f"Formula: {phi}")
    global_model_checking(ts, phi)
    print()

