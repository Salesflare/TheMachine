---
title: Hulp vragen
area: troubleshooting
summary: Meld een bug via je dashboard, schrijf ons of geef ons team een dag toegang tot je Machine.
covers: support-bundle, support-access
code: support.py, cli.py, dashboard.html, fleet.py
site: Report a problem
order: 9
translated: 419a75e887b25e20
---
## Schrijf ons

Mail naar support@themachine.computer. Iemand antwoordt.

Bij een gehoste Machine staat onderaan het dashboard ‘Er gaat iets mis?’. Daarmee open je het formulier **Een probleem melden** van je account.

## Een bug melden

Open **Help** en kies **Een bug melden**. Ook in een foutmelding staat de knop **Een bug melden**.

1. Beschrijf wat er misging.
2. Voeg een screenshot toe als dat helpt: **Screenshot maken** van het dashboard, of **Afbeelding toevoegen**.
3. Laat **Supportrapport meesturen** ingeschakeld als dat kan. Het voegt versies, controles en recente fouten toe, maar geen berichten, sleutels of adressen. Zo kan ons team 24 uur lang de logs en instellingen van je Machine bekijken. Zie [Toegang voor support](get-support.md#support-access). Als je het uitvinkt, worden alleen je beschrijving en screenshot verstuurd.
4. Tik op **Versturen**. Het formulier sluit meteen en het supportrapport wordt automatisch verstuurd.

Wij nemen het vanaf daar over. Een zelfgehoste Machine kan een rapport versturen zodra hij op de Network staat. Schrijf ons anders zelf.

Je kunt ook gewoon in de chat aan je Machine vertellen dat er iets mis is. Hij opent dan **Een bug melden** voor je, met jouw woorden en een korte samenvatting alvast ingevuld. Er wordt niets verstuurd tot je op **Versturen** tikt.

Zodra we een bug die je hebt gemeld oplossen en je Machine de oplossing uitvoert, laten we je dat één keer weten: met een korte melding op je dashboard en een korte e-mail. Een zelfgehoste Machine krijgt dit bericht zodra hij op de Network staat.

In de melding staat de vraag of het nu echt werkt. Tik op **Werkt nu**, of op **Nog niet goed** om te vertellen wat er nog niet klopt. Voeg een afbeelding toe als dat helpt. Je reactie wordt een nieuw rapport voor ons, gekoppeld aan het eerste. Met **×** sluit je de melding zonder te antwoorden.

Offline of meerdere rapporten achter elkaar verstuurd? Je rapport gaat niet verloren. Je Machine bewaart het en verstuurt het later automatisch. Tot die tijd staat het onder **Wacht op verzending**.

## Toegang voor support

Ons team kan je Machine voor je bekijken, maar alleen als je daar toestemming voor geeft. Als je een bug meldt met **Supportrapport meesturen** ingeschakeld, wordt de toegang ingeschakeld zodra je op **Versturen** drukt. Op je eigen computer moet je Machine [gekoppeld zijn aan je account](friends.md).

- Alleen-lezen: logs, instellingen, versies, hoe elke verbinding synchroniseert en recente fouten, opgeschoond zoals in het supportrapport. Nooit je berichten, sleutels, wachtwoorden of de identiteit van je contacten.
- De toegang eindigt automatisch na 24 uur. Zolang hij actief is, zie je dat onder **Instellingen**, **Beveiliging**. Met **Uitzetten** beëindig je de toegang meteen.
- Elke keer dat iemand je Machine bekijkt, staat in Instellingen onder **Activiteit**, met het tijdstip. Zie [Activiteit](activity.md).

## Vanaf je eigen computer

Voer `assistant support-bundle` uit. Er wordt een bestand opgeslagen met versies, de controles van `assistant doctor`, recente logs en je instellingen, zonder sleutels, tokens, wachtwoorden of adressen. Bekijk het bestand en stuur het daarna naar degene die je helpt.

Meld bugs in de open-source-app als issue op [GitHub](https://github.com/Salesflare/TheMachine/issues), en gebruik alleen verzonnen gegevens.
