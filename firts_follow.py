# first_follow.py - Algoritmos FIRST y FOLLOW
# Calculo iterativo hasta punto fijo (sin cambios entre iteraciones)

from parser import EPSILON, is_nonterminal, format_production


def compute_first(nonterminals, terminals, productions, verbose=True):
    # Calcula FIRST para todos los no-terminales
    # Itera hasta punto fijo
    first = {nt: set() for nt in nonterminals}

    iteration = 0
    changed = True

    if verbose:
        print("=" * 50)
        print("=== Calculando FIRST ===")
        print("=" * 50)

    while changed:
        changed = False
        iteration += 1
        if verbose:
            print(f"\nIteración {iteration}:")

        for nt in nonterminals:
            for prod in productions[nt]:
                prod_str = format_production(nt, prod)
                before = first[nt].copy()

                # Caso: produccion es epsilon directamente
                if prod == [EPSILON]:
                    first[nt].add(EPSILON)
                    if verbose and first[nt] != before:
                        added = first[nt] - before
                        print(f"  FIRST({nt}): procesando {prod_str}  =>  "
                              f"agrega {_fmt_set(added)}")
                    if first[nt] != before:
                        changed = True
                    continue

                # Recorrer simbolos de izquierda a derecha
                all_have_epsilon = True
                for i, sym in enumerate(prod):
                    if sym == EPSILON:
                        continue

                    if sym in terminals or sym not in nonterminals:
                        # sym es terminal: agregar a FIRST y parar
                        before_sym = first[nt].copy()
                        first[nt].add(sym)
                        if verbose and first[nt] != before_sym:
                            added = first[nt] - before_sym
                            print(f"  FIRST({nt}): procesando {prod_str}  =>  "
                                  f"agrega {_fmt_set(added)} (terminal '{sym}')")
                        if first[nt] != before_sym:
                            changed = True
                        all_have_epsilon = False
                        break
                    else:
                        # sym es no-terminal: agregar FIRST(sym) - {ε}
                        before_sym = first[nt].copy()
                        to_add = first[sym] - {EPSILON}
                        first[nt] |= to_add
                        if verbose and first[nt] != before_sym:
                            added = first[nt] - before_sym
                            print(f"  FIRST({nt}): procesando {prod_str}  =>  "
                                  f"agrega {_fmt_set(added)} (desde FIRST({sym}))")
                        if first[nt] != before_sym:
                            changed = True

                        # Si ε no esta en FIRST(sym), parar
                        if EPSILON not in first[sym]:
                            all_have_epsilon = False
                            break

                # Si todos los simbolos derivan ε, agregar ε
                if all_have_epsilon:
                    before_eps = first[nt].copy()
                    first[nt].add(EPSILON)
                    if verbose and first[nt] != before_eps:
                        print(f"  FIRST({nt}): procesando {prod_str}  =>  "
                              f"agrega 'ε' (todos los símbolos derivan ε)")
                    if first[nt] != before_eps:
                        changed = True

        if verbose and not changed:
            print("  (sin cambios — punto fijo alcanzado)")

    # Mostrar resultado final
    if verbose:
        print(f"\n{'─' * 40}")
        print("Resultado final FIRST:")
        for nt in nonterminals:
            print(f"  FIRST({nt}) = {{ {', '.join(sorted(first[nt]))} }}")
        print()

    return first


def first_of_string(symbols, first_sets, nonterminals, terminals):
    # Calcula FIRST de una cadena de simbolos (usado por FOLLOW)
    result = set()

    all_have_epsilon = True
    for sym in symbols:
        if sym == EPSILON:
            continue
        if sym in terminals or sym not in nonterminals:
            # Terminal
            result.add(sym)
            all_have_epsilon = False
            break
        else:
            # No-terminal: agregar FIRST(sym) - {ε}
            result |= (first_sets[sym] - {EPSILON})
            if EPSILON not in first_sets[sym]:
                all_have_epsilon = False
                break

    if all_have_epsilon:
        result.add(EPSILON)

    return result


def compute_follow(start_symbol, nonterminals, terminals, productions,
                   first_sets, verbose=True):
    # Calcula FOLLOW para todos los no-terminales
    # Itera hasta punto fijo
    follow = {nt: set() for nt in nonterminals}

    # Regla 1: $ en FOLLOW del simbolo inicial
    follow[start_symbol].add('$')

    iteration = 0
    changed = True

    if verbose:
        print("=" * 50)
        print("=== Calculando FOLLOW ===")
        print("=" * 50)
        print(f"\nRegla inicial: FOLLOW({start_symbol}) contiene '$'")

    while changed:
        changed = False
        iteration += 1
        if verbose:
            print(f"\nIteración {iteration}:")

        for head in nonterminals:
            for prod in productions[head]:
                prod_str = format_production(head, prod)

                for i, sym in enumerate(prod):
                    # Solo interesan los no-terminales
                    if sym not in nonterminals:
                        continue

                    before = follow[sym].copy()
                    beta = prod[i + 1:]  # Simbolos despues de sym

                    if beta:
                        # Agregar FIRST(β) - {ε} a FOLLOW(sym)
                        first_beta = first_of_string(
                            beta, first_sets, nonterminals, terminals
                        )
                        to_add = first_beta - {EPSILON}
                        follow[sym] |= to_add

                        if verbose and follow[sym] != before:
                            added = follow[sym] - before
                            beta_str = ' '.join(beta)
                            print(f"  FOLLOW({sym}): en {prod_str}, "
                                  f"β = {beta_str}  =>  "
                                  f"agrega {_fmt_set(added)} (de FIRST(β))")
                            before = follow[sym].copy()

                        # Si ε ∈ FIRST(β), agregar FOLLOW(head)
                        if EPSILON in first_beta:
                            follow[sym] |= follow[head]
                            if verbose and follow[sym] != before:
                                added = follow[sym] - before
                                print(f"  FOLLOW({sym}): en {prod_str}, "
                                      f"ε ∈ FIRST(β)  =>  "
                                      f"agrega {_fmt_set(added)} "
                                      f"(de FOLLOW({head}))")
                    else:
                        # β vacio: agregar FOLLOW(head) a FOLLOW(sym)
                        follow[sym] |= follow[head]
                        if verbose and follow[sym] != before:
                            added = follow[sym] - before
                            print(f"  FOLLOW({sym}): en {prod_str}, "
                                  f"{sym} al final  =>  "
                                  f"agrega {_fmt_set(added)} "
                                  f"(de FOLLOW({head}))")

                    if follow[sym] != before:
                        changed = True

        if verbose and not changed:
            print("  (sin cambios — punto fijo alcanzado)")

    # Mostrar resultado final
    if verbose:
        print(f"\n{'─' * 40}")
        print("Resultado final FOLLOW:")
        for nt in nonterminals:
            print(f"  FOLLOW({nt}) = {{ {', '.join(sorted(follow[nt]))} }}")
        print()

    return follow


def _fmt_set(s):
    # Formatea un conjunto para mostrar: 'a', 'b'
    return ', '.join(f"'{x}'" for x in sorted(s))
