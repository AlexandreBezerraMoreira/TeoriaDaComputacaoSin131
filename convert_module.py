import os
import base_module

class AutomatonCreator:
    def __init__(self, special_characters):
        self.special_characters = special_characters
        self.automaton_states = []
        self.automaton_alphabet = []
        self.automaton_transitions = {}
        self.automaton_initial_state = ""
        self.automaton_final_states = []
        self.dfa_directory = "DFAs/"
        self.nfa_directory = "NFAs/"

    def create_automaton(self):
        while True:
            print("Menu de Opções")
            print("1. Criar um AFD")
            print("2. Criar um AFN")
            print("3. Testar linguagem no AFD ou AFN")
            print("4. Voltar para o Menu")
            option = int(input("Digite a opção desejada: "))
            if option == 1:
                self.create_dfa()
            elif option == 2:
                self.create_nfa()
            elif option == 3:
                self.test_language()
            elif option == 4:
                print("Retornando ao menu principal.")
                break

    def create_dfa(self):
        print("Criando um AFD")

        if not os.path.exists(self.dfa_directory):
            os.mkdir(self.dfa_directory)

        self.automaton_states = self.get_input("Digite o conjunto de estados: ")
        if not self.is_input_valid(self.automaton_states):
            return

        self.automaton_alphabet = self.get_input("Digite o alfabeto do autômato: ")
        if not self.is_input_valid(self.automaton_alphabet):
            return

        self.automaton_initial_state = input("Digite o estado inicial: ")
        if not self.is_input_valid([self.automaton_initial_state]):
            return

        self.automaton_final_states = self.get_input("Digite o(s) estado(s) final(is): ")
        if not self.is_input_valid(self.automaton_final_states):
            return

        self.define_transitions()

        dfa_file = base_module.FileHandler.save_transitions(self.dfa_directory, self.automaton_transitions)
        dfa_file.close()

        dfa_info_file = base_module.FileHandler.save_info(
            self.dfa_directory,
            self.automaton_initial_state,
            self.automaton_final_states,
            self.automaton_alphabet
        )
        dfa_info_file.close()

    def create_nfa(self):
        print("Criando um AFN")

        if not os.path.exists(self.nfa_directory):
            os.mkdir(self.nfa_directory)

        self.automaton_states = self.get_input("Digite o conjunto de estados: ")
        if not self.is_input_valid(self.automaton_states):
            return

        self.automaton_alphabet = self.get_input("Digite o alfabeto do autômato: ")
        if not self.is_input_valid(self.automaton_alphabet):
            return

        self.automaton_initial_state = input("Digite o estado inicial: ")
        if not self.is_input_valid([self.automaton_initial_state]):
            return

        self.automaton_final_states = self.get_input("Digite o(s) estado(s) final(is): ")
        if not self.is_input_valid(self.automaton_final_states):
            return

        self.define_transitions(e_nfa=True)

        nfa_file = base_module.FileHandler.save_transitions(self.nfa_directory, self.automaton_transitions)
        nfa_file.close()

        nfa_info_file = base_module.FileHandler.save_info(
            self.nfa_directory,
            self.automaton_initial_state,
            self.automaton_final_states,
            self.automaton_alphabet
        )
        nfa_info_file.close()

    def test_language(self):
        print("Testando uma cadeia de entrada")
        input_string = input("Digite a cadeia de entrada: ")
        print("Escolha o tipo de autômato:")
        print("a. AFD")
        print("b. AFN")
        automaton_type = input("Opção: ")

        if automaton_type == "a":
            self.run_test(input_string, self.dfa_directory)
        elif automaton_type == "b":
            self.run_test(input_string, self.nfa_directory)

    def run_test(self, input_string, directory):
        initial_state, final_states, alphabet = base_module.FileHandler.get_initial_final_states_and_alphabet(directory)
        transitions = base_module.FileHandler.convert_txt_to_dict(directory)
        current_states = [initial_state]

        for symbol in input_string:
            print(f"Estados atuais: {current_states}")
            new_states = []

            for current_state in current_states:
                next_states = transitions.get((current_state, symbol), [])
                new_states.extend(next_states)

            current_states = new_states

            print(f"Entrada atual: {symbol}")
            print(f"Próximos estados: {current_states}")

        if any(state in final_states for state in current_states):
            print("Reconhecido!")
        else:
            print("Não reconhecido!")

    def get_input(self, prompt):
        print(prompt, end="")
        return input().split()

    def is_input_valid(self, input_list):
        if (
            any(char in self.special_characters for char in input_list)
            or not input_list
        ):
            print("Vazio ou contém caracteres inválidos, retornando ao menu de opções.")
            return False
        return True

    def define_transitions(self, e_nfa=False):
        print("Defina as funções de transição (delta)")
        for state in self.automaton_states:
            for symbol in self.automaton_alphabet:
                print(f"\t {symbol}")
                print(f"{state}\t------>\t", end="")
                next_states = input().split() if e_nfa else [input().strip()]
                self.automaton_transitions[(state, symbol)] = next_states
