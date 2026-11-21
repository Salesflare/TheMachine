---
title: Conexões
area: connections
summary: Veja suas fontes em um só lugar: confira o status de cada uma, adicione novas fontes ou desconecte as que não usa mais.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 353fdfaa67678a1f
---
## Como estão

A aba **Conexões** lista suas fontes por tipo, com **Logins** e **Verificações** abaixo de uma linha. No celular, toque em um tipo para abri-lo e em **Conexões** para voltar. O tipo que tiver uma fonte que precisa de você aparece primeiro. Cada fonte aparece em uma linha: com o status (Conectada, Aguardando a primeira sincronização, Reconectando automaticamente ou Precisa da sua ajuda) e o que chegou recentemente. Toque nela para abrir o cartão e ver **Detalhes**.

Uma sincronização que falhou, mas foi compensada por uma sincronização posterior, aparece em cinza. Só uma falha que ainda seja a mais recente aparece como um problema, junto com a data da próxima tentativa.

Os números mostram tudo o que a fonte trouxe, incluindo o [histórico](history.md), o que chegou nas últimas 24 horas e o que ainda não foi verificado. Para um calendário, os números mostram os eventos.

Cada fonte recebe o nome da conta, como o serviço a identifica: seu endereço, um perfil do X, um workspace do Slack ou de quem é a conta do Signal ou do Telegram. Abaixo do nome aparece primeiro **Trabalho** ou **Pessoal**, além do endereço ou nome de usuário quando o nome não deixa isso claro. Se houver duas fontes do mesmo tipo com o mesmo nome, também aparece o que as diferencia, como Slack ou X, ou o endereço do workspace.

Cada fonte também informa em uma linha o que ela traz e, se puder realizar ações, que só faz isso depois que você toca em **Enviar** ou confirma.

## Adicionar uma fonte

Abra um tipo (**E-mail**, **Calendário**, **Chat**, **Reuniões**, **Documentos e arquivos**, **Clientes**, **Projetos e código**, **Outras**) e escolha uma fonte em **Adicionar outro** ou abaixo da lista, se ainda não houver nenhuma conectada. As opções gerais aparecem por último: **Outro e-mail** em E-mail, **Link de calendário (ICS)** e **Outro calendário** em Calendário. O Exchange Server lê reuniões, por isso fica em Calendário.

**Sugerido para você** aparece no topo de **Conexões** quando sua Machine identifica um motivo para adicionar uma fonte. O motivo aparece em uma linha: e-mails do Stripe, reuniões do Zoom no seu calendário, mensagens com links para Google Docs ou uma configuração que não foi concluída. A fonte também continua no próprio grupo, marcada como **Sugerido**. Esses dados são contabilizados na sua Machine, nada sai dela. Uma fonte conectada nunca aparece como sugestão.

O Microsoft Teams aparece duas vezes: em **Chat**, para as conversas, e em **Reuniões**, como **Reuniões do Teams**, para as notas das reuniões. As duas opções usam o mesmo login da Microsoft, então conectar uma também conecta a outra.

Na lista, as fontes que você já conectou aparecem com essa indicação e com a conta usada. Selecione uma delas para adicionar outra ao lado: o formulário informa isso e traz um link para a fonte que você já tem.

Preencha as informações necessárias, como uma chave ou um endereço, escolha **Trabalho** com o nome da empresa ou **Pessoal** (para e-mails e calendários, essa opção só aparece quando o endereço não deixa isso claro) e toque em **Conectar**. Em sites como LinkedIn ou X, a página de login abre no navegador da sua Machine e o processo continua automaticamente depois que você entra. GitHub, WhatsApp e Codex mostram um código para inserir. As conversas do Telegram e do Signal mostram um código QR para escanear.

**Cancelar** interrompe a conexão. Saiu antes de terminar? Abra **Conexões** novamente, em qualquer dispositivo, para continuar de onde parou. Depois de conectar, sua Machine começa a ler a fonte na hora e mostra o andamento da primeira sincronização.

Em uma Machine hospedada, você faz login diretamente aqui nas fontes que têm um login próprio: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Escolha **Trabalho** ou **Pessoal** e toque no botão de login da fonte, como **Fazer login com o Google**. Você volta ao formulário, que mostra o resultado. GitHub, WhatsApp, Codex, conversas do Telegram e seu celular Android também mostram o código aqui.

No seu próprio computador, as mesmas fontes permitem fazer login depois que sua Machine estiver pareada com sua conta. Na primeira vez, toque em **Parear esta Machine**. Algumas fontes também oferecem outra opção, como usar seu próprio aplicativo ou uma chave.

**Reconectar**, na fonte ou em **Precisa de você**, abre o mesmo formulário. No seu próprio computador, `assistant connect` faz a mesma coisa em um terminal.

## Trabalho ou pessoal

Cada fonte é classificada como de trabalho, para uma empresa que você informa, ou pessoal. Altere essa opção em **Detalhes**. **Estimado** significa que sua Machine identificou a categoria pelo endereço. As tarefas de trabalho aguardam seus dias de trabalho.

O Google e a Microsoft identificam a categoria dos e-mails e calendários pelo endereço, quando isso fica claro: um provedor de e-mail como Gmail ou Outlook.com indica uma conta pessoal; o domínio da sua equipe indica uma conta de trabalho. Caso contrário, a Machine pergunta uma vez, logo depois que você faz login. **Mudar** permite escolher a categoria. Se os e-mails da conta indicarem outra categoria mais tarde, a tarefa **Aproveite mais a The Machine** pergunta uma vez se você quer alterá-la.

## Recursos

Uma fonte pode trazer sinais (o que chega vira tarefa), realizar ações para suas tarefas (ler um documento, enviar ou responder algo, ou fazer uma alteração depois da sua confirmação), ou fazer as duas coisas. Quando pode fazer as duas coisas, **Detalhes** mostra uma opção para cada recurso: **Traz sinais** e **Pode fazer coisas**. Uma das opções precisa permanecer ativada. Para desativar as duas, desconecte a fonte. Uma conversa só tem a opção **Pode fazer coisas**.

Com **Traz sinais** desativado, a fonte não sincroniza. Com **Pode fazer coisas** desativado, sua Machine nunca lê, cria rascunhos nem altera nada usando essa fonte.

## Remover uma fonte

Abra a fonte, toque em **Detalhes** e depois em **Desconectar**. Ela para de ser lida. O que já trouxe continua disponível. Em uma Machine hospedada, **Desconectar ↗** aparece nas fontes cujo login é gerenciado pela página de configuração (Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce). Toque para abrir essa página.

**Desconectado recentemente** lista as contas do Google, Microsoft, Zoom, Slack, Stripe e Salesforce que você removeu nos últimos 30 dias, com a data da remoção. Enquanto o serviço não confirmar, o status será Pendente e a Machine continuará tentando. Uma conta do Google aparece uma só vez, mesmo quando o Google Meet ou o Google Docs tinha um login próprio. Cada conta aparece no tipo correspondente: uma conta do Google ou da Microsoft em **E-mail**, e uma conta do Slack em **Chat**.

## Logins salvos

Em sites como LinkedIn ou X, marque **Salvar para a próxima vez** ao fazer login. Depois, **Logins** lista essas contas. Se um site desconectar sua Machine, você poderá entrar de novo com um toque. As senhas ficam criptografadas na sua Machine. Toque em **Esquecer** para remover um login.

Um site pode ter várias contas, como **Trabalho** e **Pessoal**. **Salvar como** usa por padrão a categoria da própria tarefa, e **Outro nome…** permite escolher um nome. Uma tarefa faz login com a conta correspondente. Se não der para saber qual conta usar, a caixa de diálogo pergunta uma vez e lembra a escolha para aquela tarefa.

**Logins** lista cada site uma vez, com as contas abaixo: o nome de usuário e um menu com a categoria da conta. Você pode mudar a categoria a qualquer momento nesse menu. Os logins salvos antes da opção de contas aparecer mostram **Trabalho ou pessoal?** até você escolher uma categoria. Se você mudar a categoria de um login usado por uma tarefa, ela fará login novamente.

**Importar** traz logins de um gerenciador de senhas. Escolha uma opção:

- **LastPass**, **Bitwarden** ou **Gerenciador de senhas do Google**: a página de exportação abre no navegador da sua Machine e aparece diretamente na caixa de diálogo, como acontece quando você toca em **Fazer** em uma tarefa. Faça login na página e sua Machine seguirá as etapas para exportar. Uma linha informa o que falta fazer, como digitar sua senha mestra. No celular, a visualização dá zoom no campo de digitação. Se a página estiver diferente do esperado, aparecem as instruções para concluir a exportação manualmente. Sua Machine pega o arquivo, lê uma vez e o exclui.
- **1Password**: exporte um arquivo CSV pelo aplicativo do 1Password em um computador e selecione esse arquivo. Se `op` do 1Password estiver conectado à sua Machine, ela importa os dados de lá (o mesmo vale para `lpass` do LastPass).
- **De um arquivo de exportação**: use um arquivo CSV do 1Password, LastPass, Bitwarden ou Chrome. Exclua o arquivo quando terminar.

Depois, marque os logins que quer manter. Sua Machine nunca faz login no gerenciador de senhas por você, nem digita ou lê sua senha mestra, e nunca mostra a página à assistente. Você digita a senha na própria página.

Um login salvo só é usado no endereço web correspondente: o mesmo site, `https` e porta. Ele não é usado em um endereço parecido nem em outro subdomínio.

## Verificações

**Verificações** mostra como sua Machine lê o que chega: as verificações recentes e o que cada uma encontrou. Consulte [Sem novas tarefas](reviews-paused.md).

Cada conexão tem um artigo próprio nesta seção, com informações sobre o que ela lê e o que pode enviar.
