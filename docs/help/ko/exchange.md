---
title: Exchange Server
area: connections
summary: 회사에서 운영하는 Exchange Server(2013~2019 또는 Subscription Edition)의 회의를 확인해요. 읽기 전용이에요.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
---
## 가져오는 정보

참석자, 회의실, 메모가 포함된 회의 정보를 연결 시 지난 일주일과 다음 한 달 동안 가져오고, 이후에는 변경 사항을 모두 가져와요. 회의는 캘린더와 회의 준비에 표시돼요.

읽기 전용이라 회의를 추가하거나 옮기거나 삭제하지 않아요. Exchange Server의 메일은 아직 읽지 않아요.

## Microsoft 365와 Exchange Server 중 무엇을 사용하나요?

Exchange Server는 회사에서 운영해요. Microsoft 365(Exchange Online)는 Microsoft의 클라우드 서비스예요. 대신 **Outlook 캘린더**를 선택하세요. 주소가 Microsoft 365에 연결된 것으로 확인되면 양식에 표시돼요.

## 연결하기

1. 대시보드에서 **연결**을 연 다음 **캘린더**를 선택하고 **Exchange Server**를 골라요.
2. 회사 이메일 주소와 Windows 비밀번호를 입력해요.
3. **연결**을 눌러요.

주소를 바탕으로 서버를 찾습니다(Autodiscover). 찾을 수 없나요? **서버 설정**을 열고 IT 팀에서 알려준 Outlook 서버를 입력하세요. 예: `mail.example.com`. 주소와 다른 이름으로 로그인하나요? **사용자 이름**에 `DOMAIN\name`를 입력하세요.

NTLM 또는 Basic으로 로그인하며, https 연결만 지원해요.

## 연결이 끊긴 경우

- **캘린더 서버에서 비밀번호를 거부했어요**: Windows 비밀번호가 변경됐어요. 다시 연결하세요.
- **Microsoft 365 메일함**: 메일함이 Microsoft 365로 옮겨졌어요. 이 연결을 해제하고 **Outlook 캘린더**를 연결하세요.
- **캘린더 서버에 연결할 수 없어요**: 자동으로 다시 시도해요. 일부 서버는 회사 네트워크나 VPN 안에서만 연결할 수 있어요.

## 연결 해제하기

**연결**에서 캘린더를 열고 **세부 정보**를 선택한 다음 **연결 해제**를 누르세요. 이미 가져온 정보는 그대로 남아요.
