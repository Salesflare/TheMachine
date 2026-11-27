---
title: Modelo
area: settings
summary: Qual modelo de IA responde por você, quanto ele raciocina e quanto dos limites do seu plano já foi usado.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: b76f4f927bfd7be1
---
**Configurações**, **Modelo** mostra qual modelo de IA faz o **Trabalho em segundo plano** e como você está conectado, por exemplo, pelo ChatGPT.

Em uma Machine hospedada com uma conta do ChatGPT conectada, o modelo principal é o GPT-6.2 Sol: respostas mais rápidas que as do GPT-6.1 Sol pelo mesmo preço.

Em uma Machine hospedada, a conexão com Claude dura cerca de um ano. Com `claude auth login`, ela termina cerca de quatro semanas depois que você se conectou. Três dias antes, **Precisa de você** avisa, e você recebe um e-mail. Quando a conexão termina, você recebe uma notificação e, se ainda não tiver recebido, aquele e-mail. **Entrar de novo** resolve isso em uma etapa.

Um plano pessoal do ChatGPT ou Claude pode usar suas conversas para treinamento por padrão. **Desativar o treinamento com seus dados** abre essa configuração no serviço, e **Feito** oculta o aviso.

## Modelo e raciocínio nas conversas

Em **Chats**, escolha o modelo e o nível de raciocínio para suas conversas sobre tarefas e para a Ajuda. Você só vê os modelos e níveis disponíveis na sua conta conectada.

Mais raciocínio ajuda a responder melhor a perguntas difíceis, mas é mais lento e usa mais do seu plano. **Raciocínio ultra** usa assistentes para as perguntas mais difíceis e consome mais. Uma Machine nova começa com **Raciocínio baixo**: bons resultados usando bem menos do seu plano. A mudança vale a partir da próxima mensagem.

Para mudar o modelo ou o nível de raciocínio só em uma conversa, toque no modelo ou no nível de raciocínio abaixo da caixa de mensagem. Selecione novamente a opção Configurações para seguir as Configurações.

As verificações, seu perfil e os rascunhos preparados com antecedência usam modelos próprios.

## Limites

Se seu plano tiver limites de uso, como os limites de 5 horas e semanais de um plano do ChatGPT ou Claude, você verá quanto já foi usado e quando cada limite será redefinido. Consultar essas informações não usa seu plano.

## Espaço para suas conversas

O Trabalho em segundo plano deixa espaço para suas conversas. Ele pausa quando você usa cerca de 65% do limite de 5 horas. As verificações de novas mensagens continuam até você usar cerca de 90% do limite semanal. Outros trabalhos usam cerca de um sétimo do limite semanal por dia. Uma conta sem limites, como uma chave de API, nunca pausa.

O Trabalho em segundo plano nunca é executado no GPT-6 Astra. Com uma conta do ChatGPT conectada e uma versão do OpenClaw anterior à 2026.11.10, ele usa o GPT-6.1 Sol, mesmo que seu modelo principal seja o GPT-6.2 Sol. Nesse caso, o 6.2 não reutiliza as instruções armazenadas em cache e, por isso, usa mais do seu plano. A partir do OpenClaw 2026.11.10, o Trabalho em segundo plano volta a usar seu modelo principal. Suas conversas continuam usando o modelo que você escolheu.

Antes de uma verificação, um modelo pequeno (GPT-6 Luna no ChatGPT, Haiku no Claude) separa newsletters, promoções e avisos de apps que claramente não precisam de atenção, para que as verificações usem menos do seu plano. Eles continuam disponíveis na busca. Mensagens escritas por uma pessoa, contas, alertas de segurança e códigos de acesso sempre são verificados.

## Antes de atingir um limite

Se ainda houver redefinições disponíveis no seu plano do ChatGPT, Tarefas mostra um aviso curto quando o Trabalho em segundo plano fica mais lento: quando você usa cerca de 65% do limite de 5 horas ou 90% do limite semanal. O aviso mostra quanto já foi usado e quantas redefinições restam. **Usar uma redefinição** reinicia os limites depois que você confirmar. × oculta o aviso até o limite ser redefinido. Se não houver redefinições, nada aparece.

Em uma Machine hospedada, sua Machine reconhece e usa as redefinições assim que o Codex na sua Machine estiver conectado à mesma conta do ChatGPT. Até lá, Tarefas e Configurações mostram **Ativar redefinições**. Essa opção abre a etapa do Codex na página de configuração, onde você entra com um código, como na conexão com o ChatGPT.

## Quando um limite é atingido

No topo do painel, aparece qual limite foi atingido e quando será redefinido. O trabalho fica aguardando e depois continua de onde parou. Nada se perde. Se seu plano do ChatGPT tiver redefinições, **Usar uma redefinição** reinicia os limites. Em uma Machine hospedada sem o Codex conectado, **Ativar redefinições** abre a página de configuração. Caso contrário, **Ver redefinições no ChatGPT** abre a página do ChatGPT.

## Com um modelo alternativo

Se sua Machine tiver um modelo alternativo em outro plano ou serviço, ele assume quando um limite é atingido e nada fica aguardando. No topo do painel, aparece "Limite do ChatGPT atingido, usando seu modelo alternativo." Se o modelo alternativo parar de funcionar, as pausas voltam.

## Mudar o modelo principal

O modelo principal é o modelo usado pelo restante da The Machine. Em uma Machine hospedada, mude-o na página de configuração, em Sua IA. No seu computador, consulte [ChatGPT](chatgpt.md), [Mistral](mistral.md) e o [guia de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
