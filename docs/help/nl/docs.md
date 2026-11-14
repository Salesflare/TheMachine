---
title: Microsoft OneDrive: Word-bestanden in OneDrive en SharePoint
area: connections
summary: Reacties, vermeldingen, bijgehouden wijzigingen en gedeelde bestanden in je Word-bestanden in OneDrive en SharePoint, plus nieuwe privédocumenten, en wijzigingen die je goedkeurt.
covers: connector:docs
code: connectors/docs.py, doc_writes.py, next_actions.py, onboarding.py
site: Sign in with Microsoft
---
## Wat het leest

De koppeling **Microsoft OneDrive** leest Word-bestanden in OneDrive en SharePoint. Je logt er apart voor in met Microsoft, met of zonder gekoppelde Outlook. Dat werkt op een gehoste Machine en op je eigen computer die aan je account gekoppeld is. Voor Google Docs, zie verderop. Het haalt binnen:

- Documenten die iemand met je deelt.
- Reacties en antwoorden op documenten van jou, en reacties die jou vermelden.
- Bijgehouden wijzigingen in Word-bestanden van jou.

De eerste sync kijkt 30 dagen terug. Elk item wordt een gebeurtenis, gekoppeld aan de personen en projecten in je [Graph](graph.md). Als een reactie jou nodig heeft, wordt ze een to-do.

## Wat het kan doen

Als een to-do de tekst van een document nodig heeft, leest je Machine dat ene document, en alleen terwijl hij aan die to-do werkt.

Hij kan een antwoord op een reactie schrijven. Bij Word-bestanden kan een antwoord niet van buiten Word geplaatst worden, dus het antwoord blijft een concept dat je zelf naar Word kopieert.

Hij aanvaardt nooit een suggestie, sluit nooit een reactie af, deelt nooit een bestand en wijzigt nooit een document zonder je OK.

Een documentenkoppeling kan alleen dingen doen: zet **Brengt signalen binnen** uit onder **Details**, dan zoekt en leest ze alleen de documenten die je to-do's nodig hebben, en maakt ze nieuwe. Een Google-koppeling zonder toegang tot heel Drive leest documenten via hun link, en de documenten die je Machine maakte.

## Documenten maken en bewerken

Je Machine kan een nieuw document schrijven, of een document aanpassen waar een van je to-do's over gaat:

- Een nieuw document maakt hij meteen, als de to-do of een skill zegt er een te maken: een privédocument in je eigen Google Drive of OneDrive, met niemand gedeeld. De to-do toont het met **Open het document**. Het delen, of de link naar iemand sturen, wacht op je OK.
- Een wijziging aan een bestaand document bereidt hij alleen voor, elke alinea voor en na. Tik op **Wijzigingen nakijken**, lees het en dan **Opslaan**. Een wijziging waar je in de chat van de to-do om vraagt, maakt hij meteen.
- Hij schrijft een wijziging één keer, en alleen in het document zoals je het zag. Heeft iemand het intussen aangepast, dan wordt er niets geschreven en zegt de to-do dat. Vraag dan een nieuw concept.
- In Talk leest hij de hele wijziging voor en wacht op een duidelijk ja.
- Weigert Google of Microsoft een nieuw document, dan zegt de to-do wat geweigerd werd en toont **Nakijken en maken** om het opnieuw te proberen.

Hij vervangt tekst, voegt tekst toe en voegt alinea's en koppen toe. Tabellen, afbeeldingen, bijgehouden wijzigingen en velden laat hij met rust. Een nieuw document komt in je Google Drive of OneDrive en blijft privé tot je het deelt.

Een nieuw document gaat naar een account in het eigen gebied van de taak: een document voor een Werk-taak naar het account van dat bedrijf, het account van het gesprek als dat kan, nooit naar een privé-account. Op je eigen computer kan ook een Google-account dat voor Gmail is aangemeld en al toegang tot Drive heeft een nieuw Google-document krijgen. Past geen enkel account, dan zegt de taak wat je voor Werk kunt koppelen: Microsoft OneDrive, of Google Docs waar je Machine het kan gebruiken.

Is het document niet het einde van de taak, zoals een antwoord met de link, dan blijft de taak open en maakt hij die volgende stap klaar voor je OK.

Microsoft OneDrive koppelen staat dit al toe: er is geen aparte stap. Een oudere koppeling van Microsoft OneDrive die alleen leest, toont **Bewerken toestaan** op haar kaart bij **Koppelingen**. Druk er één keer op en accepteer.

## Waar het om vraagt

Microsoft OneDrive vraagt Microsoft om één OK, los van je login voor mail: om je bestanden te lezen en te wijzigen, ook die met je gedeeld zijn in OneDrive en SharePoint. Elke wijziging wacht nog altijd op je OK in haar taak. Je toegang tot je mail en je agenda blijft zoals ze is. Zonder Outlook geldt de login alleen voor je bestanden, nooit voor je mail of agenda.

Wordt die OK later ingetrokken, dan zegt de kaart van Microsoft OneDrive **Wacht op je OK om documenten te lezen**.

## Koppelen

Je hebt er geen gekoppelde Outlook voor nodig.

- Gehoste Machine: open in het dashboard **Koppelingen**, **Documenten en bestanden**, kies **Microsoft OneDrive** en druk op **Inloggen met Microsoft**. Microsoft vraagt je om het lezen en bewerken van je bestanden toe te staan, daarna kom je terug in het dashboard.
- Je eigen computer, gekoppeld aan je account: open **Koppelingen**, **Documenten en bestanden**, kies **Microsoft OneDrive** en druk op **Inloggen met Microsoft**.

Hij controleert of de login documenten mag lezen. Zonder die OK wordt het niet toegevoegd. Druk je op **Bewerken toestaan** en staat Microsoft bewerken niet toe, dan zegt hij dat in plaats van Gekoppeld.

## Google Docs

Open op een gehoste Machine **Koppelingen**, dan **Documenten en bestanden**, en kies **Google Docs**. Google vraagt je om hem de documenten te laten zien en bewerken die je hem aanwijst, en nieuwe te laten maken. Gmail hoeft niet gekoppeld te zijn, en je Gmail-toegang verandert niet.

Daarna kan je Machine:

- Een Google-document lezen dat gelinkt is in de berichten van een taak, alleen terwijl hij aan die taak werkt.
- Wijzigingen aan dat document voorbereiden. Elke wijziging wacht op je OK, zoals hierboven.
- Nieuwe privédocumenten maken in je Google Drive.

Hij doorzoekt je Drive niet. Reacties, delen en suggesties ziet hij alleen bij documenten die hij zelf maakte. Meer zou toegang tot je hele Drive vragen, en daar vraagt hij niet om.

Op je eigen computer kan je Machine een nieuw Google-document maken in een Gmail-account dat daar is aangemeld en al toegang tot Drive heeft. Je andere Google Docs en hun reacties leest hij niet. **Documenten en bestanden** toont het als Google Docs, op dat account. Een document dat hij daar voor een to-do maakte, kan hij ook aanpassen.

## Werk of privé

Microsoft OneDrive volgt het label werk of privé van de koppeling, net als mail. Werkdocumenten kunnen in de Graph van je team terechtkomen volgens je [deelregels](sharing-rules.md). Privédocumenten nooit.

## Verwijderen

In het dashboard: **Koppelingen**, open Microsoft OneDrive of Google Docs, **Details**, dan **Ontkoppelen**. Het stopt met lezen. Wat al binnengehaald is, blijft.
