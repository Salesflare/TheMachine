---
title: The Graph
area: graph
summary: De mensen, organisaties en projecten in je berichten, die vanzelf worden bijgewerkt.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 181ff5fa2a9d8f47
---
Je Machine brengt in kaart met wie je contact hebt en wat er speelt, op basis van je berichten, meetings en beslissingen. Je hoeft niets in te stellen en alles blijft op je Machine.

- [Personen](people.md): iedereen met wie je contact hebt, met een samenvatting en tijdlijn per persoon.
- [Organisaties](organizations.md): de bedrijven waar ze werken, met hun mensen en projecten.
- [Projecten](projects.md): wat er speelt, op borden met fases, zoals deals in een CRM.

Je eigen wijzigingen zijn meteen zichtbaar. Nieuwe mensen, nieuwe berichten op hun tijdlijn en opgezochte gegevens verschijnen binnen 30 minuten.

## Vandaag bijgewerkt

Bovenaan elke lijst staat een subtiele melding met wat je Machine vandaag heeft bijgewerkt, zoals **Vandaag 4 mensen bijgewerkt**. Klik erop om te zien wie en wat er is veranderd. Als je een naam aanklikt, wordt de pagina geopend met **Recente wijzigingen** in beeld. Een stip markeert elke rij en tegel op een bord die vandaag is gewijzigd. Alleen wijzigingen van je Machine vanaf middernacht tellen mee.

## Filteren en sorteren

Met **Filteren**, naast de tabbladen, beperk je de lijst. Elke lijst heeft eigen filters. Personen: contactfrequentie, laatste contact, organisatie, eigenaar, tag en **Heeft een open project**. Organisaties: branche, specialisme, grootte, land, laatste contact, eigenaar, tag en **Heeft een open project**. Projecten: eigenaar, bord, fase, tag, organisatie, waarde, verwachte afsluitdatum en **Geen antwoord in 10+ dagen**.

De filters die je hebt gekozen, staan boven de lijst, samen met **Wissen**. Bij Projecten geldt één filter voor zowel de lijst als het bord. Op een telefoon openen filters in een paneel.

Met het sorteermenu sorteer je de lijst. Personen en Organisaties worden gesorteerd op contactfrequentie, nieuwste of oudste contact en naam. Organisaties kunnen ook op grootte worden gesorteerd. Projecten worden gesorteerd op laatste activiteit, naam, fase, **Waarde** en **Afsluitdatum**. Met **CSV downloaden**, onder het sorteermenu, sla je het tabblad dat je bekijkt op als spreadsheet.

## Velden en tags

Klik onder Velden bij een persoon, organisatie of project op een waarde om die te wijzigen. Met **Opslaan** of Enter bewaar je de wijziging. Met **Annuleren** of Escape sluit je af zonder op te slaan. Met **Verwijderen** maak je het veld leeg.

Met **Velden beheren** (of **Veld toevoegen** als er nog geen velden zijn) voeg je velden toe aan of verwijder je ze voor alle items van dat type. Met **Nieuw veld** voeg je een veld toe: tekst, getal, datum of een keuze uit een lijst.

Met **+ Tag** voeg je een tag toe, zoals VIP of partner. Met **×** verwijder je die. Tags staan in de lijsten (op een telefoon staan de tags van een persoon op diens pagina) en met **Filteren** kun je ze vinden.

## Verjaardag

De verjaardag van een persoon staat onder Contact, met erbij waar die vandaan komt: het Google-contact, een verjaardag in Google Calendar (de routine Verjaardagen slaat die op voor een nauw contact), een Facebook-import, je notities of jijzelf. Met **Bewerken** stel je de verjaardag in of pas je die aan: een maand en dag, en het jaar als je dat weet (dan wordt ook de leeftijd getoond).

Wat je zelf invult, gaat altijd voor en blijft staan. Met **Verwijderen** verwijder je de verjaardag. Een contact of import voegt die daarna niet opnieuw toe.

Als er nog geen verjaardag is, kun je die met **Verjaardag toevoegen** onder Velden toevoegen. De routine Verjaardagen leest dezelfde verjaardag als op de pagina. Een verjaardag is persoonlijk en wordt nooit gedeeld met je team, ook niet bij een gedeeld item.

## Een spreadsheet importeren

Met **CSV importeren…**, onder het sorteermenu van Personen, Organisaties of Projecten, voeg je een spreadsheet toe die als CSV is opgeslagen.

1. Controleer de kolommen. Je Machine raadt aan de hand van de koppen en de inhoud waar elke kolom voor is. Je kunt dit aanpassen. Als je model beschikbaar is, controleert het de kolommen ook en geeft het een korte reden als het ergens niet zeker van is. Het model ziet alleen de koppen, een paar waarden per kolom en de cellen die de regels niet konden lezen.
2. Controleer de aanpassingen. **Nakijken** toont de oorspronkelijke en aangepaste gegevens: extra spaties, namen in hoofdletters, telefoonnummers in internationaal formaat, typefouten in e-mailadressen (gmial.com), websites als domein, datums en waarden in elk formaat ("€12k" wordt 12000), meerdere tags in één cel, een anders gespelde fase en dubbele rijen. Haal het vinkje bij een soort aanpassing of rij weg om die ongewijzigd te laten.
3. Controleer het voorbeeld. Elke rij is nieuw, komt overeen met een item in je Graph of wordt overgeslagen, met uitleg. Een persoon wordt gekoppeld op basis van e-mailadres (anders op naam en organisatie), een organisatie op basis van website of naam en een project op basis van naam.
4. Met **Importeren** voeg je nieuwe items toe en vul je bestaande items aan. Een lege cel verandert niets.

Met **Ongedaan maken** direct na het importeren, of **Laatste import ongedaan maken** onder het sorteermenu, draai je de laatste import terug zolang die items sindsdien niet zijn gewijzigd. Als dit een latere correctie zou overschrijven, krijg je in plaats daarvan te zien waarom dat niet kan. Het bestand blijft op je Machine.

## Eigenaar

In een Werk-Fleet heeft elke persoon, organisatie en elk project een eigenaar. Je vindt **Eigenaar** onder Bij jou op de pagina van het item. Jij bent de eigenaar, tenzij je iemand uit je Werk-Fleet kiest. Met **Eigenaar** in Filteren zie je alleen je eigen items. Elke wijziging verschijnt in de tijdlijn.

## Team

Met **Team**, naast Mijn items, bekijk je wat je teamgenoten delen, met dezelfde tabbladen en hetzelfde sorteermenu. Met **Filteren** beperk je de lijst op wie het item heeft gedeeld, een organisatie (Personen) of status (Projecten). Wat je daar toevoegt, is van jou.

Klantwerk wordt gedeeld met de Machine van elke teamgenoot, inclusief eigenaar, velden en tags. Wat zij delen, verschijnt op jouw Machine. Bij elk item staat **Team** of **Alleen jij**. Bekijk [Team-Graph](team-graph.md).
