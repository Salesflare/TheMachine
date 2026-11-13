---
title: 컴퓨터 문제
area: troubleshooting
summary: The Machine은 컴퓨터 자체의 로그를 읽고, 실제 문제가 있으면 원인과 해결 방법을 알려줘요. 해결은 실행을 눌렀을 때만 진행돼요.
covers: computer-logs
code: machine/system_logs.py, machine/sources/gateway.py, onboarding.py
keywords: logs, journal, journalctl, crash, coredump, systemd, Hyprland, Omarchy, bar
order: 3
---
## 읽는 정보

systemd를 사용하는 Linux에서 The Machine은 현재 사용자 세션의 로그를 읽어요. 직접 사용하는 서비스와 프로그램의 충돌 보고서만 읽어요. Omarchy에서는 Hyprland와 bar도 확인해요. 시스템 전체의 로그는 읽지 않고, 더 많은 접근 권한을 요청하지도 않아요.

어떤 서비스가 중단됐는지, 어떻게 종료됐는지, 어떤 프로그램이 충돌했는지 확인해요. 로그 줄의 내용은 읽지 않으므로 로그 텍스트를 저장하거나 컴퓨터 밖으로 보내지 않아요.

## 문제로 판단하는 항목

계속 재시작되는 서비스, 하루 동안 여러 번 실패했거나 계속 중단된 서비스, 메모리가 부족해진 서비스, 충돌한 프로그램이에요. Omarchy에서는 Hyprland나 bar 충돌, Hyprland 설정 오류도 포함돼요.

한 번 재시작되거나 한 번 실행에 실패한 것은 정상으로 보고 알리지 않아요. 몇 번 실패했지만 다시 정상적으로 실행된 서비스도 마찬가지예요.

테스트와 에이전트가 제어하는 브라우저(headless, Playwright, Puppeteer, CI)는 알리지 않아요. 서비스가 중지되거나 재시작되는 동안 함께 종료되는 프로그램도 마찬가지예요. 개발 실행도 알리지 않아요. 코딩 에이전트가 실행하는 항목, 테스트, 임시 폴더나 캐시 폴더에서 실행되는 프로그램이 여기에 포함돼요. 프로그램이 계속 충돌하면 충돌 횟수와 시간을 알려주는 할 일 하나를 만들어요.

스크립트는 python3나 node가 아니라 backup.py처럼 스크립트 자체의 이름으로 표시해요.

## 받게 되는 내용

무슨 일이 있었는지, 왜 중요한지, 어떻게 해결할 수 있는지 쉬운 말로 설명하는 할 일이 생겨요. 원인을 보여주는 명령어는 더 보기 아래에서 확인할 수 있어요. 할 일의 채팅에서 물어보면 The Machine이 문제를 살펴봐요. 변경 사항은 실행과 마찬가지로 확인을 받을 때까지 적용하지 않아요.

안전하게 해결할 수 있는 경우 할 일에 실행이 표시돼요. 계속 중단된 서비스는 다시 시작하고, Omarchy에서는 bar를 다시 띄워요. 실행은 해당 명령어만 실행하며, 결과는 할 일의 채팅에 표시돼요. The Machine 자체의 서비스나 OpenClaw Gateway에는 손대지 않아요.

같은 문제로 할 일은 2주에 한 번까지만 만들고, 해당 할 일이 아직 열려 있으면 새로 만들지 않아요. 하루에 새로 만들 수 있는 할 일은 최대 두 개예요.

## 터미널에서

`assistant doctor`은 지난 하루 동안 발생한 같은 문제를 표시해요.

## 다른 컴퓨터

macOS, Windows, systemd가 없는 컴퓨터에서는 아무것도 읽지 않고 `assistant doctor`에 그 사실을 표시해요.

호스팅된 Machine은 서버를 계속 실행하는 책임이 저희에게 있어요. 서버 문제는 할 일로 전달하지 않고 The Machine 팀에 전달해요.

## 끄기

config.json에서 `"computer_logs": false`을 설정하고 서비스를 다시 시작하세요.
