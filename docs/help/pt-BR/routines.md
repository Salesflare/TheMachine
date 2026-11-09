---
title: Rotinas
area: cards
summary: Trabalho que sua Machine faz sozinha, num ritmo, como um resumo de segunda-feira dos seus deals abertos. Ela só lê.
covers: tab:routines
code: routines.py, routines_app.py, routine_recipe.py, routine_imports.py, routine_patterns.py, routine_changes.py, dashboard/routines-page.js
order: 10
keywords: routine, automation, scheduled, every week, every morning, report, suggested, digest, newsletter
---
## Criar uma

Abra **Rotinas** na barra lateral e diga numa linha o que ela deve fazer e quando: "toda segunda às 9, resuma meus deals abertos" ou "todo dia útil de manhã, liste os e-mails que ainda devo responder". Depois **Adicionar**.

Sem horário, ela roda às 8:00. O horário é o do relógio da sua Machine.

## O que uma rotina faz

Na hora marcada, sua Machine lê o que precisa, como suas mensagens, reuniões e o Graph, e coloca o resultado na página Rotinas. Cada resultado diz **Para revisar**, **Nada de novo** (com o porquê) ou **Não funcionou** (com o porquê). Uma execução que termina sem resultado conta como uma que não funcionou, nunca como feita.

Rotinas só leem: suas mensagens, páginas da web, o GitHub e sites como o X no navegador. Elas não enviam, respondem, publicam nem mudam nada.

Quando a tarefa de uma rotina termina num post ou numa mensagem, ela faz tudo até essa etapa e mostra o rascunho, como **Postaria no X:**. Depois de uma execução real, você recebe como tarefa para aprovar; uma execução de teste só mostra. O nome diz do que se trata e para onde vai, o botão diz a etapa, como **Publicar**, e **Da sua rotina** embaixo abre a rotina.

A tarefa começa na área da conta de onde sai, como Trabalho para a conta do X da sua empresa, então nunca pede para mudar.

Cada execução conhece o último resultado, então pode dizer o que mudou desde então.

Depois de uma boa execução, sua Machine pode escrever para si uma receita para a leitura que é igual toda vez, como quais e-mails ou mudanças no GitHub olhar. As próximas execuções leem isso primeiro, em código simples, e a IA só escolhe o que importa e escreve, com menos tokens. Uma receita só lê; se parar de funcionar, a execução lê por conta própria e a conserta. Ela aparece em **Avançado: etapas de script** no menu ⋯.

## Dias perdidos

Se sua Machine estava desligada ou ocupada, as execuções perdidas não se acumulam: só a mais recente roda, uma vez. Cada data roda uma vez, mesmo depois de reiniciar.

As rotinas rodam uma de cada vez e esperam quando o uso do seu plano de IA está baixo, como todo o trabalho em segundo plano. **Rodar agora** roda na hora.

## Mudar ou parar

Fica no menu ⋯ da rotina. **Mudar quando** aceita um novo ritmo com suas próprias palavras, como "todo dia útil às 8". **Pausar** para as execuções até **Retomar**; o que foi perdido durante a pausa não roda depois. **Parar** encerra uma rotina de vez.

Quando você usa **Pedir mudanças** em uma tarefa de uma rotina e sua nota vale para toda execução, como "nunca use emoji", a tarefa oferece **Mudar também a rotina**. Ela mostra o que muda nas palavras da rotina, e a rotina só muda quando você toca em **Mudar**. **Deixar como está** a deixa como está. Uma correção só desse rascunho não oferece nada.

## Avançado: etapas de script

Você nunca precisa de um script: diga com suas palavras o que uma rotina deve fazer.

Para usuários avançados, uma rotina também pode rodar seus próprios comandos na sua Machine: no menu ⋯, escolha **Avançado: etapas de script**. **Editar** só as mostra se uma rotina já tiver. **Buscar dados** roda primeiro um comando, na pasta dele (vazia: sua pasta pessoal) e no máximo pelos segundos dele. O que ele imprime vai para a execução trabalhar. Sem palavras, o que ele imprime é o resultado.

**Verificação** recebe o resultado como entrada depois da execução. Se terminar com erro, a execução mostra **Não funcionou** com o que a verificação disse. Um comando de Buscar dados que falha aparece do mesmo jeito.

Um comando é uma linha e roda sem shell: sem pipes nem variáveis. As etapas de script são suas, definidas só no seu painel. Uma execução de teste e **Testar** também rodam Buscar dados e avisam; continuam sem enviar nem guardar nada. Uma rotina nunca envia, então uma etapa de script deve só ler.

## Dos seus jobs do OpenClaw

Se você criou jobs agendados no OpenClaw antes, sua Machine os lê (ela nunca os muda) e oferece os que servem como rotinas em **Sugerido**. Cada um rodou uma vez, para você ver um resultado real.

Ela mantém suas correções no job e deixa de fora o que ele enviava ou publicava. Um job que rodava um script, ou lia o que um job de script coletava, traz isso como Buscar dados. **Adicionar** transforma em rotina, **Não, obrigado** nunca mais pergunta sobre esse job. Um job que lembrava você de fazer algo chega como oferta de tarefa recorrente em Tarefas.

No máximo três sugestões esperam ao mesmo tempo. Depois de uma semana de boas execuções, a rotina pergunta **Desativar o antigo job do OpenClaw?** Ele só é desativado quando você toca em **Desativar**, e você pode reativá-lo no OpenClaw.

## Do que você faz

Sua Machine também percebe trabalho que você faz num ritmo e o oferece como rotina em **Sugerido**, mesmo sem OpenClaw. Ela procura:

- o mesmo pedido, três vezes ou mais seguidas, como "resuma os tickets de suporte abertos" toda segunda;
- um e-mail que você envia num ritmo, como um relatório semanal para sua equipe;
- newsletters e e-mails de novidades que chegam toda semana;
- um canal do Slack movimentado onde outras pessoas escrevem toda semana;
- e-mails que você encaminha um por um para a mesma pessoa, como os da escola e do clube para quem divide a casa com você: um resumo semanal para essa pessoa poupa os encaminhamentos;
- o mesmo pedido que você responde num ritmo, como uma aprovação mensal para a mesma pessoa.

Cada sugestão diz o que viu, como "Pedido 4 vezes seguidas" ou "6 emails encaminhados para Sam em 3 semanas", e rodou uma vez para você ver um resultado real. Pense num resumo da equipe, um briefing antes de uma call semanal, um resumo de suporte ou de desenvolvimento, o pulso dos seus números ou um resumo das newsletters que você recebe.

Ela só sugere o que é seu e claramente útil: um resumo de notícias só das suas próprias newsletters, nunca um genérico. Quando nada serve, não há sugestão.

Ela olha no máximo uma vez por dia e traz no máximo uma sugestão nova por semana, sem notificação. **Não, obrigado** nunca a traz de volta. Encaminhamentos e respostas ficam com a conta de onde saíram, para que Trabalho e Pessoal não se misturem. Tudo fica na sua Machine. Uma tarefa que você fecha num ritmo chega como oferta de tarefa recorrente.

## Rotinas e tarefas recorrentes

Uma tarefa recorrente (recurring.md) lembra você de fazer algo. Uma rotina é trabalho que sua Machine faz sozinha e mostra para você. Use uma tarefa recorrente para "pagar o aluguel no dia 1", e uma rotina para "toda sexta, diga quais deals ficaram parados".
