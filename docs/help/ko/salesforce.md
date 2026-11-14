---
title: Salesforce
area: connections
summary: Salesforce의 거래, 할 일, 활동을 사람과 프로젝트에서 확인할 수 있어요. 설정을 켜면 연락처 정보도 최신 상태로 유지할 수 있어요.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
translated: e2394748e0a676b1
---
## 읽는 정보

새 거래, 다른 단계로 이동하거나 금액이 변경된 거래를 읽어요. 진행 중인 할 일, 통화, 완료로 기록된 다른 할 일과 메모, 설명이 있는 회의를 읽어요. 연결할 때는 최근 7일의 정보를 가져오고, 이후에는 15분마다 새 정보를 가져와요.

각 거래는 Graph의 프로젝트가 되고, 거래에 연결된 연락처는 해당 계정의 Salesforce 연락처로 사람 페이지에 표시돼요.

## 변경할 수 있는 정보

**연락처 정보 업데이트**를 켜기 전까지는 아무것도 변경하지 않아요. Salesforce 로그인 정보는 Machine에 보관돼요.

## 연결하기

호스팅된 Machine에서:

1. app.themachine.computer/setup에서 설정 페이지를 열고 **추가 데이터 소스**로 이동해요.
2. Salesforce를 열고 **Salesforce 연결**을 눌러요.
3. Salesforce에 로그인하고 Salesflare에서 만든 The Machine을 허용해요.

또는 대시보드에서 **연결**, **고객**을 차례로 열고 Salesforce를 선택한 다음 **Salesforce로 로그인**을 눌러요.

Salesforce 사용자에게 API 액세스 권한이 필요해요. 대부분의 에디션에 이 권한이 포함돼요.

## 연락처 정보 업데이트

Machine에서 Salesforce 연락처의 최신 정보를 확인하면 Salesforce의 연락처를 업데이트할 수 있어요. 직함, 전화번호, 그리고 조직에 연락처용 LinkedIn 필드가 있는 경우 LinkedIn 링크를 업데이트해요.

1. **연결**에서 Salesforce를 열고 **변경될 내용 보기**를 눌러요.
2. 목록을 확인한 다음 **켜기** 또는 **나중에**를 눌러요.

다음 기준을 따라요.

- LinkedIn이나 Slack 프로필처럼 해당 사용자가 직접 작성한 정보나 사람 페이지에 직접 설정한 정보만 사용해요. 추측한 정보는 사용하지 않아요.
- Salesforce 연락처를 마지막으로 변경한 시점보다 최신인 정보만 사용해요. Salesforce에서 수정한 정보가 우선이에요.
- 값이 다를 때만 업데이트하고, 빈 값은 반영하지 않아요. 이메일 주소와 계정은 변경하지 않아요.
- 변경 사항은 날짜와 함께 사람 페이지에 기록돼요.

중지하려면 **끄기**를 눌러요. Fleet에서 공유하는 연결은 읽기만 가능해요.

## 연결 해제

- 대시보드에서 **연결**을 열고 Salesforce, **세부정보**, **연결 해제**를 차례로 눌러요. 이미 가져온 정보는 그대로 남아요.
- 호스팅된 Machine에서는 설정 페이지에서 Salesforce 옆의 **삭제**를 눌러도 돼요.

## Salesforce에서 액세스 권한 취소하기

Salesforce에서 개인 설정을 열고 Connected Apps OAuth Usage로 이동해요. 또는 관리자에게 요청해 The Machine의 액세스 권한을 취소해요. 그러면 더 이상 정보를 읽거나 변경할 수 없어요.
