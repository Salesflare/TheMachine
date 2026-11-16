---
title: 유사 발신자
area: security
summary: 아는 상대를 흉내 낸 주소에서 온 메일은 해당 할 일에 표시하고, 초안은 그 주소로 보내지 않아요.
covers: lookalike-senders
code: lookalike.py, dashboard/todos-cards.js
order: 5
keywords: phishing, fake address, spoof, scam, impersonation, lookalike domain, fraud
translated: 15a6a5dafcfa807b
---
## 감지하는 항목

아는 주소와 비슷해 보이는 주소에서 사기가 올 수 있어요. 예를 들면 `example.com` 대신 `examp1e.com`을 쓰거나, `example-billing.com`처럼 한 글자가 다르거나 두 글자의 순서가 바뀐 주소예요. The Machine은 각 발신자의 도메인을 이미 연락해 온 도메인과 비교해요.

비슷한 주소 두 개 중 직접 이메일을 보냈거나, 만났거나, 직접 설정한 쪽이 진짜예요. 다른 쪽에서 먼저 연락했더라도 마찬가지예요. 어느 쪽도 그런 이력이 없다면 더 최근에 나타난 주소를 유사 발신자로 봐요.

`example.com` 옆의 `example.nl`처럼 끝부분만 다른 같은 이름의 주소는 같은 조직으로 보며, 유사 발신자로 보지 않아요. gmail.com 같은 무료 메일 주소는 비교 대상에 포함하지 않아요.

## 할 일에서

이런 메시지에 관한 할 일에는 "이 사람은 Alex가 아니에요. example.com이 아니라 examp1e.com에서 보낸 메일이에요."처럼 분명하게 표시해요. 발신자는 사진이나 사칭 대상의 연락처 링크 없이 이메일 주소만 표시돼요.

## The Machine이 하지 않는 일

- 유사 발신자에게 Graph의 역할을 부여하지 않으며, 해당 도메인을 프로젝트의 조직으로 지정하지 않아요.
- 같은 이름으로 같은 대화에 글을 썼더라도 사칭 대상과 합치지 않으며, **같은 사람인가요?** 아래에 추천하지 않아요.
- 답장을 준비할 때 유사 발신자 주소가 아니라 등록된 주소로 보내요.

언제나 직접 선택할 수 있어요. 유사 발신자에게 역할을 부여하거나, 사칭 대상과 합치거나, 어떤 주소로든 메일을 보낼 수 있어요.
