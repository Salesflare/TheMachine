---
title: 유사 발신자
area: security
summary: 거래하는 사람을 흉내 낸 주소에서 온 메일은 할 일에서 표시하고, 초안은 그 주소로 보내지 않아요.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 457e3111d2e26dd6
---
## 감지하는 항목

아는 주소와 비슷해 보이는 주소에서 사기가 올 수 있어요. 예를 들어 `examp1e.com`이 `example.com`나 `example-billing.com`으로 바뀌거나, 글자 하나만 다른 경우예요. The Machine은 각 발신자의 도메인을 이미 거래하는 곳의 도메인과 비교해요. 새 주소가 기존에 아는 주소와 비슷하게만 보이면 유사 주소로 판단해요.

`example.com` 옆에 있는 `example.nl`처럼 끝부분만 다른 같은 이름은 유사 주소가 아니라 같은 조직이에요. gmail.com 같은 무료 메일은 해당하지 않아요.

## 할 일에서

이런 메시지에 관한 할 일에는 "이 사람은 Alex가 아니에요. example.com이 아니라 examp1e.com에서 온 메일이에요."처럼 명확하게 표시돼요. 발신자는 사진이나 흉내 낸 사람으로 연결되는 링크 없이 주소만 표시돼요.

## The Machine이 하지 않는 일

- 유사 발신자에게 Graph의 역할을 부여하지 않아요.
- 유사 발신자를 흉내 낸 사람과 병합하지 않고, **같은 사람인가요?**에 해당 사람을 추천하지도 않아요.
- 준비한 답장은 유사 주소가 아니라 기록된 주소로 보내져요.

언제나 직접 선택한 내용이 우선해요. 유사 발신자에게 역할을 부여하거나 병합하거나, 어떤 주소로든 메일을 쓸 수 있어요.
