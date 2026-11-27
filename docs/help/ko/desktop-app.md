---
title: 데스크톱 앱
area: getting-started
summary: Windows, Mac, Linux에서 사용하는 The Machine: 별도 창으로 열리는 대시보드와 화면 구석에 나타나는 로봇이에요.
code: desktop/README.md, desktop/windows/hooks.nsh, desktop/linux/PKGBUILD, desktop/tools/version.py
order: 3
keywords: desktop, computer, windows, mac, macos, linux, omarchy, arch, ubuntu, debian, appimage, robot, download, install
translated: abfbc82137a6f702
---
데스크톱 앱을 열면 대시보드가 별도 창으로 열려요. 화면 구석에는 작은 로봇이 있어요. 로봇을 클릭하면 할 일을 추가하거나, 메시지에 관해 질문하거나, 나를 위한 항목을 확인할 수 있어요. 아직 프로토타입이에요.

## 다운로드

각 링크에서 항상 최신 버전을 다운로드할 수 있어요.

- Windows 10 또는 11, 64비트: [the-machine-desktop-setup.exe](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-setup.exe)
- macOS 13 이상이 설치된 Mac: [the-machine-desktop-mac.zip](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-mac.zip)
- Linux, 64비트: [AppImage](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-x86_64.AppImage), Ubuntu 및 Debian용 [.deb](https://github.com/Salesflare/TheMachine/releases/latest/download/the-machine-desktop-amd64.deb), Arch 및 Omarchy용 [PKGBUILD](https://github.com/Salesflare/TheMachine/releases/latest/download/PKGBUILD)

## Windows

설치 프로그램을 열어요. 관리자 권한 없이 현재 사용자만을 위해 설치되며, Salesflare에서 서명했어요. WebView2를 사용한 적 없는 컴퓨터에서는 준비하는 데 몇 초 더 걸려요. 준비가 끝나면 앱이 바로 시작돼요. 앱은 자동으로 업데이트돼요. 새 버전을 사용할 수 있으면 **설정**에 표시돼요.

## Mac

zip 파일을 풀고 The Machine을 Applications로 옮긴 다음, 그곳에서 열어요. macOS에서 인터넷에서 받은 앱을 열 것인지 한 번 물어봐요. **열기**를 선택하면 돼요. 앱은 서명과 공증을 거쳤으며 자동으로 업데이트돼요.

## Linux

- 모든 배포판: `chmod +x`로 AppImage에 실행 권한을 부여한 다음 실행해요. FUSE가 없다는 메시지가 표시되면 `fuse3`를 설치해요.
- Ubuntu 22.04, Debian 12 이상: `sudo apt install ./the-machine-desktop-amd64.deb`을 사용해요. WebKitGTK와 gtk-layer-shell이 함께 설치돼요.
- Arch 및 Omarchy: 빈 폴더에 PKGBUILD를 넣고 그 폴더에서 `makepkg -si`를 실행해요. 해당 버전을 다운로드하고 파일에 있는 체크섬과 비교해 확인한 다음 설치해요. Omarchy에서 사용하는 Hyprland에서는 로봇이 별도 창 없이 다른 창 위에 표시돼요.

Linux 앱은 자동으로 업데이트되지 않아요. 최신 버전을 사용하려면 파일을 다시 다운로드하거나 최신 PKGBUILD를 다운로드해요.

## 다운로드 확인

모든 파일에는 GitHub의 빌드 출처 정보가 포함되어 있어요. The Machine의 코드로 자체 워크플로에서 빌드되었음을 확인할 수 있어요. [GitHub CLI](https://cli.github.com)를 사용하면 다음과 같이 확인할 수 있어요. `gh attestation verify <file> -R Salesflare/TheMachine`.

## 로그인

처음 실행하면 로그인 창이 열려요. 호스팅된 Machine이나 The Machine Network에 있는 Machine을 사용하면 브라우저에서 계정이 열리고, 로그인 후 앱으로 돌아와요. 자체 호스팅한 Machine을 사용하려면 Tailscale 네트워크에 연결된 컴퓨터에서 해당 Machine의 주소를 입력해야 해요.

대신 Chrome 또는 Edge에서 대시보드를 앱으로 사용하려면 [앱 설치](phone-app.md)를 참고하세요.
