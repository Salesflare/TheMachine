---
title: Shortcut
area: connections
summary: 상태가 변경된 스토리와 담당자, 마감일을 확인해요. 읽기만 해요.
covers: connector:shortcut
code: connectors/shortcut.py
site: Sign in with Shortcut, Connect, More sources, Remove
translated: 68419e11fabc157c
---
## 읽어 오는 항목

Shortcut 워크스페이스에서 상태가 변경된 스토리와 담당자, 마감일을 확인해요.

## 할 수 있는 작업

Shortcut에서 아무 작업도 하지 않아요. 읽기만 해요.

## 연결하기

1. 대시보드에서 **연결**, **프로젝트 및 코드**, Shortcut을 차례로 선택하세요. 호스팅된 Machine의 설정 페이지(app.themachine.computer/setup)에서는 **추가 소스**, Shortcut을 선택하세요. 내 컴퓨터에서는 먼저 계정과 페어링하세요.
2. **Shortcut으로 로그인**을 누르고 읽기 권한을 허용하세요. Shortcut에는 읽기 권한만 요청해요.
3. The Machine으로 돌아오면 바로 로그인을 확인하고, 어떤 워크스페이스에서 어떤 계정으로 연결했는지 표시해요.

Shortcut 워크스페이스가 여러 개라면 먼저 Shortcut에서 원하는 워크스페이스로 전환하세요. 다른 워크스페이스를 연결하려면 Shortcut을 다시 추가하세요.

## 토큰 붙여넣기

**또는 API 토큰을 붙여 넣으세요** 아래에서 **토큰 받기**를 누르세요. Shortcut에서 API 토큰 페이지가 새 탭으로 열려요. 토큰을 만든 다음 복사해 붙여 넣고 **연결**을 누르세요. 내 컴퓨터에서는 `assistant connect shortcut`에서도 토큰을 요청해요. 토큰은 계정 전체에 대한 액세스 권한을 제공하지만, The Machine은 토큰으로 읽기만 해요.

## 연결 해제하기

- 대시보드에서 **연결**을 열고 Shortcut을 선택한 다음 **세부 정보**, **연결 해제**를 누르세요. 이미 가져온 내용은 그대로 남아요.
- 호스팅된 Machine에서는 설정 페이지에서 Shortcut 옆에 있는 **삭제**를 눌러도 돼요.

## Shortcut에서 액세스 권한 취소하기

붙여넣은 토큰은 API 토큰 페이지에서 삭제하세요. 로그인한 경우 여기서 연결을 해제하면 더는 읽지 않아요.
