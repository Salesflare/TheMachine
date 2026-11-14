---
title: Mistral
area: connections
summary: Mistral API 키로 The Machine에서 Mistral 모델을 사용해요. Le Chat Pro에는 API 크레딧이 포함돼요.
covers: mistral
code: docs/models.md, dashboard/settings-models.js
site: Other AI services, Save key, Keys, Remove
translated: 5d782f28fb69efef
---
## 용도

Mistral은 유럽의 AI 제공업체예요. Mistral API 키를 연결하면 The Machine에서 Mistral 모델로 읽고 초안을 작성해요. The Machine 자체 AI는 없어요. 요청은 계정과 Mistral의 이용 약관에 따라 Mistral로 바로 전송돼요.

## API 키 발급

Mistral은 다른 앱에서 로그인할 수 없어서 API 키를 사용해요. [Mistral 콘솔](https://console.mistral.ai/)에서 API 키를 열고 새 키를 만드세요. Le Chat Pro에는 매월 API 크레딧이 포함돼요. 크레딧을 다 쓰면 사용량에 따라 Mistral에서 요금을 청구해요.

## 연결

호스팅된 Machine에서는 설정 페이지를 열고 Your AI로 이동한 다음 **Other AI services**를 여세요. 제공업체로 Mistral을 선택하고 키를 붙여 넣은 다음 **키 저장**을 누르세요. The Machine에서 먼저 아주 작은 요청을 보내 키를 확인해요. 키가 잘못되면 바로 표시되고, 아무것도 저장되지 않아요.

Mistral Large가 기본 모델이 돼요. 더 저렴한 옵션인 Mistral Small도 있어요. 채팅에 사용하거나 대체 모델로 설정할 수 있어요.

내 컴퓨터에서 실행하는 경우 [모델 가이드](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md)를 참고하세요.

## 사용량

**설정**의 **모델**에 "Mistral API 키 사용 중"이라고 표시돼요. API 키에는 사용량 제한이 없어서 백그라운드 작업이 멈추지 않아요. 자세한 내용은 [모델](model.md)을 참고하세요.

## 연결 해제

설정 페이지의 Your AI에서 **키** 아래에 있는 Mistral 옆의 **삭제**를 누르세요. The Machine에서 키가 삭제되고, Mistral이 기본 모델이었다면 연결된 다른 모델이 대신 사용돼요. API 키 자체를 취소하려면 Mistral 콘솔에서 삭제하세요.
