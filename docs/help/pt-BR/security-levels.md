---
title: Níveis de segurança
area: security
summary: Um único seletor, Padrão ou Cuidadoso, define suas configurações de segurança e privacidade. O admin de um Fleet de Trabalho escolhe um para o Fleet.
covers: settings:security
code: security_levels.py, dashboard.html, fleet.py
order: 2
---
## Dois níveis

Abra **Configurações** e depois **Segurança**.

- **Padrão**: os padrões atuais. Nada muda.
- **Cuidadoso**: mais rígido, para quando você quer menos coisa no celular e menos coisa guardada.

Um nível é um ponto de partida. Se depois você mudar qualquer configuração, o nível mostra **Personalizada**. Escolha um nível de novo para restaurar tudo.

## O que o Cuidadoso muda para você

- **Texto nas notificações** desligado: uma notificação diz "Nova tarefa" ou "Pronta", não o que a tarefa diz.
- **Oferecer para salvar logins** desligado. Os sites com login salvo continuam até você tocar em **Esquecer todos os logins salvos**.
- **Buscar contatos de trabalho**, **Oferecer compartilhar aprendizados** e **Compartilhar o que se pergunta à ajuda** desligados.
- **Verificar quais dos meus contatos têm uma Machine** e **Deixar quem tem meu e-mail me encontrar** desligados.
- **Manter detalhes de Fazer por 90 dias** desligado: eles são guardados por 30 dias.
- Em uma Família, os horários livres e ocupados perguntam a você antes. Com Amigos, o contexto de reuniões é recusado.

## O nível de um Fleet de Trabalho

O proprietário ou um admin do Fleet escolhe o nível na página da conta, nas configurações do Fleet. Todos no Fleet veem o nível. Quando ele é Cuidadoso:

- Respostas a colegas esperam seu OK, sem nomes, e só sobre pessoas das suas contas de trabalho.
- Apresentações e repasses também esperam por você.
- O Graph da equipe compartilha e-mails de clientes sem os anexos.
- As notificações de tarefas de trabalho não mostram texto.
- Contatos de trabalho não são buscados.
- Sua Machine não verifica seus contatos na Network nem deixa que encontrem você por e-mail, a não ser que você tenha ligado isso.
- Todos entram de novo a cada 7 dias.
- Um link de convite só funciona para o e-mail para o qual foi enviado.

Os membros podem ser mais rígidos que o Fleet, não mais flexíveis. As escolhas deles são mantidas e voltam se o Fleet voltar para Padrão.

## O que é igual nos dois

Nada é enviado sem o seu OK: você vê cada rascunho e clica em Enviar. Fazer e os agentes de código funcionam do mesmo jeito. Entrar sempre exige um código de autenticador ou uma passkey.
