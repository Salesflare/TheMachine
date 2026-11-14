---
title: Conexões
area: connections
summary: Suas fontes em um só lugar: veja como estão, adicione uma nova ou desconecte uma.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 1ca62ab8f65b77ff
---
## Como estão

A aba **Conexões** mostra suas fontes por tipo, com **Logins** e **Verificações** abaixo de uma linha. No celular, toque em um tipo para abri-lo e em **Conexões** para voltar. O tipo que tiver uma fonte que precisa de você aparece primeiro. Cada fonte é uma linha: mostra como está (Conectada, Aguardando a primeira sincronização, Reconectando automaticamente ou Precisa da sua ajuda) e o que recebeu recentemente. Toque nela para abrir o cartão e ver **Detalhes**.

Uma sincronização que falhou, mas foi compensada por uma posterior, aparece em cinza. Só uma falha que ainda é a mais recente aparece como problema, com a data da próxima tentativa.

As contagens mostram tudo o que a fonte trouxe, incluindo o [histórico](history.md), o que chegou nas últimas 24 horas e o que ainda não foi verificado. Um calendário conta os eventos.

Cada fonte recebe o nome da conta, como o serviço a identifica: seu endereço, um perfil no X, um workspace do Slack ou de quem é a conta no Signal ou no Telegram. Abaixo do nome, aparece primeiro **Trabalho** ou **Pessoal**, seguido do endereço ou nome de usuário quando o nome não deixa isso claro. Se duas fontes do mesmo tipo tiverem o mesmo nome, elas também mostram o que as diferencia, como Slack ou X, ou o endereço do workspace.

Cada fonte também informa em uma linha o que traz e, se puder realizar ações, que só fará isso depois que você tocar em **Enviar** ou aprovar.

## Adicionar uma fonte

Abra um tipo (**E-mail**, **Calendário**, **Chat**, **Reuniões**, **Documentos e arquivos**, **Clientes**, **Projetos e código**, **Outras**) e escolha uma fonte em **Adicionar outro**, ou abaixo da lista se ainda não houver nenhuma conectada. As opções genéricas aparecem no final: **Outro e-mail** em E-mail, **Link de calendário (ICS)** e **Outro calendário** em Calendário. O Exchange Server lê reuniões, por isso fica em Calendário.

**Sugerido para você** aparece no topo de **Conexões** quando sua Machine identifica um motivo para sugerir uma fonte. O motivo é explicado em uma linha: e-mails da Stripe, reuniões do Zoom no seu calendário, mensagens com links para o Google Docs ou uma configuração que não foi concluída. A fonte também continua no grupo correspondente, marcada como **Sugerido**. Essa contagem é feita na sua Machine; nada sai dela. Uma fonte conectada nunca é sugerida.

O Microsoft Teams aparece duas vezes: em **Chat**, para as conversas, e em **Reuniões**, como **Reuniões do Teams**, para as anotações das reuniões. Ambos usam o mesmo login da Microsoft, então conectar um também conecta o outro.

A lista mostra quando você já conectou uma fonte, junto com a conta usada. Selecione-a para adicionar outra ao lado: o formulário informa isso e inclui um link para a que você já tem.

Preencha as informações necessárias, como uma chave ou um endereço, escolha **Trabalho** com o nome da empresa ou **Pessoal** e toque em **Conectar**. Para e-mails e calendários, essa escolha só é solicitada quando o endereço não deixa isso claro. Um site como LinkedIn ou X abre a tela de login no navegador da sua Machine e continua automaticamente depois que você entra. GitHub, WhatsApp e Codex mostram um código para inserir. Os chats do Telegram mostram um código QR para escanear.

**Cancelar** interrompe a adição. Saiu antes de terminar? Abra **Conexões** novamente, em qualquer dispositivo, e o processo continua na mesma etapa. Depois que a fonte é conectada, sua Machine começa a lê-la na hora e mostra o andamento da primeira sincronização.

Em uma Machine hospedada, o login do Google, Microsoft, Microsoft OneDrive, Zoom, Stripe e Intercom é feito aqui mesmo: escolha **Trabalho** ou **Pessoal** e toque em **Entrar**. Você volta ao formulário, que mostra o resultado. GitHub, WhatsApp, Codex, os chats do Telegram e seu celular Android também mostram o código aqui.

**Reconectar**, na fonte ou em **Precisa de você**, abre o mesmo formulário. No seu próprio computador, `assistant connect` faz o mesmo em um terminal.

## Trabalho ou pessoal

Cada fonte é classificada como de trabalho, para uma empresa que você identifica, ou pessoal. Mude essa opção em **Detalhes**. **Estimado** significa que sua Machine identificou a categoria pelo endereço. As tarefas de trabalho aguardam seus dias úteis.

O Google e a Microsoft identificam se e-mails e calendários são de trabalho ou pessoais pelo endereço, quando isso fica claro: um provedor de e-mail como Gmail ou Outlook.com indica uso pessoal; o domínio da sua equipe indica uso de trabalho. Se não ficar claro, a Machine pergunta uma vez, logo depois que você entra. **Mudar** permite escolher por conta própria. Se os e-mails indicarem depois a outra opção, a tarefa **Aproveite mais a The Machine** pergunta uma vez se você quer mudar.

## Recursos

Uma fonte pode trazer sinais, que se transformam em tarefas, realizar ações para suas tarefas, como ler um documento, enviar, responder ou alterar algo depois da sua aprovação, ou fazer as duas coisas. Quando faz as duas coisas, **Detalhes** tem uma opção para cada recurso: **Traz sinais** e **Pode fazer coisas**. Uma delas precisa continuar ativada. Para desativar as duas, desconecte a fonte. Um chat só tem **Pode fazer coisas**.

Com **Traz sinais** desativado, a fonte não sincroniza. Com **Pode fazer coisas** desativado, sua Machine nunca lê, cria rascunhos nem altera nada usando essa fonte.

## Remover uma fonte

Abra a fonte, toque em **Detalhes** e depois em **Desconectar**. Ela para de ser lida. O que já trouxe continua disponível. Em uma Machine hospedada, Google, Microsoft, Microsoft OneDrive, Zoom e Stripe mostram **Desconectar ↗**, que abre a página de configuração.

**Desconectado recentemente** mostra as contas do Google, Microsoft, Zoom, Slack, Stripe e Salesforce que você removeu nos últimos 30 dias, e quando foram removidas. Uma conta do Google aparece uma vez, mesmo quando o Google Meet ou o Docs tinham um login próprio. Cada conta aparece no tipo correspondente: uma conta do Google ou Microsoft em **E-mail**, e uma conta do Slack em **Chat**.

## Logins salvos

Para sites como LinkedIn ou X, marque **Salvar para a próxima vez** ao entrar. Depois, eles aparecem em **Logins**. Se um site desconectar sua Machine, ela entra novamente com um toque. As senhas ficam criptografadas na sua Machine. Toque em **Esquecer** para remover um login.

## Verificações

**Verificações** mostra como sua Machine lê o que chega: as verificações recentes e o que cada uma encontrou. Consulte [Sem novas tarefas](reviews-paused.md).

Cada conexão tem seu próprio artigo nesta seção, que explica o que ela lê e o que pode enviar.
