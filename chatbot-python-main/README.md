PASSO 1
instale as bibliotecas necessárias:
pip install flask twilio

PASSO 2
execute o servidor Flask:
python main.py

PASSO 3
Autenticação e Instalação no ngrok:
1. Instale o ngrok (ngrok.com) faça o login
2. No menu lateral, clique em Your Authtoken.
3. Copie o código (token) que aparece lá.
4. No terminal digite: 
./ngrok config add-authtoken SEU_TOKEN_AQUI

PASSO 4
Em um segundo terminal, inicie o Ngrok na porta 5000:
ngrok http 5000

PASSO 5
Entre no Console do Twilio.
No menu lateral, vá em Messaging > Try it out > Send a WhatsApp Message.
Clique na aba Sandbox Settings.
No campo "WHEN A MESSAGE COMES IN", cole o link do Ngrok e não esqueça de colocar /bot no final.
Ficará assim: https://seu-link-aqui.ngrok-free.app/bot
Verifique se ao lado está selecionado HTTP POST.
Importante: Vá até o fim da página e clique no botão azul Save.
