---
title: ChatGPT
area: connections
summary: Meld je aan met ChatGPT om The Machine op je ChatGPT-abonnement te gebruiken en je ChatGPT-skills te importeren.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
translated: fc97be60c0b68336
---
## Waarvoor het bedoeld is

Meld je aan met ChatGPT en The Machine leest en maakt concepten met ChatGPT, op je eigen ChatGPT-abonnement. The Machine heeft geen eigen AI: verzoeken gaan rechtstreeks naar OpenAI, via jouw account en onder hun voorwaarden.

## Aanmelden

Klik op een gehoste Machine op **Aanmelden met ChatGPT** op de installatiepagina en voer de code die daar wordt getoond in bij ChatGPT. Later uitgelogd? Klik op **Opnieuw verbinden met ChatGPT**.

Wijst OpenAI de code af? Open je [ChatGPT-beveiligingsinstellingen](https://chatgpt.com/settings/security), scrol naar beneden en zet de schakelaar "Aanmelden met een apparaatcode inschakelen voor Codex, Excel, PowerPoint en Word" aan. Voer de code daarna opnieuw in.

Zie je die schakelaar niet? Bij een werkaccount (Business, Enterprise of Edu) moet je ChatGPT-beheerder deze inschakelen via [Machtigingen en rollen](https://chatgpt.com/admin/permissions), onder "Codex en Work Local".

Voer op je eigen computer `openclaw models auth login` uit in een terminal.

## Gebruikslimieten

Een ChatGPT-abonnement heeft een limiet van 5 uur en een wekelijkse limiet. **Instellingen**, **Model** toont hoeveel je van elke limiet hebt gebruikt en wanneer die wordt gereset. Werk op de achtergrond wordt ruim voordat je een limiet bereikt gepauzeerd, zodat er ruimte blijft voor je eigen chats. Wanneer je een limiet bereikt, zie je bovenaan het dashboard wanneer die wordt gereset. Zie [Model](model.md).

## Je ChatGPT-skills importeren

Klik in **Instellingen** op **Skills**, klik op **Importeren**, kies **Van ChatGPT** en klik op **Zoek mijn skills**. Alleen de instructies ervan worden geïmporteerd. Zie [Skills](skills.md).

## Verwijderen

Kies een ander model op de installatiepagina (of meld je op je eigen computer op dezelfde manier aan bij een andere provider). Als je de toegang aan de kant van OpenAI wilt intrekken, meld je je af bij de sessie in je ChatGPT-beveiligingsinstellingen.
