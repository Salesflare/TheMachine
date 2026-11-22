---
title: Modelo
area: settings
summary: Qual modelo de IA responde para você, quanto ele raciocina e quanto do limite do seu plano já foi usado.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: ee95ad4fa5323e3a
---
**Configurações**, **Modelo** mostra qual modelo de IA faz seu **Trabalho em segundo plano** e como você entrou, por exemplo, com o ChatGPT.

Em uma Machine hospedada com login do ChatGPT, o modelo principal é o GPT-6.2 Sol: respostas mais rápidas que as do GPT-6.1 Sol pelo mesmo preço.

Um plano pessoal do ChatGPT ou do Claude pode usar seus chats para treinamento por padrão: **Desativar o treinamento com seus dados** abre essa configuração no provedor, e **Feito** oculta a linha.

## Modelo e raciocínio dos chats

Em **Chats**, escolha o modelo e o nível de raciocínio para seus chats de tarefas e para a Ajuda. Você só vê os modelos e níveis disponíveis no seu login.

Mais raciocínio ajuda a responder melhor a perguntas difíceis, mas é mais lento e consome mais do seu plano. **Raciocínio ultra** usa assistentes para as perguntas mais difíceis e é o que mais consome. Uma Machine nova começa com **Raciocínio baixo**: bons resultados usando bem menos do seu plano. A alteração vale a partir da próxima mensagem.

Para mudar isso em apenas um chat, toque no modelo ou no nível de raciocínio abaixo da caixa de mensagem. Escolha novamente a opção de Configurações para seguir as Configurações.

As verificações, seu perfil e os rascunhos preparados com antecedência mantêm o próprio modelo.

## Limites

Se seu plano tiver limites de uso, como os limites de 5 horas e semanais de um plano do ChatGPT ou Claude, você verá quanto já foi usado e quando cada limite será redefinido. Consultar não consome seu plano.

## Espaço para seus próprios chats

O trabalho em segundo plano deixa espaço para seus próprios chats. Ele pausa quando o limite de 5 horas chega a cerca de 65%. As verificações de novas mensagens continuam até o limite semanal chegar a cerca de 90%; outros trabalhos usam cerca de um sétimo do limite semanal por dia. Um login sem limites, como uma chave de API, nunca pausa.

O trabalho em segundo plano nunca é executado no GPT-6 Astra. Por enquanto, com login do ChatGPT, ele usa o GPT-6.1 Sol, mesmo quando seu modelo principal é o GPT-6.2 Sol: nesse login, o 6.2 ainda não reutiliza as instruções em cache, então consome mais do seu plano. Seus chats continuam usando o modelo escolhido.

Antes de uma verificação, um modelo pequeno (GPT-6 Luna com o ChatGPT, Haiku com o Claude) separa newsletters, promoções e avisos de apps que claramente não precisam de nada, para que as verificações consumam menos do seu plano. Eles continuam aparecendo na pesquisa. Uma mensagem de uma pessoa, uma conta, um alerta de segurança ou um código de login sempre são verificados.

## Antes de atingir um limite

Se o seu plano do ChatGPT ainda tiver redefinições, **Tarefas** mostra uma linha curta quando o trabalho em segundo plano desacelera: em cerca de 65% do limite de 5 horas ou 90% do limite semanal. Ela diz quanto já foi usado e quantas redefinições restam. **Usar uma redefinição** reinicia os limites, depois que você confirma. × oculta a linha até esse limite ser redefinido. Sem redefinições, nada novo aparece.

Em uma Machine hospedada, sua Machine vê e usa as redefinições assim que o Codex na sua Machine estiver conectado à mesma conta do ChatGPT. Até lá, Tarefas e Configurações mostram **Ativar redefinições**. Isso abre a etapa do Codex na sua página de configuração, onde você entra com um código, como no login do ChatGPT.

## Quando um limite é atingido

No topo do painel, aparece qual limite foi atingido e quando será redefinido. O trabalho aguarda e depois continua de onde parou. Nada se perde. Se seu plano do ChatGPT tiver redefinições, **Usar uma redefinição** reinicia os limites. Em uma Machine hospedada sem o Codex conectado, **Ativar redefinições** abre sua página de configuração. Caso contrário, **Ver redefinições no ChatGPT** abre a página do ChatGPT.

## Com um modelo alternativo

Se sua Machine tiver um modelo alternativo em outro plano ou provedor, ele assume quando um limite é atingido, e nada fica aguardando. No topo do painel, aparece "Limite do ChatGPT atingido. Usando seu modelo alternativo." Se o modelo alternativo parar de funcionar, as pausas voltam.

## Mudar o modelo principal

O modelo principal é usado pelo restante da The Machine. Em uma Machine hospedada, mude-o na página de configuração, em Sua IA. No seu próprio computador, consulte [ChatGPT](chatgpt.md), [Mistral](mistral.md) e o [guia de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
