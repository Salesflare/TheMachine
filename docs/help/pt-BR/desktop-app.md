---
title: O app para computador
area: getting-started
summary: A The Machine no Windows, Mac e Linux: seu painel em uma janela própria e um robô no canto da tela.
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: af0a8a2994af969d
---
O app para computador abre seu painel em uma janela própria. Um robô pequeno fica no canto da tela: clique nele para adicionar uma tarefa, perguntar sobre suas mensagens ou ver o que é para você. É um protótipo.

## Baixar o app

Cada link sempre tem a versão mais recente:

- Windows 10 ou 11, 64 bits: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- Mac com macOS 13 ou mais recente: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64 bits: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), o [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb) para Ubuntu e Debian ou o [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD) para Arch e Omarchy

Eles também aparecem no seu painel. No computador, **Configurações**, **Apps** lista os três, e **Este computador** identifica o app instalado nele. A tarefa **Aproveite mais a The Machine** inclui **Baixar o app para computador**, que baixa a versão para o seu computador ou abre as instruções para Linux abaixo. A tarefa desaparece quando o app entra na sua Machine. Ela não aparece no celular nem dentro do app para computador.

## Windows

Abra o instalador. Ele instala o app só para você, sem precisar de permissões de administrador, e é assinado pela Salesflare. Em um computador que nunca usou o WebView2, a instalação demora alguns segundos a mais para configurá-lo. Depois disso, o app abre imediatamente. O app se atualiza sozinho. Em Configurações, você vê quando uma nova versão está pronta.

## Mac

Descompacte o arquivo zip, mova The Machine para Aplicativos e abra o app de lá. O macOS pergunta uma vez se você quer abrir um app baixado da internet: selecione Abrir. O app é assinado e notarizado, e se atualiza sozinho.

## Linux

- Qualquer distribuição: torne o AppImage executável com `chmod +x` e inicie-o. Se aparecer uma mensagem dizendo que o FUSE está faltando, instale `fuse3`.
- Ubuntu 22.04, Debian 12 ou mais recente: `sudo apt install ./the-machine-desktop-amd64.deb`. O pacote já inclui WebKitGTK e gtk-layer-shell.
- Arch e Omarchy: coloque o PKGBUILD em uma pasta vazia e execute `makepkg -si` nela. O comando baixa essa versão, confere o arquivo com a soma de verificação indicada no próprio arquivo e instala o app. No Hyprland, como configurado no Omarchy, o robô fica acima das outras janelas sem ter uma janela própria.

O AppImage se atualiza sozinho quando está em uma pasta sua, como ~/Applications. Em Configurações, você vê quando uma nova versão está pronta. O .deb e o pacote do Arch são atualizados pelo apt e pelo pacman: em Configurações, você vê quando há uma versão mais recente, com a opção de baixar o .deb ou o PKGBUILD. Um AppImage descompactado em uma pasta não se atualiza sozinho. Use o AppImage como está.

## Conferir um download

Todos os arquivos incluem a procedência de compilação do GitHub, que mostra que foram compilados a partir do código da The Machine pelo próprio fluxo de trabalho do projeto. Com a [CLI do GitHub](https://cli.github.com): `gh attestation verify <file> -R Salesflare/TheMachine`.

## Entrar

Na primeira vez, a janela do app abre para você entrar. Para uma Machine hospedada ou uma na The Machine Network, o app abre sua conta no navegador e depois volta para o app. Para uma Machine hospedada por você, é preciso informar o endereço dela, usando um computador na sua rede do Tailscale.

Uma página da sua Machine pode trazer o app para a frente com um link próprio, `computer.themachine.desktop://open`. O link só abre o app, sem incluir nenhuma informação.

Para usar o painel como um app do Chrome ou Edge, consulte [Instalar o app](phone-app.md).

## O robô

O robô desaparece quando a janela do app está em primeiro plano e reaparece quando outra janela fica na frente ou quando você minimiza ou fecha a janela. Se você tiver mais de um monitor, ele fica no monitor onde está a janela do app, até você arrastá-lo para outro lugar. No Hyprland, Sway e KDE, ele fica no monitor principal. Para ativar ou desativar o robô: **Configurações** (Ctrl+comma ou Command-comma no Mac), **Mostrar o robô**.
