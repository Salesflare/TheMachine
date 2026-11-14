---
title: 브라우저의 홈 인터넷 연결
area: troubleshooting
summary: Tailscale을 사용해 호스팅된 Machine의 브라우저가 집의 인터넷으로 연결되게 하면 사이트에서 로그인을 허용해요.
code: browser_login.py
site: Tailscale, Sign in to Tailscale, Use this exit node, Open it in Tailscale, Test it, Sign in again, Stop using it, Sign it out of Tailscale too
keywords: tailscale, exit node, home internet, ip address, cloudflare, linkedin
order: 4
translated: 9935ac3c09fa5c00
---
LinkedIn, X, Cloudflare 확인 절차가 있는 사이트처럼 클라우드의 브라우저에서는 로그인을 허용하지 않는 사이트가 있어요. 설정 페이지에서 Tailscale을 사용하면 호스팅된 Machine의 브라우저가 집의 인터넷을 통해 연결되게 할 수 있어요. 무료이고 10분 정도 걸리며, 대부분의 과정은 자동으로 진행돼요.

## 설정하기

1. 설정 페이지에서 Machine의 브라우저 아래에 있는 **Tailscale**을 선택하고 **Tailscale에 로그인**을 누르세요. 로그인하거나 무료 계정을 만드세요.
2. 집에서 계속 켜 두는 컴퓨터에 Tailscale을 설치한 다음, 같은 계정으로 로그인하세요. 휴대폰은 사용하지 마세요. 절전 모드로 전환되니까요.
3. 해당 컴퓨터를 출구 노드로 설정하세요. 설정 페이지에 시스템에 맞는 메뉴가 표시돼요. Linux에서는 `sudo tailscale set --advertise-exit-node`을 실행하세요.
4. **Tailscale에서 열기**를 누르고 다음 설정을 허용하세요. Machine 설정, 경로 설정 수정, 출구 노드로 사용, 저장. 같은 메뉴에서 키 만료 사용 안 함을 선택하세요.

설정 페이지에서 각 단계를 자동으로 완료 표시해요. 출구 노드가 하나라면 브라우저가 바로 해당 노드를 사용해요. 여러 개라면 하나를 선택하고 **이 출구 노드 사용**을 누르세요.

## 확인하기

**테스트**를 누르세요. 웹에서 브라우저가 연결된 위치를 보여 줘요. 도시와 인터넷 제공업체가 표시돼요.

## 집 컴퓨터가 꺼져 있을 때

브라우저는 Machine에서 직접 연결되고, 컴퓨터를 다시 켜면 집의 인터넷을 통해 연결돼요. Tailscale에서 로그아웃된 경우 **다시 로그인**을 누르세요. 키 만료를 사용하지 않도록 설정하지 않으면 Tailscale에서 6개월 후 기기에서 로그아웃해요. 설정 페이지에 날짜가 표시돼요.

## 사용 중지하기

**사용 중지**를 누르면 다시 직접 연결돼요. **Tailscale에서도 로그아웃**을 누르면 Machine의 브라우저에서도 Tailscale이 로그아웃돼요. 그러면 Tailscale의 관리 콘솔에 만료됨으로 표시되고, 그곳에서 삭제할 수 있어요.
