---
title: Amigos e a Network
area: fleet
summary: Adicione amigos pelo nome de usuário, encontre pessoas que você conhece e que têm uma Machine, e pareie uma Machine no seu próprio computador.
covers: friends
code: friends.py, network.py, meet.py, meet_app.py, dashboard.html
site: Pair a self-hosted Machine
order: 5
translated: 3565b3898b234575
---
## Amigos

Adicione alguém pelo nome de usuário exato, na aba **Fleet**, em Amigos. Seus amigos podem perguntar quem conhece alguém, receber contexto sobre reuniões e apresentações feitas por alguém em comum, e ver quando você está ocupado (apenas os horários, nunca o que você está fazendo). Você pode remover ou bloquear um amigo a qualquer momento.

## Encontre pessoas que você conhece

Em **Fleet**, na seção **Network**:

- **Verificar quais dos meus contatos têm uma Machine** sugere pessoas que você conhece.
- **Permitir que pessoas que tenham meu e-mail me encontrem** permite que elas encontrem você.

As duas opções vêm ativadas por padrão e ficam desativadas no nível de segurança Cuidadoso. Você pode desativar qualquer uma a qualquer momento, e sua escolha fica salva. As pessoas podem encontrar você pelo e-mail usado para entrar (sempre ativado) e pelos seus endereços conectados, cada um com seu próprio controle em **Pode ser encontrado por**. Endereços compartilhados, como info@, ficam desativados até você ativá-los.

As pessoas que você conhece aparecem assim que você ativa essa opção e também quando entram na Network mais tarde. Para cada uma, você pode escolher **Conectar**, **Agora não** ou **Nunca sugerir**. Depois que vocês se tornam amigos, essa pessoa deixa de ser sugerida. **Sair da Network** remove você da Network.

As pessoas encontradas aparecem como **Tem uma Machine** na sua lista de Pessoas. A busca verifica os endereços nas suas mensagens e os que você adicionou ao perfil de alguém com **Editar**. Se alguém se cadastrou com outro endereço, adicione-o ao perfil dessa pessoa. Na página de alguém que a busca encontrou, **Adicionar como amigo** envia o mesmo pedido que **Conectar** (**Adicionar como família** fica no menu ⋯).

Para alguém sem uma Machine, aparece **Convidar para a The Machine**. Essa opção abre o e-mail de convite em **Enviar este e-mail?**, igual ao usado para qualquer tarefa, para você editar se quiser. Nada é enviado antes de você selecionar **Enviar agora**. Feche a janela e o convite fica como uma tarefa. Se você não tiver uma caixa de e-mail que possa enviar mensagens, use **Copiar** ou **Abrir no seu e-mail**.

Os números de telefone também contam: os números nas conversas do WhatsApp com pessoas para quem você escreveu ou que conheceu, e os que você adicionou com **Editar**. Seu número do WhatsApp conectado e os números na seção **Sobre você** permitem que outras pessoas encontrem você, cada um com seu próprio controle em **Pode ser encontrado por**. Um número só encontra alguém se essa pessoa também tiver procurado você ou se vocês forem amigos. Assim, ninguém pode testar números para descobrir quem tem uma Machine.

## Agende com outras Machines

Quando alguém com uma Machine escreve “vamos nos encontrar na próxima semana”, sua Machine pede à Machine da outra pessoa os horários livres e encontra um que funcione para vocês duas, dentro do seu horário de trabalho. Cada pessoa recebe uma tarefa, como “Encontrar Alex Example”, com o horário logo abaixo. Toque em **Marcar**, **Outro horário** ou **Não precisa**. O convite só é enviado depois que vocês duas tocarem em **Marcar**.

Só os horários livres ou ocupados são compartilhados, com criptografia de ponta a ponta, por no máximo 14 dias e arredondados para intervalos de 15 minutos. Eventos privados contam como ocupados. Uma Machine só pode perguntar quando vocês já trocaram e-mails. Configure isso em **O que outras Machines podem perguntar à minha**: **Livre/ocupado para agendar** ou **Desligada**, junto com a duração da reunião, o intervalo entre reuniões e os horários de sua preferência. Cada solicitação aparece em **Atividade**, em **Calendário**.

Se a outra pessoa não tiver uma Machine ou não responder, o rascunho do e-mail inclui um link para ela escolher um dos seus horários livres. A escolha dela vira uma tarefa com a opção **Marcar**. Nada é agendado antes de você tocar nessa opção.

O link mostra apenas os horários livres, seguindo as mesmas regras, e nenhuma outra informação sobre você. Ele deixa de funcionar quando a reunião é marcada ou depois de 14 dias. No e-mail, ele aparece como “Escolha um horário”. No fim da página, aparece “Sua Machine encontrou estes horários. Tenha a sua.” com seu primeiro nome. Desative essa mensagem em **Rodapé nos links de agendamento**. Cada link e escolha aparece em **Atividade**.

## Uma Machine no seu próprio computador

Para entrar na Network usando uma Machine que você mesmo executa:

1. No painel da sua Machine, abra **Configurações** e selecione **Entrar na Network**.
2. Na página que abrir, entre na sua conta (ou crie uma) e confirme. Sua Machine reconhece a alteração automaticamente, sem precisar reiniciar.

O método com código continua funcionando: selecione **Parear uma Machine auto-hospedada** na página da sua conta em app.themachine.computer. Depois, execute `assistant fleet-pair` com o código no seu computador e reinicie. O código só pode ser usado uma vez e expira após 15 minutos.

Você pode ter até 5 Machines por conta. Cada uma pode ser desconectada nessa página.
