---
title: Uma conexão precisa de ajuda
area: troubleshooting
summary: Uma fonte mostra Precisa da sua ajuda ou para de trazer dados. Veja o que tentar.
covers: 
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: 1c530fc2b291d640
---
## Confira o status

Abra **Conexões**. Cada fonte mostra como está:

- **Reconectando automaticamente**: uma falha rápida. A fonte tenta novamente sozinha.
- **Aguardando a primeira sincronização**: acabou de conectar. Aguarde alguns minutos.
- **Lê novamente às** 07:00: X e LinkedIn só fazem leituras durante o dia. Não é preciso fazer nada.
- **Precisa da sua ajuda**: abra **Detalhes**. Lá você encontra o que deu errado e o que fazer.
- **Celular desconectado**: seu celular Android não está se comunicando com sua Machine. Abra o app OpenClaw nele.

Uma fonte que não traz nada por mais tempo que o normal deixa de aparecer como conectada. O status desaparece sozinho assim que novos itens chegam.

O número em **Conexões** conta apenas as fontes que precisam da sua ajuda.

## Soluções comuns

- "Faça login no Google novamente" (ou na Microsoft): uma vez em **Reconectar** basta para restabelecer todas as fontes dessa conta, como Gmail e Agenda.
- "você precisa fazer login novamente": pressione **Reconectar** e faça login.
- A Microsoft ainda está configurando o acesso: ela tenta novamente sozinha.
- Slack: pressione **Reconectar**. Conectou usando uma chave do Maton? Confira a chave e a conexão do Slack no Maton.
- Android: abra o app OpenClaw no celular e permita o acesso às notificações.

No seu próprio computador, `assistant doctor` verifica todas as fontes e explica como resolver cada problema.

Ainda não conseguiu? Acesse [Fale com o suporte](get-support.md).
