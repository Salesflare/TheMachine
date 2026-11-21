---
title: Conexões
area: connections
summary: Veja todas as suas fontes em um só lugar: confira como estão, adicione uma nova ou desconecte uma.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 0896d8f689ca9699
---
## Como estão

A guia **Conexões** lista suas fontes por tipo, com **Logins** e **Verificações** abaixo de uma linha. No celular, toque em um tipo para abrir e em **Conexões** para voltar. Se alguma fonte precisar de você, o tipo dela aparece primeiro. Cada fonte é exibida em uma linha com o status (Conectada, Aguardando a primeira sincronização, Reconectando automaticamente ou Precisa da sua ajuda) e o que chegou recentemente. Toque nela para abrir o cartão e ver **Detalhes**.

Uma sincronização com falha que foi corrigida por uma sincronização posterior aparece em cinza. Só uma falha que ainda seja a mais recente aparece como problema, com a informação de quando haverá uma nova tentativa.

As contagens mostram tudo o que a fonte trouxe, incluindo o [histórico](history.md), o que chegou nas últimas 24 horas e o que ainda não foi verificado. No caso de calendários, a contagem mostra os eventos.

Cada fonte recebe o nome da conta, da forma como o serviço a identifica: seu endereço, um perfil no X, um espaço de trabalho do Slack ou de quem é a conta do Signal ou do Telegram. Abaixo do nome, aparece primeiro **Trabalho** ou **Pessoal**, além do endereço ou nome de usuário quando o próprio nome não deixa isso claro. Se houver duas fontes do mesmo tipo com o mesmo nome, também aparece uma informação que as diferencia, como Slack ou X, ou o endereço do espaço de trabalho.

Cada fonte também informa em uma linha o que traz e, se puder realizar ações, que só age depois que você toca em **Enviar** ou aprova a ação.

## Adicionar uma fonte

Abra um tipo (**E-mail**, **Calendário**, **Chat**, **Reuniões**, **Documentos e arquivos**, **Clientes**, **Projetos e código**, **Outras**) e escolha uma fonte em **Adicionar outro** ou abaixo da lista, se ainda não houver nenhuma conectada. As opções genéricas aparecem no fim: **Outro e-mail** em E-mail, **Link de calendário (ICS)** e **Outro calendário** em Calendário. O Exchange Server lê reuniões, por isso aparece em Calendário.

**Sugerido para você** aparece no topo de **Conexões** quando sua Machine identifica um motivo para adicionar uma fonte. O motivo é explicado em uma linha, como e-mails do Stripe, reuniões do Zoom na sua agenda, mensagens com links para o Google Docs ou uma configuração que não foi concluída. A fonte também continua no grupo correspondente, marcada como **Sugerido**. Essa informação é calculada na sua Machine, nada é enviado para fora dela. Uma fonte conectada nunca aparece como sugestão.

O Microsoft Teams aparece duas vezes: em **Chat**, para as conversas, e em **Reuniões**, como **Reuniões do Teams**, para as anotações das reuniões. As duas opções usam o mesmo login da Microsoft. Então, ao conectar uma, você conecta a outra também.

Se uma fonte já estiver conectada, isso aparece na lista junto com a conta. Selecione-a para adicionar outra ao lado: o formulário indica que você está adicionando outra e inclui um link para a que já está conectada.

Preencha as informações necessárias, como uma chave ou um endereço, escolha **Trabalho** e o nome da empresa ou **Pessoal**. Para e-mails e calendários, essa escolha só aparece quando o endereço não deixa a categoria clara. Depois, toque em **Conectar**. Sites como LinkedIn ou X abrem a página de login no navegador da sua Machine e continuam automaticamente quando você entra. GitHub, WhatsApp e Codex mostram um código para inserir. As conversas do Telegram e do Signal mostram um código QR para ler.

**Cancelar** interrompe a conexão. Saiu antes de terminar? Abra **Conexões** de novo, em qualquer dispositivo, e o processo continua de onde parou. Depois de conectada, sua Machine começa a ler a fonte imediatamente e mostra o andamento da primeira sincronização.

Em uma Machine hospedada, você entra diretamente por aqui nas fontes que têm login próprio: Google, Microsoft (Outlook, OneDrive e Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce e Trello.

Escolha **Trabalho** ou **Pessoal** e toque no botão de login, como **Entrar com Google**. Você volta ao formulário, que mostra o resultado. GitHub, WhatsApp, Codex, as conversas do Telegram e seu celular Android também mostram os códigos aqui.

No seu próprio computador, você entra nas mesmas fontes depois que sua Machine é pareada com sua conta: na primeira vez, toque em **Parear esta Machine**. Algumas fontes também oferecem outra opção, como usar seu próprio aplicativo ou uma chave.

**Reconectar**, em uma fonte ou em **Precisa de você**, abre o mesmo formulário. No seu próprio computador, `assistant connect` faz o mesmo no terminal.

## Trabalho ou pessoal

Cada fonte é classificada como de trabalho, para uma empresa que você identifica, ou pessoal. Altere essa opção em **Detalhes**. **Estimado** significa que sua Machine identificou a categoria pelo endereço. As tarefas de trabalho aguardam seus dias úteis.

O Google e a Microsoft identificam se e-mails e calendários são de trabalho ou pessoais pelo endereço, quando isso fica claro: um provedor de e-mail, como Gmail ou Outlook.com, indica uso pessoal; o domínio da sua equipe indica uso profissional. Se não der para saber, sua Machine pergunta uma vez, logo depois que você entra. Toque em **Mudar** para definir a categoria. Se os e-mails indicarem outra categoria mais tarde, a tarefa **Aproveite mais a The Machine** perguntará uma vez se você quer alterá-la.

## Recursos

Uma fonte pode trazer sinais, que se tornam tarefas, realizar ações para suas tarefas, como ler um documento, enviar ou responder algo ou fazer uma alteração depois da sua aprovação, ou fazer as duas coisas. Se puder fazer as duas coisas, **Detalhes** mostra uma opção para cada recurso: **Traz sinais** e **Pode fazer coisas**. Pelo menos uma opção precisa ficar ativada. Para desativar as duas, desconecte a fonte. Uma conversa só tem a opção **Pode fazer coisas**.

Com **Traz sinais** desativado, a fonte não sincroniza. Com **Pode fazer coisas** desativado, sua Machine não lê, cria rascunhos nem altera nada nessa fonte.

## Remover uma fonte

Abra a fonte, toque em **Detalhes** e depois em **Desconectar**. Ela para de ser lida. O que já foi importado continua na sua Machine. Em uma Machine hospedada, fontes cujo login fica salvo na sua página de configuração (Google, Microsoft, Google Meet, Slack, Zoom, Stripe e Salesforce) mostram **Desconectar ↗**, que abre essa página.

**Desconectado recentemente** lista as contas do Google, Microsoft, Zoom, Slack, Stripe e Salesforce que você removeu nos últimos 30 dias, além da data da remoção. Até que o serviço confirme, o status fica como Pendente e a Machine continua tentando. Uma conta do Google aparece uma só vez, mesmo quando o Google Meet ou o Docs tinha um login próprio. Cada conta aparece no tipo correspondente: uma conta do Google ou da Microsoft em **E-mail**, e uma conta do Slack em **Chat**.

## Logins salvos

Para sites como LinkedIn ou X, marque **Salvar para a próxima vez** ao entrar. Depois, o site aparece em **Logins** e, quando desconectar sua Machine, basta tocar uma vez para entrar de novo. As senhas ficam criptografadas na sua Machine. Toque em **Esquecer** para remover um login.

Um site pode ter várias contas, como **Trabalho** e **Pessoal**. **Salvar como** começa com a categoria da própria tarefa, e **Outro nome…** permite escolher um nome. A tarefa usa o login correspondente à categoria. Se não der para saber qual é, uma caixa de diálogo pergunta qual conta usar e memoriza sua escolha para aquela tarefa.

**Logins** lista cada site uma vez, com as contas abaixo: o nome de usuário e um menu com a categoria. Você pode alterá-la ali quando quiser. Os logins salvos antes da criação das categorias mostram **Trabalho ou pessoal?** até você escolher uma. Depois que você altera a categoria, uma tarefa que usava aquele login pergunta novamente qual conta usar.

**Importar** adiciona logins de um gerenciador de senhas. Escolha uma opção:

- **LastPass**, **Bitwarden** ou **Gerenciador de senhas do Google**: a página de exportação abre no navegador da sua Machine, dentro da caixa de diálogo, como acontece com a opção **Fazer** de uma tarefa. Entre na página e sua Machine continua até a exportação. Uma linha indica o que falta fazer, como digitar sua senha mestra. O LastPass envia um link por e-mail para confirmar a exportação. Sua Machine inicia o processo uma vez e abre o link quando o e-mail chega a uma caixa de entrada conectada, dentro de 10 minutos. Caso contrário, pede que você confirme e exporte de novo. No celular, a visualização aumenta o zoom até o campo de digitação. Se a página estiver diferente do esperado, aparecem instruções para concluir o processo manualmente. Sua Machine pega o arquivo, lê e o exclui.
- **1Password**: exporte um CSV pelo aplicativo 1Password no computador e escolha o arquivo. Se `op` do 1Password estiver conectado à sua Machine, ela importa os dados de lá. O mesmo vale para `lpass` do LastPass.
- **De um arquivo de exportação**: use um CSV do 1Password, LastPass, Bitwarden ou Chrome. Exclua o arquivo quando terminar.

Depois, marque os logins que quer manter. Sua Machine nunca entra no gerenciador de senhas por você, nunca digita nem lê sua senha mestra e nunca mostra a página à assistente: você mesmo digita a senha na página.

Um login salvo só é usado no endereço web ao qual pertence: no mesmo site, `https` e porta. Ele não é usado em um endereço parecido nem em outro subdomínio.

## Verificações

**Verificações** mostra como sua Machine lê o que chega: as verificações recentes e o que cada uma encontrou. Consulte [Sem novas tarefas](reviews-paused.md).

Cada conexão tem um artigo nesta seção com informações sobre o que ela lê e o que pode enviar.
