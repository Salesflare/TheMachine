---
title: Google Meet
area: connections
summary: 직접 주최한 Meet 회의의 대본과 Gemini 메모를 가져와요. 읽기만 해요.
covers: connector:google_meet
code: connectors/google_meet.py, onboarding.py
site: Sign in with Google
---
## 읽는 항목

직접 주최한 Google Meet 회의의 대본과 Gemini 메모를 읽어요. Meet에서 생성된 항목만 가져오며, 연결할 때는 최근 7일간의 항목을 가져오고 이후에는 새 항목이 생길 때마다 가져와요. Meet은 이 항목을 30일 동안 보관해요.

회의 중에 대본이나 Gemini 메모 기능을 켜 둔 경우에만 생성돼요.

각 항목은 Calendar의 해당 회의에 표시돼요. Gemini 메모는 메모 아래에, 대본은 대본 아래에 표시되고, **Google Meet에서 가져옴**으로 표시돼요. 직접 추가한 내용은 그대로 남아요.

## 할 수 있는 작업

Meet, Docs, Drive에서는 아무 작업도 하지 않아요. 읽기만 하며, 대본 기능도 직접 켜지 않아요.

## 요청하는 권한

메일 권한과는 별도로 권한을 승인해야 해요. Google에서 The Machine에 다음 권한을 요청해요.

- Google Meet 회의와 대본, Gemini 메모 보기
- Gemini 메모 문서를 읽기 위해 Google Docs 보기

Drive 권한은 요청하지 않아요. Gmail과 Calendar 권한은 그대로 유지돼요.

## 연결하기

Gmail을 연결하지 않아도 돼요. 연결하려면 다음 단계를 따르세요.

- 호스팅된 Machine: 대시보드에서 **연결**을 열고 **회의**를 선택한 다음 **Google Meet**을 선택하고 **Google로 로그인**을 눌러요. 위 권한을 승인하면 대시보드로 돌아와요.
- 계정과 페어링된 개인 컴퓨터: 같은 단계를 따라요. 로그인 페이지가 새 탭에서 열려요.

Google Meet 권한을 승인하지 않으면 연결되지 않아요. 붙여넣거나 갱신할 항목은 없어요.

나중에 권한을 취소하면 **연결**의 Google Meet에서 다시 로그인하라는 메시지가 표시돼요.

## 연결 해제하기

대시보드에서 **연결**을 열고 Google Meet을 선택한 다음 **세부정보**, **연결 해제**를 차례로 눌러요. 이미 가져온 내용은 그대로 남아요.

## Google에서 권한 취소하기

myaccount.google.com/permissions를 열고 The Machine의 Google Meet 액세스 권한을 삭제해요. Gmail과 Calendar는 계속 사용할 수 있어요.
