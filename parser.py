# parser.py - Lee y parsea un archivo .txt de gramatica libre de contexto
# Formato por linea: A -> B C | d | epsilon

EPSILON = 'ε'


def parse_grammar(filepath):
    # Lee un archivo .cfg y retorna (start_symbol, nonterminals, terminals, productions)
    productions = {}
    nonterminals = []
    terminals = set()
    start_symbol = None

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Separar lado izquierdo y derecho de ->
            if '->' not in line:
                raise ValueError(f"Línea inválida (falta '->'): {line}")

            left, right = line.split('->', 1)
            head = left.strip()

            if not head:
                raise ValueError(f"No-terminal vacío en línea: {line}")

            # Registrar no-terminal y simbolo inicial
            if head not in productions:
                productions[head] = []
                nonterminals.append(head)
            if start_symbol is None:
                start_symbol = head

            # Separar alternativas por |
            alternatives = right.split('|')
            for alt in alternatives:
                symbols = alt.split()
                # Reemplazar 'epsilon' por ε
                prod = [EPSILON if s == 'epsilon' else s for s in symbols]
                if not prod:
                    prod = [EPSILON]
                productions[head].append(prod)

    # Terminales = todo simbolo que no es no-terminal ni ε
    for prods in productions.values():
        for prod in prods:
            for sym in prod:
                if sym != EPSILON and sym not in productions:
                    terminals.add(sym)

    return start_symbol, nonterminals, terminals, productions


def is_nonterminal(symbol, nonterminals):
    # Verifica si un simbolo es no-terminal
    return symbol in nonterminals


def format_production(head, body):
    # Formatea una produccion: A -> B C d
    return f"{head} -> {' '.join(body)}"
