---
title: Rodar no seu próprio computador
area: getting-started
summary: Instale o app de código aberto no Linux, macOS ou Windows. Grátis, com o seu próprio modelo e os seus próprios dados.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
---
A The Machine é de código aberto (AGPL). No seu próprio computador ela é grátis, e os seus dados ficam lá.

## O que é preciso

- OpenClaw 2026.10.7 ou mais recente. O instalador oferece para instalar.
- Python 3.12 ou mais recente, e Node.js 24 (24.22.1 ou mais recente) ou 26.12.1 ou mais recente, não 25.
- Tailscale, para acessar seu painel pelo celular.
- Sua própria conta de usuário, não root.

## Instalar

No Linux ou macOS (o macOS está em beta):

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

No Windows (beta), ela roda dentro do WSL2. No PowerShell, rode `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex`. Ele configura o WSL2 com Ubuntu e tudo o que o app precisa, depois roda `./install.sh`.

O instalador encontra suas contas, conecta uma por uma e mostra uma prévia da semana passada antes de qualquer coisa ser ativada.

## Depois de instalar

- Adicione fontes com `assistant connect`, ou em **Conexões**, depois **+ Adicionar**, no painel.
- Verifique tudo com `assistant doctor`. Ele mostra uma solução para cada problema.
- As atualizações chegam como versões assinadas.

O guia completo está no repositório: [Primeiros passos](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
