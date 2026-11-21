---
title: Problemas no seu computador
area: troubleshooting
summary: Sua Machine lê os próprios registros do computador e avisa sobre problemas reais, explicando a causa e como corrigir. Uma correção só é executada quando você toca em Fazer.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: b18e5f4989d6baff
---
## O que ela lê

No Linux com systemd, sua Machine lê o registro da sua própria sessão de usuário: seus próprios serviços e os relatórios de falha dos seus próprios programas. No Omarchy, ela também verifica o Hyprland e a barra. Ela nunca lê o registro de todo o sistema nem pede mais acesso.

Ela lê qual serviço parou, como terminou e qual programa travou. Nunca lê o conteúdo das linhas de registro, então nenhum texto dos registros é guardado ou sai do seu computador.

## O que é considerado um problema

Um serviço que fica reiniciando, um serviço que falha várias vezes em um dia ou continua parado, um serviço que fica sem memória e um programa que trava. No Omarchy, ela também verifica falhas do Hyprland ou da barra e erros nas configurações do Hyprland.

Uma única reinicialização ou falha é normal e não gera avisos. O mesmo vale para um serviço que falhou algumas vezes, mas voltou a funcionar, e para um serviço com falha que ninguém tenta iniciar: um serviço que não está habilitado e que nenhum outro serviço ou temporizador inicia.

Navegadores controlados por testes e agentes (headless, Playwright, Puppeteer, CI) não geram avisos. O mesmo vale para programas que param enquanto o serviço está sendo interrompido ou reiniciado. Execuções de desenvolvimento também não geram avisos: o que um agente de programação executa, testes e programas iniciados de uma pasta temporária ou de cache. Se um programa trava várias vezes, uma única tarefa informa quantas vezes isso aconteceu e quando.

Um script é identificado pelo próprio nome, como backup.py, não por python3 ou node.

## O que você recebe

Uma tarefa que explica em palavras simples o que aconteceu, por que isso importa e o que você pode fazer. Os comandos que mostram o motivo ficam em **Mostrar mais**. Pergunte no chat da tarefa e The Machine vai investigar. Qualquer alteração que ela fizer espera sua aprovação, assim como em **Fazer**.

Quando há uma correção segura, a tarefa inclui **Fazer**. Se um serviço seu continua parado, ela o inicia novamente. No Omarchy, ela também restaura a barra. **Fazer** executa somente aquele comando, e o resultado aparece no chat da tarefa. Ela nunca mexe nos próprios serviços de The Machine nem no OpenClaw Gateway.

O mesmo problema gera no máximo uma tarefa a cada duas semanas e nunca enquanto a tarefa ainda estiver aberta. São criadas no máximo duas tarefas por dia. Uma tarefa sobre um serviço parado é encerrada automaticamente quando ele volta a funcionar ou o problema é resolvido.

## No terminal

`assistant doctor` lista os mesmos problemas das últimas 24 horas.

## Outros computadores

No macOS, Windows e em computadores sem systemd, ela não lê nada e informa isso em `assistant doctor`.

Em uma Machine hospedada, nossa equipe mantém o servidor funcionando. Os problemas dele são enviados à equipe de The Machine, não aparecem para você como tarefas.

## Desativar

Defina `"computer_logs": false` em config.json e reinicie o serviço.
