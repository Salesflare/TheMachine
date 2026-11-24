---
title: Amigos e a Network
area: fleet
summary: Adicione amigos pelo nome de usuário, encontre pessoas que você conhece e têm uma Machine e conecte uma Machine que roda no seu próprio computador.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 70a39b4999d112b7
---
## Amigos

Adicione alguém pelo nome de usuário exato, na aba **Fleet**, em Amigos. Seus amigos podem perguntar quem conhece alguém, receber contexto sobre reuniões e apresentações por conhecidos, e ver quando você está ocupado (só os horários, nunca o motivo). Os dias que não aparecem no calendário são mostrados como desconhecidos, nunca como livres. Você pode remover ou bloquear um amigo a qualquer momento.

## Encontre pessoas que você conhece

Em **Fleet**, na seção **Network**:

- “Verificar quais dos meus contatos têm uma Machine” sugere pessoas que você conhece.
- “Permitir que pessoas com meu e-mail me encontrem” permite que elas encontrem você.

As duas opções vêm ativadas por padrão e desativadas no nível de segurança Cuidadoso. Você pode desativar qualquer uma a qualquer momento. Sua escolha é mantida. As pessoas podem encontrar você pelo e-mail usado para entrar (sempre ativado) e pelos seus endereços conectados, cada um com uma opção própria em **Pode ser encontrado por**, exceto endereços compartilhados, como info@, que ficam desativados até você ativá-los.

As pessoas que você conhece aparecem como uma tarefa assim que você ativa a opção e também quando entram na Network mais tarde. Para cada pessoa, aparecem as opções **Amigo** e **Família** (**Conectar** para colegas), **Agora não** e **Nunca sugerir** no menu ⋯. Depois que vocês viram amigos, a pessoa deixa de ser sugerida. **Sair da Network** remove você dela.

As pessoas encontradas aparecem com **Tem uma Machine** na sua lista de Pessoas. A busca verifica os endereços nas suas mensagens e os que você adicionou ao perfil de alguém com **Editar**. Se a pessoa se cadastrou com outro endereço, adicione-o ao perfil dela. Na página de alguém que a busca encontrou, **Adicionar como amigo** envia o mesmo pedido que Conectar (**Adicionar como família** fica no menu ⋯).

Para quem não tem uma Machine, aparece **Convidar para a The Machine**. A opção abre o e-mail que a pessoa receberá em **Enviar este e-mail?**, igual ao de qualquer tarefa, para você editar se quiser. O e-mail só é enviado quando você toca em **Enviar agora**. Se fechar, o convite fica aguardando como tarefa. Se não houver uma caixa de e-mail para enviar: **Copiar** ou **Abrir no seu e-mail**.

Os números de telefone também contam: os números das conversas no WhatsApp com pessoas para quem você escreveu ou que conheceu, além dos que adicionou com **Editar**. Seu número do WhatsApp vinculado e os números em Sobre você permitem que as pessoas encontrem você, cada um com uma opção própria em **Pode ser encontrado por**. Um número só encontra alguém se essa pessoa também procurou você ou se vocês são amigos. Assim, ninguém pode testar números para descobrir quem tem uma Machine.

## Agendamento com outras Machines

Quando alguém com uma Machine escreve “vamos nos encontrar na semana que vem”, sua Machine pergunta à Machine dessa pessoa quais horários estão livres e encontra um que sirva para vocês dois, dentro do seu horário de trabalho. Cada um recebe uma tarefa, como “Encontrar Alex Example”, com o horário logo abaixo. Toque em **Marcar**, **Outro horário** ou **Não precisa**. O convite só é enviado depois que vocês dois tocarem em Marcar.

Só os horários livres ou ocupados são compartilhados, com criptografia de ponta a ponta, por no máximo 14 dias e em intervalos de 15 minutos. Eventos privados contam como ocupados. Uma Machine só pode perguntar quando vocês já trocaram e-mails nos dois sentidos. Configure em **O que outras Machines podem perguntar à minha**: **Livre/ocupado para agendar** ou **Desativado**, além da duração da reunião, do intervalo e dos horários de preferência. Cada pedido aparece em Atividade, na seção Calendário.

Um horário só conta como livre quando o calendário indica isso. Sua Machine não oferece horários se nenhum calendário estiver conectado, se não conseguir ler o calendário por um dia ou se o horário for mais de 30 dias à frente. Eventos de dia inteiro contam como ocupados quando estão marcados como Busy, e eventos marcados como Free nunca contam como ocupados. Um evento de dia inteiro adicionado por uma tarefa fica como Free, a menos que você esteja fora ou já tenha outros compromissos nesses dias. Nesse caso, ele indica “ocupado” antes de você adicionar o evento.

Se a outra pessoa não tiver uma Machine ou não responder, o rascunho do e-mail incluirá um link para ela escolher um dos seus horários livres. A escolha dela aparece como uma tarefa com **Marcar**. Nada é agendado até você tocar nessa opção.

O link mostra apenas os horários livres, segundo as mesmas regras, e nenhuma outra informação sobre você. Ele deixa de funcionar quando a reunião é agendada ou após 14 dias. No e-mail, ele aparece como “Escolher um horário”. Na parte inferior, a página diz “A Machine de Alex encontrou estes horários. Conheça a sua.”, com seu primeiro nome. Desative essa opção em **Rodapé nos links de agendamento**. Cada link e escolha aparece em Atividade.

## Uma Machine no seu próprio computador

Para entrar na Network usando uma Machine que você executa:

1. No painel da sua Machine, abra **Configurações** e toque em **Entrar na Network**.
2. Na página que abrir, entre na sua conta (ou crie uma) e confirme. Sua Machine reconhece a conexão automaticamente, sem precisar reiniciar.

O método com código continua funcionando: toque em **Conectar uma Machine auto-hospedada** na página da sua conta em app.themachine.computer, execute `assistant fleet-pair` com o código no seu computador e reinicie. O código pode ser usado uma vez e expira após 15 minutos.

Você pode ter até 5 Machines por conta. Cada uma pode ser desconectada nessa página.
