---
title: O app para computador
area: getting-started
summary: A The Machine no Windows, Mac e Linux: seu painel em uma janela própria e um robô no canto da tela.
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: c590899c2622b818
---
O app para computador abre seu painel em uma janela própria. Um pequeno robô fica no canto da tela: clique nele para adicionar uma tarefa, perguntar sobre suas mensagens ou ver o que é para você. É um protótipo.

## Baixe o app

Cada link sempre leva à versão mais recente:

- Windows 10 ou 11, 64 bits: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac com macOS 13 ou mais recente: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bits: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) para Ubuntu e Debian ou [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) para Arch e Omarchy

Você também encontra os downloads no seu painel. Em um computador, **Configurações** > **Apps** lista os três, e o download para o computador que você está usando aparece como **Este computador**. A tarefa **Aproveite mais a The Machine** inclui **Baixar o app para computador**, que baixa a versão para o seu computador ou abre as instruções para Linux abaixo. A tarefa desaparece quando o app está conectado à sua Machine. Essas opções não aparecem no celular nem dentro do app para computador.

## Windows

Abra o instalador. Ele é instalado só para você, sem precisar de administrador, e é assinado pela Salesflare. Em um computador que ainda não tenha usado o WebView2, a instalação dele leva alguns segundos a mais. Depois, o app abre imediatamente. O app se atualiza sozinho: em **Configurações**, você vê quando uma nova versão está pronta.

## Mac

Descompacte o arquivo zip, mova a The Machine para Aplicativos e abra o app por lá. O macOS pergunta uma vez se você quer abrir um app baixado da internet: escolha **Abrir**. O app é assinado e notarizado, e se atualiza sozinho.

## Linux

- Qualquer distribuição: torne o AppImage executável com `chmod +x` e inicie-o. Se aparecer uma mensagem dizendo que o FUSE está faltando, instale `fuse3`.
- Ubuntu 22.04, Debian 12 ou mais recente: `sudo apt install ./the-machine-desktop-amd64.deb`. Ele já inclui o WebKitGTK e o gtk-layer-shell.
- Arch e Omarchy: coloque o PKGBUILD em uma pasta vazia e execute `makepkg -si` nela. Ele baixa essa versão, confere se ela corresponde ao checksum no arquivo e a instala. No Hyprland, como no Omarchy, o robô fica acima das outras janelas sem ter uma janela própria.

O AppImage se atualiza sozinho quando está em uma pasta sua, como ~/Applications: em **Configurações**, você vê quando uma nova versão está pronta. O .deb e o pacote do Arch são gerenciados pelo apt e pelo pacman: em **Configurações**, você vê quando há uma versão mais recente, com **Baixar** para baixar o .deb ou o PKGBUILD. Um AppImage extraído em uma pasta não se atualiza sozinho. Use o AppImage como está.

## Conferir um download

Todos os arquivos têm a procedência de build do GitHub, que mostra que foram compilados a partir do código da The Machine pelo próprio fluxo de trabalho dela. Com o [GitHub CLI](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Entrar

Na primeira vez, a janela do app abre com a tela de entrada. Para uma Machine hospedada ou uma na The Machine Network, o app abre sua conta no navegador e depois volta para o app. Para uma Machine auto-hospedada, use o endereço dela em um computador da sua rede Tailscale.

Para usar o painel como um app do Chrome ou Edge, consulte [Instalar o app](phone-app.md).

## O robô

O robô some enquanto a janela do app está em primeiro plano e volta quando outra janela fica em primeiro plano ou quando você minimiza ou fecha a janela. Se você tiver mais de um monitor, ele aparece no monitor em que está a janela do app, até você arrastá-lo para outro (no Hyprland, Sway e KDE, ele fica no monitor principal). Para ativar ou desativar o robô: **Configurações** (Ctrl+comma ou Command-comma no Mac), **Mostrar o robô**.
