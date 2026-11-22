# Glossary

How The Machine's product terms read in each language. The daily translator (`scripts/translate.py`) sends it with
every request, so a new term goes here, with a form for every language, in the pull request that first uses it.
Every catalog in this folder follows it, and `tests/test_i18n.py` checks that: when an English string uses a term from the **Terms** table, its translation uses one
of the forms listed for that language (any of the forms after the first are inflections the check also accepts). A
capitalized term (Ready, Settings) is the name of a status or a screen and only counts capitalized; a lowercase one
counts in any case. File names (.skill, SKILL.md) don't count.

**Ready** (a to-do's status, its section, its notifications) means prepared and waiting for the owner, never done:
Dutch *Klaargezet* and *Voor jou klaargezet*, never *Klaar* alone; Spanish and Brazilian Portuguese *Para revisar*, never
*Lista* or *Pronta* alone (they read as finished). *Klaar om ...*, *Lista para ...*, *Pronta para ...* are fine.

Tone: short UI copy, the way a native product says it, never word for word. Dutch uses *je*, French *vous*, German *du*,
Spanish *tú*, Italian *tu*, Brazilian Portuguese *você*, Russian *вы* (lowercase), Chinese *你* (never 您). Japanese
writes polite *です/ます* and Korean polite *해요체* (요 endings), both without a word for "you" (the subject is left out).
Chinese and Japanese use full-width punctuation (，。：？！) in their own text. No em dashes. Placeholders (`{}`, `{0}`,
`{1}`) stay; reorder with `{0}`, `{1}` when the sentence needs it.

Plurals: Chinese, Japanese and Korean have one form (a plural entry is `{"other": ...}`); Russian has four
(`one`, `few`, `many`, `other`, CLDR: 1, 21 задача; 2-4, 22 задачи; 5-20, 25 задач; 1.5 задачи).

## The Machine is "she" (and "he" in Dutch)

One grammatical gender for The Machine, and for an owner's Machine, in each language: the one its word for "machine"
has, so pronouns, articles and agreement never switch within a page. The name itself stays The Machine. Calling
it an assistant follows the same gender (the last part of each rule), and so does The Machine speaking for itself
("I'm stuck": *Je suis bloquée*, *Estoy atascada*, *Sono bloccata*; "by myself": *toute seule*, *sozinha*). The same
table is in the control plane's glossary (cloud/i18n/glossary.md) for the site and the setup pages.

| Language | Gender | Rule |
|---|---|---|
| nl | masculine | hij, hem, zijn: "The Machine leest je mail. Hij stuurt je alleen wat telt." Never ze or haar for it. Assistant: assistent. |
| fr | feminine | elle, la, sa, and feminine agreement (prête, connectée): "The Machine lit vos e-mails. Elle ..." Never il. Assistant: une assistante, votre assistante. |
| de | feminine | sie, ihr, die, deine Machine: "The Machine liest deine Mails. Sie ..." Never er or sein. Assistant: Assistentin, KI-Assistentin. Also for German: Work Fleet, Family Fleet and Team Graph stay names (never Arbeits-Fleet, Familien-Fleet, Team-Graph); team brief is das Team-Briefing; the phone you carry is the Handy (never Telefon or Smartphone); Set aside (a paused review) is Beiseitegelegt, never Zurückgestellt (that is snooze); Ready is Bereit, never fertig; the owner of a record or a Fleet is the Inhaber; counted follow-ups are Nachfassnachrichten; a button or page named in a sentence goes in „…“. |
| es | feminine | ella, la, su, and feminine agreement (lista, conectada): "tu Machine está lista". Never él. Assistant: una asistente, tu propia asistente. |
| it | feminine | lei, la, sua, and feminine agreement (pronta, collegata): "la tua Machine è pronta". Never lui. Assistant: un’assistente, la tua assistente. The reader and people of unknown gender get neutral wording: Hai effettuato l’accesso, Ti diamo il benvenuto, Serve il tuo intervento, never Sei entrato, Benvenuto, richiede te. AI is IA, except in product names (Google AI Pro). Work Fleet: Fleet di lavoro; Family Fleet: Fleet di famiglia. |
| pt-BR | feminine | ela, a, sua, dela, da, na, and feminine agreement (pronta, conectada): "sua Machine está pronta". Never ele, o, do, no. Assistant: uma assistente, sua assistente. The name too: da, na, pela The Machine, never de, em, do, no The Machine. Fleet is masculine (o Fleet, Fleet de Trabalho, Fleet da Família); vaga and Network are feminine (paga por, na Network). Write e-mail with a hyphen; follow-up stays follow-up (Fazer follow-up). |
| zh-CN | none | No gender: say The Machine again, or 它 when a pronoun can't be left out. Never 他 or 她. Machine stays Machine, never 机器: your Machine is 你的Machine, never 你的The Machine. Assistant: 助手. No space between Chinese and a Latin word or number, “” quotes, one … for an ellipsis, menu paths as “设置”>“通知”. Words: thread or conversation 对话 (never 线程 or 讨论串 outside Slack); plan (ChatGPT, ours) 套餐; deal 商机, won 赢单, lost 丢单; Linear issue and Shortcut story 事项; newsletter 新闻邮件; Activity 动态; For you 待你处理; learning 心得 (never 学习心得); setup code 设置码; payment card 银行卡; Sign out 退出登录; pair 配对. |
| ja | none | No gender or pronoun: say The Machine again or leave the subject out. Assistant: アシスタント. |
| ko | none | No gender or pronoun: say The Machine again or leave the subject out. Assistant: 어시스턴트. |
| ru | feminine | она, её, and feminine agreement (готова, подключена, сама), after машина: "The Machine прочитала почту. Она ...". Never он or его for it. Speaking for itself: "Я застряла". Assistant: ассистентка, ваша ассистентка. |

`tests/test_i18n.py` checks the forms that are always wrong (a masculine article before Machine or assistant, a
masculine "I" in French, Spanish and Italian); the rest is for the translator to keep.

## Names

Product and brand names stay exactly as they are in every language, and the check requires them verbatim:

The Machine, Machine (an owner's own Machine: "your Machine"), The Machine Network, Network, Graph, Fleet, Telegram,
Gmail, Google, Outlook, Microsoft, Slack, WhatsApp, LinkedIn, Intercom, Zoom, Stripe, GitHub, Salesflare, OpenClaw,
ClawHub, Claude, Claude Code, Codex, ChatGPT, Trello, Shortcut, Granola, Tailscale, GPT-6.2 Sol.

## Terms

| English | nl | fr | de | es | it | pt-BR | zh-CN | ja | ko | ru |
|---|---|---|---|---| --- | --- | --- | --- | --- | --- |
| to-do | to-do, to-do's | tâche, tâches | Aufgabe, Aufgaben | tarea, tareas | attività | tarefa, tarefas | 待办 | ToDo | 할 일 | задача, задачи, задачу, задач, задаче, задачей, задачам, задачами, задачах |
| snooze | snooze, snoozen, gesnoozed | mettre en attente, en attente, attente | zurückstellen, zurückgestellt, Zurückstellen | posponer, pospuesto, pospuesta, pospón | posticipa, posticipare, posticipata, posticipato, posticipate, posticipati, posticipo, posticipi | adiar, adiada, adiado, adiadas, adiados, adie, adia | 稍后处理, 推迟 | スヌーズ | 미루기, 미루, 미뤄, 미룬, 미룸, 미뤘 | отложить, отложено, отложена, отложен, отложены, отложите, отложенные, отложенных, отложенной, откладывать, отложи |
| hand off | overdragen, overdracht, draag over | transférer, transfert, transférez | übergeben, Übergabe, übergib | pasar, traspaso, pasa | passa, passare, passala, passalo, passaggio | passar, passe, repasse, repassar | 转交 | 引き継ぎ, 引き継ぐ, 引き継い, 引き継が | 넘기기, 넘기, 넘겨, 넘긴, 인계 | передать, передача, передайте, передачи, передачу, передано, передала, передаст, передавайте, передаче, передачей |
| handoff | overdracht, overdragen | transfert, transférer | Übergabe, übergeben | traspaso, pasar | passaggio, passare, passaggi | repasse, passar | 转交 | 引き継ぎ | 인계, 넘기기 | передача, передачи, передачу, передать, передаче, передачей |
| Ready | Klaargezet, klaar | Prêt, Prête, Prêts | Bereit | Para revisar, Listo, Lista, Listos | Pronto, Pronta, Pronti, Pronte | Para revisar, Pronto, Pronta, Prontos, Prontas | 已备好, 备好 | 準備完了, 準備済み, 準備でき | 준비됨, 준비 완료, 준비되 | Подготовлено, Подготовлена, Подготовлен, Подготовлены, Готово к, Готова к, Готовы к |
| To decide | Te beslissen | À décider | Zu entscheiden | Por decidir | Da decidere | A decidir | 待决定 | 判断待ち | 결정 필요 | Решить |
| Not needed | Niet nodig | Pas nécessaire | Nicht nötig | No hace falta | Non serve | Não precisa | 不需要 | 不要 | 필요 없음 | Не нужно |
| signal | signaal, signalen | signal, signaux | Signal, Signale | señal, señales | segnale, segnali | sinal, sinais | 信号 | シグナル | 신호 | сигнал, сигналы, сигнала, сигналов, сигналу, сигналам, сигналами, сигналах, сигнале, сигналом |
| draft | concept, concepten | brouillon, brouillons | Entwurf, Entwürfe | borrador, borradores | bozza, bozze | rascunho, rascunhos | 草稿 | 下書き | 초안 | черновик, черновики, черновика, черновиков, черновику, черновике, черновиком, черновикам, черновиками, черновиках |
| skill | skill, skills | compétence, compétences | Skill, Skills | habilidad, habilidades | skill | habilidade, habilidades | 技能 | スキル | 스킬 | навык, навыки, навыка, навыков, навыку, навыке, навыком, навыкам, навыками, навыках |
| Connections | Koppelingen | Connexions | Verbindungen | Conexiones | Connessioni | Conexões | 连接 | 接続 | 연결 | Подключения |
| Settings | Instellingen | Paramètres | Einstellungen | Ajustes | Impostazioni | Configurações | 设置 | 設定 | 설정 | Настройки |
| Suggestions | Suggesties | Suggestions | Vorschläge | Sugerencias | Suggerimenti | Sugestões | 建议 | 提案 | 제안 | Предложения |
| saved sign-in | opgeslagen login, opgeslagen logins | identifiant enregistré, identifiants enregistrés | gespeicherte Anmeldung, gespeicherte Anmeldungen, gespeicherten Anmeldungen | inicio de sesión guardado, inicios de sesión guardados | accesso salvato, accessi salvati | login salvo, logins salvos | 已保存的登录, 保存的登录 | 保存済みのログイン, 保存したログイン | 저장된 로그인 | сохранённый вход, сохранённые входы, сохранённого входа, сохранённых входов, сохранённым входом, сохраненный вход, сохраненные входы |
| work hours | werkuren | heures de travail | Arbeitszeiten | horario laboral | orario di lavoro | horário de trabalho | 工作时间 | 勤務時間 | 근무 시간 | рабочие часы, рабочих часов, рабочее время, рабочего времени, рабочим часам |
| digest | overzicht | récap | Zusammenfassung | resumen | riepilogo | resumo | 摘要 | ダイジェスト | 요약 | дайджест, дайджеста, дайджесты, дайджесте, дайджестом |
| promise | belofte, beloftes, beloofd | promesse, promesses, promis | Versprechen, versprochen | promesa, promesas, prometido, prometiste, prometió, prometieron | promessa, promesse, promesso, promessi | promessa, promessas, prometeu, prometido, prometi, prometeram | 承诺 | 約束 | 약속 | обещание, обещания, обещаний, обещанию, обещанием, обещаниях, обещаниям, обещал, обещала, обещали, обещано, обещании |
| learning | inzicht, inzichten, Leren | apprentissage, apprentissages | Erkenntnis, Erkenntnisse, Lernen | aprendizaje, aprendizajes | apprendimento, apprendimenti | aprendizado, aprendizados | 心得, 学习 | 学び, 学習 | 배운 점, 학습 | вывод, выводы, выводов, вывода, выводом, выводам, Обучение, обучения |
| error report | foutrapport, foutrapporten | rapport d’erreur, rapports d’erreur | Fehlerbericht, Fehlerberichte | informe de errores, informes de errores | segnalazione di errore, segnalazioni di errore | relatório de erro, relatórios de erro | 错误报告 | エラーレポート | 오류 보고서 | отчёт об ошибке, отчёты об ошибках, отчёта об ошибке, отчётов об ошибках, отчёт об ошибках, отчет об ошибке |
| routine | routine, routines | routine, routines | Routine, Routinen | rutina, rutinas | routine | rotina, rotinas | 例行程序 | ルーティン | 루틴 | сценарий, сценарии, сценария, сценариев, сценарию, сценарием, сценариям, сценариями, сценариях, сценарии |
| Stay in touch | Contact houden | Garder le contact | In Kontakt bleiben | Mantenerse en contacto | Restare in contatto | Manter contato | 保持联系 | 連絡を保つ | 연락 유지 | Оставаться на связи, Остаться на связи |

## Exceptions

English strings the check skips, with why:

- `Claude sends its result back through The Machine connector. Add it once in claude.ai, Settings, Connectors, Add custom connector:` names claude.ai's own menus, which read in English.
- `Zoom in` is the browser viewer's zoom button, not the Zoom app.
- `Zoom out` is the browser viewer's zoom button, not the Zoom app.
- `Signal chats` names the Signal app, not a signal.
- `Signal` names the Signal app, not a signal.
- `Signal message sent.` names the Signal app, not a signal.
- `Signal message sent at {}.` names the Signal app, not a signal.
- `Signal unlinked this Machine` names the Signal app, not a signal.
- `Update The Machine for Signal` names the Signal app, not a signal.
- `In Signal on your phone: Settings, Linked devices, Link new device. Then scan this code:` names the Signal app, not a signal.
- `Signal unlinked this Machine. Link it again to keep reading.` names the Signal app, not a signal.
- `Signal no longer accepts this Machine’s Signal client. Update The Machine.` names the Signal app, not a signal.
- `Signal gives a new linked device no older messages, so this reads from when you linked it.` names the Signal app, not a signal.
- `Send this Signal message?` names the Signal app, not a signal.
- `Sent to {} on Signal` names the Signal app, not a signal.
- `kind is fact (true about the world), draft (how a kind of task is done) or voice (how the owner writes on one channel, with channel)` names a tool's literal values, which stay in English.
- `when is "now", "digest" or a date/time like 2026-10-12 or 2026-10-12T09:00` names a tool's literal values, which stay in English.
- `the Signal message` names the Signal app, not a signal.
- `Signal message sent` names the Signal app, not a signal.
- `Signal message sent.` names the Signal app, not a signal.
- `Signal message sent at {}.` names the Signal app, not a signal.
- `Signal can’t be read right now, so I can’t find the chat. Put the message in the body and say in one line that they can send it on Signal themselves.` names the Signal app, not a signal.
- `Your Signal chats, as a linked device.` names the Signal app, not a signal.
- `Signal needs Java {} or later on this computer` names the Signal app, not a signal.
- `Unsupported Signal fields; plain text only, no media` names the Signal app, not a signal.
- `Use one of the owner’s Signal accounts` names the Signal app, not a signal.
- `Provide the concrete Signal message, at most {} characters` names the Signal app, not a signal.
- `Signal button labels must say Send, such as Send reply` names the Signal app, not a signal.
- `Only an owner-approved Signal message can use the Signal transport` names the Signal app, not a signal.
- `I couldn’t reach Signal on this computer. Nothing was sent; tap Send again.` names the Signal app, not a signal.
- `Signal no longer accepts this Machine’s Signal client. Nothing was sent.` names the Signal app, not a signal.
- `Signal is unlinked, or linked to another account. Nothing was sent.` names the Signal app, not a signal.
- `I couldn’t find that Signal chat. Nothing was sent.` names the Signal app, not a signal.
- `Signal was not linked{}` names the Signal app, not a signal.
- `Could not start the Signal link ({})` names the Signal app, not a signal.
- `Signal, any mailbox, any calendar` names the Signal app, not a signal.
- `WhatsApp, Telegram, Signal and other chats now look like the app they came from.` names the Signal app, not a signal.
- `Connect Signal chats, any mailbox over IMAP, and calendars from iCloud, Proton, Exchange or any CalDAV server.` names the Signal app, not a signal.

## Buttons and calls to action

Buttons: a button, link, menu item, tab, chip or status label is what a native app in that language would print there,
never the English verb carried over. The test: would a native speaker say it? "Get the phone app" takes the verb that
language's own apps use for it, not its word for "get", "obtain" or "fetch"; "Get help" asks for help. A section label
("For you") is the label a native app gives that section. Machine stays Machine and The Machine stays The Machine
(never machine, máquina, 机器); an owner's Machine is "your Machine" in the language's own way (je Machine, 내 Machine),
never The Machine. The table gives each language's verbs for starting and trying, and the literal ones to avoid.
`scripts/translate.py` sends this paragraph and the language's row with every request. The control plane's glossary
(cloud/i18n/glossary.md) has the same section for the site.

| Language | Rule |
|---|---|
| nl | Start: Start je Machine, Aan de slag. Try: Probeer, Bekijk. Never Haal je, Krijg, Verkrijg on a button or for a feature ("Ontvang je to-do's", not "Krijg je to-do's"). Buttons are an infinitive (Opslaan, Hulp vragen) or a short je-imperative. |
| fr | Start: Lancer votre Machine, Commencer. Try: Essayer, Découvrir. Never Obtenir for an app, a sign-up or help (Contacter le support, Télécharger l’app). Buttons are an infinitive (Enregistrer, Essayer). |
| de | Start: Hol dir deine Machine, Loslegen. Try: Ausprobieren, Ansehen. Never Bekommen or Erhalten on a button (Hilfe holen, Support kontaktieren). Buttons are an infinitive or a short du-imperative. |
| es | Start: Consigue tu Machine, Empieza. Try: Prueba, Descubre. Never Obtener on a button (Pedir ayuda, Descargar la app). Spanish from Spain: ordenador (never computadora or equipo), móvil, vosotros for a group (never ustedes), presupuesto (never cotización). Email is correo (never email); an OK that approves is visto bueno. Fleet is masculine: el Fleet, tu Fleet de trabajo, el Fleet familiar (never Work Fleet or Family Fleet in English); the Network is la Network; Team Graph is Graph del equipo. A bold label in a help article is copied exactly from the app catalog. |
| it | Start: Attiva la tua Machine, Inizia. Try: Prova, Scopri. Never Prendi or Ottieni on a button (Chiedi aiuto, Scarica l’app). |
| pt-BR | Start: Quero minha Machine, Começar. Try: Experimente, Conheça. Never Obter or Pegue on a button (Pedir ajuda, Baixar o app). |
| zh-CN | Start: 开通你的Machine, 开始使用. Try: 试用, 查看. Never 获取 for an app or a sign-up (获取验证码 for a code is fine; 下载手机应用 for the app). Labels are short: 查看, not 查看它们. |
| ja | Start: Machineを始める, 始める. Try: 試す, 見る. Never 入手 or 取得 for an app or a sign-up (アプリをダウンロード). No あなた and no それら: 確認する, not それらを見る. |
| ko | Start: Machine 시작하기, 시작하기. Try: 사용해 보기, 보기. Never 받기 for an app or a sign-up (앱 다운로드). An owner's Machine is 내 Machine, never The Machine. |
| ru | Start: Создать свою Machine, Начать. Try: Попробовать, Посмотреть. Never Получить for an app or a sign-up (Скачать приложение). Buttons are an infinitive (Начать, Сохранить). |

## Not checked, but use these

The user-facing name is *to-do* (decided 2026-10-26): Dutch keeps "to-do", the others use their own word, the same one every time.

**For you** is the one list of open to-dos that wait on the owner (it replaced Ready for you and To decide). Each one's chip says **Prepared**, **Needs you** or **Preparing…** (there is no Preparing list any more, so a to-do never moves while it prepares), and the help pages use the same words: For you is Voor jou, Pour vous, Für dich, Para ti, Per te, Para você; Prepared is Klaargezet, Préparée, Vorbereitet, Preparada, Preparata, Preparada; Needs you is Wacht op jou, Vous attend, Braucht dich, Te necesita, Serve il tuo intervento, Precisa de você. In zh-CN, ja, ko, ru: For you is 待你处理, 確認待ち, 내 확인, Для вас; Prepared is 已备好, 準備済み, 준비됨, Подготовлено; Needs you is 需要你, 対応が必要, 확인 필요, Ждёт вас; Preparing… is 准备中…, 準備中…, 준비 중…, Готовится….

The sidebar pages (renamed 2026-11-01): Suggestions is now *To-dos* (the plural of to-do, as above), Feedback is now *Learning* (the page; in nl and de "Leren" and "Lernen", while one learning stays inzicht and Erkenntnis), and the Events search is *Messages*. Learning: Leren, Apprentissage, Lernen, Aprendizaje, Apprendimento, Aprendizado. Messages: Berichten, Messages, Nachrichten, Mensajes, Messaggi, Mensagens. In zh-CN, ja, ko, ru: To-dos is 待办, ToDo, 할 일, Задачи; Learning is 心得, 学び, 배운 점, Обучение; Messages is 消息, メッセージ, 메시지, Сообщения.

| English | nl | fr | de | es | it | pt-BR | zh-CN | ja | ko | ru |
|---|---|---|---|---| --- | --- | --- | --- | --- | --- |
| Done (a to-do) | Gedaan | Fait | Erledigt | Hecho | Fatto | Feito | 已完成 | 完了 | 완료 | Готово |
| Due (a to-do's date) | Deadline (never "Te doen": that means to do) | Échéance | Fällig | Vence | Scadenza | Vence, Prazo | 截止 | 期限 | 마감 | Срок |
| Do it | Doe het | Faire | Ausführen | Hazlo | Fallo | Fazer | 执行 | 実行 | 실행 | Выполнить |
| Ask for changes (one name for redoing a to-do, with or without a draft; never "Change how" or "Change") | Wijzigingen vragen | Demander des modifications | Änderungen anfragen | Pedir cambios | Chiedi modifiche | Pedir mudanças | 要求修改 | 修正を依頼 | 수정 요청 | Попросить изменить |
| Not happening (a promise the owner lets go of; was Drop, which read like Mark done) | Gaat niet door | N’aura pas lieu | Findet nicht statt | No va a pasar | Non succederà | Não vai acontecer | 不会发生 | 実現しない | 진행 안 함 | Не состоится |
| Nudge (a short follow-up on someone else's promise) | Herinneren | Relancer | Erinnern | Recordar | Sollecita | Lembrar | 提醒 | リマインド | 알림 보내기 | Напомнить |
| Dismiss (a tip or suggestion The Machine raised, never a to-do: that is Not needed) | Afwijzen | Écarter | Verwerfen | Descartar | Scarta | Descartar | 忽略 | 却下 | 무시 | Отклонить |
| task, Tasks (when it means a to-do: "All tasks", "View task") | to-do, To-do's | tâche, Tâches | Aufgabe, Aufgaben | tarea, Tareas | attività, Attività | tarefa, Tarefas | 待办, 待办 | ToDo, ToDo | 할 일, 할 일 | задача, Задачи |
| task (an agent's job: "your agent can use it in any task") | taak | tâche | Aufgabe | tarea | compito | tarefa | 任务 | タスク | 작업 | задание |
| task page (the shared page for someone outside) | taakpagina | page de tâche | Aufgabenseite | página de tarea | pagina attività | página de tarefa | 待办页面 | ToDoページ | 할 일 페이지 | страница задачи |
| Close / Regular / Occasional / Faint (closeness) | Hecht / Regelmatig / Af en toe / Zwak | Proche / Régulier / Occasionnel / Faible | Eng / Regelmäßig / Gelegentlich / Schwach | Cercano / Habitual / Ocasional / Débil | Stretto / Regolare / Occasionale / Debole | Próximo / Regular / Ocasional / Fraco | 密切 / 常联系 / 偶尔 / 疏远 | 親しい / 定期的 / ときどき / 疎遠 | 가까움 / 정기적 / 가끔 / 드묾 | Близкий / Регулярный / Изредка / Слабый |
| Only about (a sharing limit) | Alleen over | Seulement à propos de | Nur über | Solo sobre | Solo su | Só sobre | 仅关于 | 次のみ | 다음만 | Только о |
| Previous / Next (week, month, days) | one whole string per step ("Vorige week"), never "Previous {}": the word agrees with the noun | | | | | |  |  |  |  |
| Work / Personal | Werk / Privé | Travail / Perso | Arbeit / Privat | Trabajo / Personal | Lavoro / Personale | Trabalho / Pessoal | 工作 / 个人 | 仕事 / 個人 | 업무 / 개인 | Работа / Личное |
| People / Organizations / Projects | Personen / Organisaties / Projecten | Personnes / Organisations / Projets | Personen / Organisationen / Projekte | Personas / Organizaciones / Proyectos | Persone / Organizzazioni / Progetti | Pessoas / Organizações / Projetos | 人员 / 组织 / 项目 | 人物 / 組織 / プロジェクト | 사람 / 조직 / 프로젝트 | Люди / Организации / Проекты |
| Note, Notes (a page of its own in the Graph, next to People; not meeting notes or the Notes field on a record) | Notitie, Notities | Note, Notes | Notiz, Notizen | Nota, Notas | Nota, Note | Nota, Notas | 笔记 | メモ | 메모 | Заметка, Заметки |
| Linked from (the notes that link to a page) | Gelinkt vanuit | Lié depuis | Verlinkt von | Enlazado desde | Collegato da | Vinculado de | 链接自 | リンク元 | 링크한 곳 | Ссылаются |
| Trip, Trips (a dated note The Machine fills in from booking mail) | Reis, Reizen | Voyage, Voyages | Reise, Reisen | Viaje, Viajes | Viaggio, Viaggi | Viagem, Viagens | 行程 | 旅行 | 여행 | Поездка, Поездки |
| Event, Events (a dated note The Machine fills in from ticket mail: a concert, a match, a conference; not a calendar event) | Evenement, Evenementen | Événement, Événements | Veranstaltung, Veranstaltungen | Evento, Eventos | Evento, Eventi | Evento, Eventos | 活动 | イベント | 이벤트 | Мероприятие, Мероприятия |
| Home (the notes about the owner's own home: its bills, appliances and upkeep; not the app's home page) | Thuis | Maison | Zuhause | Hogar | Casa | Casa | 家 | 自宅 | 집 | Дом |
| Health (the notes about the owner's own health: appointments, doctors, medicines) | Gezondheid | Santé | Gesundheit | Salud | Salute | Saúde | 健康 | 健康 | 건강 | Здоровье |
| Kids (the notes about the owner's children: their school, activities and care) | Kinderen | Enfants | Kinder | Hijos | Figli | Filhos | 孩子 | 子ども | 아이 | Дети |
| board | bord | tableau | Board | tablero | bacheca | quadro | 看板 | ボード | 보드 | доска |
| chat | chat | chat | Chat | chat | chat | chat | 聊天 | チャット | 채팅 | чат |
| Careful / Standard (security) | Voorzichtig / Standaard | Prudent / Standard | Vorsichtig / Standard | Prudente / Estándar | Prudente / Standard | Cuidadoso / Padrão | 谨慎 / 标准 | 慎重 / 標準 | 신중 / 표준 | Осторожно / Стандарт |
| Fleet rules | Fleet-regels | règles Fleet | Fleet-Regeln | reglas de Fleet | regole Fleet | regras do Fleet | Fleet 规则 | Fleet のルール | Fleet 규칙 | правила Fleet |
| sign in / sign out | inloggen / uitloggen | se connecter / se déconnecter | anmelden / abmelden | iniciar sesión / cerrar sesión | accedi / esci | entrar / sair | 登录 / 退出登录 | ログイン / ログアウト | 로그인 / 로그아웃 | войти / выйти |
| thinking (a model's level) | denkwerk | réflexion | Nachdenken | razonamiento | ragionamento | raciocínio | 思考 | 思考 | 사고 | размышление |

## Open questions for the maintainer

- German *du* and French *vous*: right register for the customers?
- *skill*: kept in Dutch and German, translated in French and Spanish.
- *Learned from a task*: a skill The Machine wrote itself from a Do it task that went well; *task* as in to-do work, not a new term.
- Italian uses informal *tu*, like Apple, Google and Spotify in Italian. Keeps "skill" in English, like Dutch and German.
- Brazilian Portuguese uses *você*. Settings reads "Configurações" (Android and web apps); iOS says "Ajustes".
- Portuguese from Portugal (and plain pt) reads Brazilian Portuguese until it has its own catalog.
- Any Chinese (zh-TW, zh-HK, zh-Hant too) reads Simplified Chinese until there is a Traditional Chinese catalog.
- Russian uses *вы*, the usual register for an app; *ты* would read too familiar.
- *to-do*: Chinese 待办, Japanese ToDo (as written in Japanese apps), Korean 할 일, Russian задача.
