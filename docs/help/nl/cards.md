---
title: To-do's
area: cards
summary: Eén to-do per ding dat jou nodig heeft, klaar voor je ja. Wat de onderdelen van een to-do betekenen.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
---
Je Machine leest alles wat nieuw is en maakt alleen een to-do als iets jou nodig heeft. Eén to-do per zaak, hoeveel berichten er ook bij horen.

## Waar to-do's staan

De pagina **To-do's** groepeert ze:

- **Klaar voor jou**: voorbereid en wacht op je goedkeuring.
- **Wacht op je beslissing**: iets wat alleen jij kunt beslissen.
- **Wordt voorbereid**: je Machine werkt eraan. Een to-do waarop je net **Doe het** zei, blijft staan waar hij stond terwijl hij voorbereid wordt, en gaat dan naar **Klaar voor jou**.
- **Komt later terug**: gesnoozed.
- **Beloftes**: wat jij beloofde en wat anderen jou beloofden. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: elke afgeronde to-do, nieuwste eerst, 30 tegelijk terwijl je scrolt. To-do's die al af lijken staan bovenaan, met het label **Lijkt gedaan**.

Een to-do met **Lijkt gedaan** ziet eruit als een gedane, met wat laat zien dat hij gedaan is, zoals "PR #3451 gemerged". Hij is nog niet gesloten: **Heropenen** zet hem terug op je lijst, en je Machine leert ervan. Ze staan nooit als te laat en tellen niet mee als wachtend op jou.

Een to-do waarvan de laatste stap nog openstaat bij iemand anders, zoals een review, een merge of een antwoord, zegt **Wacht op:** die stap en blijft open. Hij wacht in **Wacht op anderen**, ingeklapt boven Komt later terug, en telt niet mee als klaar voor jou. Een nieuw bericht erover brengt hem terug.

**Alles is rustig.** betekent dat er nu niets op je wacht. De regel eronder zegt wanneer je Machine voor het laatst heeft gekeken.

**Alle**, **Werk** en **Privé** boven de lijst in de zijbalk tonen alle to-do's of maar één soort. Je Machine onthoudt de keuze, zodat je telefoon en computer dezelfde lijst tonen. Staat Werk of Privé aan, dan staat dat bovenaan de lijst, met **Alles tonen** om terug te gaan.

Een to-do bij een project toont de naam van het project in de regel onder de titel; die opent het project. **Project** onder **Details** wijzigt het of haalt het weg. Zie [de to-do's van een project](graph.md#a-projects-to-dos).

**Gebied** onder **Details** verplaatst de to-do naar je andere gebied, zoals een privé-to-do die vanaf je werkadres moet vertrekken. Wat hij mag lezen en waarvandaan hij mag versturen, verhuist mee; de berichten waar hij uit kwam, blijven waar ze zijn. **Ongedaan maken** in de melding die volgt, zet hem terug.

Heeft een to-do een ander gebied nodig om verder te kunnen, dan vraagt hij het met een knop **Naar Werk verplaatsen**. Er verhuist niets tot je erop tikt; daarna gaat hij zelf verder.

Start je een to-do, dan mag hij altijd de berichten lezen waar hij uit kwam, ook in de mailbox van een ander bedrijf. Heeft hij andere berichten uit een ander gebied nodig, dan vraagt hij het met **Deze mail voor deze to-do gebruiken**; een tik voegt ze toe en hij gaat verder. Mail voor een ander bedrijf van je komt meteen bij de to-do's van dat bedrijf.

## De knoppen

Een to-do toont zijn volgende stap, zoals **Doe het** of **Nakijken en versturen**, met **Snoozen** ernaast. Zie [Doe het](do-it.md) en [Snoozen](snooze.md). Een klaarstaande heeft ook **Wijzigingen vragen** (zeg wat er in het concept moet veranderen en hij doet het opnieuw). **Markeer als gedaan** (hij is geregeld) is er ook: in beeld zonder concept, anders bovenaan onder **…**.

Wil je hem anders laten doen, zeg het dan in zijn **Chat**.

Onder **…** (op een telefoon schuift dat open vanaf de onderkant van het scherm):

- **Overdragen…**: geef hem aan een teamgenoot, aan [Claude Code of Codex](hand-to-agent.md) (die je ingesteld hebt), of [vraag iemand om een review](ask-to-review.md).
- **Herhalen…**: hij [komt terug in een ritme](recurring.md).
- **Niet nodig**: hij verdwijnt. Kies eventueel waarom: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel, of op **Naam** onder **Details**, om hem te hernoemen. Je titel blijft, ook als de to-do verandert.

Een gesloten to-do kan terugkomen met **Heropenen**. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van de ander. Je eigen antwoord brengt hem niet terug.

Een to-do die maar tot een bepaald moment telde, zoals een bevestiging voor een vergadering, sluit vanzelf zodra dat moment voorbij is. Hij gaat naar **Gedaan / afgewezen** met "Niet meer nodig" en wanneer het was. **Ongedaan maken** brengt hem een dag lang terug.

Bij je eerste to-do's staat onder de knoppen één korte regel met wat je moet weten: **Anders aanpakken** (of **Wijzigingen vragen**) en **Niet nodig** als een to-do niet helemaal klopt, en bij je eerste klaarstaande concept dat er niets weggaat tot je op **Versturen** drukt. Een tip verdwijnt voorgoed zodra je die knop gebruikt of op × drukt, op al je apparaten.

Op je eerste dag zegt de bovenkant van To-do's hallo met je naam en wie het langst op je antwoord wacht. The Machine schrijft dat antwoord eerst, zodat het klaarstaat als je binnenkomt. Er gaat niets weg tot je het verstuurt. De regel verdwijnt na je eerste dag of je eerste besliste to-do.

Elke to-do begint met de titel. De regel eronder zegt over wie hij gaat, hun organisatie, het project, Werk of Privé (onder **Alle**) en wanneer hij binnenkwam, en waar hij staat als de groep dat niet al zegt. Tik op een naam om de pagina in de Graph te openen.

Soms zegt een rustige regel onder de tekst wat niet bekend is, zoals "Laatste contact 12 dagen geleden via e-mail; niets sindsdien." Die staat er alleen als het laatste contact oud is of nog onbeantwoord, en noemt kanalen die niet gekoppeld zijn waar ze misschien geantwoord hebben, zoals WhatsApp. Je Machine bereidt voor met dezelfde feiten, dus hij zegt wat hij niet weet in plaats van te gokken.

Een titel zegt wat er moet gebeuren. Hij verandert alleen als dat verandert, zoals bij een nieuwe vraag. Een to-do die gedaan is houdt zijn titel, met eronder hoe hij afliep, zoals wat er verstuurd is of "Gedaan: Sam heeft dinsdag getekend".

**Details** toont zijn naam, project en gebied (tik erop om het te wijzigen), het bericht waar hij uit komt (tik erop om de thread te lezen), je laatste notitie en het resultaat van een codeeragent. **Chat ›** aan het eind van die regel opent de chat. Een afgeronde to-do blijft kort: de titel, één regel en wat er verstuurd is.

Een to-do "Wacht op" (iemand heeft je iets beloofd) linkt naar je eigen laatste bericht aan die persoon, het bericht waarop je een antwoord verwacht: "E-mail aan Pat · di".

## Er zelf een maken

**Nieuwe to-do** (onder **Zoeken** op een computer) voegt een to-do toe voor wat dan ook. Aanmaken verstuurt niets.

- **Deadline**: typ een dag of een tijd, zoals "morgen", "volgende vr", "3 nov", "15:00", "over 2 uur" of "morgen 9u". Engels werkt ook ("in 2 hours", "tomorrow 9"). Het agenda-icoon heeft snelle keuzes, zoals bij snoozen, en **Kies een datum**.
- **E-mail**: voeg de e-mail toe waarover het gaat. Hij zoekt alleen in je e-mail, op onderwerp of afzender.
- **Bestanden**: tik op de paperclip in het vak, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon kun je ook een foto maken. Maximaal 5 bestanden, dezelfde soorten en groottes als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). × haalt er een weg.

De bestanden blijven bij de to-do: ze staan erop en in de chat ervan, en The Machine leest ze als hij eraan werkt.
