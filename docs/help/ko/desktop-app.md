---
title: 데스크톱 앱
area: getting-started
summary: Windows, Mac, Linux에서 The Machine을 사용해 보세요. 대시보드는 별도 창으로 열리고, 화면 한쪽에는 로봇이 표시돼요.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: 2e9388c58b957501
---
데스크톱 앱을 열면 대시보드가 별도 창으로 표시돼요. 화면 한쪽에 작은 로봇이 있어요. 로봇을 클릭하면 할 일을 추가하거나, 메시지에 관해 질문하거나, 나를 위한 내용을 볼 수 있어요. 아직 프로토타입이에요.

## 다운로드

각 링크에서 항상 최신 버전을 다운로드할 수 있어요.

- Windows 10 또는 11, 64비트: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- macOS 13 이상을 사용하는 Mac: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64비트: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), Ubuntu 및 Debian용 [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb), Arch 및 Omarchy용 [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

대시보드에서도 다운로드할 수 있어요. 컴퓨터에서 **설정**을 열고 **앱**을 선택하면 세 가지 앱이 모두 표시되고, 현재 사용 중인 컴퓨터에는 **이 컴퓨터**가 표시돼요. **The Machine 더 알차게 사용하기** 할 일에는 **데스크톱 앱 다운로드**가 있어요. 선택하면 컴퓨터에 맞는 앱을 다운로드하거나 아래의 Linux 설치 단계를 열어요. 앱에서 내 Machine에 로그인하면 이 할 일은 사라져요. 휴대폰이나 데스크톱 앱에서는 둘 다 표시되지 않아요.

## Windows

설치 프로그램을 열면 돼요. 관리자 권한 없이 현재 사용자만 사용할 수 있도록 설치되고, Salesflare에서 서명했어요. WebView2를 사용한 적이 없는 컴퓨터에서는 준비하는 데 몇 초 더 걸려요. 준비가 끝나면 앱이 바로 시작돼요. 앱은 자동으로 업데이트돼요. 새 버전을 사용할 수 있으면 설정에 표시돼요.

## Mac

zip 파일의 압축을 풀고 The Machine을 Applications로 옮긴 다음 그곳에서 열어요. macOS에서 인터넷에서 다운로드한 앱을 열지 한 번 물어보면 **열기**를 선택해요. 앱은 서명 및 공증을 받았고, 자동으로 업데이트돼요.

## Linux

- 모든 배포판: `chmod +x`을 실행해 AppImage를 실행 파일로 만든 다음 실행해요. FUSE가 없다는 메시지가 표시되면 `fuse3`를 설치해요.
- Ubuntu 22.04, Debian 12 이상: `sudo apt install ./the-machine-desktop-amd64.deb`을 실행해요. WebKitGTK와 gtk-layer-shell이 함께 설치돼요.
- Arch 및 Omarchy: 빈 폴더에 PKGBUILD를 넣고 그 폴더에서 `makepkg -si`를 실행해요. 해당 버전을 다운로드하고, 파일에 있는 체크섬과 비교해 확인한 다음 설치해요. Omarchy처럼 Hyprland를 사용하는 경우 로봇은 별도 창을 만들지 않고 다른 창 위에 표시돼요.

Linux 앱은 자동으로 업데이트되지 않아요. 최신 버전을 사용하려면 파일이나 최신 PKGBUILD를 다시 다운로드하세요.

## 다운로드 확인

모든 파일에는 GitHub 빌드 출처 정보가 있어요. 이 정보를 통해 The Machine의 코드로 자체 워크플로에서 빌드한 파일인지 확인할 수 있어요. [GitHub CLI](https://cli.github.com)를 사용하려면 `gh attestation verify <file> -R Salesflare/TheMachine`를 실행하세요.

## 로그인

처음 실행하면 로그인 화면이 열려요. 호스팅된 Machine이나 The Machine Network의 Machine을 사용하면 브라우저에서 계정이 열리고, 로그인 후 앱으로 돌아와요. 자체 호스팅 Machine을 사용하려면 Tailscale 네트워크에 연결된 컴퓨터에서 Machine의 주소를 입력해야 해요.

대신 Chrome이나 Edge에서 대시보드를 앱처럼 사용하려면 [앱 설치](phone-app.md)를 참고하세요.

## 로봇

앱 창이 앞에 있으면 로봇이 숨겨지고, 다른 창을 앞에 두거나 앱 창을 최소화하거나 닫으면 다시 표시돼요. 모니터가 여러 대라면 앱 창이 있는 모니터에 표시돼요. 다른 곳으로 드래그할 수도 있어요. Hyprland, Sway, KDE에서는 기본 모니터에 표시돼요. 로봇을 켜거나 끄려면 설정을 열고(Ctrl+comma, Mac에서는 Command-comma) **로봇 표시**를 선택하세요.
