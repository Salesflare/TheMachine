---
title: Google Calendar
area: connections
summary: 회의를 미리 준비하고 후속 조치를 할 수 있도록 일정을 가져와요. 직접 탭하지 않으면 아무것도 변경되지 않아요.
covers: connector:calendar
code: onboarding.py, google_api.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google
order: 11
translated: 7ff20ade2206d43f
---
## 가져오는 정보

지난 7일부터 앞으로 30일까지의 일정이에요. 반복 일정은 각각 표시돼요. 일정은 [캘린더](calendar.md) 탭에 표시되고, 회의 관련 할 일을 도와줘요.

## 할 수 있는 작업

스스로는 아무 작업도 하지 않아요. 초대에 응답하지 않고, 직접 지정한 사람만 초대해요.

로그인에 캘린더 수정 권한이 있으면 게스트 없이 내 캘린더나 수정 권한이 있는 공유 캘린더에서 일정을 추가, 변경 또는 삭제할 수 있어요. [캘린더](calendar.md)에서 하거나 해당 기능이 있는 할 일에서 할 수 있으며, 모든 변경은 직접 탭해야 해요. **Google 연결**로 로그인하면 일정을 읽기만 해요.

내 캘린더에서는 [캘린더](calendar.md) 양식으로 사람을 초대할 수도 있어요. 버튼에 초대받을 사람 수가 표시되고, 탭하면 Google에서 초대장을 보내요. 할 일에서는 누구도 초대하지 않아요.

## 연결하기

호스팅된 Machine에서는 Gmail과 함께 연결돼요. 설정 페이지의 **메일 및 캘린더**에서 **Google 연결**을 누르세요.

내 컴퓨터에서 사용하려면 먼저 [계정과 페어링](friends.md#a-machine-on-your-own-computer)하세요. **연결**을 열고 **캘린더**를 선택한 다음 Google Calendar를 선택하고 **Google로 로그인**을 누르세요. Gmail과 함께 연결돼요.

자체 앱을 사용하려면 `assistant connect calendar`을 실행하거나, 그곳에서 **자체 앱 사용**을 여세요. 읽을 캘린더를 선택하라는 메시지가 표시돼요.

## 연결 해제하기

- 호스팅된 Machine에서는 설정 페이지에서 주소 옆의 **연결 해제**를 누르세요. 해당 주소의 Gmail과 Calendar 연결이 모두 해제돼요.
- 내 컴퓨터에서는 **연결**을 열고 캘린더를 선택한 다음 **세부정보**, **연결 해제**를 누르세요.

## Google에서 앱 삭제하기

Google 계정에서 보안을 열고 **서드 파티 앱 및 서비스 연결**로 이동한 다음 앱을 삭제하세요. [Gmail](gmail.md)을 참고하세요.
