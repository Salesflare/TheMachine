---
title: ChatGPT
area: connections
summary: Log in met ChatGPT om je Machine op je ChatGPT-abonnement te laten draaien, en importeer je ChatGPT-skills.
covers: chatgpt
code: docs/models.md, docs/skills.md, skills.py
site: Sign in with ChatGPT, Reconnect ChatGPT
---
## Waarvoor het dient

ChatGPT is het model dat voor je leest en concepten schrijft, op je eigen ChatGPT-abonnement. The Machine heeft geen eigen AI. De verzoeken van je Machine gaan rechtstreeks naar OpenAI, onder jouw account en hun voorwaarden.

## Inloggen

Druk op een gehoste Machine op je setuppagina op **Inloggen met ChatGPT** en typ de code die je ziet in bij ChatGPT. Later uitgelogd? Druk op **ChatGPT opnieuw koppelen**.

Weigert OpenAI de code? Open je [beveiligingsinstellingen van ChatGPT](https://chatgpt.com/settings/security), scrol naar beneden en zet de schakelaar "Enable device code sign-in for Codex, Excel, PowerPoint, and Word" aan. Vul de code dan opnieuw in.

Staat die er niet? Bij een werkaccount (Business, Enterprise of Edu) zet een beheerder van de workspace hem aan in [Permissions & roles](https://chatgpt.com/admin/permissions), onder "Codex and Work Local". Eén schakelaar geldt voor beide codes: werkte de code voor je model, dan werkt die voor Codex ook.

Log op je eigen computer OpenClaw in bij ChatGPT met `openclaw models auth login`.

## Gebruikslimieten

Een ChatGPT-abonnement heeft een 5-uurslimiet en een weeklimiet. **Instellingen**, dan **Model**, toont hoeveel van elke limiet gebruikt is en wanneer die weer vrijkomt. Werk op de achtergrond stopt ruim voor een limiet, zodat er ruimte blijft voor je eigen chats. Als een limiet bereikt is, staat bovenaan het dashboard welke en wanneer die weer vrijkomt, en daarna gaat het werk verder. Zie [Model](model.md).

## Je ChatGPT-skills importeren

Druk in **Instellingen**, **Skills** op **Importeren**, kies **Van ChatGPT** en druk op **Zoek mijn skills**. Hij leest de skills die je gemaakt hebt, in de browser van je Machine. Alleen instructies komen binnen. Zie [Skills](skills.md).

## Verwijderen

Kies een ander model op je setuppagina, of log OpenClaw in bij een andere provider. Om de toegang aan de kant van OpenAI te beëindigen, log je de sessie uit in je beveiligingsinstellingen van ChatGPT.
