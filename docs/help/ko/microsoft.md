---
title: Microsoft Outlook 및 캘린더
area: connections
summary: Microsoft 365와 Outlook.com의 Outlook 메일과 회의를 연결해요. 승인한 후에만 이메일을 보내요.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: 7229063d9365735d
---
## 읽는 항목

- **Outlook**: 모든 메일을 읽어요. 연결할 때는 최근 7일간의 메일을 읽고, 이후에는 새 메일을 모두 읽어요.
- **Outlook 캘린더**: 회의를 읽기만 해요.

기타 메일과 뉴스레터는 먼저 보낸 사람, 제목, 몇 단어만 빠르게 확인해요. 중요한 메일은 전체 내용을 읽고 할 일로 만들 수 있어요.

## 보낼 수 있고 변경할 수 있는 항목

- 할 일에서 이메일을 보내요. 승인한 후에만 전송해요. 별칭이 아닌 메일함 자체 주소로 전송해요.
- 답장은 원본 이메일이 있는 Outlook 대화에 추가돼요.
- 답장을 보내면 해당 대화의 메시지는 며칠 동안 Outlook의 미룬 폴더로 이동해요. 할 일에 별도 기간이 지정되지 않았다면 3일 후 받은 편지함으로 돌아와요. 누군가 답장하면 더 일찍 돌아와요. 할 일의 마감일 이후까지 미뤄 두지 않아요. 보내기 전에 검토 화면에서 이 내용을 안내해요.

캘린더는 변경하지 않아요.

## 동료 및 연락처 사진

Microsoft에 조직의 기본 프로필 정보(이름, 이메일, 사진)와 Outlook 연락처도 읽도록 요청해요. 내 Machine은 Graph에 이미 있는 사람의 사진, 직책, 회사 정보에만 사용하며, 하루 최대 200장의 사진을 확인해요. 사진이 없는 사람은 30일 후 다시 확인해요.

동료 사진을 사용하려면 조직 관리자의 승인이 필요할 수 있어요. 승인하지 않아도 Outlook은 연결되지만, 동료 사진은 사용할 수 없어요. 이 기능을 도입하기 전에 연결한 계정에는 할 일이 하나 표시돼요. **다시 연결**을 누르거나, **필요 없음**을 눌러 할 일을 완전히 닫으세요. 개인 계정(Outlook.com, Hotmail)에는 동료가 없으므로 연락처 사진만 요청하는 할 일이 표시돼요.

## 연결하기

호스팅된 Machine에서:

1. app.themachine.computer/setup에서 설정 페이지를 열어요.
2. **Microsoft 연결**을 누르고 로그인해요.
3. Microsoft에서 관리자 승인을 요청하면 Microsoft 365 관리자에게 링크를 보내세요(**링크 복사**). 승인이 완료되면 조직의 누구나 연결할 수 있어요. 관리자라면 **관리자예요: 지금 승인**을 누르세요.

또는 대시보드에서 **연결**, **이메일**을 열고 Outlook을 선택한 다음 **Microsoft로 로그인**을 누르세요. 관리자 링크는 버튼 바로 아래에 있어요.

내 컴퓨터에서 사용하려면 먼저 [계정과 페어링](friends.md#a-machine-on-your-own-computer)하세요. 그런 다음 **연결**을 열고 **이메일**에서 Outlook을 선택한 뒤 **Microsoft로 로그인**을 누르세요. 메일과 캘린더가 함께 연결돼요. Microsoft에서 로그인한 후 대시보드의 **연결**로 돌아와요.

Microsoft Entra 앱을 직접 사용하는 IT 팀은 여기에서 **내 앱 사용**을 열거나 `assistant connect outlook`을 실행하세요.

## 연결 해제하기

- 호스팅된 Machine에서: 설정 페이지의 계정 옆에 있는 **연결 해제**를 누르세요. 연결 페이지에서 **연결 해제 ↗**를 누르면 설정 페이지로 이동해요.
- 내 컴퓨터에서: **연결**을 열고 계정을 선택한 다음 **세부 정보**, **연결 해제**를 누르세요.

## Microsoft에서 제거하기

Microsoft에서는 로그인을 취소할 수 없으므로 Microsoft에서도 앱을 제거하세요.

- 회사 또는 학교 계정: myapps.microsoft.com
- 개인 계정: account.live.com/consent/Manage
