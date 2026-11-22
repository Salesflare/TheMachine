---
title: Granola
area: connections
summary: Granola에서 참여한 회의의 메모와 녹취록을 가져와요. 읽기만 해요.
covers: connector:granola
code: connectors/granola.py, meeting_notes.py, onboarding.py
site: Connect, More sources, Remove
translated: fb6244142af7800d
---
## 읽는 항목

참여한 회의의 Granola 메모와 녹취록을 가져와요. 연결할 때 최근 7일분을 가져오고, 이후 새 항목이 생기면 가져와요. 작성 중인 메모는 Granola에서 작성이 끝난 뒤 가져와요.

각 항목은 캘린더에서 해당 회의에 추가돼요. Granola가 회의 이름을 지정했다면 그 이름을 사용하고, 그렇지 않으면 같은 시간대의 회의에 추가해요. Granola 메모는 메모에, 녹취록은 녹취록에 추가하고 **Granola에서**라고 표시해요. 직접 추가한 내용은 그대로 남아요.

회의가 끝나면 The Machine은 약속한 내용, 결정한 내용, 아직 해야 할 일을 확인해요. 예를 들면 "자료를 보낼게요" 같은 내용이에요. 다음 단계가 분명한 경우에만 할 일을 만들어요. 회의 참석자는 이메일 주소를 기준으로 [Graph](graph.md)에 연결돼요.

## 할 수 있는 작업

Granola에서 아무 작업도 하지 않아요. 읽기만 하고 메모를 수정하거나 공유하거나 삭제하지 않아요.

## 필요한 권한

Granola의 개인 API 키가 필요해요. Granola의 Business 및 Enterprise 요금제에서 API 키를 사용할 수 있어요. 키로는 Granola에서 직접 확인할 수 있는 내 메모와 나와 공유된 메모를 읽어요.

## 연결하기

1. Granola 데스크톱 앱에서 **설정**, **커넥터**, **API 키**를 선택해요. 개인 메모 액세스 권한이 있는 키를 만들고 복사해요.
2. 대시보드에서 **연결**, **회의**, Granola를 선택해요. 호스팅된 Machine의 설정 페이지(app.themachine.computer/setup)에서는 **소스 더 보기**, Granola를 선택해요. 내 컴퓨터에서는 `assistant connect granola`에서도 키를 입력하라는 메시지가 표시돼요.
3. 키를 붙여 넣고 **업무** 또는 **개인**을 선택한 다음 **연결**을 눌러요.

키는 바로 확인돼요. 나중에 Granola에서 키를 더 이상 허용하지 않으면 **연결**에서 Granola를 열어 새 키를 입력하라는 메시지가 표시돼요.

## 연결 해제하기

- 대시보드에서 **연결**을 선택하고 Granola를 연 다음 **세부 정보**, **연결 해제**를 선택해요. 이미 가져온 내용은 그대로 남아요.
- 호스팅된 Machine에서는 설정 페이지에서 Granola 옆의 **삭제**를 눌러도 돼요.

## Granola에서 키 폐기하기

Granola 데스크톱 앱에서 **설정**, **커넥터**, **API 키**를 선택한 다음 키를 삭제해요.
