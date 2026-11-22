---
title: Configurações
area: settings
summary: Onde encontrar cada configuração, do modo claro à segurança e à sua conta.
covers: settings:general
code: dashboard.html
order: 1
translated: 4b0cf1cc99529e64
---
Abra **Configurações** pela engrenagem no topo. As guias:

- **Conta**: **Seus endereços** (os que contam como seus) e **Sair**, no topo. Em uma Machine hospedada, também ficam aqui seu plano, faturas, Fleet, amigos, login e dados, com **Cancelar plano** e **Excluir conta** lá no fim. Em uma Machine no seu próprio computador, pareada com a Network, ficam seu Fleet, nome de usuário, amigos e login, cada um com um link que abre essa parte da sua conta (faça login por lá), e **Excluir conta** no fim. Se ainda não estiver pareada: **Entrar na Network**, no topo. Veja [Planos e cobrança](plans-and-billing.md).
- **Geral**: idioma e região, este dispositivo, entrada por voz, o navegador da sua Machine, seu Fleet, exportação e importação, além da versão em uso. Sem a guia Conta, **Entrar na Network** aparece no fim.
- **Segurança**: Padrão ou Cuidadoso. Veja [Níveis de segurança](security-levels.md). Também há **Acesso de suporte** enquanto estiver ativado: veja [Falar com o suporte](get-support.md#support-access).
- **Atividade**: tudo o que The Machine fez por você, começando pelo mais recente. Veja [Atividade](activity.md).
- **Notificações**: o que chega até você e onde, além do seu horário de trabalho. Veja [Notificações](notifications.md) e [Horário de trabalho](work-hours.md).
- **Escrita**: assinaturas e seu jeito de escrever. Veja [Escrita](writing.md).
- **Habilidades**: instruções que sua Machine segue. Veja [Habilidades](skills.md).
- **Apps**: os apps da The Machine para seu celular e computador; depois Claude, ChatGPT e outras IAs que você conectou, e o que cada uma pode fazer. Veja [O app para celular](mobile-app.md) e [Conectar outras IAs](ai-connections.md).
- **Modelo**: a IA que lê e prepara rascunhos para você, e os limites dela. Veja [Modelo](model.md). Também há **Codex e Claude Code**: veja [Passar para Claude Code ou Codex](hand-to-agent.md). E **Busca por significado**, abaixo.

Uma guia sem conteúdo fica oculta.

## Geral

- **Idioma e região**: sua **Região** define como datas, horários e números aparecem (24 de out. ou 24 out.). **Formato de hora** permite escolher entre 12 horas (2:05 PM) e 24 horas (14:05). As tarefas, mensagens do Telegram, o resumo e as mensagens do Fleet seguem essas configurações. Uma Machine hospedada usa o fuso horário escolhido no cadastro.
- **Idioma**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 ou Русский. O idioma inicial é o do seu navegador. O painel, a Ajuda, as notificações, o Telegram, o resumo semanal e as tarefas que sua Machine escreve mudam assim que você escolhe outro idioma. Os textos antigos não mudam. Os colegas de equipe recebem as perguntas do Fleet e da Família no próprio idioma, e os rascunhos para outras pessoas continuam no idioma da conversa.
- **Este dispositivo**: **Instalar app**, **Notificações**, com **Enviar um teste**, e **Modo claro**, só para este navegador ou celular. Veja [Instalar o app e ativar as notificações](phone-app.md). No [Omarchy](omarchy.md), também há **Tema do Omarchy**.
- **Entrada por voz**: como o que você diz vira texto e qual voz é usada no Falar ao vivo. Veja [Entrada por voz](voice-input.md) e [Falar ao vivo](talk-live.md).
- **Abrir o navegador da Machine ↗**: o navegador que sua Machine usa para sites como o LinkedIn.
- **Regras do Fleet**: veja [Regras de compartilhamento](sharing-rules.md).
- **Exportar**:
  - **Tudo**: tudo o que sua Machine sabe em um arquivo criptografado, para transferir ou guardar, e **Importar** para trazer um arquivo. Veja [Mudar para outro computador](moving.md).
  - **Conhecimento para outra IA**: o que sua Machine aprendeu, em arquivos que qualquer IA pode ler. Veja [Conhecimento para outra IA](knowledge-export.md).

## Versão

A versão que sua Machine usa. As atualizações são instaladas automaticamente. Quando há uma versão mais recente disponível em uma Machine hospedada, **Atualizar agora** instala a atualização na hora. Isso leva alguns minutos, e seus dados são mantidos.

No seu próprio computador, um temporizador diário instala cada nova versão assinada no Linux. Veja [Rodar no seu próprio computador](self-hosted-setup.md).

## Busca por significado

Em **Configurações**, **Modelo**. Ela encontra e-mails, mensagens e notas pelo assunto, não só pelas palavras usadas. Em uma Machine hospedada, uma IA pequena faz isso na própria Machine, sem enviar nada para lugar nenhum. O recurso fica ativado a partir de 8 GB de memória. Com 4 GB, ative-o pela chave. Ele usa cerca de meio gigabyte, então uma Machine ocupada pode ficar mais lenta.

No seu próprio computador, essa opção é o bloco `embeddings` em `config.json`. Reinicie a Machine depois de mudar a configuração.

## Nesta Machine

Quando sua Machine está no seu próprio computador, algumas tarefas são feitas lá, em um terminal:

- O arquivo de configurações, `config.json`: todas as configurações em um só lugar. Reinicie a Machine depois de mudar uma configuração.
- `assistant connect`: adicione uma fonte, como `assistant connect gmail` ou `assistant connect outlook`.
- `assistant telegram on` ou `off`: mensagens no Telegram. Veja [Telegram](telegram.md).
- `assistant doctor`: verifica tudo e mostra uma correção para cada problema.

## Seus endereços

Todos os seus endereços que a Machine encontrou: suas contas, aliases do Gmail ou Outlook, seu calendário e seus perfis do Slack e Intercom. E-mails e reuniões de qualquer um deles contam como seus. Use **Remover** nos que não forem seus.

Um endereço compartilhado, como info@ ou um Google Group, nunca conta por conta própria. Os endereços sobre os quais a Machine tem dúvidas ficam em **Talvez seus**. Escolha uma opção:

- **Meu: só eu respondo**: o endereço conta como seu. E-mails enviados para ele podem virar tarefas.
- **Da equipe: outros também respondem**: o endereço não é seu. E-mails enviados só para ele não geram tarefas nem rascunhos para você. Mesmo assim, eles aparecem no Graph.
- **Não é meu**: o endereço não conta como seu.

Escolha com base em quem responde hoje. Uma caixa de entrada da equipe, como support@, pertence à equipe. Uma como partnerships@, à qual só você responde, é sua. Mude a opção quando outras pessoas também começarem a responder.

Use **Mudar** na linha do endereço para trocar a opção depois. Seu próprio endereço de login sempre conta como seu.

### Domínios da sua empresa

Os domínios dos seus próprios endereços contam como domínios da sua empresa. Você também usa outro, como acme.co além de acme.com? Digite-o em **Domínios da sua empresa** e pressione **Adicionar**.

As pessoas desses domínios passam a ser colegas, nunca clientes: as conversas delas ficam fora do Graph da equipe e nenhuma organização é criada para elas. Use **Remover** para excluir o domínio. Não é possível adicionar domínios de e-mail gratuitos, como gmail.com.

Um alias seu do Gmail também pode aparecer como **De** em um rascunho, se o Gmail confirmar que você pode enviar mensagens por ele. Veja [Gmail](gmail.md#what-it-can-send).
