---
title: 유사 발신자
area: security
summary: 교류하는 사람을 사칭한 주소에서 온 메일은 해당 할 일에 표시되고, 초안은 그 주소로 보내지지 않아요.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 6a2d62a74cec9ee4
---
## 감지하는 항목

사기는 알고 지내는 사람의 주소와 비슷한 주소에서 오기도 해요. 예를 들어 `example.com` 대신 `examp1e.com`이나 `example-billing.com`을 쓰거나, 글자 하나만 다른 주소예요. The Machine은 발신자별 도메인을 이미 교류한 도메인과 비교해요. 새 주소가 기존 주소와 비슷할 뿐이면 유사 주소로 판단해요.

`example.com` 옆의 `example.nl`처럼 이름은 같고 도메인 끝부분만 다른 경우에는 같은 조직으로 보고, 유사 주소로 판단하지 않아요. gmail.com 같은 무료 메일도 유사 주소로 판단하지 않아요.

## 할 일에 표시되는 내용

이런 메시지에 관한 할 일에는 "Alex가 아니에요. example.com이 아니라 examp1e.com에서 온 메일이에요."처럼 분명하게 표시돼요. 발신자는 사진이나 사칭 대상의 링크 없이 주소만 표시돼요.

## The Machine이 하지 않는 일

- 유사 발신자에게 Graph에서 역할을 부여하지 않아요.
- 사칭 대상과 유사 발신자를 병합하거나 **같은 사람인가요?** 아래에 유사 발신자를 추천하지 않아요.
- 답장을 준비할 때 유사 주소가 아닌, 기록된 주소로 보내요.

직접 선택한 내용이 우선이에요. 유사 발신자에게 역할을 부여하거나, 병합하거나, 원하는 주소로 메일을 보낼 수 있어요.
