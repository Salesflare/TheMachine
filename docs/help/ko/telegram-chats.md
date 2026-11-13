---
title: Telegram 채팅
area: connections
summary: 내 Telegram 계정의 로그인 기기로 Telegram 채팅과 소규모 그룹을 읽어요. 답장은 승인한 뒤에만 보내요.
covers: connector:telegram
code: onboarding.py, telegram_mirror.py, telegram_store.py, next_actions.py
---
## 읽는 내용

Telegram Desktop처럼 내 Telegram 계정에 로그인한 기기로 비공개 채팅과 최대 50명까지 참여하는 그룹을 읽어요. 연결하면 최근 7일간의 내용을 읽고, 그다음부터는 새로 들어오는 내용을 읽어요.

채널, 봇, 저장된 메시지, Telegram 자체 서비스 메시지는 읽지 않아요. 알림을 끈 채팅과 보관된 채팅도 건너뛰어요.

읽음 상태나 온라인 상태에는 영향을 주지 않아요. 메시지를 읽음으로 표시하지 않으며, 휴대폰에는 새 메시지가 계속 새 메시지로 표시돼요.

이 연결은 자체 봇이 할 일을 보내 주는 [Telegram](telegram.md)과는 별개예요.

## 보낼 수 있는 내용

이미 있는 채팅에 텍스트를 보내요. 할 일에서 승인한 뒤에만 전송돼요. 한 번에 하나씩 보내고, 전송 사이에 잠시 간격을 둬요.

할 일이 이메일로 들어왔지만 Telegram에서 그 사람과 대화한다면, 할 일의 채팅에 알려 주세요. The Machine이 그 사람과의 기존 채팅을 찾아 초안을 Telegram으로 바꿔요. 내용을 검토하고 보내면 돼요. 새 채팅을 시작하지는 않아요.

## 연결하기

1. 대시보드에서 **연결**을 열고 **채팅**을 선택한 다음 Telegram 채팅을 골라요.
2. **다른 기기의 Telegram으로 QR 코드 스캔**을 선택해요.
3. 휴대폰에서 Telegram을 열고 설정, 기기, **데스크톱 기기 연결**을 차례로 선택한 다음 코드를 스캔해요.
4. 계정에 클라우드 비밀번호가 설정되어 있다면 요청될 때 입력해요. 비밀번호는 Telegram으로 전송되며 저장되지 않아요.

휴대폰에서는 같은 화면에서 QR 코드를 스캔할 수 없으므로 양식에 **전화번호로 코드 받기**가 먼저 표시돼요. Telegram에서 코드를 보낸 곳도 안내해요. 다른 기기의 Telegram 앱, SMS 또는 로그인 이메일일 수 있어요. 코드가 오지 않나요? **코드 다시 보내기**를 눌러요.

직접 사용하는 컴퓨터에서는 개인 Telegram 앱 ID도 필요해요. [my.telegram.org](https://my.telegram.org)의 API development tools에서 앱 ID를 만든 다음 양식에 api_id와 api_hash를 입력해요.

또는 터미널에서 `assistant connect telegram`을 실행하고 화면에 표시된 코드를 스캔해요.

## 연결이 끊기는 경우

- **Telegram에서 로그아웃됨**: Telegram에서 이 기기의 로그인을 종료했거나 휴대폰에서 로그아웃했어요. **연결**에서 **다시 연결**을 눌러요.
- **Telegram에서 앱 ID를 더 이상 허용하지 않음**: Telegram에서 The Machine이 사용하는 앱 ID를 더 이상 허용하지 않아요. **다시 연결**을 누르고 개인 앱 ID를 추가할 때까지는 아무것도 읽거나 보내지 않아요.

Telegram은 The Machine 같은 앱의 로그인을 제한하거나 종료할 수 있어요.

## 사진

The Machine은 Graph에 있는 사람 중 프로필 사진이 없는 사람의 사진을 Telegram에 요청해요. 채팅을 읽는 것과 같은 로그인으로 요청하며, 하루 최대 50명까지, 읽는 채팅에 있는 사람만 대상으로 해요. 상대에게 아무것도 보내지 않아요. 사진을 숨긴 사람은 계속 사진이 표시되지 않아요.

## 연결 해제

**연결**에서 Telegram 채팅을 열고 **세부정보**를 선택한 다음 **연결 해제**를 눌러요. The Machine이 Telegram에서 로그아웃하고 Telegram 관련 데이터를 삭제해요.

또는 휴대폰에서 세션을 종료할 수 있어요. Telegram에서 설정, 기기를 차례로 열고 The Machine을 누른 다음 세션을 종료해요.
