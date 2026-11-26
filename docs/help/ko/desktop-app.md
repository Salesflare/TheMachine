---
title: 데스크톱 앱
area: getting-started
summary: Windows, Mac, Linux에서 사용하는 The Machine이에요. 전용 창으로 대시보드를 열고 화면 한쪽 구석에 로봇을 표시해요.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: baeef035dc2e24bd
---
데스크톱 앱을 열면 전용 창으로 대시보드가 열려요. 화면 한쪽 구석에 작은 로봇이 표시돼요. 로봇을 클릭하면 할 일을 추가하거나 메시지에 관해 질문하거나 나를 위한 항목을 확인할 수 있어요. 프로토타입이에요.

## 다운로드

각 링크에서 항상 최신 버전을 다운로드할 수 있어요.

- Windows 10 또는 11, 64비트: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- macOS 13 이상을 사용하는 Mac: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64비트: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), Ubuntu 및 Debian용 [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb), Arch 및 Omarchy용 [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

## Windows

설치 프로그램을 열어요. 관리자 권한 없이 현재 사용자만 설치할 수 있으며, Salesflare에서 서명했어요. WebView2를 사용한 적 없는 컴퓨터에서는 준비하는 데 몇 초 더 걸려요. 준비가 끝나면 앱이 바로 시작돼요. 앱은 자동으로 업데이트돼요. 새 버전을 사용할 수 있으면 **설정**에 표시돼요.

## Mac

zip 파일을 풀고 The Machine을 Applications로 옮긴 다음 그곳에서 열어요. macOS에서 인터넷에서 받은 앱을 열지 한 번 물어봐요. **열기**를 선택하세요. 앱은 서명 및 공증을 받았고 자동으로 업데이트돼요.

## Linux

- 모든 배포판: `chmod +x`을 사용해 AppImage를 실행 가능한 파일로 만들고 시작하세요. FUSE가 없다는 메시지가 표시되면 Arch에서는 `fuse2`를, Ubuntu 24.04에서는 `libfuse2t64`을 설치하세요.
- Ubuntu 22.04, Debian 12 이상: `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK와 gtk-layer-shell이 함께 설치돼요.
- Arch 및 Omarchy: PKGBUILD를 빈 폴더에 넣고 그곳에서 `makepkg -si`를 실행하세요. 해당 버전을 다운로드하고 파일에 있는 체크섬과 대조해 확인한 다음 설치해요. Omarchy에서 사용하는 Hyprland에서는 로봇이 자체 창 없이 다른 창 위에 표시돼요.

Linux에서는 앱이 자동으로 업데이트되지 않아요. 최신 버전을 사용하려면 파일이나 최신 PKGBUILD를 다시 다운로드하세요.

## 로그인

처음 실행하면 앱 창에 로그인 화면이 열려요. 호스팅된 Machine이나 The Machine Network에 있는 Machine을 사용하면 브라우저에서 계정이 열리고, 로그인 후 앱으로 돌아와요. 자체 호스팅하는 Machine을 사용하려면 Tailscale 네트워크에 연결된 컴퓨터에서 해당 주소를 입력해야 해요.

대신 Chrome이나 Edge에서 대시보드를 앱으로 사용하려면 [앱 설치하기](phone-app.md)를 참고하세요.
