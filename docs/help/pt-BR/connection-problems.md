---
title: Uma conexão precisa de ajuda
area: troubleshooting
summary: Uma fonte mostra Precisa da sua ajuda, ou para de trazer coisas. O que tentar.
covers: 
code: onboarding.py, dashboard.html
order: 1
---
## Veja o status

Abra **Conexões**. Cada fonte mostra como está:

- **Reconectando automaticamente**: uma falha rápida. Ela tenta de novo sozinha.
- **Aguardando a primeira sincronização**: acabou de conectar. Espere alguns minutos.
- **Lê de novo às** 07:00: X e LinkedIn só leem durante o dia. Não precisa fazer nada.
- **Precisa da sua ajuda**: abra **Detalhes**. Ali diz o que deu errado e o que fazer.

O número em **Conexões** só conta as fontes que precisam da sua ajuda.

## Soluções comuns

- "precisa que você entre de novo": toque em **Reconectar** e entre. Em uma Machine hospedada, você entra ali mesmo e volta para o painel.
- Microsoft ainda configurando o acesso: ela tenta de novo sozinha.
- Slack: confira sua chave de API do Maton e a conexão do Slack no Maton.
- Android: abra o app OpenClaw no celular e permita o acesso às notificações.

No seu próprio computador, `assistant doctor` verifica cada fonte e mostra a solução para cada problema.

Ainda sem solução? Veja [Obter suporte](get-support.md).
