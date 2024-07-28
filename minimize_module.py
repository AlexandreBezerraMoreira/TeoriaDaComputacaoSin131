from graphviz import Digraph

class DFA:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

class DFAOptimizer:
    def __init__(self, dfa):
        self.dfa = dfa

    def minimize_dfa(self):
        print("Minimizando DFA")

        # Particionamento inicial: aceitação vs não aceitação
        partition = [self.dfa.final_states, self.dfa.states - self.dfa.final_states]

        while True:
            new_partition = []
            for group in partition:
                new_groups = {}
                for state in group:
                    key = tuple(self.dfa.transitions.get((state, symbol), None) for symbol in self.dfa.alphabet)
                    if key not in new_groups:
                        new_groups[key] = set()
                    new_groups[key].add(state)

                new_partition.extend(new_groups.values())
            if set(map(frozenset, new_partition)) == set(map(frozenset, partition)):
                break
            partition = new_partition

        return partition

    def print_minimized_dfa(self, partition):
        print("DFA Minimizado:")
        for group in partition:
            print(group)

        # Gerar o gráfico do DFA minimizado
        automaton_graph = Digraph()
        automaton_graph.attr(rankdir='LR')  # LR significa da esquerda para a direita
        automaton_graph.attr('node', shape='circle')

        state_map = {}
        new_initial_state = ''
        new_final_states = []

        # Criar um mapeamento de estados
        for i, group in enumerate(partition):
            new_state = f'q{i}'
            for state in group:
                state_map[state] = new_state
                if state == self.dfa.initial_state:
                    new_initial_state = new_state
                if state in self.dfa.final_states:
                    new_final_states.append(new_state)

        # Adicionar os nós e transições
        for group in partition:
            state_repr = next(iter(group))
            if state_repr in new_final_states:
                automaton_graph.node(state_map[state_repr], shape='doublecircle', fontsize='19', fontcolor='green')
            else:
                automaton_graph.node(state_map[state_repr])

        for (state, symbol), destination in self.dfa.transitions.items():
            new_state = state_map.get(state, state)
            new_destination = state_map.get(destination, destination)
            automaton_graph.edge(new_state, new_destination, label=symbol)

        automaton_graph.render('MinimizedAutomaton', format='png', cleanup=True)

def minimize_dfa():
    # Suponha que você tenha um DFA definido aqui
    # Isso deve ser substituído com a lógica real de obtenção do DFA
    # Exemplo de dados do DFA:
    states = {'q0', 'q1', 'q2'}
    alphabet = {'0', '1'}
    transitions = {
        ('q0', '0'): 'q0',
        ('q0', '1'): 'q1',
        ('q1', '0'): 'q2',
        ('q1', '1'): 'q0',
        ('q2', '0'): 'q1',
        ('q2', '1'): 'q2'
    }
    initial_state = 'q0'
    final_states = {'q2'}

    dfa = DFA(states, alphabet, transitions, initial_state, final_states)
    optimizer = DFAOptimizer(dfa)
    minimized_partition = optimizer.minimize_dfa()
    optimizer.print_minimized_dfa(minimized_partition)
