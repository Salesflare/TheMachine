---
title: Conectar outras IAs
area: connections
summary: Permita que Claude, ChatGPT, Cursor, Codex ou GBrain leiam suas tarefas e seu Graph. Com Ler e editar, elas também podem fazer alterações que você pode desfazer.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: ac5a894df13907fd
---
## O que outra IA pode fazer

Claude, ChatGPT, Cursor, Codex, GBrain e outras IAs podem se conectar à sua Machine. Elas podem ler suas tarefas, promessas, resumos da equipe e as pessoas e empresas do seu Graph.

Com **Ler e editar**, elas também podem adicionar uma tarefa ou um rascunho de e-mail e atualizar seu Graph: salvar uma informação, corrigir detalhes, campos e tags ou adicionar uma linha ao resumo de uma pessoa.

Cada alteração aparece em **Atividade**, com a opção **Desfazer**. Elas nunca mesclam, excluem ou compartilham registros. O que salvam é identificado como **AI:** seguido do nome delas, e sua Machine trata isso como algo afirmado pela IA, nunca como uma instrução sua.

Um rascunho fica esperando até você ler e pressionar **Enviar**. Uma IA conectada nunca envia nada nem age em seu nome.

## Conectar uma IA

Abra **Configurações** e **Apps**. Abaixo de **Os apps da The Machine**, você encontra **Adicionar no ChatGPT** e **Adicionar no Claude**. Em **Ou adicione por endereço**, ficam o endereço do app oficial, `https://mcp.themachine.computer/mcp`, que é o mesmo para todas as Machines, e **Seu endereço**, `https://<your name>.mcp.themachine.computer/mcp`. Cada um tem a opção **Copiar**.

Em uma Machine no seu próprio computador, primeiro pressione **Configurar**, abaixo de **Criar seu endereço**. Uma página da sua conta será aberta: confira se ela mostra o mesmo código, confirme e escolha um nome. O pareamento da sua Machine acontece automaticamente, sem reiniciar. É necessário fazer isso das duas formas.

Sua Machine configura o endereço seguro automaticamente. Isso leva alguns minutos.

Para Claude, pressione **Adicionar no Claude** ou abra [The Machine no diretório do Claude](https://claude.ai/directory/the-machine) e pressione **Conectar**. Nos planos Team e Enterprise, um proprietário precisa adicioná-la nas configurações da organização.

Para usar um endereço no Claude, em vez disso, abra **Personalizar**, **Conectores**, pressione **+ Adicionar** e, depois, **Adicionar conector personalizado**. Dê o nome The Machine, cole o endereço, pressione **Continuar** e, depois, **Adicionar**.

Para ChatGPT, pressione **Adicionar no ChatGPT** ou abra [The Machine no ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) e pressione **Instalar plugin**. Nos planos Business e Enterprise, talvez um administrador precise permitir o uso primeiro.

O app oficial se conecta a uma Machine hospedada e também a uma Machine no seu próprio computador, depois que ela tiver um endereço.

Para usar seu endereço privado ou uma Machine que não esteja na Network, adicione um servidor MCP personalizado no ChatGPT: abra chatgpt.com/plugins, pressione **+** e, depois, **Adicionar servidor MCP personalizado**. Dê o nome The Machine, cole o endereço e escolha **OAuth**. Confirme o aviso e pressione **Criar como plugin**. Seu plano ou espaço de trabalho precisa permitir servidores MCP personalizados.

Com o app oficial, a IA pede que você entre com sua conta da The Machine. Se você tiver mais de uma Machine, escolha esta e aprove o acesso na página da própria Machine. Com o endereço privado, a IA se conecta diretamente à sua Machine.

IAs em um dispositivo da sua rede privada (Tailscale), como Claude Code ou Cursor, também podem usar o endereço do painel da sua Machine seguido de `/mcp`. A opção **Desfazer o pareamento desta Machine**, na parte inferior de **Configurações**, **Conta**, remove uma Machine do seu próprio computador da sua conta.

Sua Machine mostra qual IA está pedindo acesso. Se não conseguir identificá-la, mostra de onde veio a solicitação: conecte somente se você acabou de iniciar o processo.

Escolha o que ela pode fazer: **Ler** ou **Ler e editar**. Se você tiver contas de Trabalho e Pessoal, escolha o que ela pode ver. Depois, escolha por quanto tempo: **1 dia**, **7 dias**, **30 dias** ou **1 ano**. Pressione **Conectar** ou **Cancelar** para encerrar sem conceder acesso.

## App oficial ou endereço privado

O app oficial é a opção mais simples: um endereço para todos, e sua conta encontra sua Machine. Nossa nuvem encaminha as solicitações e não armazena nada.

Com seu endereço privado, tudo é criptografado até chegar à sua Machine. A nuvem só encaminha os dados e não consegue lê-los.

Nos dois casos, quem decide é sua Machine. Só uma IA que você aprovou na página dela pode entrar, com o acesso que você escolheu. Em **Configurações**, **Apps**, uma IA conectada pelo app oficial aparece como **App oficial**.

## O que ela pode ver

Uma conexão só acessa a área que você autorizou. Trabalho inclui as tarefas e promessas das suas contas de trabalho, as pessoas, empresas e projetos de trabalho, além do resumo da equipe do seu Fleet de Trabalho. Pessoal inclui o restante. O texto das mensagens continua na sua Machine, a menos que você ative **Mensagens**. Sem essa opção, uma IA só vê o remetente, o assunto e a data das fontes de uma tarefa.

Os registros do Team Graph dos seus colegas nunca são enviados a uma IA externa.

## Mensagens

**Mensagens** permite que uma IA pesquise e leia seus e-mails, mensagens do Slack e do WhatsApp e outras conversas. A opção fica desativada até você ativá-la, na página de conexão ou depois em **Configurações**, **Apps**. A IA só lê: nunca envia, exclui ou marca nada.

Ela só lê mensagens da área autorizada. Algumas mensagens nunca são compartilhadas: códigos de uso único e links de acesso, mensagens de um quadro ou projeto definido como **Só você**, conversas que a The Machine considerou sensíveis (negócios, RH, assuntos jurídicos, saúde e dinheiro), conversas que você manteve privadas e mensagens excluídas.

Cada leitura aparece em **Atividade**, com a quantidade de mensagens e as conversas acessadas, mas sem o texto. Sua Machine entrega o texto identificado como dado, para que a IA não siga instruções escritas em uma mensagem.

Enquanto **Mensagens** estiver ativada, as alterações no Graph feitas por uma IA com **Ler e editar** aguardam sua aprovação. Pressione **Aplicar** ou **Descartar** na alteração em **Atividade**.

## Nas Configurações

Abra **Configurações**, **Apps** para ver cada IA que se conectou, uma vez, com o acesso, a área, a data de término e o último uso. Você pode ativar ou desativar **Mensagens** nessa mesma página. Pressione **Mudar** para alterar o acesso, a área ou a duração. A próxima solicitação já usará as novas opções. **Atividade** mostra todas as solicitações, inclusive as recusadas. **Desativar agora** pausa o acesso: todas as sessões são encerradas, mas o histórico permanece. **Remover** revoga o acesso e apaga o histórico.

Quando você entrar de novo na mesma IA, a nova aprovação substituirá a anterior.

Uma IA que não consegue entrar por conta própria pode usar uma chave. Em **Adicionar uma chave**, dê um nome, escolha o acesso e a duração e pressione **Criar chave**. Copie a chave na hora: ela só aparece uma vez. A IA a envia como `Authorization: Bearer <key>`.

## Mantenha tudo seguro

Todas as solicitações são registradas, inclusive as recusadas. Uma conexão expirada ou desativada é recusada até que você a altere. Sua Machine guarda apenas uma impressão digital de cada acesso, então uma cópia dos dados não dá acesso a nada.
