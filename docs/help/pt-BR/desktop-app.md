---
title: O app para desktop
area: getting-started
summary: Sua Machine no Windows, Mac e Linux: seu painel em uma janela própria e um robô no canto da tela.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: baeef035dc2e24bd
---
O app para desktop abre seu painel em uma janela própria. Um pequeno robô fica no canto da tela: clique nele para adicionar uma tarefa, perguntar sobre suas mensagens ou ver o que é para você. É um protótipo.

## Baixar

Cada link sempre tem a versão mais recente:

- Windows 10 ou 11, 64 bits: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac com macOS 13 ou mais recente: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bits: o [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), o [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) para Ubuntu e Debian ou o [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) para Arch e Omarchy

## Windows

Abra o instalador. Ele instala o app só para você, sem precisar de administrador, e é assinado pela Salesflare. Em um computador que nunca usou o WebView2, a configuração leva alguns segundos a mais. Depois disso, o app inicia imediatamente. O app se atualiza sozinho: em **Configurações**, você vê quando uma nova versão está pronta.

## Mac

Descompacte o arquivo ZIP, mova The Machine para Aplicativos e abra o app por lá. O macOS pergunta uma vez se você quer abrir um app baixado da internet: escolha **Abrir**. O app é assinado e notarizado e se atualiza sozinho.

## Linux

- Qualquer distribuição: torne o AppImage executável com `chmod +x` e inicie-o. Se aparecer uma mensagem dizendo que falta o FUSE, instale `fuse2` no Arch ou `libfuse2t64` no Ubuntu 24.04.
- Ubuntu 22.04, Debian 12 ou mais recente: `sudo apt install ./the-machine-desktop-amd64.deb`. O pacote inclui WebKitGTK e gtk-layer-shell.
- Arch e Omarchy: coloque o PKGBUILD em uma pasta vazia e execute `makepkg -si` nessa pasta. O comando baixa essa versão, verifica se ela corresponde ao checksum no arquivo e a instala. No Hyprland, como no Omarchy, o robô fica acima das outras janelas sem ter uma janela própria.

No Linux, o app não se atualiza sozinho. Para instalar uma versão mais recente, baixe o arquivo novamente ou baixe o PKGBUILD mais recente.

## Fazer login

Na primeira vez, a janela do app abre na tela de login. Se você usa uma Machine hospedada ou uma na The Machine Network, o app abre sua conta no navegador e depois volta. Para uma Machine auto-hospedada, informe o endereço dela, acessível por um computador da sua rede Tailscale.

Para usar o painel como um app do Chrome ou do Edge, consulte [Instalar o app](phone-app.md).
