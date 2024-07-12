from typing import Dict, Set

from mu_calculus.formula import Formula, AP, Conjunction, Disjunction, Top, Bottom, Negation, Box, Diamond, Variable, \
    Lfp, Gfp
from mu_calculus.transition_system import TransitionSystem


def global_model_checking(ts: TransitionSystem, phi: Formula, valuation: Dict[Variable, Set[int]] = None, depth=0):
    if valuation is None:
        valuation = {}
    valuation_str = ', '.join(map(lambda x: f'{x[0]}: {x[1]}', valuation.items()))

    if isinstance(phi, Top):
        return set(ts.states)
    if isinstance(phi, Bottom):
        return set()
    if isinstance(phi, AP):
        return set(ts.states_by_label(phi.name))
    if isinstance(phi, Variable):
        return valuation[phi]
    if isinstance(phi, Conjunction):
        return set.intersection(*[global_model_checking(ts, psi, valuation, depth=depth+1) for psi in phi.formulae])
    if isinstance(phi, Disjunction):
        return set.union(*[global_model_checking(ts, psi, valuation, depth=depth+1) for psi in phi.formulae])
    if isinstance(phi, Negation):
        return ts.states.difference(global_model_checking(ts, phi.formula, valuation, depth=depth+1))
    if isinstance(phi, Box):
        psi_states = global_model_checking(ts, phi.formula, valuation, depth=depth+1)
        return {state for state in ts.states if ts.post({state}).issubset(psi_states)}
    if isinstance(phi, Diamond):
        psi_states = global_model_checking(ts, phi.formula, valuation, depth=depth+1)
        return {state for state in ts.states if ts.post({state}).intersection(psi_states)}
    if isinstance(phi, Lfp):
        approximant, size = set(), -1
        while len(approximant) != size:
            size = len(approximant)
            updated_valuation = dict(valuation)
            updated_valuation[phi.variable] = approximant
            approximant = global_model_checking(ts, phi.formula, updated_valuation, depth=depth+1)
        print(f"{depth * '  '}({valuation_str}) | {phi} ≡ {approximant}")
        return approximant
    if isinstance(phi, Gfp):
        approximant, size = ts.states, -1
        while len(approximant) != size:
            size = len(approximant)
            updated_valuation = dict(valuation)
            updated_valuation[phi.variable] = approximant
            approximant = global_model_checking(ts, phi.formula, updated_valuation, depth=depth+1)
        print(f"{depth * '  '}({valuation_str}) | {phi} ≡ {approximant}")
        return approximant
