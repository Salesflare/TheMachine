---
title: 데스크톱 앱을 통해 웹 탐색하기
area: troubleshooting
summary: 호스팅된 내 Machine의 브라우저가 데스크톱 앱을 실행하는 컴퓨터를 통해 인터넷에 접속하게 해요. 그러면 웹사이트에 내 인터넷 연결로 표시돼요.
code: desktop/src/exit.rs, desktop/src/settings.rs
keywords: desktop app, exit node, home internet, office, ip address, linkedin, sign in, proxy
order: 5
translated: 6da69c78d7e60574
---
일부 사이트(예: LinkedIn)는 클라우드 브라우저에서 로그인을 거부해요. [데스크톱 앱](desktop-app.md)에 로그인하면 호스팅된 내 Machine의 브라우저가 해당 컴퓨터를 통해 인터넷에 접속할 수 있어요. 그러면 사이트에는 데이터 센터가 아니라 집이나 사무실의 인터넷 연결로 표시돼요.

## 켜기

내 Machine에서 이 기능을 사용할 수 있게 되면 기본적으로 켜져 있어요. 데스크톱 앱의 **설정**에서 스위치 이름은 **내 Machine이 이 컴퓨터를 통해 웹을 탐색하도록 허용**이에요. 이 기능을 끄면 내 Machine의 브라우저가 즉시 다시 직접 인터넷에 접속해요.

내 Machine의 브라우저가 이 기능을 사용하는 동안 로봇 상자와 메뉴 막대 또는 작업 표시줄의 앱 아이콘에 **내 Machine이 이 컴퓨터를 통해 웹을 탐색 중**이라고 표시돼요.

## 이 기능을 통해 전송되는 항목

내 Machine의 브라우저가 웹사이트에 접속할 때만 사용해요. 공용 인터넷 주소의 포트 80과 443만 사용해요. 앱은 이 컴퓨터 자체나 집 또는 사무실 네트워크, 그 밖의 사설 주소에 연결하지 않으며, 컴퓨터에서 포트를 열지도 않아요. 속도는 다운로드 4 MB/s, 업로드 1 MB/s로 제한되고, 하루 사용량은 2 GB로 제한돼요.

## 컴퓨터가 꺼져 있을 때

내 Machine의 브라우저는 내 Machine에서 직접 인터넷에 접속해요. 앱이 다시 실행되면 컴퓨터를 통해 접속해요.
