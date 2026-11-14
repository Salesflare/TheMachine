---
title: ChatGPT
area: connections
summary: ChatGPT로 로그인하면 ChatGPT 요금제로 Machine을 실행하고 ChatGPT 스킬을 가져올 수 있어요.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
translated: fc97be60c0b68336
---
## 용도

ChatGPT로 로그인하면 Machine이 ChatGPT를 사용해 읽고 초안을 작성해요. 개인 ChatGPT 요금제가 적용돼요. The Machine에는 자체 AI가 없어요. 요청은 계정과 OpenAI 이용 약관에 따라 OpenAI로 직접 전송돼요.

## 로그인

호스팅 환경의 Machine에서는 설정 페이지에서 **ChatGPT로 로그인**을 누르고, ChatGPT에 표시된 코드를 입력해요. 나중에 로그아웃됐다면 **ChatGPT 다시 연결**을 눌러요.

OpenAI에서 코드를 거부하면 [ChatGPT 보안 설정](https://chatgpt.com/settings/security)을 열고 맨 아래로 스크롤한 다음 "Codex, Excel, PowerPoint, Word의 기기 코드 로그인 사용" 스위치를 켜요. 그런 다음 코드를 다시 입력해요.

이 스위치가 보이지 않나요? 업무용 계정(Business, Enterprise 또는 Edu)을 사용한다면 ChatGPT 관리자가 [권한 및 역할](https://chatgpt.com/admin/permissions)의 "Codex 및 Work Local"에서 스위치를 켜야 해요.

개인 컴퓨터에서는 터미널에서 `openclaw models auth login`을 실행해요.

## 사용량 한도

ChatGPT 요금제에는 5시간 한도와 주간 한도가 있어요. **설정**의 **모델**에서 각 한도의 사용량과 초기화 시점을 확인할 수 있어요. 백그라운드 작업은 한도에 도달하기 훨씬 전에 일시 중지돼요. 직접 채팅할 여유를 남겨 두기 위해서예요. 한도에 도달하면 대시보드 상단에 초기화 시점이 표시돼요. [모델](model.md)을 참고하세요.

## ChatGPT 스킬 가져오기

**설정**에서 **스킬**을 열고 **가져오기**를 누른 다음 **ChatGPT에서**를 선택하고 **내 스킬 찾기**를 눌러요. 스킬의 지침만 가져와요. [스킬](skills.md)을 참고하세요.

## 연결 해제

설정 페이지에서 다른 모델을 선택해요. 개인 컴퓨터에서는 같은 방법으로 다른 제공업체에 로그인하면 돼요. OpenAI 쪽의 접근 권한을 차단하려면 ChatGPT 보안 설정에서 세션을 로그아웃해요.
