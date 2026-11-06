---
title: Uma conexão precisa de ajuda
area: troubleshooting
summary: Uma fonte mostra Precisa da sua ajuda, ou para de trazer coisas. O que tentar.
covers: 
code: onboarding.py, dashboard.html, assistant.py
order: 1
---
## Veja o status

Abra **Conexões**. Cada fonte mostra como está:

- **Reconectando automaticamente**: uma falha rápida. Ela tenta de novo sozinha.
- **Aguardando a primeira sincronização**: acabou de conectar. Espere alguns minutos.
- **Lê de novo às** 07:00: X e LinkedIn só leem durante o dia. Não precisa fazer nada.
- **Precisa da sua ajuda**: abra **Detalhes**. Ali diz o que deu errado e o que fazer.
- **Celular desconectado**: o celular não chega ao OpenClaw. Abra o app OpenClaw nele.

Uma fonte que continua falhando e não traz nada novo por horas, mais do que seu período calmo de sempre, não aparece como conectada. Isso se resolve sozinho assim que algo novo chega.

O número em **Conexões** só conta as fontes que precisam da sua ajuda.

## Soluções comuns

- "Entre de novo no Google" (ou Microsoft): uma linha por conta. Um só **Reconectar** traz de volta todas as fontes dela, como Gmail e Agenda.
- "precisa que você entre de novo": toque em **Reconectar** e entre. Em uma Machine hospedada, você entra ali mesmo e volta para o painel.
- Microsoft ainda configurando o acesso: ela tenta de novo sozinha.
- Slack: confira sua chave de API do Maton e a conexão do Slack no Maton.
- Android: abra o app OpenClaw no celular e permita o acesso às notificações.

No seu próprio computador, `assistant doctor` verifica cada fonte e mostra a solução para cada problema.

Ainda sem solução? Veja [Obter suporte](get-support.md).
