---
title: Salesforce
area: connections
summary: Salesforce의 거래, 작업, 활동 정보를 사람 및 프로젝트에 표시해요. 설정을 켜면 Salesforce의 연락처 정보도 최신 상태로 유지할 수 있어요.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
translated: eee5e084bac6dbd1
---
## 읽어오는 정보

새 거래와 다른 단계로 이동하거나 금액이 변경된 거래를 읽어와요. 진행 중인 작업, 통화, 메모와 함께 완료로 기록된 기타 작업, 설명이 있는 회의도 읽어와요. 연결할 때는 지난 7일간의 정보를 가져오고, 이후에는 15분마다 새 정보를 가져와요.

각 거래는 Graph의 프로젝트가 되고, 거래에 연결된 연락처는 해당 계정의 Salesforce 연락처로 각 사람의 페이지에 표시돼요.

## 변경할 수 있는 정보

**연락처 정보 업데이트**를 켜기 전까지는 아무것도 변경하지 않아요. Salesforce 로그인 정보는 내 Machine에 저장돼요.

## 연결하기

호스팅 버전의 내 Machine에서:

1. app.themachine.computer/setup에서 설정 페이지를 열고 **소스 더 보기**로 이동해요.
2. Salesforce를 열고 **Salesforce 연결**을 눌러요.
3. Salesforce에 로그인하고 The Machine(Salesflare 제작)을 허용해요.

대시보드에서도 연결할 수 있어요. **연결**, **고객**을 차례로 열고 Salesforce를 선택한 다음 **Salesforce로 로그인**을 눌러요. 내 컴퓨터에서 사용하는 경우 먼저 계정과 페어링해요.

Salesforce 사용자에게는 API 액세스 권한이 필요해요. 대부분의 에디션에 이 권한이 포함돼 있어요.

## 연락처 정보 업데이트

내 Machine이 Salesforce 연락처의 정보보다 최신 정보를 알고 있으면 Salesforce의 연락처 정보를 업데이트할 수 있어요. 업데이트할 수 있는 정보는 직함, 전화번호, 그리고 조직에서 연락처에 LinkedIn 필드를 설정한 경우 LinkedIn 링크예요.

1. **연결**에서 Salesforce를 열고 **변경될 내용 보기**를 눌러요.
2. 목록을 확인한 다음 **켜기** 또는 **나중에**를 눌러요.

다음 기준을 따라요.

- LinkedIn 또는 Slack 프로필에 적힌 정보처럼 당사자가 직접 작성한 정보나 사람 페이지에 직접 입력한 정보만 사용해요. 추측한 정보는 사용하지 않아요.
- 정보가 Salesforce 연락처의 마지막 변경 사항보다 최신인 경우에만 업데이트해요. Salesforce에서 수정한 내용이 우선 적용돼요.
- 값이 다르고 비어 있지 않은 필드만 업데이트해요. 이메일 주소와 계정은 변경하지 않아요.
- 변경 사항은 날짜와 함께 사람 페이지에 기록돼요.

중지하려면 **끄기**를 눌러요. Fleet에서 공유하는 연결은 읽기만 해요.

## 연결 삭제

- 대시보드에서 **연결**을 열고 Salesforce를 선택한 다음 **세부 정보**, **연결 해제**를 눌러요. 이미 가져온 정보는 그대로 남아요.
- 호스팅 버전의 내 Machine에서 **연결 해제 ↗**를 누르면 설정 페이지가 열려요. 그 옆에 있는 **삭제**를 눌러요.

## Salesforce에서 액세스 권한 취소하기

Salesforce에서 개인 설정을 열고 Connected Apps OAuth Usage로 이동해 권한을 취소해요. 관리자에게 요청해도 돼요. 권한을 취소하면 The Machine은 더 이상 정보를 읽거나 변경할 수 없어요.
