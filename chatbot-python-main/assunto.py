MENU_PRINCIPAL = (
    "*Tutor IA - Python*\n\n"
    "Escolha uma opção:\n"
    "1. Introdução ao Python\n"
    "2. Exemplos Práticos\n"
    "3. Estruturas de Repetição\n"
    "4. Listas e Funções\n"
    "5. Desafio (Quiz)\n"
    "6. Status de Comportamento\n"
    "7. Ajuda"
) 

LICOES = {
    '1': "Python é uma linguagem de alto nível focada em legibilidade. É amplamente usada em IA e Data Science.",
    '2': (
        "*Exemplos Práticos:*\n\n"
        "1. Saída: `print('Olá IFAM')`\n"
        "2. Variáveis: `x = 10`\n"
        "3. Condicionais: `if x > 5: print('Maior')`\n"
        "4. Entrada do usuário: `input()`"
    ),
    '3': (
        "*Estruturas de Repetição:*\n\n"
        "O 'for' percorre sequências:\n"
        "for i in range(5): print(i) → imprime 0, 1, 2, 3, 4\n\n"
        "O 'while' repete enquanto a condição for verdadeira:\n"
        "`x = 0`\n"
        "`while x < 3:`\n"
        "`print(x)`\n"
        "`x += 1`"
    ),
    '4': (
        "*Listas e Funções:*\n\n"
        "Listas armazenam múltiplos valores:\n"
        "`frutas = ['maçã', 'banana', 'uva']`\n"
        "`frutas.append('pera')` → adiciona item\n\n"
        "Funções encapsulam código reutilizável:\n"
        "`def saudacao(nome):`\n"
        "`return 'Olá, ' + nome`"
    )
}

QUIZ_PERGUNTAS = [
    {
        'pergunta': "Qual função é usada para ler a entrada do usuário em Python?\n\nA) read()\nB) input()\nC) get()",
        'correta': 'b',
        'explicacao': "A resposta correta é B) input(). Em Python, `input()` é a função nativa para capturar o que o usuário digita. `read()` é usada para arquivos e `get()` não existe como função padrão."
    },
    {
        'pergunta': "Como se declara uma variável que recebe um número inteiro?\n\nA) x = 10\nB) int x = 10\nC) var x = 10",
        'correta': 'a',
        'explicacao': "A resposta correta é A) x = 10. Python tem tipagem dinâmica: basta atribuir o valor diretamente. As sintaxes `int x` (C/Java) e `var x` (JavaScript) não são válidas em Python."
    },
    {
        'pergunta': "Qual estrutura é usada para repetição?\n\nA) if\nB) else\nC) for",
        'correta': 'c',
        'explicacao': "A resposta correta é C) for. O `for` é a estrutura de repetição que percorre sequências. `if` e `else` são estruturas de decisão, não de repetição."
    },
    {
        'pergunta': "Como se adiciona um item ao final de uma lista em Python?\n\nA) lista.add('item')\nB) lista.append('item')\nC) lista.insert('item')",
        'correta': 'b',
        'explicacao': "A resposta correta é B) lista.append('item'). O método `append()` adiciona ao final. `insert()` exige informar a posição. `add()` não existe em listas — é método de conjuntos (set)."
    },
    {
        'pergunta': "Qual palavra-chave define uma função em Python?\n\nA) function\nB) func\nC) def",
        'correta': 'c',
        'explicacao': "A resposta correta é C) def. Em Python, funções são definidas com `def nome():`. `function` é usada em JavaScript e `func` não é uma palavra-chave válida em Python."
    }
]

def responder_duvida(mensagem):
    # Verificações mais específicas primeiro para evitar conflitos entre termos
    if "while" in mensagem:
        return "O 'while' repete enquanto a condição for verdadeira. Exemplo: `while x < 10: x += 1`."
    elif "for" in mensagem:
        return "O 'for' percorre sequências. Exemplo: `for i in range(5): print(i)` → imprime de 0 a 4."
    elif "função" in mensagem or "funcao" in mensagem or "def" in mensagem:
        return "Funções encapsulam código reutilizável. Exemplo: `def soma(a, b): return a + b`."
    elif "lista" in mensagem or "list" in mensagem:
        return "Listas armazenam múltiplos valores. Exemplo: `frutas = ['maçã', 'banana']`. Use `.append()` para adicionar itens."
    elif "string" in mensagem or "texto" in mensagem:
        return "Strings são sequências de caracteres. Exemplo: `nome = 'Maria'`."
    elif "variável" in mensagem or "variavel" in mensagem:
        return "Variáveis armazenam dados. Exemplo: `nome = 'Maria'`."
    elif "input" in mensagem:
        return "O 'input()' captura o que o usuário digita. Exemplo: `idade = input('Sua idade?')`."
    elif "print" in mensagem:
        return "O 'print()' exibe mensagens na tela. Exemplo: `print('Olá')`."
    elif "if" in mensagem:
        return "O 'if' é usado para condições. Exemplo: `if x > 0: print('Positivo')`."
    return None