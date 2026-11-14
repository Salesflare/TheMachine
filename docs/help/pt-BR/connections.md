---
title: Conexões
area: connections
summary: Suas fontes em um só lugar: veja como cada uma está, adicione outra ou desconecte uma.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 60304f2504ee5676
---
## Como estão

A aba **Conexões** lista suas fontes por tipo, com **Logins** e **Verificações** abaixo de uma linha divisória. No celular, toque em um tipo para abri-lo e em **Conexões** para voltar. Se um tipo tiver uma fonte que precisa de você, ele aparece primeiro. Cada fonte aparece em uma linha, com o status (Conectada, Aguardando a primeira sincronização, Reconectando automaticamente ou Precisa da sua ajuda) e o que chegou recentemente. Toque nela para abrir o cartão e ver **Detalhes**.

Uma sincronização com falha que foi compensada por uma sincronização posterior aparece em cinza. Só uma falha que ainda é a mais recente aparece como problema, junto com a informação de quando haverá outra tentativa.

As contagens mostram tudo o que a fonte trouxe, inclusive o [histórico](history.md), o que chegou nas últimas 24 horas e o que ainda não foi conferido. No caso de um calendário, a contagem é de eventos.

Cada fonte recebe o nome da conta, como o serviço a identifica: seu endereço, um perfil do X, um espaço de trabalho do Slack ou o nome da pessoa a quem pertence no Signal ou no Telegram. Abaixo do nome aparece primeiro **Trabalho** ou **Pessoal**, além do endereço ou nome de usuário, caso ainda não apareça no nome. Se duas fontes do mesmo tipo tiverem o mesmo nome, também aparece uma informação para diferenciá-las, como Slack ou X, ou o endereço do espaço de trabalho.

Cada fonte também informa em uma linha o que traz e, se puder realizar ações, que só age depois que você pressiona **Enviar** ou aprova a ação.

## Adicionar uma fonte

Abra um tipo (**E-mail**, **Calendário**, **Chat**, **Reuniões**, **Documentos e arquivos**, **Clientes**, **Projetos e código**, **Outras**) e escolha uma fonte em **Adicionar outro**, ou abaixo da lista se ainda não houver nenhuma conectada. No fim aparecem as opções para casos específicos: **Outro e-mail** em E-mail, **Link de calendário (ICS)** e **Outro calendário** em Calendário. O Exchange Server lê reuniões, por isso fica em Calendário.

**Sugerido para você** aparece no topo de **Conexões** quando sua Machine identifica um motivo para sugerir uma fonte. Esse motivo é explicado em uma linha: e-mails do Stripe, reuniões do Zoom na sua agenda, mensagens com links para Google Docs ou uma configuração que não foi concluída. A fonte também continua no grupo dela, marcada como **Sugerido**. Essas sugestões são calculadas na sua Machine; nada sai dela. Uma fonte conectada nunca é sugerida.

O Microsoft Teams aparece em dois lugares: em **Chat**, para as conversas, e em **Reuniões**, como **Reuniões do Teams**, para as anotações das reuniões. Ambos usam o mesmo login da Microsoft, então conectar um também conecta o outro.

Se você já conectou uma fonte, ela aparece na lista junto com a conta. Selecione-a para adicionar outra ao lado: o formulário informa isso e inclui um link para a fonte que você já tem.

Preencha as informações necessárias, como uma chave ou um endereço, escolha **Trabalho** e informe a empresa, ou escolha **Pessoal**. E-mails e calendários só perguntam quando o endereço não deixa isso claro. Depois, pressione **Conectar**. Um site como LinkedIn ou X abre a tela de login no navegador da sua Machine e continua automaticamente assim que você entra. GitHub, WhatsApp e Codex mostram um código para você informar. Para conversas do Telegram e do Signal, aparece um código QR para você escanear.

**Cancelar** interrompe a conexão. Saiu antes de terminar? Abra **Conexões** novamente, em qualquer dispositivo, e continue do mesmo ponto. Depois que a fonte se conectar, sua Machine começa a lê-la imediatamente e mostra o andamento da primeira sincronização.

Em uma Machine hospedada, você pode fazer login diretamente aqui nas fontes que têm login próprio: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Escolha **Trabalho** ou **Pessoal** e pressione o botão de login, como **Entrar com Google**. Você volta ao formulário, que mostra o resultado. GitHub, WhatsApp, Codex, conversas do Telegram e seu celular Android também mostram o código aqui.

No seu próprio computador, essas mesmas fontes permitem fazer login depois que sua Machine é pareada com sua conta. Na primeira vez, pressione **Parear esta Machine**. Algumas também oferecem outra opção, como usar seu próprio app ou uma chave.

**Reconectar**, na fonte ou em **Precisa de você**, abre o mesmo formulário. No seu próprio computador, `assistant connect` faz o mesmo em um terminal.

## Trabalho ou pessoal

Cada fonte é classificada como de trabalho, para uma empresa que você informa, ou pessoal. Você pode mudar essa opção em **Detalhes**. **Estimado** significa que sua Machine deduziu a classificação pelo endereço. As tarefas de trabalho aguardam seus dias de trabalho.

O Google e a Microsoft identificam e-mails e calendários pelo endereço quando isso é claro: um provedor de e-mail, como Gmail ou Outlook.com, indica uso pessoal; o domínio da sua equipe indica trabalho. Caso contrário, a Machine pergunta uma vez, logo após você fazer login. **Mudar** permite escolher a classificação. Se os e-mails indicarem depois que a outra opção é a correta, a tarefa **Aproveite mais a The Machine** pergunta uma vez se você quer mudar.

## Recursos

Uma fonte pode trazer sinais, que viram tarefas, realizar ações para suas tarefas, como ler um documento ou enviar, responder ou alterar algo depois da sua aprovação, ou fazer as duas coisas. Se ela fizer as duas coisas, **Detalhes** mostra um botão para cada opção: **Traz sinais** e **Pode fazer coisas**. Uma das opções precisa ficar ativada. Para desativar as duas, desconecte a fonte. Uma conversa só tem a opção **Pode fazer coisas**.

Com **Traz sinais** desativado, a fonte não sincroniza. Com **Pode fazer coisas** desativado, sua Machine nunca lê, cria rascunhos ou altera nada usando essa fonte.

## Remover uma fonte

Abra a fonte, selecione **Detalhes** e depois **Desconectar**. Ela para de ser lida, mas o que já trouxe continua disponível. Em uma Machine hospedada, as fontes cujo login é gerenciado pela página de configuração (Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce) mostram **Desconectar ↗**, que abre essa página.

**Desconectado recentemente** lista as contas do Google, Microsoft, Zoom, Slack, Stripe e Salesforce que você removeu nos últimos 30 dias, com a data da remoção. Até que o serviço confirme, o status aparece como Pendente e a Machine continua tentando. Uma conta do Google aparece uma só vez, mesmo quando o Google Meet ou o Docs tinha um login próprio. Cada conta aparece no tipo correspondente: uma conta do Google ou da Microsoft em **E-mail**, e uma conta do Slack em **Chat**.

## Logins salvos

Em sites como LinkedIn ou X, marque **Salvar para a próxima vez** ao fazer login. Depois, a conta aparece em **Logins**. Se o site desconectar sua Machine, ela poderá entrar novamente com um toque. As senhas ficam criptografadas na sua Machine. **Esquecer** remove uma conta.

## Verificações

**Verificações** mostra como sua Machine lê o que chega: as verificações recentes e o que cada uma encontrou. Consulte [Sem novas tarefas](reviews-paused.md).

Cada conexão tem um artigo próprio nesta seção, que explica o que ela lê e o que pode enviar.
