from typing import Set, Tuple, Dict


class TransitionSystem:

    def __init__(self, states: Set[int], transitions: Set[Tuple[int, int]], labeling: Dict[int, Set[str]]):
        self._states = states
        self._transitions = transitions
        self._state_to_successors: Dict[int, Set[int]] = {}
        self._state_to_predecessors: Dict[int, Set[int]] = {}
        self._label_to_states: Dict[str, Set[int]] = {}
        self._labeling = labeling
        for s, t in transitions:
            successors = self._state_to_successors.setdefault(s, set())
            successors.add(t)
            predecessors = self._state_to_predecessors.setdefault(t, set())
            predecessors.add(s)
        for state, labels in labeling.items():
            for label in labels:
                labeled_states = self._label_to_states.setdefault(label, set())
                labeled_states.add(state)

    def pre(self, states: Set[int]) -> Set[int]:
        return {state for state in self._states if self._state_to_successors.get(state, set()).intersection(states)}

    def post(self, states: Set[int]) -> Set[int]:
        return {state for state in self._states if self._state_to_predecessors.get(state, set()).intersection(states)}

    def states_by_label(self, label: str) -> Set[int]:
        return self._label_to_states[label]

    @property
    def states(self) -> Set[int]:
        return self._states

    def to_dot(self):
        out = 'digraph{\n'
        for state in self.states:
            labels = ', '.join(self._labeling[state]) if state in self._labeling else ''
            out += f'    node [label=\"{state}\", xlabel=\"{labels}\", style=filled, color=lightgrey] {state};\n'
        for transition in self._transitions:
            out += f'    {transition[0]} -> {transition[1]};\n'
        return out + "}"

