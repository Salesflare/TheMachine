---
title: Uma conexão precisa de ajuda
area: troubleshooting
summary: Uma fonte mostra Precisa da sua ajuda ou para de trazer dados. Veja o que fazer.
covers:
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: cc4b227abd053022
---
## Confira o status

Abra **Conexões**. Cada fonte mostra como está:

- **Reconectando automaticamente**: uma falha rápida. Ela tenta de novo sozinha.
- **Aguardando a primeira sincronização**: acabou de conectar. Aguarde alguns minutos.
- **Lê novamente às** 07:00: X e LinkedIn só fazem leituras durante o dia. Não é preciso fazer nada.
- **Ainda não configurado**: ninguém fez login nessa fonte por aqui ainda. Toque em **Conectar**. Ela começa em até um minuto.
- **Precisa da sua ajuda**: abra **Detalhes**. Lá você encontra o que deu errado e como resolver.
- **Celular desconectado**: seu celular Android não está se conectando à sua Machine. Abra o app OpenClaw nele.

Uma fonte que não traz nada por mais tempo que o normal mostra **Aguardando uma nova sincronização**. A mensagem desaparece sozinha quando uma sincronização é concluída.

O número exibido em **Conexões** conta apenas as fontes que precisam da sua ajuda.

## Soluções comuns

- “Faça login no Google novamente” (ou na Microsoft): basta tocar em **Reconectar** para restaurar todas as fontes dessa conta, como Gmail e Calendário.
- “precisa que você faça login novamente”: toque em **Reconectar** e faça login.
- “precisa de um programa que não está neste computador”: execute o comando do cartão da fonte em um terminal nesse computador. Ele informa o que instalar ou encontra um programa que mudou de lugar.
- A configuração de acesso da Microsoft ainda está em andamento: ela tenta novamente sozinha.
- Slack: toque em **Reconectar**. Conectou usando uma chave do Maton? Confira a chave e a conexão do Slack no Maton.
- Android: abra o app OpenClaw no celular e permita que ele acesse as notificações.

No seu próprio computador, `assistant doctor` verifica todas as fontes e informa como resolver cada problema.

Ainda não conseguiu resolver? Veja [Falar com o suporte](get-support.md).
