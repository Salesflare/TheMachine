---
title: Telegram
area: connections
summary: 내 봇을 통해 대시보드와 같은 버튼으로 할 일을 Telegram에서 받아 보세요. 선택 사항이에요.
covers: telegram
code: assistant.py, onboarding.py, cli.py
site: Add my bot, Add more any time, Disconnect Telegram
---
## 기능

[근무 시간](work-hours.md)에 내 봇을 통해 Telegram에서 할 일을 받아 보세요. 각 할 일에는 대시보드와 같은 버튼이 있어요: **실행**, **미루기**, **수정 요청**, **완료**, **필요 없음**, 그리고 미리 작성된 메시지를 위한 **보내기**. The Machine이 Telegram 채팅을 읽게 하려면 [Telegram 채팅](telegram-chats.md)을 참고하세요.

선택 사항이에요. 휴대폰 앱에서도 같은 할 일을 알림으로 보내요.

## 보낼 수 있는 내용

내 봇에서 나에게 보내는 메시지만 보낼 수 있어요. 다른 사람에게 보내는 메시지는 할 일에서 승인을 받아야 해요.

## 연결하기

호스팅된 Machine에서:

1. Telegram에서 @BotFather에게 메시지를 보내고 /newbot을 보내세요. 받은 토큰을 복사하세요.
2. 설정 페이지에서 **언제든지 더 추가** 아래에 있는 Telegram을 열고, 토큰을 붙여 넣은 다음 **내 봇 추가**를 누르세요.

원하는 때에 추가할 수 있어요.

내 컴퓨터에서는 설치 프로그램에서 토큰을 요청해요. 또는 Telegram 사용자 ID와 함께 `assistant telegram on`을 실행하세요.

## 삭제하기

- 호스팅된 Machine에서: 설정 페이지에서 **Telegram 연결 해제**를 누르세요. 봇과 토큰이 Machine에서 삭제돼요.
- 내 컴퓨터에서: `assistant telegram off`. 봇 정보도 삭제하려면 `--remove-bot`을 추가하세요.

## Telegram에서 봇 삭제하기

@BotFather에게 메시지를 보내고 /deletebot을 보낸 다음 봇을 선택하세요.
