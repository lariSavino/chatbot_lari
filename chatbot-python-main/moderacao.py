def processar_moderacao(user_data, mensagem):
    texto = mensagem.lower()
    # Lista de termos proibidos (ajuste conforme necessário)
    TERMOS_PROIBIDOS = ['palavrao', 'ofensa', 'sua burra', 'se mata'] 

    if any(termo in texto for termo in TERMOS_PROIBIDOS):
        user_data['infracoes'] += 1
        qtd = user_data['infracoes']

        if qtd == 1:
            # Primeira ocorrência: Apenas aviso [cite: 39, 40]
            return ("Atenção: este ambiente é educacional e não permite esse tipo de linguagem.", False)
        elif qtd == 2:
            # Segunda ocorrência: Bloqueio parcial [cite: 42, 43]
            user_data['estado'] = 'bloqueio_parcial'
            return ("Segunda ocorrência: Seu acesso foi limitado às funcionalidades.", False)
        elif qtd >= 3:
            # Terceira ocorrência: Bloqueio definitivo [cite: 45, 46]
            user_data['bloqueado'] = True
            return ("Bloqueio definitivo: Encerramento da interação.", True)
    
    return None, False