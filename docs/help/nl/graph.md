---
title: De Graph
area: graph
summary: De mensen, organisaties en projecten in je berichten, die zichzelf up-to-date houden.
covers: tab:people
code: graph.py, graph_updates.py, crm.py, crm_import.py, crm_fixes.py, crm_fields.py, dashboard.html
order: 1
translated: 4dbe1a4e1702b1c1
---
Je Machine brengt in kaart met wie je contact hebt en wat er speelt, op basis van je berichten, vergaderingen en besluiten. Je hoeft niets in te stellen en alles blijft op je Machine.

- [Mensen](people.md): iedereen met wie je contact hebt, met een samenvatting en tijdlijn.
- [Organisaties](organizations.md): de bedrijven waar ze werken, met hun mensen en projecten.
- [Projecten](projects.md): wat er speelt, op borden met fasen, zoals deals in een CRM.

## Vandaag bijgewerkt

Bovenaan elke lijst staat een subtiele melding met wat je Machine vandaag heeft bijgewerkt, zoals **Vandaag 4 mensen bijgewerkt**. Tik erop om te zien wie en wat er is veranderd. Tik op een naam om de pagina te openen met **Recente wijzigingen** open. Een klein puntje markeert elke rij en elk bordtegel dat vandaag is gewijzigd. Het telt alleen wijzigingen die je Machine zelf heeft gemaakt, vanaf middernacht.

## Filteren en sorteren

Met **Filteren**, naast de tabbladen, beperk je de lijst. Elke lijst heeft eigen filters. Mensen: contactsterkte, laatste contact, organisatie, eigenaar, tag en **Heeft een open project**. Organisaties: branche, specialisme, grootte, land, laatste contact, eigenaar, tag en **Heeft een open project**. Projecten: eigenaar, bord, fase, tag, organisatie, waarde, verwachte afsluitdatum en **Geen antwoord in 10+ dagen**.

De filters die je hebt gekozen, staan boven de lijst, samen met **Wissen**. Bij Projecten gebruiken de lijst en het bord hetzelfde filter. Op een telefoon openen de filters in een paneel.

Met het sorteermenu sorteer je de lijst. Mensen en Organisaties worden gesorteerd op contactsterkte, nieuwste of oudste contact en naam. Organisaties kun je ook sorteren op grootte. Projecten kun je ook sorteren op **Waarde** en **Afsluitdatum**. Met **CSV downloaden** onder het sorteermenu sla je het tabblad dat je bekijkt op als spreadsheet.

## Velden en tags

Klik onder Velden bij een persoon, organisatie of project op een waarde om die te wijzigen. Met **Opslaan** of Enter sla je de waarde op. Met **Annuleren** of Escape sluit je af zonder op te slaan. Met **Verwijderen** maak je het veld leeg.

Met **Velden beheren** voeg je velden toe of verwijder je ze voor alle records van dat type. Met **Nieuw veld** voeg je een veld toe: tekst, getal, datum of een keuze uit een lijst.

Met **+ Tag** voeg je een tag toe, zoals VIP of partner. Met **×** verwijder je die. Tags staan in de lijsten en met **Filteren** kun je ze vinden.

## Verjaardag

De verjaardag van iemand staat onder Contact, met erbij waar de datum vandaan komt: het Google-contact, een verjaardag in Google Calendar (de routine Verjaardagen slaat die op voor een contact dat je goed kent), een Facebook-import of jijzelf. Met **Bewerken** stel je de datum in of pas je die aan: een maand en dag, en het jaar als je dat weet. Dan wordt ook de leeftijd weergegeven. Jouw invoer heeft voorrang op alle bronnen en blijft staan. Met **Verwijderen** haal je de datum weg. Een contact of import voegt die daarna niet opnieuw toe.

Als er nog geen verjaardag is, voeg je die met **Verjaardag toevoegen** toe onder Velden. De routine Verjaardagen gebruikt dezelfde verjaardag als op de pagina. Een verjaardag is persoonlijk: hij wordt nooit met je team gedeeld, ook niet bij een gedeeld record.

## Een spreadsheet importeren

Met **CSV importeren…** onder het sorteermenu bij Mensen, Organisaties of Projecten voeg je een spreadsheet toe die als CSV is opgeslagen.

1. Controleer de kolommen. Je Machine probeert op basis van de koppen en inhoud te bepalen wat elke kolom bevat. Je kunt dit aanpassen. Als je model beschikbaar is, controleert het de kolommen ook en geeft het een korte uitleg als het twijfelt. Het model ziet alleen de koppen, enkele waarden per kolom en de cellen die de regels niet konden lezen.
2. Controleer de aanpassingen. **Nakijken** toont de oude en nieuwe waarden: extra spaties, namen in hoofdletters, telefoonnummers in internationaal formaat, typefouten in e-mailadressen (gmial.com), websites als domeinnaam, datums en waarden in elk formaat ("€12k" is 12000), meerdere tags in één cel, een anders gespelde fase en dubbele rijen. Haal het vinkje bij een type of rij weg om die ongewijzigd te laten.
3. Controleer het voorbeeld. Elke rij is nieuw, komt overeen met een record in je Graph of wordt overgeslagen, met uitleg waarom. Een persoon wordt gematcht op e-mailadres (anders op naam en organisatie), een organisatie op website of naam en een project op naam.
4. Met **Importeren** voeg je de nieuwe records toe en vul je de bestaande matches aan. Een lege cel verandert niets.

Met **Ongedaan maken** direct na het importeren, of **Laatste import ongedaan maken** onder het sorteermenu, draai je de laatste import terug zolang die records sindsdien niet zijn gewijzigd. Als daardoor een latere correctie zou worden overschreven, krijg je in plaats daarvan uitleg waarom dat niet kan. Het bestand blijft op je Machine.

## Eigenaar

In een werk-Fleet heeft elke persoon, organisatie en elk project een eigenaar. Je vindt **Eigenaar** onder Met jou op de pagina. Jij bent de eigenaar, tenzij je iemand uit je werk-Fleet kiest. Met **Eigenaar** in Filteren toon je alleen je eigen records. Elke wijziging staat in de tijdlijn.

## Team

Met **Team** naast **Alleen jij** zie je wat je teamgenoten delen, met dezelfde tabbladen en hetzelfde sorteermenu. Met **Filteren** beperk je de lijst op wie iets heeft gedeeld, een organisatie (Mensen) of de status (Projecten). Wat je daar toevoegt, is van jou.

Werk voor klanten wordt gedeeld met de Machines van je teamgenoten, inclusief de eigenaar, velden en tags. Wat zij delen, verschijnt ook op die van jou. Bij elke thread staat **Team** of **Alleen jij**. Lees meer over [Team Graph](team-graph.md).
