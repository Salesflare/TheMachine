---
title: ブラウザーの接続元を自宅にする
area: troubleshooting
summary: Tailscaleを使って、ホスティング版のMachineのブラウザーを自宅のインターネット経由で接続し、サイトにログインできるようにします。
code: browser_login.py
site: Tailscale, Sign in to Tailscale, Use this exit node, Open it in Tailscale, Test it, Sign in again, Stop using it, Sign it out of Tailscale too
keywords: tailscale, exit node, home internet, ip address, cloudflare, linkedin
order: 4
translated: 9935ac3c09fa5c00
---
LinkedIn、X、Cloudflareのチェックがあるサイトなどでは、クラウド上のブラウザーからのログインが拒否されることがあります。セットアップページでは、Tailscaleを使って、ホスティング版のMachineのブラウザーを自宅のインターネット経由で接続できます。無料で、所要時間は約10分です。ほとんどの手順は自動で進みます。

## 設定する

1. セットアップページで、Machineのブラウザーの下にある **Tailscale** を選び、**Tailscaleにログイン** を押します。ログインするか、無料アカウントを作成します。
2. 自宅にある、電源を入れたままにできるコンピューターにTailscaleをインストールし、同じアカウントでログインします。スマートフォンはスリープするため使えません。
3. そのコンピューターを出口ノードに設定します。セットアップページに、そのOS用のメニューが表示されます。Linuxでは、`sudo tailscale set --advertise-exit-node` を実行します。
4. **Tailscaleで開く** を押して、次の設定を許可します：Machine settings、Edit route settings、Use as exit node、Save。同じメニューで、Disable key expiryを選びます。

セットアップページでは、各手順に自動でチェックが付きます。出口ノードが1つの場合、ブラウザーはすぐにそのノードを使い始めます。複数ある場合は、1つ選んで **この出口ノードを使う** を押します。

## 確認する

**テスト** を押します。ウェブサイト側から見えるブラウザーの接続元として、地域とインターネットプロバイダーが表示されます。

## 自宅のコンピューターがオフのとき

その場合、ブラウザーはMachineから直接接続します。コンピューターを再び起動すると、自宅経由の接続に戻ります。Tailscaleからログアウトした場合は、**再度ログイン** を押します。キーの有効期限を無効にしていない場合、Tailscaleでは6か月後にデバイスからログアウトされます。セットアップページに日付が表示されます。

## 使用を停止する

**使用を停止** を押すと、再び直接接続します。**Tailscaleからもログアウト** を押すと、MachineのブラウザーもTailscaleからログアウトします。その後、Tailscaleの管理コンソールではデバイスが「期限切れ」と表示されます。そこで削除できます。
