---
title: Configurações
area: settings
summary: Onde encontrar cada configuração, do modo claro à segurança e à sua conta.
covers: settings:general
code: dashboard.html
order: 1
translated: 31820c6221312d35
---
Abra **Configurações** pela engrenagem na parte de cima. As abas:

- **Conta**: **Seus endereços** (os que contam como seus) e **Sair**, na parte de cima. Em uma Machine hospedada, você também encontra seu plano, faturas, Fleet, amigos, login e dados, com **Cancelar plano** e **Excluir conta** bem no final. Em uma Machine no seu próprio computador, conectada à Network: seu Fleet, nome de usuário, amigos e login, cada um com um link que abre essa parte da sua conta (faça login por lá), e **Excluir conta** no final. Se ainda não estiver conectada: **Entrar na Network**, na parte de cima. Veja [Planos e cobrança](plans-and-billing.md).
- **Geral**: idioma e região, este dispositivo, entrada por voz, navegador da sua Machine, seu Fleet, exportação e importação, além da versão em execução. Sem a aba Conta, **Entrar na Network** aparece no final.
- **Segurança**: Padrão ou Cauteloso. Veja [Níveis de segurança](security-levels.md). Também há **Acesso de suporte**, enquanto estiver ativado: veja [Falar com o suporte](get-support.md#support-access).
- **Atividade**: tudo o que a The Machine fez por você, começando pelo mais recente. Veja [Atividade](activity.md).
- **Notificações**: o que chega até você e onde, além do seu horário de trabalho. Veja [Notificações](notifications.md) e [Horário de trabalho](work-hours.md).
- **Escrita**: assinaturas e seu jeito de escrever. Veja [Escrita](writing.md).
- **Habilidades**: instruções que sua Machine segue. Veja [Habilidades](skills.md).
- **Apps**: os apps da The Machine para seu celular e computador, depois Claude, ChatGPT e outras IAs conectadas, e o que cada uma pode fazer. Veja [O app para celular](mobile-app.md) e [Conectar outras IAs](ai-connections.md).
- **Modelo**: a IA que lê e escreve rascunhos para você, e os limites dela. Veja [Modelo](model.md). Também há **Codex e Claude Code**: veja [Passar para Claude Code ou Codex](hand-to-agent.md). E **Busca por significado**, mais abaixo.

Uma aba sem nada para mostrar fica oculta.

## Geral

- **Idioma e região**: sua **Região** define como datas, horários e números aparecem (24 de out. ou 24 out.). **Formato de hora** define o formato de 12 horas (2:05 PM) ou 24 horas (14:05). As tarefas, mensagens do Telegram, o resumo e as mensagens do Fleet seguem essas configurações. Uma Machine hospedada começa com o fuso horário escolhido no cadastro.
- **Idioma**: English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 ou Русский. O idioma é definido inicialmente pelo idioma do navegador. O painel, a Ajuda, as notificações, o Telegram, o resumo semanal e as tarefas escritas pela sua Machine mudam assim que você escolhe um idioma. Os textos mais antigos continuam como estavam. Seus colegas recebem perguntas do Fleet e da Família no idioma deles, e os rascunhos para outras pessoas continuam no idioma da conversa.
- **Este dispositivo**: **Instalar app**, **Notificações** com **Enviar um teste** e **Modo claro**, somente neste navegador ou celular. Veja [Instale o app e ative as notificações](phone-app.md). No [Omarchy](omarchy.md), também há **Tema do Omarchy**.
- **Entrada por voz**: como o que você diz vira texto e qual voz é usada na Conversa ao vivo. Veja [Entrada por voz](voice-input.md) e [Falar ao vivo](talk-live.md).
- **Abrir o navegador da Machine ↗**: o navegador que sua Machine usa para sites como LinkedIn.
- **Regras do Fleet**: veja [Regras de compartilhamento](sharing-rules.md).
- **Exportar**:
  - **Tudo**: tudo o que sua Machine sabe em um único arquivo criptografado, para transferir ou guardar, e **Importar** para importar um arquivo. Veja [Mudar para outro computador](moving.md).
  - **Conhecimento para outra IA**: o que sua Machine aprendeu, em arquivos que qualquer IA pode ler. Veja [Conhecimento para outra IA](knowledge-export.md).

## Versão

A versão que sua Machine está usando. As atualizações são instaladas automaticamente. Quando uma versão mais recente fica disponível em uma Machine hospedada, **Atualizar agora** instala a atualização imediatamente. O processo leva alguns minutos e seus dados são mantidos.

No seu próprio computador, um temporizador diário instala cada nova versão assinada no Linux. Veja [Rodar no seu próprio computador](self-hosted-setup.md).

## Busca por significado

Em **Configurações**, **Modelo**. Encontra e-mails, mensagens e notas pelo assunto, não apenas pelas palavras usadas. Em uma Machine hospedada, uma pequena IA na própria Machine faz isso, sem enviar nada para outro lugar. O recurso fica ativado a partir de 8 GB de memória. Com 4 GB, ative-o pela chave. Ele usa cerca de meio gigabyte, então uma Machine ocupada pode ficar mais lenta. Se estiver desativado, a preparação de uma tarefa ainda busca mensagens relacionadas pelas palavras.

No seu próprio computador, esse recurso é o bloco `embeddings` em `config.json`. Reinicie a Machine depois de fazer uma alteração.

## Nesta Machine

Quando sua Machine roda no seu próprio computador, algumas tarefas são feitas por lá, em um terminal:

- O arquivo de configurações, `config.json`: todas as configurações em um só lugar. Reinicie a Machine depois de fazer uma alteração.
- `assistant connect`: adicione uma fonte, como `assistant connect gmail` ou `assistant connect outlook`.
- `assistant telegram on` ou `off`: mensagens no Telegram. Veja [Telegram](telegram.md).
- `assistant doctor`: verifica tudo e mostra uma correção para cada problema.

## Seus endereços

Todos os seus endereços encontrados pela Machine: suas contas, aliases do Gmail ou Outlook, seu calendário e seus perfis do Slack e Intercom. E-mails e reuniões de qualquer um deles contam como seus. Use **Remover** nos que não forem seus.

Um endereço compartilhado, como info@ ou um Grupo do Google, nunca conta por conta própria. Um endereço sobre o qual a Machine não tem certeza fica em **Talvez seus**. Escolha uma opção:

- **Meu: só eu respondo**: o endereço conta como seu. E-mails enviados para ele podem virar suas tarefas.
- **Da equipe: outros também respondem**: o endereço não é seu. E-mails enviados apenas para ele não geram tarefas nem rascunhos para você. Mesmo assim, ajudam a preencher o Graph.
- **Não é meu**: o endereço não contará como seu.

Escolha com base em quem responde por ele hoje. Uma caixa de entrada da equipe, como support@, pertence à equipe. Um endereço como partnerships@, ao qual só você responde, é seu. Mude a opção quando outras pessoas também começarem a responder.

Use **Mudar** na linha do endereço para alterar essa opção depois. Seu próprio endereço de login é sempre seu.

### Domínios da sua empresa

Os domínios dos seus próprios endereços contam como domínios da sua empresa. Você também usa outro, como acme.co além de acme.com? Digite-o em **Domínios da sua empresa** e pressione **Adicionar**.

A partir daí, as pessoas desses domínios são colegas, nunca clientes: as conversas delas não aparecem no Graph da equipe, e nenhuma organização é criada para elas. Use **Remover** para excluir um domínio. Não é possível adicionar domínios de e-mail gratuitos, como gmail.com.

Um alias seu do Gmail também pode ser o **From** de um rascunho, quando o Gmail confirma que você pode enviar mensagens usando esse endereço. Veja [Gmail](gmail.md#what-it-can-send).
