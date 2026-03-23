# Computando FIRST y FOLLOW

Programa en Python que calcula los conjuntos FIRST y FOLLOW de una gramática libre de contexto, mostrando el proceso paso a paso.

## Estructura

```
first_follow/
├── main.py          # Punto de entrada
├── parser.py        # Lectura y parseo de gramáticas
├── first_follow.py  # Algoritmos FIRST y FOLLOW
├── tests/
│   ├── test_first.py
│   ├── test_follow.py
│   └── grammars/
│       ├── simple.txt      # Sin epsilon
│       ├── epsilon.txt     # Con epsilon
│       └── indirect.txt    # Expresiones (recursión eliminada)
└── README.md
```

## Uso

```bash
cd first_follow
python main.py tests/grammars/epsilon.txt
```

## Formato de gramática

Cada línea tiene la forma:

```
A -> B C | d | epsilon
```

- **No-terminales**: letras mayúsculas o identificadores (ej: `E`, `EP`, `TP`)
- **Terminales**: letras minúsculas o símbolos (ej: `a`, `+`, `id`, `(`)
- **`epsilon`**: representa la cadena vacía (ε)
- **`|`**: separa producciones alternativas
- **`#`**: líneas de comentario (se ignoran)
- La primera regla define el símbolo inicial

### Ejemplo (epsilon.txt)

```
S -> A B
A -> a | epsilon
B -> b A
```

## Tests

```bash
cd first_follow
python -m pytest tests/ -v
# o con unittest:
python -m unittest discover tests/ -v
```

## Requisitos

Python 3.6+. Sin dependencias externas.
