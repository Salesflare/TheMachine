---
title: ブラウザの接続元を自宅にする
area: troubleshooting
summary: Tailscaleを使って、ホストされているThe Machineのブラウザを自宅のインターネット経由で接続し、サイトにサインインできるようにします。
code: browser_login.py
site: Tailscale, Sign in to Tailscale, Use this exit node, Open it in Tailscale, Test it, Sign in again, Stop using it, Sign it out of Tailscale too
keywords: tailscale, exit node, home internet, ip address, cloudflare, linkedin
order: 4
---
LinkedIn、X、Cloudflareのチェックがあるサイトなどでは、クラウド上のブラウザからのサインインが拒否されることがあります。設定ページでは、Tailscaleを使って、ホストされているThe Machineのブラウザを自宅のインターネット経由で接続できます。無料で、所要時間は約10分です。ほとんどの手順は自動で進みます。

## 設定する

1. 設定ページで、The Machineのブラウザの下にある **Tailscale** を選び、**Tailscaleにサインイン** を押します。サインインするか、無料アカウントを作成します。
2. 自宅にある、電源を入れたままにできるパソコンにTailscaleをインストールし、同じアカウントでサインインします。スマートフォンはスリープするため使えません。
3. そのパソコンを出口ノードに設定します。設定ページに、システムに応じたメニューが表示されます。Linuxでは、`sudo tailscale set --advertise-exit-node` を実行します。
4. **Tailscaleで開く** を押して、次の設定を許可します：Machine settings、Edit route settings、Use as exit node、Save。同じメニューで、Disable key expiryを選びます。

設定ページで各手順が自動的に完了になります。出口ノードが1つの場合、ブラウザはすぐにそのノードを使い始めます。複数ある場合は、1つ選んで **この出口ノードを使う** を押します。

## 確認する

**テスト** を押します。ウェブサイト側から見えるブラウザの接続元として、地域とインターネットプロバイダーが表示されます。

## 自宅のパソコンがオフのとき

その場合、ブラウザはThe Machineから直接接続します。パソコンを再び起動すると、自宅経由の接続に戻ります。Tailscaleからサインアウトした場合は、**再度ログイン** を押します。キーの有効期限を無効にしていない場合、Tailscaleでは6か月後にデバイスからサインアウトされます。設定ページに日付が表示されます。

## 使用を停止する

**使用を停止** を押すと、再び直接接続します。**Tailscaleからもサインアウト** を押すと、The MachineのブラウザもTailscaleからサインアウトします。その後、Tailscaleの管理コンソールではデバイスが「期限切れ」と表示されます。そこで削除できます。
