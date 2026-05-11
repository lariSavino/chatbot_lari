from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from moderacao import processar_moderacao
from assunto import MENU_PRINCIPAL, LICOES, QUIZ_PERGUNTAS, responder_duvida

app = Flask(__name__)

# Memória temporária dos usuários
db_usuarios = {}

OPCOES_VALIDAS_QUIZ = ['a', 'b', 'c']


@app.route("/bot", methods=['POST'])
def bot():
    msg_recebida = request.values.get('Body', '').strip().lower()
    whatsapp_id = request.values.get('From')

    resp = MessagingResponse()

    # Inicializa novo usuário
    if whatsapp_id not in db_usuarios:
        db_usuarios[whatsapp_id] = {
            'estado': 'menu',
            'infracoes': 0,
            'bloqueado': False,
            'quiz_atual': 0,
            'pontuacao': 0,
            'erros_quiz': 0
        }

        resp.message(
            "Olá! Eu sou o Tutor IA de Python 🤖\n\n"
            "Vou te ajudar a aprender Python de forma interativa.\n"
            "Você também pode me perguntar diretamente sobre conceitos básicos de Python.\n\n"
            + MENU_PRINCIPAL
        )
        return Response(str(resp), mimetype='text/xml')

    user = db_usuarios[whatsapp_id]

    # 1. Verifica bloqueio definitivo
    if user['bloqueado']:
        resp.message("Você foi bloqueado definitivamente por violar as regras.")
        return Response(str(resp), mimetype='text/xml')

    # 2. Moderação obrigatória
    aviso, banir = processar_moderacao(user, msg_recebida)
    if aviso:
        resp.message(aviso)
        return Response(str(resp), mimetype='text/xml')

    # 3. Bloqueio parcial impede acesso ao quiz e às lições avançadas
    if user['estado'] == 'bloqueio_parcial' and msg_recebida in ['3', '4', '5']:
        resp.message(
            "Acesso negado devido ao seu comportamento anterior. "
            "Apenas as lições básicas (Opções 1 e 2) estão disponíveis.\n\n"
            + MENU_PRINCIPAL
        )
        return Response(str(resp), mimetype='text/xml')

    # 4. Fluxo do quiz — processado antes das palavras-chave para não haver conflito
    if user['estado'] == 'respondendo_quiz':

        pergunta_atual = QUIZ_PERGUNTAS[user['quiz_atual']]
        total = len(QUIZ_PERGUNTAS)

        # Valida se a resposta é uma opção válida
        if msg_recebida not in OPCOES_VALIDAS_QUIZ:
            resp.message(
                "Resposta inválida. Por favor, responda apenas com A, B ou C.\n\n"
                + pergunta_atual['pergunta']
            )
            return Response(str(resp), mimetype='text/xml')

        # Resposta correta
        if msg_recebida == pergunta_atual['correta']:
            user['pontuacao'] += 1
            resposta = "Correto! 🎉\n"
        # Resposta incorreta
        else:
            user['erros_quiz'] += 1
            resposta = "Incorreto.\n" + pergunta_atual['explicacao'] + "\n"

        # Próxima pergunta
        user['quiz_atual'] += 1

        # Ainda existem perguntas
        if user['quiz_atual'] < total:
            prox = user['quiz_atual'] + 1
            resp.message(
                resposta +
                f"\nPergunta {prox} de {total}:\n" +
                QUIZ_PERGUNTAS[user['quiz_atual']]['pergunta']
            )

        # Quiz finalizado
        else:
            pontos = user['pontuacao']
            nivel = "Iniciante"

            if pontos == total:
                nivel = "Avançado"
            elif pontos >= total - 1:
                nivel = "Intermediário"

            mensagem_final = (
                f"Quiz finalizado! 🧠\n"
                f"Pontuação: {pontos}/{total}\n"
                f"Nível: {nivel}\n"
            )

            # Feedback adaptativo por quantidade de erros
            if user['erros_quiz'] >= 3:
                mensagem_final += (
                    "\nRecomendação: Revise as lições de Introdução (Opção 1), "
                    "Exemplos Práticos (Opção 2), Repetição (Opção 3) e Listas e Funções (Opção 4) "
                    "para fortalecer sua base."
                )
            elif user['erros_quiz'] >= 1:
                mensagem_final += (
                    "\nRecomendação: Revise os exemplos práticos (Opção 2) "
                    "para fortalecer sua base."
                )

            resp.message(mensagem_final + "\n\n" + MENU_PRINCIPAL)

            # Reset do quiz
            user['estado'] = 'menu'
            user['quiz_atual'] = 0
            user['pontuacao'] = 0
            user['erros_quiz'] = 0

        return Response(str(resp), mimetype='text/xml')

    # 5. IA básica por palavras-chave
    resposta_ia = responder_duvida(msg_recebida)
    if resposta_ia:
        resp.message(resposta_ia + "\n\n" + MENU_PRINCIPAL)
        return Response(str(resp), mimetype='text/xml')

    # 6. Navegação principal
    if msg_recebida in ['menu', 'voltar', 'inicio', 'início', 'home', 'oi', 'olá', 'ola']:
        user['estado'] = 'menu'
        resp.message(MENU_PRINCIPAL)

    elif user['estado'] == 'menu':

        # Introdução
        if msg_recebida == '1':
            resp.message(LICOES['1'] + "\n\n" + MENU_PRINCIPAL)

        # Exemplos práticos
        elif msg_recebida == '2':
            resp.message(LICOES['2'] + "\n\n" + MENU_PRINCIPAL)

        # Estruturas de Repetição
        elif msg_recebida == '3':
            resp.message(LICOES['3'] + "\n\n" + MENU_PRINCIPAL)

        # Listas e Funções
        elif msg_recebida == '4':
            resp.message(LICOES['4'] + "\n\n" + MENU_PRINCIPAL)

        # Quiz
        elif msg_recebida == '5':
            user['quiz_atual'] = 0
            user['pontuacao'] = 0
            user['erros_quiz'] = 0
            user['estado'] = 'respondendo_quiz'

            resp.message(
                f"Pergunta 1 de {len(QUIZ_PERGUNTAS)}:\n" +
                QUIZ_PERGUNTAS[0]['pergunta']
            )

        # Status de comportamento
        elif msg_recebida == '6':
            infracoes = user['infracoes']

            if infracoes == 0:
                status = "Regular"
            elif infracoes == 1:
                status = "Aviso Prévio"
            else:
                status = "Alerta (Acesso Limitado)"

            mensagem_status = (
                f"*Seu Status Educacional*\n\n"
                f"Infrações registradas: {infracoes}\n"
                f"Situação atual: {status}\n\n"
                "Lembre-se: Na 3ª infração, o bloqueio é definitivo."
            )

            resp.message(mensagem_status + "\n\n" + MENU_PRINCIPAL)

        # Opção de ajuda
        elif msg_recebida == '7':
            resp.message(
                "Você pode me perguntar diretamente sobre:\n"
                "- variáveis\n"
                "- if\n"
                "- print\n"
                "- input\n"
                "- for\n"
                "- while\n"
                "- lista\n"
                "- função / def\n"
                "- string\n\n"
                "Exemplo: 'o que é variável?'\n\n"
                + MENU_PRINCIPAL
            )

        # Opção inválida
        else:
            resp.message("Opção inválida. Escolha uma opção válida.\n\n" + MENU_PRINCIPAL)

    return Response(str(resp), mimetype='text/xml')


if __name__ == "__main__":
    app.run(port=5000)