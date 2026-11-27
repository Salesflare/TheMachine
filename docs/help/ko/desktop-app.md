---
title: 데스크톱 앱
area: getting-started
summary: Windows, Mac, Linux에서 The Machine을 사용해 보세요. 대시보드를 별도 창에서 열고, 화면 한쪽에 로봇을 띄울 수 있어요.
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: af0a8a2994af969d
---
데스크톱 앱을 열면 대시보드가 별도 창에 표시돼요. 화면 한쪽에 작은 로봇이 있어요. 클릭하면 할 일을 추가하거나, 메시지에 관해 질문하거나, 나를 위한 내용을 확인할 수 있어요. 아직 프로토타입이에요.

## 다운로드

각 링크에서 항상 최신 버전을 다운로드할 수 있어요.

- Windows 10 또는 11, 64비트: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- macOS 13 이상이 설치된 Mac: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64비트: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), Ubuntu 및 Debian용 [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb), Arch 및 Omarchy용 [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

대시보드에서도 다운로드할 수 있어요. 컴퓨터에서 **설정**의 **앱**을 열면 세 가지 앱이 모두 표시되고, 사용 중인 컴퓨터에는 **이 컴퓨터**가 표시돼요. **The Machine 더 알차게 사용하기** 할 일에서 **데스크톱 앱 다운로드**를 선택하면 컴퓨터에 맞는 앱을 다운로드하거나 아래의 Linux 설치 방법을 볼 수 있어요. Machine에 로그인하면 이 할 일은 사라져요. 휴대전화나 데스크톱 앱에서는 표시되지 않아요.

## Windows

설치 프로그램을 열어요. 관리자 권한 없이 현재 사용자만 사용할 수 있도록 설치되고, Salesflare에서 서명해요. WebView2를 사용한 적 없는 컴퓨터에서는 준비하는 데 몇 초 더 걸려요. 준비가 끝나면 앱이 바로 시작돼요. 앱은 자동으로 업데이트돼요. 새 버전을 사용할 수 있으면 설정에 표시돼요.

## Mac

zip 파일의 압축을 풀고 The Machine을 Applications로 옮긴 다음, 그곳에서 열어요. macOS에서는 인터넷에서 다운로드한 앱을 열지 한 번 확인해요. 이때 열기를 선택하세요. 앱은 서명 및 공증을 받았으며 자동으로 업데이트돼요.

## Linux

- 모든 배포판: `chmod +x`을 사용해 AppImage를 실행 가능하게 만든 다음 실행하세요. FUSE가 없다는 메시지가 표시되면 `fuse3`를 설치하세요.
- Ubuntu 22.04, Debian 12 이상: `sudo apt install ./the-machine-desktop-amd64.deb`. WebKitGTK와 gtk-layer-shell이 함께 설치돼요.
- Arch 및 Omarchy: PKGBUILD를 빈 폴더에 넣고 그 폴더에서 `makepkg -si`를 실행하세요. 해당 버전을 다운로드하고 파일에 있는 체크섬과 대조해 확인한 다음 설치해요. Omarchy 기본 환경인 Hyprland에서는 로봇이 별도 창 없이 다른 창 위에 표시돼요.

AppImage를 ~/Applications처럼 내 폴더에 두면 자동으로 업데이트돼요. 새 버전을 사용할 수 있으면 설정에 표시돼요. .deb와 Arch 패키지는 apt와 pacman으로 관리돼요. 새 버전이 나오면 설정에 표시되며, .deb 또는 PKGBUILD를 다운로드할 수 있어요. 폴더에 압축을 푼 AppImage는 자동으로 업데이트되지 않아요. AppImage는 압축을 풀지 않고 사용하세요.

## 다운로드 확인

모든 파일에는 GitHub 빌드 출처 정보가 포함돼요. 이 정보를 통해 The Machine의 코드로 자체 워크플로를 사용해 빌드했는지 확인할 수 있어요. [GitHub CLI](https://cli.github.com)를 사용하려면 `gh attestation verify <file> -R Salesflare/TheMachine`를 실행하세요.

## 로그인

처음 실행하면 로그인 창이 열려요. 호스팅된 Machine이나 The Machine Network의 Machine을 사용하는 경우, 브라우저에서 계정이 열리고 로그인 후 앱으로 돌아와요. 자체 호스팅 Machine에서는 주소를 입력해야 해요. 이 주소는 Tailscale 네트워크에 연결된 컴퓨터에서 확인할 수 있어요.

내 Machine의 페이지에서 전용 링크 `computer.themachine.desktop://open`를 사용하면 앱을 앞으로 가져올 수 있어요. 이 링크는 앱만 열며 다른 정보는 전달하지 않아요.

대신 Chrome이나 Edge에서 대시보드를 앱처럼 사용하려면 [앱 설치하기](phone-app.md)를 참고하세요.

## 로봇

앱 창이 앞에 있으면 로봇이 사라지고, 다른 창이 앞에 있거나 앱 창을 최소화하거나 닫으면 다시 나타나요. 모니터가 여러 대라면 앱 창이 있는 모니터에 표시돼요. 로봇을 다른 모니터로 옮길 수도 있어요. Hyprland, Sway, KDE에서는 기본 모니터에 표시돼요. 로봇을 표시하거나 숨기려면 설정을 여세요. Mac에서는 Ctrl+쉼표 또는 Command+쉼표를 누른 다음 **로봇 표시**를 선택하세요.
