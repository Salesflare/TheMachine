---
title: Problemas no seu computador
area: troubleshooting
summary: Sua Machine lê os registros do próprio computador e avisa sobre problemas reais, com a causa e uma solução. Uma correção só roda quando você toca em Do it.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
---
## O que ela lê

No Linux com systemd, sua Machine lê o registro da sua própria sessão: seus próprios serviços e os relatórios de falha dos seus próprios programas. No Omarchy ela também confere o Hyprland e a barra. Ela nunca lê o registro do sistema inteiro e nunca pede mais acesso.

Ela lê qual serviço parou, como terminou e qual programa travou. Nunca o que diz uma linha do registro, então nenhum texto do registro é guardado nem sai do seu computador.

## O que conta como problema

Um serviço que fica reiniciando, um que falhou várias vezes em um dia ou continua parado, um que ficou sem memória e um programa que travou. No Omarchy também uma falha do Hyprland ou da barra, e erros nas suas configurações do Hyprland.

Um único reinício ou uma única execução com falha é normal e não gera aviso.

## O que você recebe

Uma tarefa que diz em palavras simples o que aconteceu, por que importa e o que você pode fazer. Os comandos que mostram o porquê ficam em Mostrar mais. Pergunte no chat dela e The Machine verifica. Tudo o que ela mudar espera o seu OK, como no Do it.

Quando há uma correção segura, a tarefa tem Do it. Um serviço seu que continua parado é iniciado de novo, e no Omarchy a barra volta. O Do it executa só esse comando, e o resultado aparece no chat da tarefa. Ele nunca mexe nos serviços da própria The Machine nem no OpenClaw Gateway.

O mesmo problema gera no máximo uma tarefa a cada duas semanas, e nunca enquanto a tarefa dele ainda estiver aberta. No máximo duas novas por dia.

## Em um terminal

`assistant doctor` lista os mesmos problemas do último dia.

## Outros computadores

No macOS, no Windows e em computadores sem systemd ela não lê nada e diz isso no `assistant doctor`.

## Desativar

Coloque `"computer_logs": false` no config.json e reinicie o serviço.
