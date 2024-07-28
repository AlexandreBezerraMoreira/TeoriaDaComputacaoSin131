import create_module
import convert_module
import minimize_module
import base_module

special_characters = "!@#$%&*()-+=<>:;^~.,][}{?/"

class MainSystem:
    def __init__(self):
        self.special_characters = special_characters

    def check_existence(self):
        print("\nVerificando a existência de um NFA e/ou DFA criado...\n")
        base_module.ExistenceChecker.check_existence()

    def main_menu(self):
        while True:
            print("Menu Principal")
            print("1. Criar e Testar")
            print("2. Converter AFN para AFD")
            print("3. Minimizar AFD")
            print("4. Sair")
            option = int(input("Insira uma das opções: "))
            if option == 1:
                automaton_creator = create_module.AutomatonCreator(self.special_characters)
                automaton_creator.create_automaton()
            elif option == 2:
                nfa_to_dfa_converter = convert_module.NFAtoDFAConverter()
                nfa_to_dfa_converter.convert_nfa_to_dfa()
            elif option == 3:
                minimize_module.minimize_dfa()
            elif option == 4:
                break

if __name__ == "__main__":
    automaton_system = MainSystem()
    automaton_system.check_existence()
    automaton_system.main_menu()
