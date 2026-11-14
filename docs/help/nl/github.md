---
title: GitHub
area: connections
summary: Bekijk reviewverzoeken, vermeldingen, toewijzingen en mislukte CI-runs. Issues worden alleen aangemaakt als je dit bevestigt.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
translated: e97127e156e56f7d
---
## Wat hij leest

Je GitHub-meldingen: reviewverzoeken, vermeldingen, toewijzingen, reacties en mislukte CI-runs. Hij markeert ze nooit als gelezen.

## Wat hij kan doen

Lezen verandert niets op GitHub. Eindigt een to-do met een GitHub-stap, zoals het aanmaken van een issue, dan staat dat in de to-do. De stap wordt pas uitgevoerd nadat je op **Bevestigen** tikt, of als je daar in de chat precies om hebt gevraagd. Screenshots worden via de browser van je Machine toegevoegd. Als GitHub niet is gekoppeld, staat in de to-do dat hij de browser gebruikt en zie je **GitHub koppelen**.

## Koppelen

Op een gehoste Machine:

1. Open **Koppelingen**, ga naar **Projecten en code** en kies GitHub.
2. Kies **Werk** of **Privé** en tik op **Inloggen met GitHub**.
3. Tik op **GitHub openen ↗**, voer de code in die je ziet en geef toestemming. De koppeling wordt automatisch gemaakt.

Op je instelpagina op app.themachine.computer/setup vind je dezelfde inlogoptie onder **Meer bronnen**.

Op je eigen computer:

1. Open **Koppelingen**, ga naar **Projecten en code** en kies GitHub.
2. Kies **Werk** voor je bedrijf of **Privé**, en tik op **Verbinden**.
3. Tik als dat wordt gevraagd op **GitHub openen ↗**, voer de code in en geef toestemming. De koppeling wordt automatisch gemaakt.

Of voer `assistant connect github` uit en bevestig je GitHub-aanmelding.

## Verwijderen

- Open **Koppelingen**, kies GitHub, tik op **Details** en daarna op **Ontkoppelen**. Hij leest dan niets meer. Wat hij al heeft opgehaald, blijft staan.
- Op een gehoste Machine kun je ook op **Verwijderen** tikken naast GitHub op je instelpagina.

## Verwijderen op GitHub

Open op GitHub **Instellingen**, **Toepassingen**, **Geautoriseerde OAuth-apps** en trek de toestemming voor GitHub CLI in. Op je eigen computer wordt je met `gh auth logout` ook afgemeld.
