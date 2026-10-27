---
title: ChatGPT
area: connections
summary: Entre com o ChatGPT para rodar sua Machine no seu plano do ChatGPT e importe suas habilidades do ChatGPT.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
---
## Para que serve

O ChatGPT é o modelo que lê e escreve rascunhos para você, no seu próprio plano do ChatGPT. The Machine não tem IA própria. As solicitações da sua Machine vão do seu servidor direto para a OpenAI, na sua conta e sob os termos dela.

## Entrar

Em uma Machine hospedada, na sua página de configuração, clique em **Entrar com o ChatGPT** e digite no ChatGPT o código que aparece. Foi desconectado depois? Clique em **Reconectar o ChatGPT**.

A OpenAI recusa o código? Abra suas [configurações de segurança do ChatGPT](https://chatgpt.com/settings/security), role até o fim e ative a opção "Enable device code sign-in for Codex, Excel, PowerPoint, and Word". Depois digite o código de novo.

Não está lá? Em uma conta de trabalho (Business, Enterprise ou Edu), um administrador do workspace ativa em [Permissions & roles](https://chatgpt.com/admin/permissions), em "Codex and Work Local". Uma opção vale para os dois códigos: se o código do seu modelo funcionou, o do Codex também funciona.

No seu próprio computador, conecte o OpenClaw ao ChatGPT com `openclaw models auth login`.

## Limites de uso

Um plano do ChatGPT tem um limite de 5 horas e um semanal. **Configurações** e depois **Modelo** mostra quanto de cada um já foi usado e quando ele é renovado. O trabalho em segundo plano para bem antes de um limite, para sobrar espaço para os seus próprios chats. Quando um limite é atingido, o topo do painel diz qual e quando ele é renovado, e o trabalho continua depois. Veja [Modelo](model.md).

## Importar suas habilidades do ChatGPT

Em **Configurações**, **Habilidades**, clique em **Importar**, escolha **Do ChatGPT** e clique em **Encontrar minhas habilidades**. Ela lê as habilidades que você criou, no navegador da sua Machine. Só as instruções são importadas. Veja [Habilidades](skills.md).

## Remover

Escolha outro modelo na sua página de configuração ou conecte o OpenClaw a outro provedor. Para encerrar o acesso do lado da OpenAI, saia da sessão nas configurações de segurança do ChatGPT.
