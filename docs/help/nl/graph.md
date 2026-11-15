---
title: Graph
area: graph
summary: De mensen, organisaties en projecten in je berichten, die zichzelf up-to-date houden.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: e437109f98725e65
---
Je Machine maakt op basis van je berichten, vergaderingen en besluiten een overzicht van met wie je contact hebt en wat er speelt. Je hoeft niets in te stellen en alles blijft op je Machine.

- [Mensen](people.md): iedereen met wie je contact hebt, met een samenvatting en tijdlijn voor iedereen.
- [Organisaties](organizations.md): de bedrijven waar ze werken, met hun mensen en projecten.
- [Projecten](projects.md): wat er speelt, op borden met fases, zoals deals in een CRM.
- [Notities](notes.md): één overzichtelijke pagina per onderwerp, zoals een reis of je Thuis.

## Vandaag bijgewerkt

Boven aan elke lijst staat een subtiele regel met wat je Machine vandaag heeft bijgewerkt, zoals **Vandaag 4 mensen bijgewerkt**. Tik erop om te zien wie en wat er is veranderd. Als je een naam opent, kom je op de pagina met **Recente wijzigingen** geopend. Een kleine stip markeert elke rij en tegel op een bord die vandaag is gewijzigd. Alleen wijzigingen die je Machine zelf heeft aangebracht, vanaf middernacht, tellen mee.

## Filteren en sorteren

Met **Filteren** naast de tabbladen beperk je de lijst. Elke lijst heeft eigen filters. Mensen: contactfrequentie, laatste contact, organisatie, eigenaar, tag en **Heeft een open project**. Organisaties: branche, specialisatie, grootte, land, laatste contact, eigenaar, tag en **Heeft een open project**. Projecten: eigenaar, bord, fase, tag, organisatie, waarde, verwachte afsluitdatum en **Geen antwoord in 10+ dagen**.

De filters die je hebt gekozen, staan boven de lijst, met **Wissen**. Bij Projecten gebruiken de lijst en het bord hetzelfde filter. Op je telefoon openen de filters in een paneel.

Met het sorteermenu sorteer je de lijst. Mensen en Organisaties worden gesorteerd op contactfrequentie, nieuwste of oudste contact en naam. Organisaties kun je ook op grootte sorteren. Projecten worden gesorteerd op laatste activiteit, naam, fase, **Waarde** en **Afsluitdatum**. Met **CSV downloaden** onder het sorteermenu sla je het tabblad dat je bekijkt op als spreadsheet.

## Velden en tags

Klik onder Velden op de pagina van een persoon, organisatie of project op een waarde om die te wijzigen. Met **Opslaan** of Enter bewaar je de wijziging. Met **Annuleren** of Escape verlaat je het veld. Met **Verwijderen** maak je het veld leeg.

Met **Velden beheren** (of **Veld toevoegen** als er nog geen velden zijn) voeg je velden toe of verwijder je ze voor alle gegevens van dat type. Met **Nieuw veld** voeg je een veld toe: tekst, getal, datum of een keuze uit een lijst.

Met **+ Tag** voeg je een tag toe, zoals VIP of partner. Met **×** verwijder je die. Tags staan in de lijsten en je kunt ze vinden met **Filteren**.

## Verjaardag

De verjaardag van iemand staat onder Contact, met de bron erbij: diens Google-contact, een verjaardag in Google Calendar (de routine Verjaardagen slaat die op voor een contact dat je goed kent), een Facebook-import, je notities of jijzelf. Met **Bewerken** stel je de verjaardag in of corrigeer je die: de maand en dag, en het jaar als je dat weet. Als je het jaar invult, wordt ook de leeftijd getoond.

De verjaardag die je zelf invoert, gaat altijd voor en blijft staan. Met **Verwijderen** haal je die weg. Een contact of import voegt de verjaardag daarna niet opnieuw toe.

Als er nog geen verjaardag is, voeg je die met **Verjaardag toevoegen** toe onder Velden. De routine Verjaardagen leest dezelfde verjaardag die op de pagina staat. Een verjaardag is privé: die wordt nooit met je team gedeeld, ook niet bij een gedeeld record.

## Een spreadsheet importeren

Met **CSV importeren…** onder het sorteermenu van Mensen, Organisaties of Projecten voeg je een spreadsheet toe die als CSV is opgeslagen.

1. Controleer de kolommen. Je Machine raadt aan de hand van de koppen en de inhoud waarvoor elke kolom is. Je kunt dit aanpassen. Als je model kan worden uitgevoerd, controleert het de kolommen ook en geeft het een korte uitleg als het ergens niet zeker van is. Het ziet alleen de koppen, enkele waarden per kolom en de cellen die de regels niet konden lezen.
2. Controleer de aanpassingen. **Nakijken** toont ze als voor en na: extra spaties, namen in hoofdletters, telefoonnummers in internationale notatie, typefouten in e-mailadressen (gmial.com), websites als domeinnaam, datums en waarden in elk formaat ("€12k" is 12000), meerdere tags in één cel, een anders gespelde fase en dubbele rijen. Haal het vinkje weg bij een type of rij om die ongewijzigd te laten.
3. Controleer het voorbeeld. Elke rij wordt toegevoegd, komt overeen met een bestaand item in je Graph of wordt overgeslagen, met uitleg waarom. Een persoon wordt herkend aan het e-mailadres (of anders aan de naam en organisatie), een organisatie aan de website of naam en een project aan de naam.
4. Met **Importeren** voeg je de nieuwe items toe en vul je de overeenkomsten aan. Een lege cel brengt niets teweeg.

Met **Ongedaan maken** direct na het importeren of **Laatste import ongedaan maken** onder het sorteermenu draai je de laatste import terug, zolang die records sindsdien niet zijn gewijzigd. Als daarmee een latere correctie zou worden overschreven, krijg je in plaats daarvan te zien waarom dat niet kan. Het bestand blijft op je Machine staan.

## Eigenaar

In een Work Fleet heeft elke persoon, organisatie en elk project een eigenaar. Die staat onder Met jou op de pagina, bij **Eigenaar**. Jij bent de eigenaar, tenzij je iemand uit je Work Fleet kiest. Met **Eigenaar** bij Filteren toon je alleen je eigen items. Elke wijziging staat in de tijdlijn.

## Team

Met **Team** naast Mijn zie je wat je teamgenoten delen, met dezelfde tabbladen en hetzelfde sorteermenu. Met **Filteren** beperk je de lijst op wie iets heeft gedeeld, een organisatie (Mensen) of status (Projecten). Wat je daar toevoegt, is van jou.

Werk voor klanten wordt gedeeld met de Machines van je teamgenoten, inclusief de eigenaar, velden en tags. Wat zij delen, verschijnt ook bij jou. Bij elke thread staat **Team** of **Alleen jij**. Bekijk [Team Graph](team-graph.md).
