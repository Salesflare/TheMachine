---
title: Conexões
area: connections
summary: Veja suas fontes em um só lugar: confira como cada uma está, adicione outra ou desconecte uma fonte.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 9f2a2162fe015e0b
---
## Como estão

A aba **Conexões** lista suas fontes por tipo, com **Logins** e **Verificações** abaixo de uma linha. No celular, toque em um tipo para abri-lo e em **Conexões** para voltar. O tipo que tiver uma fonte que precisa de você aparece primeiro. Cada fonte é uma linha: mostra como está (Conectada, Aguardando a primeira sincronização, Reconectando automaticamente ou Precisa da sua ajuda) e o que chegou recentemente. Toque nela para ver o cartão e **Detalhes**.

Uma sincronização que falhou, mas foi compensada por uma posterior, aparece em cinza. Só uma falha que ainda é a mais recente aparece como problema, junto com a data da próxima tentativa.

As contagens mostram tudo o que a fonte trouxe, inclusive o que está no [histórico](history.md), o que chegou nas últimas 24 horas e o que ainda não foi verificado. Uma agenda conta os eventos.

Cada fonte tem o nome da conta, como o serviço a identifica: seu endereço, um perfil do X, um espaço de trabalho do Slack ou de quem é a conta do Signal ou do Telegram. Abaixo do nome aparece primeiro **Trabalho** ou **Pessoal**, além do endereço ou nome de usuário, se o nome já não mostrar essa informação. Se duas fontes do mesmo tipo tiverem o mesmo nome, elas também mostram o que as diferencia, como Slack ou X, ou o endereço do espaço de trabalho.

Cada fonte também explica em uma linha o que traz e, se puder realizar ações, informa que só age depois que você toca em **Enviar** ou confirma.

## Adicionar uma fonte

Abra um tipo (**E-mail**, **Calendário**, **Chat**, **Reuniões**, **Documentos e arquivos**, **Clientes**, **Projetos e código**, **Outras**) e escolha uma fonte em **Adicionar outro**, ou abaixo da lista quando ainda não houver nenhuma conectada. As opções genéricas aparecem por último: **Outro e-mail** em E-mail, **Link de calendário (ICS)** e **Outro calendário** em Calendário. O Exchange Server importa reuniões, por isso fica em Calendário.

**Sugerido para você** aparece no topo de **Conexões** quando sua Machine identifica um motivo para sugerir uma fonte. O motivo aparece em uma linha: e-mails do Stripe, reuniões do Zoom na sua agenda, mensagens com links para Google Docs ou uma configuração que não foi concluída. A fonte também continua no próprio grupo, marcada como **Sugerido**. Essa contagem é feita na sua Machine, nada sai dela. Uma fonte conectada nunca é sugerida.

O Microsoft Teams aparece duas vezes: em **Chat**, para os chats, e em **Reuniões**, como **Reuniões do Teams**, para as anotações das reuniões. Os dois usam o mesmo login da Microsoft, então conectar um também conecta o outro.

Se você já conectou uma fonte, isso aparece na lista junto com a conta. Selecione-a para adicionar outra ao lado. O formulário informa isso e tem um link para a fonte que você já conectou.

Preencha os dados necessários (uma chave, um endereço), escolha **Trabalho** e informe a empresa, ou escolha **Pessoal** (e-mails e agendas só perguntam quando o endereço não deixa isso claro). Depois, toque em **Conectar**. Um site como LinkedIn ou X abre a tela de login no navegador da sua Machine e continua sozinho depois que você entra. GitHub, WhatsApp e Codex mostram um código para inserir, e os chats do Telegram e do Signal mostram um código QR para escanear.

**Cancelar** interrompe a adição. Saiu antes de terminar? Abra **Conexões** de novo, em qualquer dispositivo, para continuar de onde parou. Depois de conectar, sua Machine começa a ler a fonte na hora e mostra o andamento da primeira sincronização.

Em uma Machine hospedada, as fontes com login próprio permitem entrar aqui mesmo: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Escolha **Trabalho** ou **Pessoal** e toque no botão de login, como **Entrar com o Google**. Você volta a este formulário, que mostra o resultado. GitHub, WhatsApp, Codex, os chats do Telegram e seu celular Android também mostram o código aqui.

No seu próprio computador, você faz login nessas mesmas fontes depois de parear sua Machine com sua conta. Na primeira vez, toque em **Parear esta Machine**. Algumas fontes também oferecem outra opção, como usar seu próprio app ou uma chave.

**Reconectar**, em uma fonte ou em **Precisa de você**, abre o mesmo formulário. No seu próprio computador, `assistant connect` faz o mesmo em um terminal.

## Trabalho ou pessoal

Cada fonte é classificada como de trabalho (para uma empresa que você informa) ou pessoal. Altere essa opção em **Detalhes**. **Estimado** significa que sua Machine identificou a categoria pelo endereço. As tarefas de trabalho aguardam seus dias úteis.

O Gmail e o Microsoft Mail e Calendário identificam a categoria pelo endereço quando ela é clara: um provedor de e-mail como Gmail ou Outlook.com indica uso pessoal; o domínio da sua equipe indica trabalho. Caso contrário, a pergunta aparece uma vez, logo depois que você entra. **Mudar** permite definir a categoria. Se os e-mails indicarem outra categoria mais tarde, a tarefa **Aproveite mais a The Machine** perguntará uma vez se você quer alterá-la.

## Recursos

Uma fonte pode trazer sinais (o que chega vira tarefas), realizar ações para suas tarefas (ler um documento, enviar, responder ou alterar algo depois da sua aprovação), ou fazer as duas coisas. Se fizer as duas coisas, **Detalhes** mostra uma opção para cada recurso: **Traz sinais** e **Pode fazer coisas**. Um deles precisa continuar ativado. Para desativar os dois, desconecte a fonte. Um chat só tem **Pode fazer coisas**.

Com **Traz sinais** desativado, a fonte não sincroniza. Com **Pode fazer coisas** desativado, sua Machine nunca lê, cria rascunhos ou altera nada usando essa fonte.

## Remover uma fonte

Abra a fonte, toque em **Detalhes** e depois em **Desconectar**. Ela para de ser lida. O que já trouxe continua disponível. Em uma Machine hospedada, as fontes cujo login fica salvo na página de configuração (Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce) mostram **Desconectar ↗**, que abre essa página.

**Desconectado recentemente** lista as contas do Google, Microsoft, Zoom, Slack, Stripe e Salesforce que você removeu nos últimos 30 dias, com as datas. Até o serviço confirmar, a conta aparece como Pendente e a Machine continua tentando. Uma conta do Google aparece uma vez, mesmo quando o Google Meet ou o Docs tinham um login próprio. Cada conta aparece no seu tipo: uma conta do Google ou da Microsoft em **E-mail**, e uma conta do Slack em **Chat**.

## Logins salvos

Para sites como LinkedIn ou X, marque **Salvar para a próxima vez** ao entrar. Depois, eles aparecem em **Logins**. Quando um site desconecta sua Machine, ela entra de novo com um toque. As senhas ficam criptografadas na sua Machine. **Esquecer** remove um login salvo.

Um site pode ter várias contas, como **Trabalho** e **Pessoal**. **Salvar como** começa pela categoria da própria tarefa, e **Outro nome…** permite escolher um nome. Uma tarefa usa o login da conta adequada. Quando isso não está claro, uma janela pergunta uma vez qual conta usar e guarda essa escolha para a tarefa.

**Logins** mostra cada site uma vez, com as contas abaixo: o nome de usuário e um menu com a categoria. Você pode alterá-la ali quando quiser. Os logins salvos antes de haver contas mostram **Trabalho ou pessoal?** até você escolher uma opção. Se você mudar a categoria de um login, a tarefa que o usava perguntará de novo qual conta usar.

**Importar** adiciona logins de um gerenciador de senhas: um arquivo CSV exportado do 1Password, LastPass, Bitwarden ou Chrome, ou diretamente do 1Password e do LastPass usando as ferramentas de linha de comando, se você estiver conectado a eles neste computador. Você escolhe quais quer manter. Sua Machine nunca entra no gerenciador de senhas nem pede a senha mestra. Apague o arquivo exportado quando terminar.

Um login salvo só é usado no endereço web correspondente: o mesmo site, `https` e a mesma porta. Não é usado em um endereço parecido nem em outro subdomínio.

## Verificações

**Verificações** mostra como sua Machine lê o que chega: as verificações recentes e o que cada uma encontrou. Consulte [Nenhuma tarefa nova](reviews-paused.md).

Cada conexão tem um artigo próprio nesta seção, que explica o que ela lê e o que pode enviar.
