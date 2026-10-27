---
title: Zoom
area: connections
summary: Os resumos e transcrições do AI Companion das reuniões que você organiza. Ele só lê.
covers: connector:zoom
code: connectors/zoom.py, meeting_notes.py, onboarding.py
site: Connect Zoom, More sources, Remove, Sign in with Zoom
---
## O que ele lê

O resumo do AI Companion de cada reunião do Zoom que você organiza, e a transcrição quando o Zoom tem uma: os últimos 7 dias quando você conecta, e depois as novas conforme chegam. Ele também lê seu nome e e-mail no Zoom, para saber de quem são as reuniões.

Os resumos precisam de um plano pago do Zoom, do AI Companion ativado durante a reunião e de nenhuma criptografia de ponta a ponta.

## O que ele faz com eles

Cada resumo é associado à reunião na sua agenda. Suas revisões então usam o resumo para os follow-ups dessa reunião, e uma divisão de follow-ups no Fleet já vem preenchida com quem faz o quê. Você confere e edita primeiro. Nada é enviado até você enviar.

## O que ele pode fazer

Ele só lê. Ele nunca cria, muda ou exclui nada no Zoom, e só vê as suas próprias reuniões. Seu login do Zoom fica guardado na sua própria Machine.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup e vá em **Mais fontes**.
2. Abra Zoom, escolha trabalho ou pessoal, e clique em **Conectar Zoom**.
3. Entre no Zoom e autorize a The Machine. Ela é feita pela Salesflare.

Ou no painel: **Conexões**, **+ Adicionar**, escolha Zoom e clique em **Entrar com Zoom**. Quando terminar, você volta para o painel.

No seu próprio computador, depois que ele estiver [pareado com sua conta](fleet.md): abra **Conexões**, depois **+ Adicionar**, escolha Zoom e clique em **Entrar com Zoom**.

## Remover

- No painel: **Conexões**, abra Zoom, **Detalhes** e depois **Desconectar**. Ele para de ler. O que ele já trouxe continua.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Desinstalar no Zoom

Entre em marketplace.zoom.us, abra Manage, depois Added Apps, e remova a The Machine. Ela não consegue mais ler nada. O que ela já trouxe fica na sua Machine até você excluir: veja [Cancelar e excluir](cancel-and-delete.md).
