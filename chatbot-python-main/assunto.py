MENU_PRINCIPAL = (
    "*Tutor IA - Python*\n\n"
    "Escolha uma opção:\n"
    "1. Introdução ao Python\n"
    "2. Exemplos Práticos\n"
    "3. Desafio (Quiz)\n"
    "4. Status de Comportamento"
) 

LICOES = {
    '1': "Python é uma linguagem de alto nível focada em legibilidade. É amplamente usada em IA e Data Science.",
    '2': (
        "*Exemplos Práticos:*\n\n"
        "1. Saída: `print('Olá IFAM')`\n"
        "2. Variáveis: `x = 10`\n"
        "3. Condicionais: `if x > 5: print('Maior')`\n"
        "4. Entrada do usuário: `input()`"
    ) 
}

QUIZ_PERGUNTAS = [
    {
        'pergunta': "Qual função é usada para ler a entrada do usuário em Python?\n\nA) read()\nB) input()\nC) get()",
        'correta': 'b'
    },
    {
        'pergunta': "Como se declara uma variável que recebe um número inteiro?\n\nA) x = 10\nB) int x = 10\nC) var x = 10",
        'correta': 'a'
    },
    {
        'pergunta': "Qual estrutura é usada para repetição?\n\nA) if\nB) else\nC) for",
        'correta': 'c'
    }
]

def responder_duvida(mensagem):
    if "variável" in mensagem or "variavel" in mensagem:
        return "Variáveis armazenam dados. Exemplo: `nome = 'Maria'`."
    elif "if" in mensagem:
        return "O 'if' é usado para condições. Exemplo: `if x > 0: print('Positivo')`."
    elif "print" in mensagem:
        return "O 'print()' exibe mensagens na tela. Exemplo: `print('Olá')`."
    elif "input" in mensagem:
        return "O 'input()' captura o que o usuário digita. Exemplo: `idade = input('Sua idade?')`."
    return None