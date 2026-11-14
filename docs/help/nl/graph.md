---
title: De Graph
area: graph
summary: De mensen, organisaties en projecten in je berichten, die zichzelf up-to-date houden.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 850a4e2905f54511
---
Je Machine brengt in kaart met wie je contact hebt en wat er speelt, op basis van je berichten, vergaderingen en besluiten. Je hoeft niets in te stellen en alles blijft op je Machine.

- [Mensen](people.md): iedereen met wie je contact hebt, met een samenvatting en tijdlijn voor elke persoon.
- [Organisaties](organizations.md): de bedrijven waar ze werken, met hun mensen en projecten.
- [Projecten](projects.md): wat er speelt, op borden met fases, zoals deals in een CRM.

## Vandaag bijgewerkt

Bovenaan elke lijst staat een subtiele melding met wat je Machine vandaag heeft bijgewerkt, zoals **Vandaag 4 mensen bijgewerkt**. Tik erop om te zien wie en wat er is veranderd. Als je op een naam tikt, opent de pagina met **Recente wijzigingen** geopend. Een kleine stip markeert elke rij en tegel op het bord die vandaag is gewijzigd. Alleen wijzigingen die je Machine zelf sinds middernacht heeft gemaakt, tellen mee.

## Filteren en sorteren

Met **Filteren**, naast de tabbladen, beperk je de lijst. Elke lijst heeft eigen filters. Mensen: hoe goed je iemand kent, laatste contact, organisatie, eigenaar, tag en **Heeft een open project**. Organisaties: branche, specialisme, grootte, land, laatste contact, eigenaar, tag en **Heeft een open project**. Projecten: eigenaar, bord, fase, tag, organisatie, waarde, verwachte afsluitdatum en **Geen antwoord in 10+ dagen**.

De filters die je hebt gekozen, staan boven de lijst, met **Wissen**. Bij Projecten gebruiken de lijst en het bord hetzelfde filter. Op je telefoon openen filters als een paneel.

Met het sorteermenu sorteer je de lijst. Mensen en Organisaties sorteer je op hoe goed je iemand kent, nieuwste of oudste contact en naam. Organisaties kun je ook op grootte sorteren. Projecten sorteer je op laatste activiteit, naam, fase, **Waarde** en **Afsluitdatum**. Met **CSV downloaden** onder het sorteermenu sla je het huidige tabblad op als spreadsheet.

## Velden en tags

Onder Velden op een pagina van een persoon, organisatie of project kun je op een waarde klikken om die te wijzigen: met **Opslaan** of Enter bewaar je de waarde, met **Annuleren** of Escape sluit je zonder wijzigingen af, en met **Verwijderen** maak je het veld leeg.

Met **Velden beheren** (of **Veld toevoegen** als er nog geen velden zijn) voeg je velden toe of verwijder je ze voor alle items van dat type. Met **Nieuw veld** voeg je een veld toe: tekst, getal, datum of een keuze uit een lijst.

Met **+ Tag** voeg je een tag toe, zoals VIP of partner. Met **×** verwijder je de tag. Tags staan in de lijsten en met **Filteren** kun je ze vinden.

## Verjaardag

De verjaardag van iemand staat onder Contact, met de bron erbij: het Google-contact, een verjaardag in Google Calendar (de routine Verjaardagen slaat die op voor een contact dat je goed kent), een Facebook-import, je notities of jijzelf. Met **Bewerken** stel je de verjaardag in of corrigeer je die: een maand en dag, en het jaar als je dat weet. Dan wordt ook de leeftijd weergegeven.

Jouw invoer heeft voorrang op alle bronnen en blijft staan. Met **Verwijderen** haal je de verjaardag weg. Een contact of import voegt die daarna niet opnieuw toe.

Als er nog geen verjaardag is, kun je die met **Verjaardag toevoegen** onder Velden toevoegen. De routine Verjaardagen leest dezelfde verjaardag die op de pagina staat. Een verjaardag is persoonlijk: die wordt nooit met je team gedeeld, ook niet bij een gedeeld item.

## Een spreadsheet importeren

Met **CSV importeren…** onder het sorteermenu bij Mensen, Organisaties of Projecten voeg je een spreadsheet toe die als CSV is opgeslagen.

1. Controleer de kolommen. Je Machine raadt op basis van de kopteksten en inhoud waar elke kolom voor dient. Je kunt dit aanpassen. Als je model kan worden uitgevoerd, controleert het de kolommen ook en geeft het een korte reden als het ergens niet zeker van is. Het ziet alleen de kopteksten, een paar waarden per kolom en de cellen die de regels niet konden lezen.
2. Controleer de correcties. **Nakijken** toont de oorspronkelijke en aangepaste waarden: extra spaties, namen in hoofdletters, telefoonnummers in internationaal formaat, tikfouten in e-mailadressen (gmial.com), websites als domein, datums en waarden in elk formaat ("€12k" is 12000), meerdere tags in één cel, een anders gespelde fase en dezelfde rij die twee keer voorkomt. Haal het vinkje bij een type of rij weg om die ongewijzigd te laten.
3. Controleer het voorbeeld. Elke rij is nieuw, komt overeen met een item in je Graph of wordt overgeslagen, met de reden erbij. Een persoon wordt herkend aan het e-mailadres (anders aan de naam en organisatie), een organisatie aan de website of naam en een project aan de naam.
4. Met **Importeren** voeg je de nieuwe items toe en vul je de overeenkomende items aan. Een lege cel verandert niets.

Met **Ongedaan maken** direct na de import, of met **Laatste import ongedaan maken** onder het sorteermenu, draai je de laatste import terug zolang die items sindsdien niet zijn gewijzigd. Als hierdoor een latere correctie verloren zou gaan, krijg je in plaats daarvan de reden te zien. Het bestand blijft op je Machine.

## Eigenaar

In een Work Fleet heeft elke persoon, organisatie en elk project een eigenaar: **Eigenaar** onder Met jou op de pagina. Dat ben jij, tenzij je iemand uit je Work Fleet kiest. Met **Eigenaar** bij Filteren toon je alleen je eigen items. Elke wijziging staat in de tijdlijn.

## Team

Met **Team**, naast Van mij, zie je wat je teamgenoten delen, met dezelfde tabbladen en hetzelfde sorteermenu. Met **Filteren** beperk je de lijst op wie het item heeft gedeeld, op organisatie (Mensen) of op status (Projecten). Wat je daar toevoegt, is van jou.

Werk voor klanten wordt gedeeld met de Machines van je teamgenoten, inclusief de eigenaar, velden en tags. Items van je teamgenoten worden ook in jouw Machine weergegeven. Bij elke thread staat **Team** of **Alleen jij**. Zie [Team Graph](team-graph.md).
