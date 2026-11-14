---
title: Configurações
area: settings
summary: Onde encontrar cada configuração, do modo claro à segurança e à sua conta.
covers: settings:general
code: dashboard.html
order: 1
translated: 00e42f9aeb395d21
---
Abra **Configurações** pela engrenagem no topo. Estas são as abas:

- **Conta**: **Seus endereços** (os que contam como seus) e **Sair**, no topo. Em uma Machine hospedada, também ficam aqui seu plano, faturas, Fleet, amigos, acesso e dados, com **Cancelar plano** e **Excluir conta** no fim da página. Em uma Machine no seu próprio computador, pareada com a Network: seu Fleet, nome de usuário, amigos e acesso, cada um com um link que abre essa parte da sua conta (faça login por lá), e **Excluir conta** no fim da página. Se ainda não estiver pareada: **Entrar na Network**, no topo. Veja [Planos e cobrança](plans-and-billing.md).
- **Geral**: idioma e região, este dispositivo, entrada por voz, o navegador da sua Machine, seu Fleet, exportação e importação, e a versão em execução. Se não houver a aba Conta, **Entrar na Network** aparece no fim.
- **Segurança**: Padrão ou Cuidadoso. Veja [Níveis de segurança](security-levels.md). Também há **Acesso de suporte** enquanto estiver ativado: veja [Como receber suporte](get-support.md#support-access).
- **Atividade**: tudo o que The Machine fez por você, começando pelo mais recente. Veja [Atividade](activity.md).
- **Notificações**: o que você recebe e onde, além do seu horário de trabalho. Veja [Notificações](notifications.md) e [Horário de trabalho](work-hours.md).
- **Escrita**: assinaturas e seu jeito de escrever. Veja [Escrita](writing.md).
- **Habilidades**: instruções que sua Machine segue. Veja [Habilidades](skills.md).
- **Apps**: os apps de The Machine para seu celular e computador, depois Claude, ChatGPT e outras IAs que você conectou, e o que cada uma pode fazer. Veja [O app para celular](mobile-app.md) e [Conectar outras IAs](ai-connections.md).
- **Modelo**: a IA que lê e escreve rascunhos para você, e os limites dela. Veja [Modelo](model.md). Também há **Codex e Claude Code**: veja [Delegar para Claude Code ou Codex](hand-to-agent.md). E **Busca por significado**, abaixo.

Uma aba sem conteúdo fica oculta.

## Geral

- **Idioma e região**: sua **Região** define como datas, horários e números são exibidos (24 de out. ou 24 out.). **Formato de hora** define o formato de 12 horas (2:05 PM) ou 24 horas (14:05). As tarefas, Telegram, o resumo e as mensagens do Fleet seguem essas duas configurações. Uma Machine hospedada usa o fuso horário escolhido no cadastro.
- **Idioma**: English, Nederlands, Français, Deutsch, Español, Italiano ou Português (Brasil). O idioma inicial é o do navegador. O painel, a Ajuda, as notificações, Telegram, o resumo semanal e as tarefas escritas pela sua Machine mudam assim que você escolhe outro idioma. Os textos antigos não mudam. As pessoas da equipe recebem perguntas do Fleet e da Family no próprio idioma, e os rascunhos para outras pessoas continuam no idioma da conversa.
- **Este dispositivo**: **Instalar app**, **Notificações** com **Enviar um teste** e **Modo claro**, somente neste navegador ou celular. Veja [Instalar o app e ativar as notificações](phone-app.md). No [Omarchy](omarchy.md), também há **Tema do Omarchy**.
- **Entrada por voz**: como o que você diz vira texto e qual voz é usada no Talk ao vivo. Veja [Entrada por voz](voice-input.md) e [Talk ao vivo](talk-live.md).
- **Abrir o navegador da Machine ↗**: o navegador que sua Machine usa para sites como LinkedIn.
- **Regras do Fleet**: veja [Regras de compartilhamento](sharing-rules.md).
- **Exportar**:
  - **Tudo**: tudo o que sua Machine sabe em um arquivo criptografado, para transferir ou guardar, e **Importar** para carregar um arquivo. Veja [Mudar para outro computador](moving.md).
  - **Conhecimento para outra IA**: o que sua Machine aprendeu, em arquivos que qualquer IA pode ler. Veja [Exportar conhecimento para outra IA](knowledge-export.md).

## Versão

A versão que sua Machine está executando. As atualizações são instaladas automaticamente. Quando uma versão mais recente fica disponível em uma Machine hospedada, **Atualizar agora** instala a atualização imediatamente. Isso leva alguns minutos, e seus dados são mantidos.

No seu próprio computador, um temporizador diário instala cada nova versão assinada no Linux. Veja [Executar no seu próprio computador](self-hosted-setup.md).

## Busca por significado

Em **Configurações**, **Modelo**. Encontra e-mails, mensagens e notas pelo assunto, não apenas pelas palavras usadas. Em uma Machine hospedada, uma IA pequena faz isso na própria Machine, sem enviar nada para outro lugar. O recurso fica ativado a partir de 8 GB de memória. Com 4 GB, ative-o pela chave. Ele usa cerca de meio gigabyte, então uma Machine ocupada pode ficar mais lenta.

No seu próprio computador, esse recurso é o bloco `embeddings` em `config.json`. Reinicie a Machine depois de fazer uma alteração.

## Nesta Machine

Quando sua Machine é executada no seu próprio computador, algumas tarefas são feitas por lá, no terminal:

- O arquivo de configurações, `config.json`: todas as configurações em um só lugar. Reinicie a Machine depois de fazer uma alteração.
- `assistant connect`: adicione uma fonte, como `assistant connect gmail` ou `assistant connect outlook`.
- `assistant telegram on` ou `off`: mensagens no Telegram. Veja [Telegram](telegram.md).
- `assistant doctor`: verifica tudo e mostra uma correção para cada problema.

## Seus endereços

Todos os seus endereços encontrados pela Machine: suas contas, aliases do Gmail ou Outlook, seu calendário e seus perfis do Slack e Intercom. E-mails e reuniões de qualquer um deles contam como seus. Use **Remover** nos que não forem seus.

Um endereço compartilhado, como info@ ou um Google Group, nunca conta por conta própria. Se a Machine não tiver certeza, o endereço aparece em **Talvez seus**. Escolha uma opção:

- **Meu: só eu respondo**: o endereço conta como seu. E-mails enviados para ele podem virar suas tarefas.
- **Da equipe: outros também respondem**: o endereço não é seu. E-mails enviados somente para ele não geram tarefas nem rascunhos para você. Mesmo assim, eles aparecem no Graph.
- **Não é meu**: o endereço não vai contar como seu.

Escolha de acordo com quem responde hoje. Uma caixa de entrada da equipe, como support@, é da equipe. Um endereço como partnerships@, ao qual só você responde, é seu. Mude a opção quando outras pessoas também começarem a responder.

**Mudar** na linha do endereço permite trocar a opção depois. Seu próprio endereço de acesso sempre conta como seu.

### Domínios da sua empresa

Os domínios dos seus endereços contam como domínios da sua empresa. Você também usa outro, como acme.co além de acme.com? Digite-o em **Domínios da sua empresa** e pressione **Adicionar**.

A partir daí, as pessoas desses domínios são colegas, nunca clientes: as conversas delas ficam fora do Team Graph e nenhuma organização é criada para elas. Use **Remover** para excluir um domínio. Não é possível adicionar domínios de e-mail gratuitos, como gmail.com.

Um alias seu do Gmail também pode aparecer como **De** em um rascunho, se o Gmail confirmar que você pode enviar mensagens por ele. Veja [Gmail](gmail.md#what-it-can-send).
