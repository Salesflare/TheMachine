---
title: iCloud 및 기타 캘린더(CalDAV)
area: connections
summary: iCloud Calendar 또는 Fastmail, Nextcloud, Zoho 같은 CalDAV 캘린더의 회의를 가져와요. 읽기 전용이에요.
covers: connector:icloud_calendar, connector:caldav
code: caldav_calendar.py, ical.py, machine/sources/calendar_setup.py
order: 14
---
## 읽어오는 항목

참석자, 회의실, 메모가 포함된 회의를 가져와요. 연결할 때는 지난 한 주와 다음 한 달의 회의를 가져오고, 이후에는 변경 사항을 가져와요. Google 또는 Outlook 회의처럼 Calendar와 회의 준비에 표시돼요. 계정의 모든 캘린더를 읽거나, 지정한 캘린더만 읽어요.

읽기 전용이라 회의를 추가하거나 이동하거나 삭제하지 않아요.

## iCloud Calendar 연결

1. [appleid.apple.com](https://appleid.apple.com)의 **로그인 및 보안**에서 앱 암호를 만들어요. iCloud Mail용으로 만든 암호도 사용할 수 있어요.
2. 대시보드에서 **연결**을 연 다음 **Calendar**를 선택하고 **iCloud Calendar**를 골라요.
3. Apple ID와 앱 암호를 입력한 다음 **연결**을 눌러요.

## 다른 캘린더 연결

1. **연결**을 연 다음 **Calendar**를 선택하고 **기타 캘린더**를 골라요.
2. 이메일 주소와 암호를 입력해요. 대부분의 제공업체에서는 계정 설정에서 만든 앱 암호를 사용해야 해요.
3. **연결**을 눌러요.

Fastmail, Yahoo, Zoho 및 서버 정보를 제공하는 서버는 자동으로 찾아요. 서버를 찾을 수 없나요? **서버 설정**을 열고 CalDAV 주소를 입력해요. 예: `nextcloud.example.com/remote.php/dav`. **이 캘린더만**을 선택하면 이름으로 지정한 캘린더 하나만 읽어요.

Google 또는 Microsoft 캘린더를 연결하려면 **Google Calendar** 또는 **Outlook Calendar**를 선택해요.

## 연결이 중단되면

- **캘린더 서버에서 암호를 거부했어요**: 암호를 변경했거나 앱 암호가 삭제됐어요. 새 암호로 다시 연결해요.
- **캘린더 서버에 연결할 수 없어요**: 자동으로 다시 시도해요. 계속 실패하면 서버 설정에서 주소를 확인해요.

## 연결 해제

**연결**에서 캘린더를 연 다음 **세부 정보**, **연결 해제**를 선택해요. 이미 가져온 내용은 그대로 남아요. 제공업체에서도 앱 암호를 삭제해요.
