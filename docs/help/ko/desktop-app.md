---
title: 데스크톱 앱
area: getting-started
summary: Windows, Mac, Linux에서 The Machine을 사용해 보세요. 대시보드가 별도 창으로 열리고 화면 구석에 로봇이 표시돼요.
code: desktop/README.md, desktop/src/updates.rs, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: c590899c2622b818
---
데스크톱 앱을 열면 대시보드가 별도 창으로 열려요. 화면 구석에 작은 로봇이 표시돼요. 로봇을 클릭하면 할 일을 추가하거나, 메시지에 관해 물어보거나, 내게 맞는 내용을 확인할 수 있어요. 프로토타입이에요.

## 다운로드

각 링크에서 항상 최신 버전을 다운로드할 수 있어요.

- Windows 10 또는 11, 64비트: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- macOS 13 이상이 설치된 Mac: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64비트: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), Ubuntu 및 Debian용 [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb), Arch 및 Omarchy용 [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

대시보드에서도 다운로드할 수 있어요. 컴퓨터에서 **설정**의 **앱**을 열면 세 가지 버전이 모두 표시되고, 사용 중인 컴퓨터에는 **이 컴퓨터**라고 표시돼요. **The Machine 더 알차게 사용하기** 할 일에는 **데스크톱 앱 다운로드**가 있어요. 선택하면 사용 중인 컴퓨터에 맞는 버전을 다운로드하거나, 아래 Linux 설치 단계가 열려요. 앱에서 내 Machine에 로그인하면 할 일에서 사라져요. 이 두 항목은 휴대폰이나 데스크톱 앱 안에는 표시되지 않아요.

## Windows

설치 프로그램을 열어요. 관리자 권한 없이 현재 사용자 계정에만 설치되며 Salesflare의 서명이 있어요. WebView2를 사용한 적 없는 컴퓨터에서는 준비하는 데 몇 초 더 걸려요. 준비가 끝나면 앱이 바로 시작돼요. 앱은 자동으로 업데이트돼요. 새 버전을 사용할 수 있으면 **설정**에 표시돼요.

## Mac

zip 파일의 압축을 풀고 The Machine을 Applications로 옮긴 다음 그곳에서 열어요. macOS에서 인터넷에서 다운로드한 앱을 열지 한 번 물어봐요. 열기를 선택하면 돼요. 앱에는 서명과 공증이 완료되어 있고, 자동으로 업데이트돼요.

## Linux

- 모든 배포판: `chmod +x`을 실행해 AppImage에 실행 권한을 부여한 다음 시작해요. FUSE가 없다는 메시지가 표시되면 `fuse3`를 설치해요.
- Ubuntu 22.04, Debian 12 이상: `sudo apt install ./the-machine-desktop-amd64.deb`을 실행해요. WebKitGTK와 gtk-layer-shell도 함께 설치돼요.
- Arch 및 Omarchy: 빈 폴더에 PKGBUILD를 넣고 그 폴더에서 `makepkg -si`를 실행해요. 해당 버전을 다운로드하고 파일에 있는 체크섬과 비교해 확인한 다음 설치해요. Omarchy 기본 설정처럼 Hyprland를 사용하면 로봇이 별도 창 없이 다른 창 위에 표시돼요.

AppImage를 ~/Applications 같은 내 폴더에 두면 자동으로 업데이트돼요. 새 버전을 사용할 수 있으면 **설정**에 표시돼요. .deb 및 Arch 패키지는 apt와 pacman으로 업데이트돼요. 새 버전이 있으면 **설정**에 표시되며, .deb 또는 PKGBUILD를 다운로드할 수 있는 **다운로드**가 함께 표시돼요. 폴더에 압축을 푼 AppImage는 자동으로 업데이트되지 않으니 압축을 풀지 않은 AppImage를 사용하세요.

## 다운로드 확인

모든 파일에는 GitHub 빌드 출처 정보가 포함되어 있어요. 이를 통해 The Machine의 코드가 자체 워크플로를 거쳐 빌드되었는지 확인할 수 있어요. [GitHub CLI](https://cli.github.com)를 사용하려면 `gh attestation verify <file> -R Salesflare/TheMachine`를 실행하세요.

## 로그인

처음 실행하면 로그인 화면이 열려요. 호스팅된 Machine이나 The Machine Network에 있는 Machine을 사용하는 경우, 브라우저에서 계정이 열리고 앱으로 돌아와요. 직접 호스팅한 Machine을 사용하려면 Tailscale 네트워크에 연결된 컴퓨터에서 해당 Machine의 주소를 입력해야 해요.

Chrome 또는 Edge에서 대시보드를 앱처럼 사용하려면 [앱 설치하기](phone-app.md)를 참고하세요.

## 로봇

앱 창이 앞에 있으면 로봇이 사라지고, 다른 창을 앞으로 가져오거나 앱을 최소화하거나 닫으면 다시 표시돼요. 모니터가 여러 대라면 앱 창이 있는 모니터에 로봇이 표시돼요. 로봇을 다른 모니터로 끌어 옮길 수도 있어요. Hyprland, Sway, KDE에서는 기본 모니터에 표시돼요. 로봇을 표시하거나 숨기려면 **설정**을 열어요. 단축키는 Ctrl+comma이며, Mac에서는 Command-comma예요. **로봇 표시**를 선택하세요.
