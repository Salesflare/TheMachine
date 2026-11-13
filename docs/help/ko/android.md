---
title: Android 알림
area: connections
summary: OpenClaw 앱을 통해 Android 휴대전화의 알림을 확인해요. 읽기만 해요.
covers: connector:android
code: onboarding.py, android-notifications.mjs
site: Show a setup code, Approve, Remove
---
## 읽는 항목

OpenClaw 앱을 통해 Android 휴대전화의 알림을 확인해요. 일회용 코드는 제외하고, WhatsApp, Telegram, Signal, Discord 알림도 제외해요.

## 할 수 있는 작업

휴대전화에서 아무 작업도 할 수 없어요. 알림을 읽기만 해요.

## 연결하기

호스팅된 Machine에서:

1. 휴대전화에서 Google Play를 열고 OpenClaw를 설치해요.
2. 대시보드에서 **연결**을 열고 **기타**를 선택한 다음, Android 휴대전화를 선택하고 **설정 코드 표시**를 눌러요.
3. OpenClaw 앱에서 Gateway를 추가하고 코드를 스캔해요. 대시보드로 돌아와 **승인**을 눌러요.
4. 앱에서 요청하면 알림 접근을 허용해요. 그런 다음 앱 설정에서 알림 이벤트 전달을 켜요. 그러면 알림이 10분마다 확인될 때만 전달되는 게 아니라, 도착하는 즉시 전달돼요.

직접 소유한 컴퓨터에서는 OpenClaw 앱에서 휴대전화를 페어링한 다음 `assistant connect android`을 실행해요.

## 연결 해제하기

- 대시보드에서 **연결**을 열고 Android를 선택한 다음 **세부 정보**, **연결 해제**를 차례로 눌러요.
- 호스팅된 Machine에서는 설정 페이지에서 해당 항목 옆의 **삭제**를 눌러도 돼요.

## 휴대전화에서 연결 해제하기

Android 설정에서 OpenClaw 앱의 알림 접근을 끄거나, OpenClaw 앱에서 휴대전화의 페어링을 해제해요.
