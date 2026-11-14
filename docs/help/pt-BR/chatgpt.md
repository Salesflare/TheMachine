---
title: ChatGPT
area: connections
summary: Entre com o ChatGPT para executar sua Machine usando seu plano do ChatGPT e importar suas habilidades do ChatGPT.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
translated: fc97be60c0b68336
---
## Para que serve

Entre com o ChatGPT para que sua Machine leia e crie rascunhos com ele usando seu próprio plano do ChatGPT. A Machine não tem IA própria: as solicitações vão direto para a OpenAI, na sua conta e sujeitas aos termos dela.

## Entrar

Em uma Machine hospedada, pressione **Entrar com ChatGPT** na página de configuração e digite no ChatGPT o código exibido. Se você sair da conta depois, pressione **Reconectar ao ChatGPT**.

A OpenAI recusou o código? Abra as [configurações de segurança do ChatGPT](https://chatgpt.com/settings/security), role até o fim e ative a opção **Ativar login com código do dispositivo para Codex, Excel, PowerPoint e Word**. Em seguida, digite o código novamente.

Não encontrou essa opção? Em uma conta de trabalho (Business, Enterprise ou Edu), o administrador do ChatGPT pode ativá-la em [Permissões e funções](https://chatgpt.com/admin/permissions), em **Codex e Trabalho local**.

No seu próprio computador, execute `openclaw models auth login` em um terminal.

## Limites de uso

Um plano do ChatGPT tem um limite de 5 horas e outro semanal. Em **Configurações**, **Modelo** mostra quanto de cada limite já foi usado e quando ele será redefinido. O trabalho em segundo plano é pausado bem antes de um limite, para deixar espaço para seus próprios chats. Quando um limite é atingido, o topo do painel informa quando ele será redefinido. Consulte [Modelo](model.md).

## Importar suas habilidades do ChatGPT

Em **Configurações**, **Habilidades**, pressione **Importar**, escolha **Do ChatGPT** e pressione **Encontrar minhas habilidades**. Só as instruções delas são importadas. Consulte [Habilidades](skills.md).

## Remover

Escolha outro modelo na página de configuração (ou, no seu próprio computador, entre em outra conta de provedor da mesma forma). Para revogar o acesso pelo lado da OpenAI, saia da sessão nas configurações de segurança do ChatGPT.
