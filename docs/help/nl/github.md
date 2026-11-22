---
title: GitHub
area: connections
summary: Bekijk reviewverzoeken, vermeldingen, toewijzingen en mislukte CI-runs. Issues worden alleen aangemaakt als je bevestigt.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
translated: e97127e156e56f7d
---
## Wat het leest

Je GitHub-meldingen: reviewverzoeken, vermeldingen, toewijzingen, reacties en mislukte CI-runs. Hij markeert ze nooit als gelezen.

## Wat het kan doen

Lezen verandert niets op GitHub. Eindigt een to-do met een GitHub-stap, zoals een issue aanmaken, dan vermeldt de to-do dat. De stap wordt pas uitgevoerd nadat je op **Bevestigen** tikt, of als je daar precies om hebt gevraagd in de chat. Screenshots worden toegevoegd via de browser van je Machine. Als GitHub niet is gekoppeld, vermeldt de to-do dat hij de browser gebruikt en toont hij **GitHub koppelen**.

## Koppelen

Op een gehoste Machine:

1. Open **Koppelingen**, ga naar **Projecten en code** en kies GitHub.
2. Kies **Werk** of **Privé** en klik op **Sign in with GitHub**.
3. Klik op **GitHub openen ↗**, voer de getoonde code in en geef toestemming. De koppeling wordt automatisch gemaakt.

Op je instelpagina op app.themachine.computer/setup vind je dezelfde aanmeldoptie onder **More sources**.

Op je eigen computer:

1. Open **Koppelingen**, ga naar **Projecten en code** en kies GitHub.
2. Kies **Werk** met je bedrijf, of **Privé**, en klik op **Verbinden**.
3. Klik indien gevraagd op **GitHub openen ↗**, voer de code in en geef toestemming. De koppeling wordt automatisch gemaakt.

Je kunt ook `assistant connect github` uitvoeren en je GitHub-aanmelding bevestigen.

## De koppeling verwijderen

- Open **Koppelingen**, ga naar GitHub en kies **Details** en **Ontkoppelen**. De koppeling stopt met lezen. Wat al is binnengehaald, blijft staan.
- Op een gehoste Machine kun je ook op je instelpagina op **Verwijderen** klikken naast GitHub.

## De installatie op GitHub ongedaan maken

Open op GitHub Instellingen, Applicaties, Geautoriseerde OAuth-apps en trek de toestemming voor GitHub CLI in. Op je eigen computer meld je je met `gh auth logout` ook af.
