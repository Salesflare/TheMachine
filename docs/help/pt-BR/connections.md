---
title: Conexões
area: connections
summary: Suas fontes em um só lugar: veja como cada uma está, adicione uma nova ou desconecte uma.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 38d682b69cab758d
---
## Como estão

A guia **Conexões** lista suas fontes por categoria, com **Logins** e **Verificações** abaixo de uma linha. No celular, toque em uma categoria para abri-la e em **Conexões** para voltar. A categoria com uma fonte que precisa de você aparece primeiro. Cada fonte aparece em uma linha: com o status (Conectada, Aguardando a primeira sincronização, Reconectando automaticamente ou Precisa da sua ajuda) e o que recebeu recentemente. Toque na fonte para ver o cartão e **Detalhes**.

Uma sincronização com falha que foi compensada por uma sincronização posterior aparece em cinza. Só uma falha que continua sendo a mais recente aparece como problema, com a data da próxima tentativa.

Os números mostram tudo o que a fonte trouxe, inclusive o [histórico](history.md), o que chegou nas últimas 24 horas e o que ainda não foi verificado. No caso de um calendário, os números mostram os eventos.

Cada fonte recebe o nome da conta, como o serviço a identifica: seu endereço, um perfil no X, um espaço de trabalho no Slack ou a pessoa responsável pela conta no Signal ou no Telegram. Abaixo do nome, aparece primeiro **Trabalho** ou **Pessoal**, além do endereço ou nome de usuário quando o nome não deixa isso claro. Se duas fontes da mesma categoria tiverem o mesmo nome, também aparece a informação que as diferencia, como Slack ou X, ou o endereço do espaço de trabalho.

Cada fonte também explica em uma linha o que traz e, se puder realizar ações, informa que só age depois que você pressiona **Enviar** ou aprova a ação.

## Adicionar uma fonte

Abra uma categoria (**E-mail**, **Calendário**, **Chat**, **Reuniões**, **Documentos e arquivos**, **Clientes**, **Projetos e código**, **Outras**) e escolha uma fonte em **Adicionar outro** ou abaixo da lista, se ainda não houver nenhuma conectada. As opções gerais aparecem no fim: **Outro e-mail** em E-mail, e **Link de calendário (ICS)** e **Outro calendário** em Calendário. O Exchange Server lê reuniões, por isso fica em Calendário.

**Sugerido para você** aparece no topo de **Conexões** quando sua Machine identifica um motivo para adicionar uma fonte. O motivo é explicado em uma linha: e-mails do Stripe, reuniões do Zoom no seu calendário, mensagens com links para Google Docs ou uma configuração que não foi concluída. A fonte também continua no grupo correspondente, marcada como **Sugerido**. Essas informações são calculadas na sua Machine, nada sai dela. Uma fonte conectada nunca é sugerida.

O Microsoft Teams aparece em dois lugares: em **Chat**, para as conversas, e em **Reuniões** como **Reuniões do Teams**, para as anotações das reuniões. Os dois usam o mesmo login da Microsoft, então, ao conectar um, você conecta o outro também.

Se uma fonte já estiver conectada, isso aparece na lista junto com a conta. Selecione-a para adicionar outra ao lado: o formulário informa isso e mostra um link para a fonte que você já tem.

Preencha as informações necessárias, como uma chave ou um endereço, selecione **Trabalho** com o nome da empresa ou **Pessoal** e pressione **Conectar**. Nos serviços como LinkedIn ou X, a página de login abre no navegador da sua Machine e o processo continua automaticamente depois que você entra. GitHub, WhatsApp e Codex mostram um código para você inserir. Para conversas do Telegram e do Signal, aparece um QR code para escanear.

**Cancelar** interrompe a adição. Saiu antes de terminar? Abra **Conexões** novamente, em qualquer dispositivo, para continuar de onde parou. Depois de conectada, sua Machine começa a ler a fonte na hora e mostra como está indo a primeira sincronização.

Em uma Machine hospedada, você faz login aqui mesmo nas fontes que têm login próprio: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Selecione **Trabalho** ou **Pessoal** e pressione o botão de login, como **Entrar com Google**. Você volta a este formulário, que mostra o resultado. GitHub, WhatsApp, Codex, conversas do Telegram e seu celular Android também mostram o código aqui.

No seu próprio computador, essas mesmas fontes permitem fazer login depois que sua Machine é pareada com sua conta. Na primeira vez, pressione **Parear esta Machine**. Algumas fontes também oferecem outro método, como seu próprio app ou uma chave.

**Reconectar**, na fonte ou em **Precisa de você**, abre o mesmo formulário. No seu próprio computador, `assistant connect` faz o mesmo no terminal.

## Trabalho ou pessoal

Cada fonte é classificada como de trabalho, para uma empresa que você informa, ou pessoal. Você pode mudar essa classificação em **Detalhes**. **Inferido** significa que sua Machine identificou a categoria pelo endereço. Tarefas de trabalho ficam aguardando seus dias de trabalho.

Os e-mails e calendários do Google e da Microsoft usam o endereço para definir a categoria quando isso está claro: um provedor de e-mail como Gmail ou Outlook.com indica **Pessoal**; o domínio da sua equipe indica **Trabalho**. Se não estiver claro, a Machine pergunta uma vez, logo depois que você faz login. **Mudar** permite definir a categoria. Se os e-mails indicarem depois que a categoria é outra, a tarefa **Aproveite mais a The Machine** pergunta uma vez se você quer mudar.

## Recursos

Uma fonte pode trazer sinais, que viram tarefas, realizar ações para suas tarefas, como ler um documento ou enviar, responder ou alterar algo depois que você aprovar, ou fazer as duas coisas. Quando faz as duas coisas, **Detalhes** tem um controle para cada opção: **Traz sinais** e **Pode fazer coisas**. Uma delas precisa ficar ativada. Para desativar as duas, desconecte a fonte. No caso de um chat, só existe **Pode fazer coisas**.

Com **Traz sinais** desativado, a fonte não sincroniza. Com **Pode fazer coisas** desativado, sua Machine nunca lê, cria rascunhos ou altera nada nessa fonte.

## Remover uma fonte

Abra a fonte, selecione **Detalhes** e depois **Desconectar**. Ela para de ler os dados. O que já trouxe continua disponível. Em uma Machine hospedada, as fontes cujo login é gerenciado pela página de configuração (Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce) mostram **Desconectar ↗**, que abre essa página.

**Desconectado recentemente** lista as contas do Google, Microsoft, Zoom, Slack, Stripe e Salesforce que você removeu nos últimos 30 dias, além da data. Até o serviço confirmar a remoção, o status aparece como Pendente e a Machine continua tentando. Uma conta do Google aparece uma só vez, inclusive quando o Google Meet ou o Docs tinha um login próprio. Cada conta aparece na categoria correspondente: contas do Google ou da Microsoft em **E-mail**, e contas do Slack em **Chat**.

## Logins salvos

Em sites como LinkedIn ou X, marque **Salvar para a próxima vez** ao fazer login. Depois, **Logins** lista essas contas. Quando um site desconectar sua Machine, ela entra de novo com um toque. As senhas ficam criptografadas na sua Machine. **Esquecer** remove um login.

Um site pode ter várias contas, como **Trabalho** e **Pessoal**. **Salvar como** começa com a categoria da própria tarefa, e **Outro nome…** permite dar um nome à conta. A tarefa usa o login da conta correspondente. Se não estiver claro qual é a conta certa, a janela pergunta uma vez e memoriza sua escolha para aquela tarefa.

**Logins** lista cada site uma vez, com as contas abaixo: o nome de usuário e um menu com a categoria de cada conta. Você pode mudar a categoria pelo menu quando quiser. Os logins salvos antes da criação das categorias mostram **Trabalho ou pessoal?** até você escolher uma. Se você mudar a categoria de um login usado por uma tarefa, a tarefa pergunta de novo qual conta usar.

**Importar** adiciona logins de um gerenciador de senhas. Escolha uma opção:

- **LastPass**, **Bitwarden** ou **Gerenciador de senhas do Google**: a página de exportação abre no navegador da sua Machine. Entre na conta; sua Machine continua até a exportação. Uma linha informa o que falta fazer, como digitar a senha mestra. No celular, a página aumenta o zoom até o campo de digitação. Se a página estiver diferente do esperado, aparecem as instruções para concluir manualmente. Sua Machine encontra o arquivo, lê uma vez e o exclui.
- **1Password**: exporte um arquivo CSV pelo app do 1Password em um computador e selecione o arquivo. Se `op` do 1Password estiver conectado à sua Machine, os dados vêm de lá (o mesmo vale para `lpass` do LastPass).
- **De um arquivo de exportação**: use um arquivo CSV do 1Password, LastPass, Bitwarden ou Chrome. Exclua o arquivo quando terminar.

Depois, marque quais logins quer manter. Sua Machine nunca entra no gerenciador de senhas por você, nunca digita nem lê a senha mestra e nunca mostra a página para a assistente: você mesma digita a senha na página.

Um login salvo só pode ser usado no próprio endereço da web: no mesmo site, com o mesmo `https` e a mesma porta. Ele não é usado em um endereço parecido nem em outro subdomínio.

## Verificações

**Verificações** mostra como sua Machine lê o que chega: as verificações recentes e o que cada uma encontrou. Veja [Nenhuma tarefa nova](reviews-paused.md).

Cada conexão tem um artigo próprio nesta seção, com informações sobre o que ela lê e o que pode enviar.
