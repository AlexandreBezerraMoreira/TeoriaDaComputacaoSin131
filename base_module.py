import os
import time
from graphviz import Digraph

class Automaton:
    def __init__(self, start_state, accepting_states, transition_rules):
        self.start_state = start_state
        self.accepting_states = accepting_states
        self.transition_rules = transition_rules
        self.all_states = set()
        self.input_alphabet = set()
        self._extract_states_and_alphabet()

    def _extract_states_and_alphabet(self):
        for (src_state, transition_symbol, dst_state) in self.transition_rules:
            self.all_states.add(src_state)
            self.all_states.add(dst_state)
            self.input_alphabet.add(transition_symbol)

    def visualize_automaton(self):
        diagram = Digraph()
        diagram.attr(rankdir='LR')
        diagram.attr('node', shape='circle')

        diagram.node('->', shape='none', width='0', height='0', label='')
        diagram.edge('->', self.start_state)

        for final_state in self.accepting_states:
            diagram.node(final_state, shape='doublecircle', fontsize='19', fontcolor='green')
        for src_state, transition_symbol, dst_state in self.transition_rules:
            diagram.edge(src_state, dst_state, label=transition_symbol)

        return diagram

class FileHandler:
    @staticmethod
    def save_transitions(directory_path, transition_dict):
        with open(directory_path + "transitions.txt", "w") as trans_file:
            for key, value in transition_dict.items():
                state, symbol = key
                line = f"{state} {symbol} {' '.join(value)}\n"
                trans_file.write(line)
        return trans_file

    @staticmethod
    def save_info(directory_path, start_state, accepting_states, alphabet):
        with open(directory_path + "info.txt", "w") as info_file:
            info_file.write(f"Initial state: {start_state}\n")
            info_file.write(f"Final states: {' '.join(accepting_states)}\n")
            info_file.write(f"Alphabet: {' '.join(alphabet)}\n")
        return info_file

    @staticmethod
    def convert_txt_to_dict(directory_path):
        transitions = {}
        with open(directory_path + "transitions.txt", "r") as file:
            for line in file:
                parts = line.strip().split()
                key = (parts[0], parts[1])
                transitions[key] = parts[2:]
        return transitions

    @staticmethod
    def convert_dict_to_list(transitions_dict):
        transitions_list = []
        for key, value in transitions_dict.items():
            state, symbol = key
            for v in value:
                transitions_list.append((state, symbol, v))
        return transitions_list

    @staticmethod
    def get_initial_final_states_and_alphabet(directory_path):
        with open(directory_path + "info.txt", "r") as file:
            lines = file.readlines()
            initial_state = lines[0].split(":")[1].strip()
            final_states = lines[1].split(":")[1].strip().split()
            alphabet = lines[2].split(":")[1].strip().split()
        return initial_state, final_states, alphabet

class ExistenceChecker:
    @staticmethod
    def check_existence():
        print("ExistenceChecker: Verificação de existência de autômatos não implementada.")
