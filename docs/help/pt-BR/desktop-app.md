---
title: O app para computador
area: getting-started
summary: A Machine no Windows, Mac e Linux: seu painel em uma janela própria e um robô em um canto da tela.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: abfbc82137a6f702
---
O app para computador abre seu painel em uma janela própria. Um robô pequeno fica em um canto da tela. Clique nele para adicionar uma tarefa, perguntar sobre suas mensagens ou ver o que é para você. É um protótipo.

## Baixar

Cada link sempre tem a versão mais recente:

- Windows 10 ou 11, 64 bits: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac com macOS 13 ou mais recente: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bits: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), o [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) para Ubuntu e Debian ou o [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) para Arch e Omarchy

## Windows

Abra o instalador. Ele instala o app só para você, sem precisar de administrador, e é assinado pela Salesflare. Em um computador que nunca usou o WebView2, a preparação leva alguns segundos a mais. Depois disso, o app abre na hora. Ele se atualiza sozinho. Em **Configurações**, você vê quando uma nova versão está pronta.

## Mac

Descompacte o arquivo, mova The Machine para Applications e abra o app por lá. O macOS pergunta uma vez se você quer abrir um app baixado da internet. Escolha **Abrir**. O app é assinado e notarizado, e se atualiza sozinho.

## Linux

- Qualquer distribuição: torne o AppImage executável com `chmod +x` e inicie o app. Se aparecer uma mensagem dizendo que o FUSE está faltando, instale `fuse3`.
- Ubuntu 22.04, Debian 12 ou mais recente: `sudo apt install ./the-machine-desktop-amd64.deb`. O pacote inclui WebKitGTK e gtk-layer-shell.
- Arch e Omarchy: coloque o PKGBUILD em uma pasta vazia e execute `makepkg -si` nela. O comando baixa essa versão, confere se ela corresponde ao checksum no arquivo e a instala. No Hyprland, como no Omarchy, o robô fica acima das outras janelas sem ter uma janela própria.

No Linux, o app não se atualiza sozinho. Para instalar uma versão mais recente, baixe o arquivo novamente ou use o PKGBUILD mais recente.

## Verificar um download

Cada arquivo tem um atestado de build do GitHub, que mostra que ele foi criado a partir do código da The Machine pelo workflow da própria The Machine. Com a [CLI do GitHub](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Entrar

Na primeira vez, a janela do app abre para você entrar. Se for uma Machine hospedada ou uma na The Machine Network, o app abre sua conta no navegador e depois volta para ele. Para uma Machine hospedada por você, informe o endereço dela, acessível por um computador na sua rede Tailscale.

Se preferir usar o painel como um app do Chrome ou Edge, veja [Instalar o app](phone-app.md).
