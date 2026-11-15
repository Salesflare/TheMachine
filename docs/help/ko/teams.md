---
title: Microsoft Teams
area: connections
summary: 회사 또는 학교 계정의 Teams 채팅, 회의 채팅, 회의 메모를 읽어요. 읽기 전용이에요.
covers: connector:teams
code: connectors/teams.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
translated: 864f9e6e98309439
---
## 읽는 항목

Teams의 1:1 채팅, 그룹 채팅, 회의 채팅을 읽어요. 연결하면 최근 7일간의 메시지를 읽고, 이후에는 몇 분마다 새 메시지를 읽어요. 약 1년 치 이전 채팅과 관리자 승인을 받은 채널 스레드는 나중에 [기록](history.md)으로 조금씩 가져와요. 이 과정이 다른 작업을 지연시키지는 않아요.

관리자 승인을 받으면 다음 항목도 읽어요.

- 팀의 채널 스레드
- 직접 주최한 회의의 녹취록
- Microsoft 365 Copilot 라이선스가 있으면 Copilot의 회의 메모와 할 일

녹취록이나 메모는 캘린더의 해당 회의에 **Teams에서 가져옴**으로 표시돼요. 녹취록이나 메모가 없어도 회의 채팅은 그대로 있어요.

봇, 앱, 시스템 메시지는 제외돼요.

## 할 수 있는 작업

Teams에서는 아무 작업도 하지 않아요. 읽기만 해요. 답장하려면 **Teams에서 열기**로 채팅을 여세요.

## 필요한 권한

Microsoft에서 The Machine이 채팅과 프로필을 읽도록 허용해 달라고 요청해요. 관리자 승인은 필요하지 않아요.

채널, 녹취록, Copilot 메모를 읽으려면 조직의 관리자가 한 번 승인해야 해요. 승인 전에는 Teams 카드에 아직 읽을 수 없는 항목과 그 이유가 표시돼요.

회사 또는 학교 Microsoft 계정에서만 사용할 수 있어요. 개인 계정에는 이 방법으로 읽을 수 있는 Teams 채팅이 없어요.

## 연결하기

호스팅된 Machine에서:

1. 대시보드에서 **연결**을 열고, **Microsoft Teams**의 **채팅** 또는 **Teams 회의**의 **회의**를 여세요. 둘 다 같은 계정으로 로그인해요.
2. **Microsoft로 로그인**을 누르고 승인을 완료하세요. 대시보드로 돌아와요.
3. 채널과 회의 메모를 사용하려면 로그인 페이지에 표시된 링크를 관리자에게 보내세요. 관리자가 승인하면 Teams를 다시 연결하세요.

설정 중에는 설정 페이지에서 **Microsoft Teams 연결**을 선택할 수도 있어요.

내 컴퓨터에서 사용하려면 먼저 [계정과 페어링](friends.md#a-machine-on-your-own-computer)하세요. 그런 다음 **연결**을 열고 **채팅** 또는 **회의**를 선택한 뒤, **Microsoft Teams** 또는 **Teams 회의**를 선택하고 **Microsoft로 로그인**을 누르세요. 이 환경에서는 채팅과 회의 채팅을 읽어요. 채널과 회의 메모는 아직 사용할 수 없어요.

## 연결 해제하기

대시보드에서 **연결**을 열고 Microsoft Teams를 선택한 다음 **세부 정보**와 **연결 해제**를 선택하세요. 이미 가져온 내용은 그대로 남아요.

## Microsoft에서 권한 취소하기

myapps.microsoft.com을 열고 The Machine을 삭제하세요. 같은 주소로 Outlook도 연결되어 있으면 Outlook 연결도 해제돼요.
