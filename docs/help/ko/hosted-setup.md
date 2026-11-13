---
title: 호스팅 Machine 설정하기
area: getting-started
summary: 로그인하고 무료 이용 기간을 시작한 다음, 메일을 연결하고 AI를 선택하세요. 몇 분이면 돼요.
code: onboarding.py, dashboard.html
site: Mail and Calendar, Your AI, Continue with Google, Continue with Microsoft, Turn on, Add more any time, More sources, Open your dashboard, Sources, Ask for a source, Build it, Add a passkey, Use an authenticator app instead, Add to Claude, First to-dos, Back
order: 1
---
호스팅 Machine은 EU의 클라우드에서 전용으로 실행돼요. 계속 실행되고 최신 상태로 유지되도록 관리해 드려요.

## 가입하기

1. app.themachine.computer에서 **Google로 계속** 또는 **Microsoft로 계속**을 눌러 계정을 만드세요. Google을 선택하면 같은 화면에서 Gmail과 Calendar 연결을 요청해요. 허용하면 Google 화면을 다시 열지 않아도 메일이 연결돼요.
2. Machine의 크기와 주소를 선택하세요. 처음 {trial_days}일은 무료이며, 기간이 끝나기 전에는 요금이 청구되지 않아요. 설정 중 결제 카드를 요청하지 않으면 그 전에 계정 페이지에서 카드를 추가하세요.
3. **패스키 추가**를 누르고 지문, 얼굴 인식 또는 기기 PIN을 사용하세요. 인증 앱을 사용하려면 **대신 인증 앱 사용**을 열고 코드를 스캔한 다음 6자리 숫자를 입력하고 **켜기**를 누르세요. 이어서 표시되는 복구 코드를 저장하세요.

## 설정 페이지

설정은 화면마다 한 단계씩 진행돼요. 요금제, 패스키, **메일 및 캘린더**, **AI 설정**, **첫 할 일** 순서예요. 상단에서 현재 단계를 확인할 수 있어요. Machine은 백그라운드에서 시작되므로 기다릴 필요가 없어요.

1. **메일 및 캘린더**: **Google 연결** 또는 **Microsoft 연결**을 누르세요. 가입할 때 사용한 계정으로 시작해요. Google로 가입하면서 Gmail과 Calendar를 허용했다면 이 단계를 건너뛰고 AI 설정으로 넘어가요. 회사용인지 개인용인지는 이메일 주소에 따라 정해지며, 나중에 계정에서 변경할 수 있어요. [Gmail](gmail.md) 및 [Microsoft](microsoft.md)를 참고하세요.
2. **AI 설정**: ChatGPT 또는 Claude에 로그인하거나 AI 제공업체에서 발급한 키를 붙여넣으세요. Claude를 사용하는 경우 Claude 페이지의 코드를 붙여넣으세요. 요금제가 없다면 ChatGPT 또는 Claude를 이용하거나 키를 사용하세요. 이 단계에서 각 제공업체의 키 발급 페이지로 연결되며, 제공업체가 사용량에 따라 요금을 청구해요. [ChatGPT](chatgpt.md)를 참고하세요.
3. **첫 할 일**: Machine이 먼저 가장 최근 메일을 확인한 다음 지난 7일간의 메일을 확인해요. 확인할 사항이 없으면 읽은 내용과 다음에 연결할 항목을 알려줘요. 확인에 실패하면 몇 분 안에 다시 시도해요. 계속 실패하면 목록에 표시돼요.

**뒤로** 또는 브라우저의 뒤로 버튼을 누르면 이전 단계로 돌아가요. 메일과 AI가 작동하면 대시보드로 이동해요.

설정 중에는 선택 사항을 묻지 않아요. 설정을 마친 뒤 설정 페이지에서 **언제든 더 추가**를 누르면 Slack, WhatsApp, GitHub, [Telegram](telegram.md), [Codex](hand-to-agent.md) 같은 **추가 소스**를 연결할 수 있어요. 대시보드에서도 도움이 될 때 소스를 추천해요. 예를 들어 GitHub 메일이 계속 들어오면 GitHub를 추천해요.

Machine이 준비되면 상단에 **대시보드 열기**가 표시돼요. **Claude에 추가**를 사용하면 Claude에 메일과 할 일에 관해 물어볼 수 있어요. 알림을 받으려면 휴대폰 홈 화면에 The Machine을 추가하세요. [앱 설치 및 알림 켜기](phone-app.md)를 참고하세요.

## 소스 요청하기

원하는 소스가 없나요? **소스**에서 **소스 요청하기**를 선택하고 서비스 이름과 읽을 내용을 입력한 다음 **만들기**를 누르세요. 사용 중인 AI가 Machine에서 소스를 만들고 테스트해요. 공유하기로 선택하면 The Machine이 대신 GitHub에 공개해 모두가 이용할 수 있게 해요. GitHub 계정은 필요하지 않아요. 만든 사람으로 표시되려면 [GitHub 연결](github.md)을 하세요.

## 나중에 다시 시작하기

설정 페이지는 app.themachine.computer/setup에 있어요. 여기서 언제든 소스를 추가하거나 삭제할 수 있어요. 대시보드의 **설정**에는 **계정 열기**가 있어요.
