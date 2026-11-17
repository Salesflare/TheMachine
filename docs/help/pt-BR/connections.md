---
title: Conexões
area: connections
summary: Suas fontes em um só lugar: veja como cada uma está, adicione uma nova ou desconecte uma.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: ec53596a1636fee7
---
## Como estão

A aba **Conexões** lista suas fontes por tipo, com **Logins** e **Verificações** abaixo de uma linha. No celular, toque em um tipo para abrir e em **Conexões** para voltar. Um tipo com uma fonte que precisa de você aparece primeiro. Cada fonte é uma linha: mostra como está (Conectada, Aguardando a primeira sincronização, Reconectando automaticamente ou Precisa da sua ajuda) e o que recebeu recentemente. Toque nela para abrir o cartão e ver **Detalhes**.

Uma sincronização com falha que foi compensada por uma sincronização posterior aparece em cinza. Só uma falha que ainda é a mais recente aparece como problema, com o horário da próxima tentativa.

Os totais mostram tudo o que ela trouxe, incluindo o [histórico](history.md), o que chegou nas últimas 24 horas e o que ainda não foi verificado. Um calendário conta os eventos.

Cada fonte recebe o nome da conta, como o serviço a identifica: seu endereço, um perfil do X, um espaço de trabalho do Slack ou de quem é a conta no Signal ou no Telegram. Abaixo do nome aparece **Trabalho** ou **Pessoal**, seguido do endereço ou nome de usuário, se o nome não deixar isso claro. Duas fontes do mesmo tipo com o mesmo nome também mostram o que as diferencia, como Slack ou X, ou o endereço do espaço de trabalho.

Cada fonte também informa em uma frase o que traz e, se puder realizar ações, que só faz isso depois que você toca em **Enviar** ou aprova a ação.

## Adicionar uma fonte

Abra um tipo (**E-mail**, **Calendário**, **Chat**, **Reuniões**, **Documentos e arquivos**, **Clientes**, **Projetos e código**, **Outras**) e escolha uma fonte em **Adicionar outro** ou abaixo da lista, se ainda não houver nenhuma conectada. As opções genéricas ficam no fim: **Outro e-mail** em E-mail, **Link de calendário (ICS)** e **Outro calendário** em Calendário. O Exchange Server lê reuniões, por isso fica em Calendário.

**Sugerido para você** aparece no topo de **Conexões** quando sua Machine identifica um motivo para recomendar uma fonte. O motivo é mostrado em uma frase: e-mails da Stripe, reuniões do Zoom no calendário, mensagens com links para Google Docs ou uma configuração que não foi concluída. A fonte também continua no próprio grupo, marcada como **Sugerido**. Esses dados são contabilizados na sua Machine, nada sai dela. Uma fonte conectada nunca é sugerida.

O Microsoft Teams aparece duas vezes: em **Chat**, para as conversas, e em **Reuniões**, como **Reuniões do Teams**, para as anotações das reuniões. As duas opções usam o mesmo login da Microsoft. Ao conectar uma, você conecta a outra.

A lista indica quando uma fonte já está conectada e mostra a conta. Selecione-a para adicionar outra ao lado: o formulário informa isso e traz um link para a que você já tem.

Preencha as informações necessárias, como uma chave ou um endereço, escolha **Trabalho** e informe a empresa, ou escolha **Pessoal**. Para e-mails e calendários, essa opção só aparece quando o endereço não deixa isso claro. Depois, toque em **Conectar**. Um site como LinkedIn ou X abre a página de login no navegador da sua Machine e continua automaticamente quando você entra. GitHub, WhatsApp e Codex mostram um código para inserir. Os chats do Telegram e do Signal mostram um código QR para escanear.

**Cancelar** interrompe a adição. Saiu antes de terminar? Abra **Conexões** novamente, em qualquer dispositivo, para continuar de onde parou. Depois de conectada, sua Machine começa a ler a fonte na hora e mostra o andamento da primeira sincronização.

Em uma Machine hospedada, fontes com login próprio permitem entrar aqui mesmo: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Escolha **Trabalho** ou **Pessoal** e toque no botão de login, como **Fazer login com Google**. Você volta para este formulário, que mostra o resultado. GitHub, WhatsApp, Codex, chats do Telegram e seu celular Android também mostram o código aqui.

No seu próprio computador, essas mesmas fontes permitem entrar depois que sua Machine estiver pareada com sua conta. Na primeira vez, toque em **Parear esta Machine**. Algumas também oferecem outra opção, como seu próprio app ou uma chave.

**Reconectar**, em uma fonte ou em **Precisa de você**, abre o mesmo formulário. No seu próprio computador, `assistant connect` faz o mesmo em um terminal.

## Trabalho ou pessoal

Cada fonte é classificada como de trabalho, para uma empresa que você informa, ou pessoal. Altere essa opção em **Detalhes**. **Estimado** significa que sua Machine identificou a categoria pelo endereço. As tarefas de trabalho aguardam seus dias de trabalho.

Os e-mails e calendários do Google e da Microsoft usam o endereço para definir a categoria, quando ela está clara: um provedor de e-mail, como Gmail ou Outlook.com, é pessoal; o domínio da sua equipe é de trabalho. Caso contrário, a Machine pergunta uma vez, logo depois que você entrar. **Mudar** permite escolher a categoria. Se mais tarde os e-mails indicarem outra categoria, a tarefa **Aproveite mais a The Machine** pergunta uma vez se você quer alterá-la.

## O que cada fonte pode fazer

Uma fonte pode trazer sinais, que viram tarefas, realizar ações para suas tarefas, como ler um documento ou enviar, responder ou alterar algo depois da sua aprovação, ou fazer as duas coisas. Quando pode fazer as duas coisas, **Detalhes** mostra um botão para cada opção: **Traz sinais** e **Pode fazer coisas**. Uma delas precisa ficar ativada. Para desativar as duas, desconecte a fonte. Um chat só tem a opção **Pode fazer coisas**.

Com **Traz sinais** desativada, a fonte não sincroniza. Com **Pode fazer coisas** desativada, sua Machine nunca lê, cria rascunhos ou altera nada usando essa fonte.

## Remover uma fonte

Abra a fonte, toque em **Detalhes** e depois em **Desconectar**. Ela para de ser lida. O que já trouxe continua disponível. Em uma Machine hospedada, as fontes cujo login é gerenciado pela página de configuração, como Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce, mostram **Desconectar ↗**, que abre essa página.

**Desconectado recentemente** lista as contas do Google, Microsoft, Zoom, Slack, Stripe e Salesforce que você removeu nos últimos 30 dias, além da data. Enquanto o serviço não confirmar, aparece **Pendente** e a Machine continua tentando. Uma conta do Google aparece uma só vez, mesmo que o Google Meet ou o Docs tivesse um login próprio. Cada fonte aparece no tipo correspondente: uma conta do Google ou da Microsoft em **E-mail**, e uma conta do Slack em **Chat**.

## Logins salvos

Em sites como LinkedIn ou X, marque **Salvar para a próxima vez** ao entrar. Depois, **Logins** lista esses sites e, quando um deles desconecta sua Machine, ela entra de novo com um toque. As senhas ficam criptografadas na sua Machine. Toque em **Esquecer** para remover um login.

Um site pode ter várias contas, como **Trabalho** e **Pessoal**. **Salvar como** começa pela categoria da própria tarefa, e **Outro nome…** permite dar um nome personalizado. Uma tarefa entra com a conta adequada. Quando não fica claro qual usar, uma janela pergunta uma vez e lembra sua escolha para aquela tarefa.

**Logins** lista cada site uma vez, com as contas abaixo. Os logins salvos antes de haver contas aparecem como **Padrão** até você escolher a categoria.

**Importar** adiciona logins de um gerenciador de senhas: um arquivo CSV exportado do 1Password, LastPass, Bitwarden ou Chrome, ou uma importação direta do 1Password e LastPass pelas ferramentas de linha de comando, quando você já tiver entrado nelas neste computador. Marque quais logins quer manter. Sua Machine nunca entra no gerenciador de senhas nem pede a senha mestra. Apague o arquivo exportado quando terminar.

Um login salvo só é usado no endereço web correspondente: mesmo site, `https` e porta. Não é usado em um endereço parecido nem em outro subdomínio.

## Verificações

**Verificações** mostra como sua Machine lê o que chega: as verificações recentes e o que cada uma encontrou. Consulte [Nenhuma tarefa nova](reviews-paused.md).

Cada conexão tem um artigo próprio nesta seção, com informações sobre o que ela lê e o que pode enviar.
