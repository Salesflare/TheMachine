---
title: Uma conexão precisa da sua ajuda
area: troubleshooting
summary: Uma fonte mostra Precisa da sua ajuda ou para de trazer informações. Veja o que fazer.
covers:
code: onboarding.py, dashboard.html, assistant.py
order: 1
translated: c07a7f214b1e4deb
---
## Confira o status

Abra **Conexões**. Cada fonte mostra como está:

- **Reconectando automaticamente**: uma falha rápida. Ela tenta de novo sozinha.
- **Aguardando a primeira sincronização**: acabou de conectar. Aguarde alguns minutos.
- **Lê novamente às** 07:00: X e LinkedIn só leem informações durante o dia. Não é preciso fazer nada.
- **Precisa da sua ajuda**: abra **Detalhes**. Lá você encontra o que deu errado e o que fazer.
- **Celular desconectado**: seu celular Android não está se comunicando com sua Machine. Abra o app OpenClaw nele.

Uma fonte que não traz informações por mais tempo que o normal mostra **Aguardando uma nova sincronização**. O aviso desaparece sozinho quando uma sincronização é concluída.

O número em **Conexões** conta apenas as fontes que precisam da sua ajuda.

## Soluções comuns

- "Faça login no Google novamente" (ou na Microsoft): uma opção **Reconectar** restaura todas as fontes dessa conta, como Gmail e Calendário.
- "precisa que você faça login novamente": pressione **Reconectar** e faça login.
- A Microsoft ainda está configurando o acesso: ela tenta novamente sozinha.
- Slack: pressione **Reconectar**. Conectou com uma chave Maton? Confira a chave e a conexão do Slack no Maton.
- Android: abra o app OpenClaw no celular e permita o acesso às notificações.

No seu próprio computador, `assistant doctor` verifica todas as fontes e informa como resolver cada problema.

Ainda não conseguiu resolver? Consulte [Falar com o suporte](get-support.md).
