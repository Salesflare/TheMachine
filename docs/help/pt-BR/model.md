---
title: Modelo
area: settings
summary: Qual modelo de IA responde para você, quanto ele raciocina e quanto dos limites do seu plano já foi usado.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 9a0777c555ab5637
---
**Configurações**, **Modelo** mostra qual modelo de IA faz o **Trabalho em segundo plano** da sua Machine e como você está conectado, por exemplo, com o ChatGPT.

Em uma Machine hospedada com login do ChatGPT, o modelo principal é GPT-6.2 Sol: respostas mais rápidas que as do GPT-6.1 Sol pelo mesmo preço.

O login da Claude expira cerca de quatro semanas depois de você entrar. **Precisa de você** avisa com três dias de antecedência. Quando o login expira, você recebe uma notificação. **Entrar de novo** resolve isso em uma etapa.

Um plano pessoal do ChatGPT ou da Claude pode usar suas conversas para treinamento por padrão. **Desativar o treinamento com seus dados** abre essa configuração no serviço, e **Feito** oculta a linha.

## Modelo e raciocínio nos chats

Em **Chats**, escolha o modelo e o nível de raciocínio para seus chats de tarefas e para a Ajuda. Você só vê os modelos e níveis disponíveis no seu login.

Mais raciocínio ajuda a responder melhor a perguntas difíceis, mas deixa as respostas mais lentas e consome mais do seu plano. **Raciocínio ultra** usa assistentes para as perguntas mais difíceis e consome mais do seu plano. Uma Machine nova começa com **Raciocínio baixo**: bons resultados usando bem menos do seu plano. A mudança vale a partir da próxima mensagem.

Para mudar o modelo ou o nível de raciocínio só em um chat, toque na opção abaixo da caixa de mensagem. Escolha novamente a opção das Configurações para seguir as Configurações.

As verificações, seu perfil e os rascunhos preparados com antecedência usam seus próprios modelos.

## Limites

Se seu plano tiver limites de uso, como os limites de 5 horas e semanais de um plano do ChatGPT ou da Claude, a tela mostra quanto já foi usado e quando cada limite será redefinido. Consultar a tela não consome seu plano.

## Espaço para seus próprios chats

O trabalho em segundo plano deixa espaço para seus próprios chats. Ele pausa quando o limite de 5 horas chega a cerca de 65%. As verificações de novas mensagens continuam até o limite semanal chegar a cerca de 90%. O restante do trabalho consome cerca de um sétimo do limite semanal por dia. Um login sem limites, como uma chave de API, nunca pausa.

O trabalho em segundo plano nunca é executado com GPT-6 Astra. Com um login do ChatGPT e uma versão do OpenClaw anterior a 2026.11.10, ele usa GPT-6.1 Sol, mesmo que seu modelo principal seja GPT-6.2 Sol. Nesse caso, o GPT-6.2 não reutiliza as instruções em cache e consome mais do seu plano. A partir do OpenClaw 2026.11.10, o trabalho em segundo plano volta a usar seu modelo principal. Seus chats continuam usando o modelo que você escolheu.

Antes de uma verificação, um modelo pequeno (GPT-6 Luna com o ChatGPT, Haiku com a Claude) separa newsletters, promoções e avisos de apps que claramente não precisam de atenção. Assim, as verificações consomem menos do seu plano. Esses itens continuam aparecendo nas buscas. Mensagens de pessoas, contas, alertas de segurança e códigos de login sempre são verificados.

## Antes de atingir um limite

Se ainda houver redefinições no seu plano do ChatGPT, Tarefas mostra uma linha breve quando o trabalho em segundo plano fica mais lento: quando o limite de 5 horas chega a cerca de 65% ou o limite semanal chega a cerca de 90%. A linha mostra quanto já foi usado e quantas redefinições restam. **Usar uma redefinição** reinicia os limites depois que você confirmar. × oculta a linha até o limite ser redefinido. Se não houver redefinições, nada novo será exibido.

Em uma Machine hospedada, sua Machine vê e usa as redefinições quando o Codex na sua Machine está conectado à mesma conta do ChatGPT. Até lá, Tarefas e Configurações mostram **Ativar redefinições**. Essa opção abre a etapa do Codex na página de configuração, onde você entra com um código, como no login do ChatGPT.

## Quando um limite é atingido

Na parte de cima do painel, a tela informa qual limite foi atingido e quando ele será redefinido. O trabalho fica aguardando e depois continua de onde parou. Nada é perdido. Se seu plano do ChatGPT tiver redefinições, **Usar uma redefinição** reinicia os limites. Em uma Machine hospedada sem o Codex conectado, **Ativar redefinições** abre a página de configuração. Caso contrário, **Ver redefinições no ChatGPT** abre a página do ChatGPT.

## Com um modelo alternativo

Se sua Machine tiver um modelo alternativo em outro plano ou serviço, ele assume quando um limite é atingido e o trabalho não fica aguardando. Na parte de cima do painel, a tela mostra: "Limite do ChatGPT atingido. Usando seu modelo alternativo." Se o modelo alternativo parar de funcionar, as pausas voltam.

## Mudar o modelo principal

O modelo principal é usado pelo restante da The Machine. Em uma Machine hospedada, mude o modelo na página de configuração, em Sua IA. No seu próprio computador, consulte [ChatGPT](chatgpt.md), [Mistral](mistral.md) e o [guia de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
