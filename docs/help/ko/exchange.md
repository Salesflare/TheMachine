---
title: Exchange Server
area: connections
summary: 회사에서 운영하는 Exchange Server(2013~2019 또는 Subscription Edition)의 회의 정보를 가져와요. 읽기 전용이에요.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
translated: f2b98c9bd4f08dba
---
## 가져오는 정보

회의와 참석자, 회의실, 메모를 가져와요. 연결할 때는 지난 일주일과 다음 한 달의 정보를 가져오고, 이후에는 변경 사항을 모두 가져와요. 정보는 **캘린더**와 회의 준비에 표시돼요.

읽기 전용이라 회의를 추가하거나 옮기거나 삭제하지 않아요. Exchange Server의 메일은 아직 가져오지 않아요.

## Microsoft 365와 Exchange Server 중 무엇을 사용하나요?

Exchange Server는 회사에서 운영하는 서버예요. Microsoft 365(Exchange Online)는 Microsoft의 클라우드 서비스예요. Microsoft 365를 사용한다면 **Outlook 캘린더**를 선택하세요.

먼저 이메일 주소를 입력하세요. Microsoft 365를 사용 중이면 양식에 안내가 표시되고 비밀번호 대신 **Sign in with Microsoft**가 표시돼요. 비밀번호를 입력하지 않고 Outlook Calendar 로그인 화면이 열려요. 몇 초 안에 서버를 찾지 못했거나 회사에서 자체 서버를 운영한다면 비밀번호 입력 양식이 그대로 표시돼요.

## 연결하기

1. 대시보드에서 **연결**을 연 다음 **캘린더**를 선택하고 **Exchange Server**를 선택하세요.
2. 회사 이메일 주소와 Windows 비밀번호를 입력하세요.
3. **연결**을 누르세요.

주소를 바탕으로 서버를 찾아요(Autodiscover). 찾지 못했다면 **서버 설정**을 열고 IT 팀이 알려 준 Outlook 서버를 입력하세요. 예: `mail.example.com`. 주소와 다른 이름으로 로그인한다면 **사용자 이름**에 `DOMAIN
ame`을 입력하세요.

NTLM 또는 Basic을 사용해 로그인하며, https로만 연결해요.

## 연결이 끊기는 경우

- **캘린더 서버에서 비밀번호를 거부했어요**: Windows 비밀번호가 변경됐어요. 다시 연결하세요.
- **Microsoft 365 사서함**: 사서함이 Microsoft 365로 이전됐어요. 이 연결을 해제하고 **Outlook 캘린더**를 연결하세요.
- **캘린더 서버에 연결할 수 없어요**: 자동으로 다시 시도해요. 일부 서버는 회사 네트워크나 VPN에 연결해야 접속할 수 있어요.

## 연결 해제하기

**연결**에서 캘린더를 열고 **세부 정보**를 선택한 다음 **연결 해제**를 누르세요. 이미 가져온 정보는 그대로 남아요.
