---
title: Amigos e a Network
area: fleet
summary: Adicione amigos pelo nome de usuário, encontre pessoas que você conhece e têm uma Machine e conecte uma Machine no seu próprio computador.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 637784bf811800bb
---
## Amigos

Adicione alguém pelo nome de usuário exato, na guia **Fleet**, em Amigos. Seus amigos podem perguntar quem conhece alguém, receber contexto sobre reuniões e apresentações, e ver quando você está ocupado (apenas os horários, nunca o motivo). Você pode remover ou bloquear um amigo a qualquer momento.

## Encontre pessoas que você conhece

Em **Fleet**, na seção **Network**:

- "Ver quais contatos meus têm uma Machine" sugere pessoas que você conhece.
- "Permitir que pessoas com meu e-mail me encontrem" permite que elas encontrem você.

As duas opções ficam ativadas por padrão e desativadas no nível de segurança Cuidadoso. Você pode desativar qualquer uma delas a qualquer momento; sua escolha é mantida. As pessoas podem encontrar você pelo e-mail usado para entrar (sempre ativado) e pelos endereços conectados, cada um com seu próprio controle em **Pode ser encontrado por**, com exceção de endereços compartilhados, como info@, que ficam desativados até você ativá-los.

As pessoas que você conhece aparecem como uma tarefa assim que você ativa a opção e também quando elas entram na Network. Para cada pessoa, você pode escolher **Amigo** ou **Família** (**Conectar** para um colega), **Agora não** ou **Nunca sugerir** no menu ⋯. Quando vocês se tornam amigos, essa pessoa deixa de aparecer como sugestão. **Sair da Network** remove você da Network.

As pessoas encontradas aparecem com a indicação **Tem uma Machine** na sua lista de Pessoas. A busca verifica os endereços nas suas mensagens e os que você adicionou ao perfil de alguém com **Editar**. Se alguém se cadastrou com outro endereço, adicione-o ao perfil dessa pessoa. Na página de alguém que a busca encontrou, **Adicionar como amigo** envia o mesmo pedido que Conectar (**Adicionar como família** fica no menu ⋯).

Para quem não tem uma Machine, aparece a opção **Convidar para a The Machine**. Ela abre o e-mail que a pessoa receberia em **Enviar este e-mail?**, igual ao de qualquer tarefa, para você editar se quiser. Nada é enviado antes de você clicar em **Enviar agora**. Se fechar essa janela, o convite fica como uma tarefa. Se não houver uma caixa de e-mail que possa enviar mensagens: **Copiar** ou **Abrir no seu e-mail**.

Os números de telefone também contam: os números das suas conversas no WhatsApp com pessoas para quem você enviou mensagens ou que conheceu, além dos números que adicionou com **Editar**. Seu número do WhatsApp conectado e os números na seção Sobre você permitem que outras pessoas encontrem você, cada um com seu próprio controle em **Pode ser encontrado por**. Um número só permite encontrar alguém se essa pessoa também procurou você ou se vocês são amigos, então ninguém pode testar números para descobrir quem tem uma Machine.

## Agendamento com outras Machines

Quando alguém com uma Machine escreve "vamos nos encontrar na semana que vem", sua Machine consulta a Machine da outra pessoa para encontrar horários livres que funcionem para vocês dois, dentro do seu horário de trabalho. Cada um recebe uma tarefa, como "Encontrar Alex Example", com o horário logo abaixo. Toque em **Marcar**, **Outro horário** ou **Não precisa**. O convite só é enviado depois que vocês dois tocarem em Marcar.

Apenas a informação de livre ou ocupado é compartilhada, com criptografia de ponta a ponta, por no máximo 14 dias e arredondada para intervalos de 15 minutos. Eventos privados contam como ocupados. Uma Machine só pode consultar a outra se vocês já trocaram e-mails nos dois sentidos. Configure essa opção em **O que outras Machines podem perguntar à minha**: **Livre/ocupado para agendar** ou **Desativado**, além da duração da reunião, do intervalo e dos horários de preferência. Cada consulta aparece em Atividade, na seção Calendário.

Se a outra pessoa não tiver uma Machine ou não responder, o rascunho do e-mail inclui um link para ela escolher um dos seus horários livres. A escolha dela vira uma tarefa com **Marcar**. Nada é agendado antes de você tocar nessa opção.

O link mostra apenas os horários livres, seguindo as mesmas regras, e nenhuma outra informação sobre você. Ele deixa de funcionar quando a reunião é marcada ou depois de 14 dias. No e-mail, ele aparece como "Escolha um horário". No fim da página, aparece "A Machine de Alex encontrou estes horários. Tenha a sua.", com seu primeiro nome. Desative essa opção em **Rodapé nos links de agendamento**. Cada link e cada escolha aparecem em Atividade.

## Uma Machine no seu próprio computador

Para entrar na Network usando uma Machine que você mesmo executa:

1. No painel da sua Machine, abra **Configurações** e clique em **Entrar na Network**.
2. Na página que abrir, entre na sua conta (ou crie uma) e confirme. Sua Machine detecta a conexão automaticamente, sem precisar reiniciar.

Você também pode usar o método com código: clique em **Parear uma Machine hospedada por você** na página da sua conta em app.themachine.computer. Depois, execute `assistant fleet-pair` com o código no seu computador e reinicie. O código só pode ser usado uma vez e expira em 15 minutos.

Você pode ter até 5 Machines por conta. É possível desconectar cada uma nessa página.
