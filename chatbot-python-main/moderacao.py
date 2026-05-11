import json
import os

def _carregar_termos_proibidos():
    caminho = os.path.join(os.path.dirname(__file__), 'palavroes.json')
    with open(caminho, encoding='utf-8') as f:
        return json.load(f)

TERMOS_PROIBIDOS = _carregar_termos_proibidos()


def processar_moderacao(user_data, mensagem):
    texto = mensagem.lower()

    if any(termo in texto for termo in TERMOS_PROIBIDOS):
        user_data['infracoes'] += 1
        qtd = user_data['infracoes']

        if qtd == 1:
            # Primeira ocorrência: Apenas aviso
            return ("Atenção: este ambiente é educacional e não permite esse tipo de linguagem.", False)
        elif qtd == 2:
            # Segunda ocorrência: Bloqueio parcial
            user_data['estado'] = 'bloqueio_parcial'
            return ("Segunda ocorrência: Seu acesso foi limitado às funcionalidades.", False)
        elif qtd >= 3:
            # Terceira ocorrência: Bloqueio definitivo
            user_data['bloqueado'] = True
            return ("Bloqueio definitivo: Encerramento da interação.", True)

    return None, False