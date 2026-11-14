---
title: Problemas no seu computador
area: troubleshooting
summary: Sua Machine lê os próprios logs do computador e avisa sobre problemas reais, com a causa e uma solução. Uma solução só é aplicada quando você toca em Fazer.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
translated: 1a191d8433bfba2a
---
## O que ela lê

No Linux com systemd, sua Machine lê o log da sua própria sessão de usuário: seus próprios serviços e os relatórios de falha dos seus próprios programas. No Omarchy, ela também verifica o Hyprland e a barra. Ela nunca lê o log do sistema inteiro nem pede mais acesso.

Ela lê qual serviço parou, como terminou e qual programa travou. Nunca lê o conteúdo das linhas do log, então nenhum texto do log é armazenado ou sai do seu computador.

## O que conta como problema

Um serviço que fica reiniciando, um que falhou várias vezes em um dia ou continua parado, um que ficou sem memória e um programa que travou. No Omarchy, também uma falha do Hyprland ou da barra, e erros nas configurações do Hyprland.

Uma única reinicialização ou uma única execução com falha é normal e não gera avisos. O mesmo vale para um serviço que falhou algumas vezes e depois voltou a funcionar normalmente.

Navegadores controlados por testes e agentes (headless, Playwright, Puppeteer, CI) não geram avisos. O mesmo vale para um programa que para enquanto o serviço está sendo encerrado ou reiniciado. Execuções de desenvolvimento também não geram avisos: o que um agente de programação executa, testes e programas iniciados em uma pasta temporária ou de cache. Um programa que trava repetidamente gera uma única tarefa que informa quantas vezes e quando isso aconteceu.

Um script é identificado pelo próprio nome, como backup.py, não por python3 ou node.

## O que você recebe

Uma tarefa que explica em palavras simples o que aconteceu, por que isso importa e o que você pode fazer. Os comandos que mostram o motivo ficam em **Mostrar mais**. Pergunte no chat da tarefa e The Machine vai investigar. Qualquer alteração que ela fizer fica aguardando sua aprovação, assim como com **Fazer**.

Quando há uma solução segura, a tarefa inclui **Fazer**. Se um serviço seu continuar parado, ela o inicia novamente. No Omarchy, ela também restaura a barra. **Fazer** executa somente aquele comando, e o resultado aparece no chat da tarefa. Ela nunca mexe nos próprios serviços da The Machine nem no OpenClaw Gateway.

O mesmo problema gera no máximo uma tarefa a cada duas semanas, e nunca enquanto a tarefa estiver aberta. São criadas no máximo duas tarefas por dia. Uma tarefa sobre um serviço parado é encerrada automaticamente quando ele volta a funcionar ou é removido.

## No terminal

`assistant doctor` lista os mesmos problemas do último dia.

## Outros computadores

No macOS, no Windows e em computadores sem systemd, ela não lê nada e informa isso em `assistant doctor`.

Em uma Machine hospedada, a responsabilidade por manter o servidor funcionando é nossa: os problemas são enviados à equipe da The Machine, não a você como tarefas.

## Desativar

Defina `"computer_logs": false` em config.json e reinicie o serviço.
