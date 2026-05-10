from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from moderacao import processar_moderacao
from assunto import MENU_PRINCIPAL, LICOES, QUIZ_PERGUNTAS, responder_duvida

app = Flask(__name__)

# Memória temporária dos usuários
db_usuarios = {}


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
            "Vou te ajudar a aprender Python de forma interativa.\n\n"
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

    # 3. Bloqueio parcial impede acesso ao quiz
    if user['estado'] == 'bloqueio_parcial' and msg_recebida == '3':
        resp.message(
            "Acesso negado ao Quiz devido ao seu comportamento anterior.\n\n"
            + MENU_PRINCIPAL
        )
        return Response(str(resp), mimetype='text/xml')

    # 4. IA básica por palavras-chave
    resposta_ia = responder_duvida(msg_recebida)
    if resposta_ia:
        resp.message(resposta_ia + "\n\n" + MENU_PRINCIPAL)
        return Response(str(resp), mimetype='text/xml')

    # 5. Navegação principal
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

        # Quiz
        elif msg_recebida == '3':
            user['quiz_atual'] = 0
            user['pontuacao'] = 0
            user['erros_quiz'] = 0

            resp.message(QUIZ_PERGUNTAS[0]['pergunta'])
            user['estado'] = 'respondendo_quiz'

        # Status de comportamento
        elif msg_recebida == '4':
            infracoes = user['infracoes']

            if infracoes == 0:
                status = "Regular"
            elif infracoes == 2:
                status = "Alerta (Acesso Limitado)"
            else:
                status = "Aviso Prévio"

            mensagem_status = (
                f"*Seu Status Educacional*\n\n"
                f"Infrações registradas: {infracoes}\n"
                f"Situação atual: {status}\n\n"
                "Lembre-se: Na 3ª infração, o bloqueio é definitivo."
            )

            resp.message(mensagem_status + "\n\n" + MENU_PRINCIPAL)

        # Opção de ajuda
        elif msg_recebida == '5':
            resp.message(
                "Você pode me perguntar diretamente sobre:\n"
                "- variáveis\n"
                "- if\n"
                "- print\n"
                "- input\n\n"
                "Exemplo: 'o que é variável?'\n\n"
                + MENU_PRINCIPAL
            )

        # Opção inválida
        else:
            resp.message("Opção inválida. Escolha uma opção válida.\n\n" + MENU_PRINCIPAL)

    # 6. Fluxo do quiz
    elif user['estado'] == 'respondendo_quiz':

        pergunta_atual = QUIZ_PERGUNTAS[user['quiz_atual']]

        # Resposta correta
        if msg_recebida == pergunta_atual['correta']:
            user['pontuacao'] += 1
            resposta = "Correto! 🎉\n"

        # Resposta incorreta
        else:
            user['erros_quiz'] += 1
            resposta = "Incorreto.\n"

        # Próxima pergunta
        user['quiz_atual'] += 1

        # Ainda existem perguntas
        if user['quiz_atual'] < len(QUIZ_PERGUNTAS):
            resp.message(
                resposta +
                "\nPróxima pergunta:\n" +
                QUIZ_PERGUNTAS[user['quiz_atual']]['pergunta']
            )

        # Quiz finalizado
        else:
            nivel = "Iniciante"

            if user['pontuacao'] == 3:
                nivel = "Avançado"
            elif user['pontuacao'] == 2:
                nivel = "Intermediário"

            mensagem_final = (
                f"Quiz finalizado! 🧠\n"
                f"Pontuação: {user['pontuacao']}/3\n"
                f"Nível: {nivel}\n"
            )

            # Feedback adaptativo
            if user['erros_quiz'] >= 2:
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


if __name__ == "__main__":
    app.run(port=5000)