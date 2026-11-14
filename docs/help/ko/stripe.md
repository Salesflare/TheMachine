---
title: Stripe
area: connections
summary: 실패한 결제, 분쟁, 취소, 큰 규모의 신규 구독을 확인해요. 읽기 전용이에요.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 99a14108376ddcc1
---
## 읽는 내용

Stripe 계정에서 확인이 필요할 수 있는 이벤트를 읽어요. 실패한 결제, 분쟁, 취소, 큰 규모의 신규 구독과 해당 고객을 확인해요. 고객의 이메일 주소를 통해 이벤트를 [Graph](graph.md)의 해당 고객 및 조직과 연결해요.

## 할 수 있는 일

Stripe에서 아무 작업도 하지 않아요. 환불하거나 결제를 다시 시도하거나 내용을 변경하지 않아요. 읽기 권한만 요청하며, 설치하기 전에 Stripe에서 권한을 확인할 수 있어요.

## 연결하기

Stripe에 로그인하는 가장 쉬운 방법이에요.

1. 대시보드에서 **연결**, **고객**, Stripe를 차례로 선택해요. 호스팅된 Machine의 설정 페이지 app.themachine.computer/setup에서는 **추가 소스**, Stripe를 선택해요. 개인 컴퓨터에서는 먼저 계정과 페어링해야 해요.
2. **Stripe로 로그인**을 선택해요. Stripe에서 계정을 선택하고 The Machine이 읽을 수 있는 내용을 확인해요.
3. **설치**를 선택해요. 원래 페이지로 돌아오면 Stripe가 연결돼 있어요.

제한된 키를 붙여넣어 연결할 수도 있어요.

1. Stripe에서 이벤트, 고객, 계정에는 읽기 권한을, 나머지 항목에는 권한 없음을 설정해 제한된 키를 만들어요.
2. 설정의 비즈니스 정보에서 계정 ID(acct_...)를 찾아요.
3. 위와 같이 Stripe를 열거나 `assistant connect stripe`을 실행해요. **제한된 키 직접 붙여넣기**를 열고 계정 ID와 키를 붙여넣은 다음 **연결**을 선택해요.

개인 컴퓨터에서 아직 Stripe로 로그인을 사용할 수 없으면 연결 화면에 안내가 표시되고 이 양식이 바로 열려요.

## 팀에서 한 번만 연결하기

Work Fleet에서는 소유자나 관리자가 Stripe를 한 번 연결해 팀과 공유해요.

1. 개인 Machine에서 Stripe를 연결해요(위 내용 참고). Fleet 탭의 **공유 연결** 상자에서도 **Stripe 연결**을 선택할 수 있어요.
2. Fleet 탭에서 **Stripe 공유**를 열어요. 모든 팀원이 선택되어 있어요. 공유하지 않을 팀원은 선택을 해제하고 **공유**를 선택해요.

그러면 팀원의 Machine에서도 Stripe를 읽을 수 있어요. 연결 화면에서 공유한 사람을 확인할 수 있고, Fleet 관리자만 공유 설정을 변경하거나 공유를 중지할 수 있어요. Machine은 매시간 팀원의 액세스 권한을 갱신해요. Machine이 꺼져 있는 동안에는 팀원의 Stripe 액세스가 일시 중지돼요. 로그인 정보 자체는 공유되지 않아요. 자세한 내용은 [Fleet](fleet.md)을 참고하세요.

팀원이 같은 Stripe 계정을 직접 연결한 경우에는 한 번만 읽어요. 공유 연결은 사용되지 않아요.

다른 앱도 함께 열 수 있는 단일 키를 사용하는 서비스를 통해 연결한 Stripe는 공유할 수 없어요. 팀에서 사용하려면 Stripe를 직접 연결하세요.

## 연결 해제하기

- 대시보드에서 **연결**을 선택하고 Stripe를 연 다음 **세부 정보**, **연결 해제**를 선택해요. 이미 가져온 데이터는 그대로 남아요.
- 호스팅된 Machine에서는 설정 페이지에서 Stripe 옆의 **삭제**를 선택해도 돼요.
- Fleet과 공유 중이라면 먼저 Fleet 탭에서 **공유 중지**를 선택해요.

## Stripe에서 액세스 권한 취소하기

- Stripe로 로그인한 경우: Stripe에서 설정, 설치된 앱을 열고 The Machine을 삭제해요.
- 제한된 키를 사용한 경우: Stripe에서 개발자, API 키를 열고 키를 삭제하거나 교체해요.
