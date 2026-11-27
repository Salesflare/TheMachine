---
title: Configurações
area: settings
summary: Onde encontrar cada configuração, do modo claro à segurança e à sua conta.
covers: settings:general
code: dashboard.html
order: 1
translated: 012a9e1fdd9e1752
---
Abra **Configurações** pela engrenagem na parte superior. As abas:

- **Conta**: **Seus endereços** (os que contam como seus) e **Sair**, na parte superior. Em uma Machine hospedada, também ficam aqui seu plano, as faturas, o Fleet, os amigos, o login e os dados, com **Cancelar plano** e **Excluir conta** lá no fim. Em uma Machine no seu próprio computador, pareada com a Network: seu Fleet, nome de usuário, amigos e login, cada um com um link que abre essa parte da sua conta (faça login por lá), e **Excluir conta** na parte inferior. Se ainda não estiver pareada: **Entrar na Network**, na parte superior. Veja [Planos e cobrança](plans-and-billing.md).
- **Geral**: idioma e região, este dispositivo, entrada por voz, o navegador da sua Machine, seu Fleet, exportação e importação, e a versão em uso. Sem a aba Conta, **Entrar na Network** aparece no final.
- **Segurança**: Padrão ou Cuidadoso. Veja [Níveis de segurança](security-levels.md). Também há **Acesso de suporte** enquanto estiver ativado: veja [Falar com o suporte](get-support.md#support-access).
- **Atividade**: tudo o que a The Machine fez por você, começando pelo mais recente. Veja [Atividade](activity.md).
- **Notificações**: o que chega até você e onde, além do seu horário de trabalho. Veja [Notificações](notifications.md) e [Horário de trabalho](work-hours.md).
- **Escrita**: assinaturas e seu jeito de escrever. Veja [Escrita](writing.md).
- **Habilidades**: guias que sua Machine segue. Veja [Habilidades](skills.md).
- **Apps**: os apps da The Machine para celular e computador, seguidos por Claude, ChatGPT e outras IAs que você conectou, e o que cada uma pode fazer. No computador, a lista inclui o app para Windows, Mac e Linux, com **Baixar** para cada um, e indica qual é **Este computador**. Veja [O app para celular](mobile-app.md), [O app para computador](desktop-app.md) e [Conectar outras IAs](ai-connections.md).
- **Modelo**: a IA que lê e escreve para você, e os limites dela. Veja [Modelo](model.md). Também há **Codex e Claude Code**: veja [Passar para Claude Code ou Codex](hand-to-agent.md). E **Busca por significado**, abaixo.

Uma aba sem conteúdo fica oculta.

## Geral

- **Idioma e região**: **Região** define como datas, horários e números aparecem (24 de out. ou 24 out.). **Formato de hora** escolhe entre 12 horas (2:05 PM) e 24 horas (14:05). Tarefas, mensagens do Telegram, o resumo e as mensagens do Fleet seguem essas duas configurações. Em uma Machine hospedada, o fuso horário inicial é o que você escolheu ao se cadastrar.
- **Idioma**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 ou Русский. O idioma inicial é o do seu navegador. O painel, a Ajuda, as notificações, o Telegram, o resumo semanal e as tarefas escritas pela sua Machine mudam assim que você escolhe um idioma. Os textos antigos continuam como estavam. Seus colegas recebem perguntas do Fleet e da Família no idioma deles, e os rascunhos para outras pessoas continuam no idioma da conversa.
- **Este dispositivo**: **Instalar app**, **Notificações** com **Enviar um teste** e **Modo claro**, apenas neste navegador ou celular. Veja [Instale o app e ative as notificações](phone-app.md). No [Omarchy](omarchy.md), também há **Tema do Omarchy**.
- **Entrada por voz**: como sua fala vira texto e qual é a voz do Talk ao vivo. Veja [Entrada por voz](voice-input.md) e [Converse ao vivo](talk-live.md).
- **Abrir o navegador da Machine ↗**: o navegador que sua Machine usa em sites como o LinkedIn.
- **Regras do Fleet**: veja [Regras de compartilhamento](sharing-rules.md).
- **Exportar**:
  - **Tudo**: tudo o que sua Machine sabe em um arquivo criptografado, para transferir ou guardar, e **Importar** para trazer um arquivo. Veja [Mudar para outro computador](moving.md).
  - **Conhecimento para outra IA**: o que sua Machine aprendeu, em arquivos que qualquer IA pode ler. Veja [Conhecimento para outra IA](knowledge-export.md).

## Versão

A versão que sua Machine está usando. As atualizações são instaladas automaticamente. Quando uma versão mais nova fica pronta em uma Machine hospedada, **Atualizar agora** instala a atualização imediatamente. Isso leva alguns minutos, e seus dados permanecem intactos.

No seu próprio computador, uma tarefa agendada diária instala cada nova versão assinada no Linux. Veja [Rodar no seu próprio computador](self-hosted-setup.md).

## Busca por significado

Em **Configurações**, **Modelo**. A busca encontra e-mails, mensagens e notas pelo assunto, não só pelas palavras usadas. Em uma Machine hospedada, uma IA pequena faz isso na própria Machine, sem enviar nada para lugar nenhum. O recurso já vem ativado a partir de 8 GB de memória. Com 4 GB, ative-o pela chave. Ele usa cerca de meio gigabyte, então uma Machine ocupada pode ficar mais lenta. Com o recurso desativado, a preparação de uma tarefa ainda procura mensagens relacionadas usando palavras.

No seu próprio computador, esse recurso fica no bloco `embeddings` em `config.json`. Reinicie a Machine depois de fazer uma alteração.

## Na sua Machine

Quando sua Machine roda no seu próprio computador, algumas tarefas são feitas por lá, no terminal:

- O arquivo de configurações, `config.json`: todas as configurações em um só lugar. Reinicie a Machine depois de fazer uma alteração.
- `assistant connect`: adiciona uma fonte, como `assistant connect gmail` ou `assistant connect outlook`.
- `assistant telegram on` ou `off`: mensagens no Telegram. Veja [Telegram](telegram.md).
- `assistant doctor`: verifica tudo e mostra uma solução para cada problema.

## Seus endereços

Todos os seus endereços encontrados pela Machine: suas contas, aliases do Gmail ou Outlook, seu calendário e seus perfis do Slack e Intercom. E-mails e reuniões de qualquer um deles contam como se fossem seus. Use **Remover** nos que não forem seus.

Um endereço compartilhado, como info@ ou um Grupo do Google, nunca conta por conta própria. Um endereço sobre o qual a Machine não tem certeza fica em **Talvez seus**. Escolha uma opção:

- **Meu: só eu respondo**: o endereço conta como seu. E-mails enviados para ele podem virar tarefas.
- **Da equipe: outros também respondem**: o endereço não é seu. E-mails enviados apenas para ele não geram tarefas nem rascunhos para você. Ainda assim, eles preenchem o Graph.
- **Não é meu**: o endereço não conta como seu.

Escolha com base em quem responde hoje. Uma caixa de entrada da equipe, como support@, pertence à equipe. Um endereço como partnerships@, que só você responde, é seu. Mude a opção quando outras pessoas também começarem a responder.

**Mudar** na linha do endereço permite alterar essa opção depois. Seu próprio endereço de login é sempre seu.

### Domínios da sua empresa

Os domínios dos seus próprios endereços contam como domínios da sua empresa. Usa outro também, como acme.co além de acme.com? Digite-o em **Domínios da sua empresa** e pressione **Adicionar**.

As pessoas desses domínios passam a ser consideradas colegas, nunca clientes: as conversas delas ficam fora do Graph da equipe, e nenhuma organização é criada para o domínio. Use **Remover** para excluí-lo. Não é possível adicionar domínios de e-mail gratuitos, como gmail.com.

Um alias seu do Gmail também pode aparecer como **De** em um rascunho, quando o Gmail confirma que você pode enviar e-mails por ele. Veja [Gmail](gmail.md#what-it-can-send).
