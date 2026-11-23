---
title: Stripe
area: connections
summary: 결제 실패, 분쟁, 구독 취소, 그리고 새로 시작한 대규모 구독을 확인해요. 읽기만 해요.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 85e6e07cca1a8e8d
---
## 읽는 정보

Stripe 계정에서 확인이 필요할 수 있는 이벤트를 읽어요. 결제 실패, 분쟁, 구독 취소, 새로 시작한 대규모 구독과 해당 고객을 확인할 수 있어요. 고객의 이메일 주소를 통해 이벤트를 해당 고객과 [Graph](graph.md)의 소속 조직에 연결해요.

결제 실패 이벤트에는 결제 목적(첫 결제, 갱신 결제)과 Stripe가 다시 결제를 시도하는 시점이 표시돼요. 카드가 거부된 이유는 표시되지 않아요. Stripe 이벤트에 이유가 없으니 Stripe에서 열어 확인해 주세요.

## 할 수 있는 작업

Stripe에서 아무 작업도 하지 않아요. 환불하거나 결제를 다시 시도하거나 설정을 변경하지 않아요. 읽기 권한만 요청하며, 설치하기 전에 Stripe에서 권한을 확인할 수 있어요.

## 연결하기

간편하게 Stripe에 로그인해 연결할 수 있어요.

1. 대시보드에서 **연결**, **고객**, Stripe를 차례로 선택해요. 호스팅된 Machine의 설정 페이지(app.themachine.computer/setup)에서는 **추가 소스**, Stripe를 선택해요. 내 컴퓨터에서 사용한다면 먼저 계정과 페어링해 주세요.
2. **Stripe로 로그인**을 눌러요. Stripe에서 계정을 선택하고 The Machine이 읽을 수 있는 정보를 보여 줘요.
3. **설치**를 눌러요. 원래 페이지로 돌아오면 Stripe 연결이 완료돼요.

내 컴퓨터에서는 권한이 제한된 키를 붙여 넣어 연결할 수도 있어요.

1. Stripe에서 Events, Customers, Account에는 Read 권한을, 그 외 항목에는 None 권한을 지정해 권한이 제한된 키를 만들어요.
2. Settings, Business details에서 계정 ID(acct_...)를 확인해요.
3. 위와 같은 방법으로 Stripe를 열거나 `assistant connect stripe`을 실행한 다음 **또는 권한이 제한된 키를 붙여 넣어요**를 열어요. 계정 ID와 키를 붙여 넣고 **연결**을 눌러요.

내 컴퓨터에서 아직 Stripe로 로그인할 수 없는 경우, 연결 화면에 안내가 표시되고 바로 이 양식이 열려요.

## 팀에서 한 번만 연결하기

Work Fleet에서는 소유자나 관리자가 Stripe를 한 번 연결한 뒤 팀과 공유할 수 있어요.

1. 먼저 내 Machine에서 Stripe를 연결해요. 위 방법을 참고해 주세요. Fleet 탭의 **공유 연결** 상자에서도 **Stripe 연결**을 선택할 수 있어요.
2. Fleet 탭에서 **Stripe 공유**를 열어요. 모든 팀원이 선택되어 있으니 공유하지 않을 팀원은 선택을 해제해요. **공유**를 눌러요.

이제 팀원의 Machine에서도 Stripe를 읽을 수 있어요. 연결 화면에서 누가 공유했는지 확인할 수 있고, Fleet 관리자만 공유 설정을 변경하거나 공유를 중지할 수 있어요. 내 Machine은 매시간 팀원의 액세스 권한을 갱신해요. 내 Machine이 꺼져 있으면 팀원의 Stripe 사용도 일시 중지돼요. 팀원에게 내 로그인 정보가 공유되지는 않아요. 자세한 내용은 [Fleet](fleet.md)을 참고해 주세요.

팀원이 같은 Stripe 계정을 직접 연결한 경우에는 한 번만 읽어요. 공유된 연결은 사용되지 않아요.

다른 앱도 열 수 있는 키 하나를 사용하는 서비스를 통해 Stripe를 연결한 경우에는 공유할 수 없어요. 대신 팀에서 Stripe를 직접 연결해 주세요.

## 연결 해제하기

- 대시보드에서 **연결**을 열고 Stripe를 선택한 다음 **세부 정보**, **연결 해제**를 차례로 눌러요. 이미 가져온 정보는 그대로 남아요.
- 호스팅된 Machine에서 Stripe에 로그인했다면 **연결 해제 ↗**가 표시돼요. 이 버튼을 눌러 설정 페이지를 연 다음 Stripe 옆의 **삭제**를 눌러요.
- Fleet과 공유 중이라면 먼저 Fleet 탭에서 **공유 중지**를 눌러요.

## Stripe에서 액세스 권한 취소하기

- Stripe로 로그인한 경우: Stripe에서 Settings, Installed apps를 열고 The Machine을 삭제해요.
- 권한이 제한된 키를 사용한 경우: Stripe에서 Developers, API keys를 열고 키를 삭제하거나 교체해요.
