---
title: Stripe
area: connections
summary: 결제 실패, 분쟁, 취소, 대규모 신규 구독을 확인해요. 읽기만 해요.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 6e7ca235dc502297
---
## 읽는 내용

Stripe 계정에서 확인이 필요할 수 있는 이벤트를 읽어요. 결제 실패, 분쟁, 취소, 대규모 신규 구독과 해당 고객 정보가 포함돼요. 고객의 이메일 주소를 기준으로 [Graph](graph.md)에서 해당 고객과 조직에 이벤트를 연결해요.

## 할 수 있는 작업

Stripe에서 아무 작업도 하지 않아요. 환불하거나 결제를 다시 시도하거나 내용을 변경하지 않아요. 읽기 권한만 요청하며, 설치하기 전에 Stripe에서 권한을 확인할 수 있어요.

## 연결하기

Stripe로 로그인하는 간편한 방법:

1. 대시보드에서 **연결**, **고객**, Stripe를 차례로 열어요. 또는 호스팅된 Machine의 설정 페이지(app.themachine.computer/setup)에서 **더 많은 소스**, Stripe를 차례로 열어요. 직접 사용하는 컴퓨터에서는 먼저 계정을 페어링해야 해요.
2. **Stripe로 로그인**을 눌러요. Stripe에서 계정을 선택하고 The Machine이 읽을 수 있는 항목을 보여줘요.
3. **설치**를 눌러요. 처음 있던 화면으로 돌아오면 Stripe가 연결된 거예요.

직접 사용하는 컴퓨터에서는 제한된 키를 붙여 넣어 연결할 수도 있어요.

1. Stripe에서 Events, Customers, Account에는 Read 권한을, 나머지는 모두 None으로 설정한 제한된 키를 만들어요.
2. Stripe의 설정에서 사업자 세부정보를 열어 계정 ID(acct_...)를 확인해요.
3. 위와 같이 Stripe를 열거나 `assistant connect stripe` 명령을 실행한 다음, **또는 권한이 제한된 키를 붙여 넣어요**를 열어요. 계정 ID와 키를 붙여 넣고 **연결**을 눌러요.

직접 사용하는 컴퓨터에서 Stripe로 로그인을 아직 사용할 수 없는 경우, **연결**에 안내가 표시되고 이 양식이 바로 열려요.

## 팀에 한 번만 연결하기

업무 Fleet에서는 소유자나 관리자가 Stripe를 한 번 연결한 다음 팀과 공유해요.

1. 위 방법으로 내 Machine에 Stripe를 연결해요. Fleet 탭의 **공유 연결** 상자에서도 **Stripe 연결**을 할 수 있어요.
2. Fleet 탭에서 **Stripe 공유**를 열어요. 모든 팀원이 선택되어 있으니, 공유하지 않을 팀원의 선택을 해제하고 **공유**를 눌러요.

그러면 팀원의 Machine에서도 Stripe를 읽을 수 있어요. **연결**에 공유한 사람이 표시되고, Fleet 관리자만 공유를 변경하거나 중지할 수 있어요. 내 Machine은 매시간 팀원의 접근 권한을 갱신하므로, Machine이 꺼져 있는 동안에는 팀원의 Stripe 연결이 일시 중지돼요. 로그인 정보 자체는 누구에게도 공유되지 않아요. 자세한 내용은 [Fleets](fleet.md)를 참고하세요.

팀원이 같은 Stripe 계정을 직접 연결하면 한 번만 읽어요. 공유 연결은 사용되지 않아요.

하나의 키로 다른 앱도 열 수 있는 서비스에서 연결한 Stripe는 공유할 수 없어요. 팀과 공유하려면 Stripe를 직접 연결하세요.

## 연결 해제하기

- 대시보드에서 **연결**을 열고 Stripe를 선택한 다음 **세부 정보**, **연결 해제**를 차례로 눌러요. 이미 가져온 내용은 그대로 남아요.
- 호스팅된 Machine에서 Stripe로 로그인했다면 **연결 해제 ↗**가 표시돼요. 이 버튼을 누르면 설정 페이지가 열려요. Stripe 옆의 **삭제**를 눌러요.
- Fleet과 공유 중이라면 먼저 Fleet 탭에서 **공유 중지**를 눌러요.

## Stripe에서 권한 취소하기

- Stripe로 로그인한 경우: Stripe에서 설정, 설치된 앱을 열고 The Machine을 삭제해요.
- 제한된 키를 사용한 경우: Stripe에서 개발자, API 키를 열고 해당 키를 삭제하거나 교체해요.
