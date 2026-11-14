---
title: Microsoft Outlook 및 캘린더
area: connections
summary: Microsoft 365와 Outlook.com용 Outlook 메일과 일정이에요. 승인한 후에만 이메일을 보내요.
covers: connector:outlook, connector:outlook_calendar
code: ms_graph.py, ms_photos.py, onboarding.py
site: Connect Microsoft, Copy link, I'm the admin: approve now, Disconnect, Sign in with Microsoft, Use your own app
order: 12
translated: 41c9c0174a2a21c7
---
## 읽는 항목

- **Outlook**: 모든 메일을 읽어요. 연결할 때는 최근 7일간의 메일을 읽고, 이후에는 새 메일을 모두 읽어요.
- **Outlook 캘린더**: 일정을 읽기만 해요.

기타 폴더의 메일과 뉴스레터는 먼저 발신자, 제목, 몇 마디만 빠르게 확인해요. 중요한 메일은 전체 내용을 읽고 할 일로 만들 수 있어요.

## 보내거나 변경할 수 있는 항목

- 할 일에 있는 이메일을 승인한 후에만 보낼 수 있어요. 별칭이 아닌 메일함 자체 주소로 발송해요.
- 답장은 답변 대상 이메일이 있는 Outlook 대화에 추가돼요.
- 이메일에 관한 할 일을 미루면 해당 대화의 메시지가 Outlook의 미룬 폴더로 이동하고, 할 일이 다시 표시될 때 돌아와요.

일정은 절대 변경하지 않아요.

## 동료와 연락처 사진

Microsoft에 조직 내 기본 프로필 정보(이름, 이메일, 사진)와 Outlook 연락처를 읽도록 요청해요. Graph에 이미 있는 사람의 사진, 직함, 회사 정보를 확인하는 데만 사용하며, 하루 최대 200장의 사진을 확인해요. 사진이 없는 사람은 30일 후 다시 확인해요.

조직 관리자의 승인이 있어야 동료 사진을 가져올 수 있어요. 승인하지 않아도 Outlook은 연결되지만 사진은 가져오지 않아요. 이전에 연결한 계정에는 할 일이 하나 표시돼요. **다시 연결**을 누르거나, 할 일을 완전히 닫으려면 **필요 없음**을 누르세요. 개인 계정(Outlook.com, Hotmail)에는 동료가 없으므로 연락처 사진만 요청하는 할 일이 표시돼요.

## 연결

호스팅 환경의 Machine에서:

1. app.themachine.computer/setup에서 설정 페이지를 열어요.
2. **Microsoft 연결**을 누르고 로그인해요.
3. Microsoft에서 관리자 승인을 요청하면 Microsoft 365 관리자에게 링크를 보내세요(**링크 복사**). 승인되면 조직의 모든 사용자가 연결할 수 있어요. 관리자라면 **관리자예요: 지금 승인**을 누르세요.

또는 대시보드에서 **연결**, **이메일**을 차례로 열고 Outlook을 선택한 다음 **Microsoft로 로그인**을 누르세요. 관리자 링크는 버튼 바로 아래에 있어요.

개인 컴퓨터에서는 [계정과 페어링한 후](friends.md#a-machine-on-your-own-computer) **연결**을 열고 **이메일**을 선택한 다음 Outlook을 선택하고 **Microsoft로 로그인**을 누르세요. 메일과 일정이 함께 연결돼요. Microsoft 인증이 끝나면 대시보드의 **연결**로 돌아와요.

자체 Microsoft Entra 앱을 사용하는 IT 팀은 여기서 **자체 앱 사용**을 열거나 `assistant connect outlook`을 실행하세요.

## 연결 해제

- 호스팅 환경의 Machine: 설정 페이지에서 계정 옆의 **연결 해제**를 누르세요. 연결 페이지의 **연결 해제 ↗**를 누르면 해당 페이지로 이동해요.
- 개인 컴퓨터: **연결**에서 계정을 열고 **세부 정보**, **연결 해제**를 차례로 선택하세요.

## Microsoft에서 제거

Microsoft에서는 로그인을 취소할 수 없으므로 Microsoft에서도 앱을 제거해야 해요.

- 회사 또는 학교 계정: myapps.microsoft.com
- 개인 계정: account.live.com/consent/Manage
