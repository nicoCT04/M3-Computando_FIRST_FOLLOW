#!/usr/bin/env python3
# main.py - Punto de entrada
# Uso: python main.py <archivo.txt>

import sys
from parser import parse_grammar
from first_follow import compute_first, compute_follow


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo.txt>")
        print("Ejemplo: python main.py grammar.txt")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        start_symbol, nonterminals, terminals, productions = parse_grammar(filepath)
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{filepath}'")
        sys.exit(1)
    except ValueError as e:
        print(f"Error al parsear la gramática: {e}")
        sys.exit(1)

    # Mostrar la gramatica leida
    print("=" * 50)
    print("Gramática leída:")
    print("=" * 50)
    print(f"  Símbolo inicial: {start_symbol}")
    print(f"  No-terminales: {', '.join(nonterminals)}")
    print(f"  Terminales: {', '.join(sorted(terminals))}")
    print("  Producciones:")
    for nt in nonterminals:
        alts = ' | '.join(' '.join(p) for p in productions[nt])
        print(f"    {nt} -> {alts}")
    print()

    # Calcular FIRST y FOLLOW
    first_sets = compute_first(nonterminals, terminals, productions)
    compute_follow(start_symbol, nonterminals, terminals, productions, first_sets)


if __name__ == '__main__':
    main()
