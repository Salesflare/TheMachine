---
title: O app para computador
area: getting-started
summary: A The Machine no Windows, Mac e Linux: seu painel em uma janela própria e um robô no canto da tela.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: 2e9388c58b957501
---
O app para computador abre seu painel em uma janela própria. Um robô pequeno fica no canto da tela: clique nele para criar uma tarefa, perguntar sobre suas mensagens ou ver o que é para você. É um protótipo.

## Download

Cada link sempre leva à versão mais recente:

- Windows 10 ou 11, 64-bit: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac com macOS 13 ou mais recente: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64-bit: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), o [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) para Ubuntu e Debian ou o [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) para Arch e Omarchy

Você também encontra os links no seu painel. Em um computador, **Apps** em **Configurações** lista as três opções. No seu, aparece **Este computador**. A tarefa **Aproveite mais a The Machine** inclui **Baixar o app para computador**, que baixa a versão para seu computador ou abre as instruções para Linux abaixo. Ela desaparece assim que você entra na sua Machine pelo app. Essas opções não aparecem no celular nem dentro do app para computador.

## Windows

Abra o instalador. Ele é instalado só para você, sem precisar de acesso de administrador, e é assinado pela Salesflare. Em um computador que ainda não usa WebView2, a instalação leva alguns segundos a mais para preparar tudo. Depois disso, o app abre imediatamente. O app se atualiza sozinho: em Configurações, você vê quando uma nova versão está pronta.

## Mac

Descompacte o arquivo zip, mova The Machine para Aplicativos e abra o app por lá. O macOS pergunta uma vez se você quer abrir um app baixado da internet: escolha Abrir. O app é assinado e notarizado, e se atualiza sozinho.

## Linux

- Qualquer distribuição: torne o AppImage executável com `chmod +x` e inicie-o. Se aparecer uma mensagem de que o FUSE está faltando, instale `fuse3`.
- Ubuntu 22.04, Debian 12 ou mais recente: `sudo apt install ./the-machine-desktop-amd64.deb`. O pacote inclui WebKitGTK e gtk-layer-shell.
- Arch e Omarchy: coloque o PKGBUILD em uma pasta vazia e execute `makepkg -si` nela. O comando baixa essa versão, confere se ela corresponde ao checksum no arquivo e a instala. No Hyprland, como no Omarchy, o robô fica sobre as outras janelas sem ter uma janela própria.

No Linux, o app não se atualiza sozinho. Para instalar uma versão mais recente, baixe o arquivo ou o PKGBUILD mais novo.

## Conferir um download

Todos os arquivos incluem informações de proveniência da compilação do GitHub, que mostram que foram compilados a partir do código da The Machine pelo próprio workflow. Com a [CLI do GitHub](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Entrar

Na primeira vez, a janela do app abre na tela de entrada. Para uma Machine hospedada ou uma na The Machine Network, o app abre sua conta no navegador e depois volta. Uma Machine hospedada por você precisa do próprio endereço, acessível por um computador na sua rede Tailscale.

Para usar o painel como um app do Chrome ou Edge, consulte [Instalar o app](phone-app.md).

## O robô

O robô some enquanto a janela do app está em primeiro plano e volta quando outra janela fica na frente ou quando você minimiza ou fecha o app. Se você tiver mais de um monitor, ele fica no monitor em que a janela do app está, até você arrastá-lo para outro. No Hyprland, Sway e KDE, ele fica no monitor principal. Para ativar ou desativar o robô: **Configurações** (Ctrl+comma ou Command-comma no Mac), **Mostrar o robô**.
