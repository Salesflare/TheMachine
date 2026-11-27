---
title: 호스팅형 The Machine 설정하기
area: getting-started
summary: 로그인하고 무료 이용 기간을 시작한 다음, 메일을 연결하고 AI를 선택해요. 몇 분이면 설정이 끝나요.
code: onboarding.py, dashboard.html
site: Mail and Calendar, Your AI, Continue with Google, Continue with Microsoft, Turn on, Add more any time, More sources, Open your dashboard, Sources, Ask for a source, Build it, Add a passkey, Use an authenticator app instead, Add to Claude, Back
order: 1
translated: 45dda198434fcd3a
---
호스팅 Machine은 EU 클라우드에서 나만 사용할 수 있게 실행돼요. 실행과 업데이트는 저희가 관리해요.

## 가입하기

1. app.themachine.computer에서 **Google로 계속하기** 또는 **Microsoft로 계속하기**를 눌러 계정을 만들어요. Google로 가입하면 같은 화면에서 Gmail과 캘린더 연결을 요청해요. 허용하면 추가 Google 화면 없이 메일이 연결돼요.
2. 내 Machine의 크기와 주소를 선택해요. 처음 {trial_days}일은 무료이며, 기간이 끝나기 전에는 요금이 청구되지 않아요. 설정 중 결제 카드를 요청하지 않으면 그전에 계정 페이지에서 카드를 추가해 주세요.
3. **패스키 추가**를 누르고 지문, 얼굴 인식 또는 기기 PIN을 사용해요. 인증 앱을 사용하려면 **대신 인증 앱 사용**을 열고 코드를 스캔한 다음, 6자리 숫자를 입력하고 **켜기**를 눌러요. 이어서 표시되는 복구 코드를 저장해 두세요.

## 설정 페이지

설정은 화면마다 한 단계씩 진행돼요. 요금제, 패스키, **메일 및 캘린더**, **AI** 순서예요. 화면 상단에서 현재 단계를 확인할 수 있어요. 내 Machine은 백그라운드에서 시작되므로 기다릴 필요가 없어요.

1. **메일 및 캘린더**: **Google 연결** 또는 **Microsoft 연결**을 눌러요. 가입할 때 사용한 계정으로 연결이 시작돼요. Google로 가입하면서 Gmail과 캘린더 연결을 허용했다면 이 단계는 건너뛰고 AI 설정으로 넘어가요. 업무용인지 개인용인지는 주소를 기준으로 정해지며, 계정에서 나중에 변경할 수 있어요. [Gmail](gmail.md) 및 [Microsoft](microsoft.md)를 참고하세요.
2. **AI**: ChatGPT 또는 Claude에 로그인하거나 AI 제공업체의 키를 붙여 넣어요. Claude를 사용하려면 Claude 페이지의 코드를 붙여 넣으세요. 요금제가 없다면 ChatGPT 또는 Claude를 이용하거나 키를 사용하면 돼요. 이 단계에서 각 제공업체의 키 페이지로 연결되며, 사용한 만큼 제공업체에서 요금을 청구해요. [ChatGPT](chatgpt.md)를 참고하세요.
**뒤로**와 브라우저의 뒤로 가기 버튼을 누르면 이전 단계로 돌아가요. 메일과 AI가 연결되면 대시보드로 이동해요.

대시보드에 첫 할 일이 표시돼요. 내 Machine은 먼저 최신 메일을 확인한 다음 지난 7일간의 메일을 확인해요. 확인할 내용이 없으면 어떤 내용을 읽었는지와 다음에 연결할 항목을 알려 줘요. 확인에 실패하면 몇 분 안에 다시 시도하고, 계속 실패하면 목록에 표시해요.

설정 중에는 선택 사항을 요청하지 않아요. 설정이 끝난 뒤 설정 페이지의 **언제든 더 추가할 수 있어요**에 있는 **소스 더 보기**에서 Slack, WhatsApp, GitHub, [Telegram](telegram.md), [Codex](hand-to-agent.md) 같은 소스를 연결할 수 있어요. 대시보드에서도 도움이 될 때 소스를 추천해요. 예를 들어 GitHub 알림 메일이 계속 들어오면 GitHub를 추천해요.

내 Machine이 준비되면 화면 상단에 **대시보드 열기**가 표시돼요. **Claude에 추가**를 누르면 Claude에 메일과 할 일에 관해 물어볼 수 있어요. 알림을 받으려면 휴대폰 홈 화면에 The Machine을 추가하세요. [앱 설치하고 알림 켜기](phone-app.md)를 참고하세요.

## 소스 요청하기

원하는 소스가 없나요? **소스**에서 **소스 요청** 아래에 서비스 이름과 읽어야 할 내용을 적고 **만들기**를 눌러요. 사용 중인 AI가 내 Machine에서 소스를 만들고 테스트해요. 공유를 선택하면 The Machine이 GitHub에서 누구나 사용할 수 있도록 대신 등록해요. GitHub 계정은 필요하지 않아요. 만든 사람으로 표시되려면 [GitHub를 연결](github.md)하세요.

## 나중에 돌아오기

설정 페이지는 app.themachine.computer/setup에서 언제든 확인할 수 있어요. 여기서 소스를 추가하거나 삭제하세요. 대시보드의 **설정**에서 **계정 열기**를 누르면 돼요.
