---
title: 내 컴퓨터에서 실행하기
area: getting-started
summary: Linux, macOS 또는 Windows에 오픈 소스 앱을 설치해요. 무료이며, 모델과 데이터는 직접 관리해요.
covers: self-hosted
code: install.sh, install.ps1, docs/getting-started.md
order: 2
translated: 73526b82818f009d
---
내 컴퓨터에서 The Machine을 무료로 실행해요. 오픈 소스(AGPL)이며, 데이터는 계속 직접 관리해요. 설치하려면 터미널이 필요하지만, 계정 연결에는 필요하지 않아요.

## 필요한 항목

- OpenClaw 2026.11.2 이상. The Machine에서 실행하는 오픈 소스 에이전트예요. 설치 프로그램에서 설치할 수 있어요.
- Python 3.12 이상, Node.js 24(24.22.1 이상) 또는 26.12.1 이상. 25는 지원하지 않아요.
- 휴대폰에서 대시보드에 접속하려면 Tailscale이 필요해요.
- root가 아닌 일반 사용자 계정이 필요해요.

## 설치

Linux 또는 macOS(macOS는 베타 버전):

1. `git clone https://github.com/Salesflare/TheMachine.git ~/.openclaw/workspace/tools/personal-assistant`
2. `cd ~/.openclaw/workspace/tools/personal-assistant && ./install.sh`

Windows(베타)에서는 WSL2 안에서 실행해요. PowerShell에서 `irm https://raw.githubusercontent.com/Salesflare/TheMachine/main/install.ps1 | iex`을 실행해요. Ubuntu와 앱에 필요한 모든 항목이 포함된 WSL2 환경을 설정한 다음 `./install.sh`를 실행해요.

설치 프로그램이 계정을 찾아 하나씩 연결해요. 기능을 활성화하기 전에 지난주 기록을 미리 보여줘요.

## 설치 후

- 메일 연결: **할 일** 상단에서 **Gmail**(또는 **Outlook**)을 누른 다음 **이 Machine 연결**을 눌러 계정과 연결해요. 계정이 없다면 바로 아래에 **내 앱 사용**이 있어요.
- 그런 다음 **Google로 로그인**을 눌러요(Outlook은 **Microsoft로 로그인**). 메일과 캘린더가 함께 연결돼요.
- 다른 소스: **연결**에서 소스 유형을 선택해요. 직접 만든 Google 클라이언트나 Entra 앱을 사용하려면 터미널에서 `assistant connect`를 실행해요.
- `assistant doctor`으로 모든 항목을 확인해요. 문제가 있으면 각각 해결 방법을 표시해요.
- 최신 서명된 릴리스를 설치하며, 업데이트도 서명된 릴리스로 제공돼요.
- 계정과 연결하면 로그인 후 휴대폰 앱에서 열려요. 연결을 해제하면 해당 링크가 삭제돼요.

전체 안내는 저장소에서 확인할 수 있어요: [시작하기](https://github.com/Salesflare/TheMachine/blob/main/docs/getting-started.md).
