---
title: The Graph
area: graph
summary: De mensen, organisaties en projecten in je berichten, die zichzelf up-to-date houden.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 9052c679e45207f7
---
Je Machine maakt op basis van je berichten, meetings en beslissingen een overzicht van wie je spreekt en wat er speelt. Je hoeft niets in te stellen en alles blijft op je Machine.

- [Personen](people.md): iedereen met wie je contact hebt, met een samenvatting en tijdlijn voor elke persoon.
- [Organisaties](organizations.md): de bedrijven waar ze werken, met hun mensen en projecten.
- [Projecten](projects.md): wat er speelt, op borden met fases, zoals deals in een CRM.

## Vandaag bijgewerkt

Boven aan elke lijst staat een subtiele regel met wat je Machine vandaag heeft bijgewerkt, bijvoorbeeld **4 personen vandaag bijgewerkt**. Tik erop om te zien wie en wat er is veranderd. Tik op een naam om de pagina te openen, met **Recente wijzigingen** open. Een kleine stip markeert elke rij en tegel op het bord die vandaag is gewijzigd. Je ziet alleen wijzigingen die je Machine zelf heeft aangebracht, vanaf middernacht.

## Filteren en sorteren

Met **Filteren** naast de tabbladen beperk je de lijst. Elke lijst heeft eigen filters. Personen: hoe goed je iemand kent, laatste contact, organisatie, eigenaar, tag en **Heeft een open project**. Organisaties: branche, specialisatie, grootte, land, laatste contact, eigenaar, tag en **Heeft een open project**. Projecten: eigenaar, bord, fase, tag, organisatie, waarde, verwachte afsluitdatum en **Geen antwoord in 10+ dagen**.

De filters die je hebt gekozen, staan boven de lijst, met **Wissen**. Bij Projecten gebruiken de lijst en het bord hetzelfde filter. Op een telefoon openen filters in een paneel.

Met het sorteermenu sorteer je de lijst. Personen en Organisaties worden gesorteerd op hoe goed je iemand kent, nieuwste of oudste contact en naam. Organisaties kunnen ook op grootte worden gesorteerd. Projecten worden gesorteerd op laatste activiteit, naam, fase, **Waarde** en **Afsluitdatum**. Met **CSV downloaden** onder het sorteermenu sla je het tabblad dat je bekijkt op als spreadsheet.

## Velden en tags

Klik onder Velden bij een persoon, organisatie of project op een waarde om die te wijzigen: met **Opslaan** of Enter bewaar je de wijziging, met **Annuleren** of Escape laat je die staan zoals hij was, en met **Verwijderen** maak je het veld leeg.

Met **Velden beheren** (of **Veld toevoegen** als er nog geen velden zijn) voeg je velden toe of verwijder je ze voor alle records van dat type. Met **Nieuw veld** voeg je een veld toe: tekst, getal, datum of een keuze uit een lijst.

Met **+ Tag** voeg je een tag toe, zoals VIP of partner. Met **×** verwijder je een tag. Tags staan in de lijsten (op een telefoon staan de tags van een persoon op diens pagina) en met **Filteren** kun je ze vinden.

## Verjaardag

De verjaardag van een persoon staat onder Contact, samen met de bron: het Google-contact, een verjaardag in Google Agenda (de routine Verjaardagen slaat die op voor een contact dat je goed kent), een Facebook-import, je notities of jijzelf. Met **Bewerken** stel je de verjaardag in of corrigeer je die: een maand en dag, en het jaar als je dat weet. Dan wordt ook de leeftijd getoond.

Jouw versie heeft voorrang op alle bronnen en blijft staan. Met **Verwijderen** haal je de verjaardag weg. Een contact of import voegt hem niet opnieuw toe.

Als er nog geen verjaardag is, voeg je die met **Verjaardag toevoegen** onder Velden toe. De routine Verjaardagen leest dezelfde verjaardag als de pagina. Een verjaardag is persoonlijk: hij wordt nooit met je team gedeeld, ook niet bij een gedeeld record.

## Een spreadsheet importeren

Met **CSV importeren…** onder het sorteermenu bij Personen, Organisaties of Projecten voeg je een spreadsheet toe die is opgeslagen als CSV.

1. Controleer de kolommen. Je Machine raadt op basis van de kopteksten en inhoud aan wat elke kolom bevat. Je kunt die indeling aanpassen. Als je model kan draaien, controleert het de kolommen ook en geeft het een korte reden als het ergens niet zeker van is. Het model ziet alleen de kopteksten, een paar waarden per kolom en de cellen die de regels niet konden lezen.
2. Controleer de aanpassingen. Met **Nakijken** bekijk je ze als voor en na: extra spaties, namen in hoofdletters, telefoonnummers in internationaal formaat, typefouten in e-mailadressen (gmial.com), websites als domein, datums en waarden in elk formaat ("€12k" is 12000), meerdere tags in één cel, een anders gespelde fase en dubbele rijen. Haal het vinkje bij een type of rij weg om die ongewijzigd te laten.
3. Controleer het voorbeeld. Elke rij is nieuw, komt overeen met een bestaand item in je Graph of wordt overgeslagen, met uitleg waarom. Een persoon wordt herkend aan het e-mailadres (of anders aan de naam en organisatie), een organisatie aan de website of naam en een project aan de naam.
4. Met **Importeren** voeg je nieuwe items toe en vul je de overeenkomsten aan. Een lege cel verandert niets.

Met **Ongedaan maken** direct na het importeren, of **Laatste import ongedaan maken** onder het sorteermenu, maak je de laatste import ongedaan zolang die records sindsdien niet zijn gewijzigd. Als daarmee een latere correctie zou worden overschreven, krijg je in plaats daarvan te zien waarom dat niet kan. Het bestand blijft op je Machine.

## Eigenaar

In een Werk-Fleet heeft elke persoon, organisatie en elk project een eigenaar: **Eigenaar** onder Met jou op de pagina. Jij bent de eigenaar, tenzij je iemand uit je Werk-Fleet kiest. Met **Eigenaar** bij Filteren toon je alleen items waarvan jij eigenaar bent. Elke wijziging staat in de tijdlijn.

## Team

Met **Team** naast Van mij zie je wat je teamgenoten delen, met dezelfde tabbladen en hetzelfde sorteermenu. Met **Filteren** beperk je de lijst op wie iets heeft gedeeld, een organisatie (Personen) of status (Projecten). Wat je daar toevoegt, is van jou.

Werk voor klanten wordt gedeeld met de Machines van je teamgenoten, inclusief eigenaar, velden en tags. Wat zij toevoegen, staat ook op jouw Machine. Bij elke thread staat **Team** of **Alleen jij**. Zie [Team-Graph](team-graph.md).
