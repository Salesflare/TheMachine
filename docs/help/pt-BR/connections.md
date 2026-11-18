---
title: Conexões
area: connections
summary: Veja todas as suas fontes em um só lugar: confira como estão, adicione uma nova ou desconecte uma.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 809547189ccfa026
---
## Como estão

A guia **Conexões** lista suas fontes por tipo, com **Logins** e **Verificações** abaixo de uma linha divisória. No celular, toque em um tipo para abri-lo e em **Conexões** para voltar. O tipo com uma fonte que precisa de você aparece primeiro. Cada fonte aparece em uma linha: mostra como está (Conectada, Aguardando a primeira sincronização, Reconectando automaticamente ou Precisa da sua ajuda) e o que chegou recentemente. Toque nela para abrir o cartão e ver **Detalhes**.

Uma falha de sincronização compensada por uma sincronização posterior aparece em cinza. Só uma falha que ainda seja a mais recente aparece como problema, junto com a data da próxima tentativa.

As contagens mostram tudo o que a fonte trouxe, inclusive o que está no [histórico](history.md), o que chegou nas últimas 24 horas e o que ainda não foi verificado. Para um calendário, a contagem mostra os eventos.

Cada fonte tem o nome da conta, como o serviço a identifica: seu endereço, um perfil do X, um espaço de trabalho do Slack ou de quem é a conta do Signal ou do Telegram. Abaixo do nome aparece primeiro **Trabalho** ou **Pessoal**, além do endereço ou nome de usuário quando isso não fica claro pelo nome. Se duas fontes do mesmo tipo tiverem o mesmo nome, elas também mostram o que as diferencia, como Slack ou X, ou o endereço do espaço de trabalho.

Cada fonte também explica em uma linha o que traz e, se puder realizar ações, informa que só faz isso depois que você toca em **Enviar** ou aprova a ação.

## Adicionar uma fonte

Abra um tipo (**E-mail**, **Calendário**, **Chat**, **Reuniões**, **Documentos e arquivos**, **Clientes**, **Projetos e código**, **Outras**) e escolha uma fonte em **Adicionar outro**, ou abaixo da lista quando ainda não houver nenhuma conectada. As opções genéricas aparecem no fim: **Outro e-mail** em E-mail, e **Link de calendário (ICS)** e **Outro calendário** em Calendário. O Exchange Server lê reuniões, por isso fica em Calendário.

**Sugerido para você** aparece no topo de **Conexões** quando sua Machine identifica um motivo para adicionar uma fonte. O motivo é explicado em uma linha: e-mails do Stripe, reuniões do Zoom na sua agenda, mensagens com links para Google Docs ou uma configuração que não foi concluída. A fonte também continua no próprio grupo, marcada como **Sugerido**. Essa contagem é feita na sua Machine, nada sai dela. Uma fonte conectada nunca aparece como sugestão.

O Microsoft Teams aparece duas vezes: em **Chat**, para as conversas, e em **Reuniões**, como **Reuniões do Teams**, para as anotações das reuniões. As duas opções usam o mesmo login da Microsoft, então conectar uma também conecta a outra.

Se você já conectou uma fonte, ela aparece na lista com a conta correspondente. Selecione-a para adicionar outra ao lado. O formulário informa isso e inclui um link para a fonte já conectada.

Preencha as informações necessárias, como uma chave ou um endereço, escolha **Trabalho** com o nome da empresa ou **Pessoal** e toque em **Conectar**. Para e-mails e calendários, essa escolha só é solicitada quando o endereço não deixa isso claro. Um site como LinkedIn ou X abre a página de login no navegador da sua Machine e continua automaticamente quando você entra. GitHub, WhatsApp e Codex mostram um código para inserir. Para conversas do Telegram e do Signal, aparece um código QR para escanear.

Toque em **Cancelar** para interromper a conexão. Saiu antes de terminar? Abra **Conexões** novamente, em qualquer dispositivo, e continue de onde parou. Depois de conectar, sua Machine começa a ler a fonte na hora e mostra o andamento da primeira sincronização.

Em uma Machine hospedada, as fontes com login próprio permitem que você entre diretamente aqui: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Escolha **Trabalho** ou **Pessoal** e toque no botão de login, como **Fazer login com Google**. Você volta a este formulário, que mostra o resultado. GitHub, WhatsApp, Codex, conversas do Telegram e seu celular Android também mostram o código aqui.

No seu próprio computador, você entra nessas mesmas fontes depois de parear sua Machine com sua conta. Na primeira vez, toque em **Parear esta Machine**. Algumas fontes também oferecem outra forma de conexão, como usar seu próprio app ou uma chave.

Toque em **Reconectar** em uma fonte ou em **Precisa de você** para abrir o mesmo formulário. No seu próprio computador, `assistant connect` faz o mesmo em um terminal.

## Trabalho ou pessoal

Cada fonte é classificada como de trabalho, para uma empresa que você informa, ou pessoal. Altere essa classificação em **Detalhes**. **Adivinhado** significa que sua Machine identificou a categoria pelo endereço. As tarefas de trabalho aguardam seus dias úteis.

Para e-mails e calendários do Google e da Microsoft, a categoria é definida pelo endereço quando isso fica claro: um provedor de e-mail como Gmail ou Outlook.com indica uma conta pessoal; o domínio da sua equipe indica uma conta de trabalho. Caso contrário, a pergunta aparece uma vez, logo depois que você entra. **Mudar** permite escolher a categoria. Se mais tarde os e-mails indicarem a outra categoria, a tarefa **Aproveite mais a The Machine** perguntará uma vez se você quer alterá-la.

## Recursos

Uma fonte pode trazer sinais, que viram tarefas, realizar ações para suas tarefas, como ler um documento, enviar, responder ou alterar algo depois da sua aprovação, ou fazer as duas coisas. Se fizer as duas coisas, **Detalhes** terá uma opção para cada recurso: **Traz sinais** e **Pode fazer coisas**. Um deles precisa continuar ativado. Para desativar os dois, desconecte a fonte. Uma conversa só tem a opção **Pode fazer coisas**.

Com **Traz sinais** desativado, a fonte não sincroniza. Com **Pode fazer coisas** desativado, sua Machine nunca lê, cria rascunhos nem altera nada usando essa fonte.

## Remover uma fonte

Abra a fonte, toque em **Detalhes** e depois em **Desconectar**. Ela para de ser lida, mas o que já trouxe continua disponível. Em uma Machine hospedada, as fontes cujo login é gerenciado pela página de configuração mostram **Desconectar ↗**. Essa opção abre a página de configuração. Isso se aplica ao Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce.

**Desconectado recentemente** lista as contas do Google, Microsoft, Zoom, Slack, Stripe e Salesforce que você removeu nos últimos 30 dias, com a data da remoção. Até o serviço confirmar, aparece como Pendente e a tentativa continua. Uma conta do Google aparece uma só vez, mesmo quando o Google Meet ou o Google Docs tinham um login próprio. Cada conta aparece no tipo correspondente: uma conta do Google ou Microsoft em **E-mail**, e uma conta do Slack em **Chat**.

## Logins salvos

Para sites como LinkedIn ou X, marque **Salvar para a próxima vez** ao entrar. Depois, a guia **Logins** mostra os sites salvos. Se um site encerrar a sessão da sua Machine, ela poderá entrar novamente com um toque. As senhas ficam criptografadas na sua Machine. Toque em **Esquecer** para remover um login.

Um site pode ter várias contas, como **Trabalho** e **Pessoal**. **Salvar como** começa com a categoria da própria tarefa. Em **Outro nome…**, você pode informar um nome. A tarefa usa a conta adequada. Quando não fica claro qual conta usar, uma caixa de diálogo pergunta uma vez e guarda a escolha para aquela tarefa.

**Logins** mostra cada site uma vez, com as contas abaixo: o nome de usuário e um menu com a categoria da conta. Você pode alterar a categoria pelo menu quando quiser. Os logins salvos antes da criação das contas mostram **Trabalho ou pessoal?** até você escolher uma opção. Se você alterar a categoria, uma tarefa que usava esse login fará uma nova seleção.

**Importar** adiciona logins de um gerenciador de senhas. Escolha uma opção:

- **LastPass**, **Bitwarden** ou **Gerenciador de senhas do Google**: a página de exportação do serviço abre no navegador da sua Machine. Entre na conta e exporte o arquivo. As instruções aparecem ao lado. Sua Machine encontra o arquivo, lê uma vez e o exclui.
- **1Password**: exporte um CSV pelo app do 1Password em um computador e selecione o arquivo. Se a `op` do 1Password estiver conectada à sua Machine, ela lê os dados de lá. O mesmo vale para a `lpass` do LastPass.
- **De um arquivo de exportação**: selecione um CSV do 1Password, LastPass, Bitwarden ou Chrome. Exclua o arquivo quando terminar.

Depois, marque os logins que quer manter. Sua Machine nunca entra no gerenciador de senhas por você nem pede a senha mestra. Você mesmo digita a senha na página.

Um login salvo só pode ser usado no endereço web correspondente: no mesmo site, `https` e porta. Ele não será usado em um endereço parecido nem em outro subdomínio.

## Verificações

**Verificações** mostra como sua Machine lê o que chega: as verificações recentes e o que cada uma encontrou. Consulte [Nenhuma tarefa nova](reviews-paused.md).

Cada conexão tem seu próprio artigo nesta seção, com informações sobre o que ela lê e o que pode enviar.
