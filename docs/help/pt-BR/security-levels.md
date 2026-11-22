---
title: Níveis de segurança
area: security
summary: Um único seletor, Padrão ou Cuidadoso, define suas configurações de segurança e privacidade. O administrador de um Fleet de Trabalho escolhe um nível para o Fleet.
covers: settings:security
code: security_levels.py, dashboard.html, fleet.py
order: 2
translated: cf3ba86c8c1a23f3
---
## Dois níveis

Acesse **Configurações** e depois **Segurança**.

- **Padrão**: as configurações padrão de hoje. Nada muda.
- **Cuidadoso**: mais restritivo, para quando você quer manter menos informações no celular e guardar menos dados.

Um nível é um ponto de partida. Se depois você mudar qualquer configuração, o nível passa a ser **Personalizada**. Escolha um nível novamente para redefinir as configurações.

## O que Cuidadoso muda para você

- **Texto nas notificações**: **Desativado**. A notificação diz “Nova tarefa” ou “Para revisar”, não o conteúdo da tarefa.
- **Oferecer para salvar logins**: **Desativado**. Os sites em que você entrou e salvou o login continuam salvos até você tocar em **Esquecer todos os logins salvos**.
- **Buscar contatos de trabalho**, **Oferecer compartilhar aprendizados** e **Compartilhar o que se pergunta à ajuda**: **Desativado**.
- **Verificar quais dos meus contatos têm uma Machine** e **Deixar quem tem meu e-mail me encontrar**: **Desativado**.
- **Manter detalhes de Fazer por 90 dias**: **Desativado**. Eles ficam salvos por 30 dias.
- **O que outras Machines podem perguntar à minha**: definido como **Desativado**. Não há agendamento com outras Machines. Consulte [Amigos e a Network](friends.md#scheduling-with-other-machines).
- Em uma família, o compartilhamento dos horários em que você está livre ou ocupado pede sua confirmação. Com Amigos, o contexto da reunião é recusado.

## Nível de um Fleet de Trabalho

O proprietário do Fleet ou um administrador escolhe o nível nas configurações do Fleet: em **Configurações** › **Conta**, toque em **Fleet**. Todas as pessoas do Fleet podem vê-lo. Quando está definido como Cuidadoso:

- As respostas para colegas de equipe aguardam sua aprovação, sem nomes e só sobre pessoas das suas contas de trabalho.
- Apresentações e repasses também aguardam sua aprovação.
- O Graph da equipe compartilha e-mails de clientes sem os anexos.
- As notificações de tarefas de trabalho não mostram o texto.
- Os contatos de trabalho não são consultados.
- Sua Machine não verifica seus contatos na Network nem permite que encontrem você pelo e-mail, a menos que você tenha ativado isso.
- Todas as pessoas precisam entrar novamente a cada 7 dias.
- Um link de convite só funciona para o e-mail para o qual foi enviado.

As pessoas podem escolher configurações mais restritivas que as do Fleet, mas não menos. As escolhas pessoais são mantidas e voltam a valer se o Fleet voltar para Padrão.

## O que não muda

Nada é enviado sem sua aprovação: você vê cada rascunho e toca em Enviar. **Fazer** e os agentes de programação funcionam da mesma forma. Para entrar, sempre é necessário um código de autenticador ou uma chave de acesso.
