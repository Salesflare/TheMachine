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

- **Voor jou**: alles wat op jou wacht, het dringendste eerst. Elke to-do zegt **Klaargezet** (het werk is gedaan, en **Doe het** of **Versturen** voert het uit) **Wacht op jou** (eerst je beslissing of een antwoord nodig) of **Aan het voorbereiden…** (je Machine werkt eraan).
- **Net gedaan**: een laatste stap die je bevestigde, zoals een formulier indienen of een issue aanmaken, is gelukt terwijl je weg was. Hij toont wat er gebeurde tot je op **Begrepen** tikt, hoogstens een dag, en je telefoon hoort het ook. Daarna staat hij alleen in Gedaan.
- **Komt later terug**: gesnoozed, en to-do's zonder antwoord op **Nog nodig?** (hieronder).
- **Beloftes**: wat jij beloofde en wat anderen jou beloofden. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: elke afgeronde to-do, op het moment dat hij af was, nieuwste eerst, 30 tegelijk terwijl je scrolt. Een to-do die je net verstuurd hebt staat bovenaan, en elke to-do zegt wanneer, zoals "Gedaan 5 minuten geleden". To-do's die al af lijken staan ertussen op het moment dat ze zo begonnen te lijken, met het label **Lijkt gedaan**.

Na het versturen zegt een korte melding waar de to-do nu staat, zoals "Verstuurd. Verplaatst naar Gedaan." of, als hij op een antwoord wacht, "Verstuurd. Verplaatst naar Later tot ma." **Openen** brengt je erheen. Dat de mailthread een paar dagen uit je inbox gaat, gaat alleen over je mailbox. Zoeken vindt een to-do op titel of op wie hij naartoe ging, ook in Later en Gedaan.

**Voor jou** zet bovenaan wat te laat is of uiterlijk morgen moet, dan vragen uit je Fleet, dan de rest. Binnen elk deel nieuwste eerst. Een to-do blijft op zijn plaats terwijl je Machine hem voorbereidt en als hij klaar is: alleen zijn label verandert. De andere open groepen zetten wat te laat is of uiterlijk morgen moet bovenaan, de rest nieuwste eerst. De zijbalk houdt dezelfde volgorde.

Een to-do met **Lijkt gedaan** ziet eruit als een gedane, met wat laat zien dat hij gedaan is, zoals "PR #3451 gemerged". Hij is nog niet gesloten: **Heropenen** zet hem terug op je lijst, en je Machine leert ervan. Ze staan nooit als te laat en tellen niet mee als wachtend op jou. Na een dag sluit hij vanzelf, met **Ongedaan maken**. Een to-do die je al zelf hebt afgehandeld, zoals met een antwoord in Gmail of Slack, sluit ook vanzelf.

Een to-do waarvan de laatste stap nog openstaat bij iemand anders, zoals een review, een merge of een antwoord, zegt **Wacht op:** die stap en blijft open. Hij wacht in **Wacht op anderen**, ingeklapt boven Komt later terug, en telt niet mee als klaar voor jou. Een nieuw bericht erover brengt hem terug. Hetzelfde als je een wedervraag stelde: hij komt terug op de ochtend voor zijn deadline, op de deadline als die later vandaag is, of de ochtend erna als die voorbij is, en zegt op wie hij nog wacht.

Gaat een to-do om een resultaat dat iemand anders levert, zoals een getekend contract of een betaling, dan tonen zijn **Details** dat resultaat als **Klaar als**. Je deel versturen sluit hem niet: hij wacht in **Wacht op anderen** tot een bericht dat resultaat toont, en sluit dan vanzelf, met **Ongedaan maken**. Komt er niets tegen de tijd om na te vragen, dan komt hij terug met **Schrijf een korte herinnering** in zijn chat. Zeg in de chat wat als klaar telt om dat te veranderen.

Een to-do die een week niemand aanraakte, vraagt één keer: **Nog nodig?** **Niet nodig** sluit hem, met **Ongedaan maken**. **Houden** houdt hem, en hij vraagt het nooit meer. Openen, een chatbericht, een aanpassing, snoozen of een nieuw bericht erover tellen allemaal als aanraken. Komt er een week later nog geen antwoord, dan vouwt hij weg in Komt later terug, onder Nog nodig?, in plaats van te verdwijnen. Dan telt hij ook niet meer mee in het getal op het app-icoon en het ochtendoverzicht. Aanraken haalt hem terug.

Als er niets op je wacht, doet je Machine een dutje op de lege lijst. Terwijl hij checkt, wordt hij wakker en zegt hij dat. Is een check mislukt of laat, dan zegt zijn regel dat, met **Nu checken** eronder.

**Alle**, **Werk** en **Privé** boven de lijst in de zijbalk tonen alle to-do's of maar één soort. Je Machine onthoudt de keuze, zodat je telefoon en computer dezelfde lijst tonen. Staat Werk of Privé aan, dan staat dat bovenaan de lijst, met **Alles tonen** om terug te gaan.

Een to-do bij een project toont de naam van het project in de regel onder de titel; die opent het project. **Project** onder **Details** wijzigt het of haalt het weg. Zie [de to-do's van een project](projects.md#a-projects-to-dos).

**Gebied** onder **Details** verplaatst de to-do naar je andere gebied. Wat hij mag lezen en waarvandaan hij mag versturen, verhuist mee; de berichten waar hij uit kwam, blijven waar ze zijn. **Ongedaan maken** in de melding die volgt, zet hem terug.

Heeft een to-do een ander gebied nodig om verder te kunnen en komen de berichten waaruit hij ontstond allemaal daarvandaan, dan verhuist hij zelf en gaat hij verder. Anders vraagt hij het met een knop **Naar Werk verplaatsen**. Er verhuist niets tot je erop tikt; daarna gaat hij zelf verder. Een to-do die je zonder Werk of Privé toevoegde, verhuist zelf zodra hij weet waar hij hoort.

Start je een to-do, dan mag hij altijd de berichten lezen waar hij uit kwam, ook in de mailbox van een ander bedrijf. Heeft hij andere berichten uit een ander gebied nodig, dan vraagt hij het met **Deze mail voor deze to-do gebruiken**; een tik voegt ze toe en hij gaat verder. Mail voor een ander bedrijf van je komt meteen bij de to-do's van dat bedrijf. Een to-do uit je eigen leven, zoals familie die naar je werkadres mailt, is meteen Privé.

Zo'n privé-to-do antwoordt toch vanaf het werkadres waar de mail binnenkwam, en hij komt nooit in een Work Fleet of de Team-Graph.

Wachten er twee of meer, dan loopt **Doorlopen** in de kop van Voor jou ze een voor een door, in de volgorde van de lijst, elk concept volledig, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat in beeld is, `S` snoozet, `→` slaat over en Esc stopt. Onder de titel zegt de kop ook hoe lang ze op jouw tempo duren, zoals "ongeveer 2 min".

Een to-do die je iets vraagt, telt bij geen van beide mee: die heeft je antwoord nodig, geen tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht, en checkt wat er binnenkwam op to-do’s zodra er 40 berichten wachten of het oudste bericht van een persoon 15 minuten wacht. Nieuwsbrieven, meldingen en bonnetjes gaan mee met de volgende check, binnen het uur.

**Nu checken** leest meteen elke bron. Staat er niets open, tik dan op de regel van je Machine om het te zien, met **Details**, dat Checks onder Koppelingen opent. Staan er to-do's open, dan staat het op een computer bovenaan. Een korte regel verschijnt daar alleen terwijl een check loopt, of als er een mislukt of laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare houden hun eigen tempo.

## Laatste check

Na een check die nieuwe berichten las, zegt een regel boven je to-do’s wat hij in alle bronnen vond, zoals "13 berichten gecheckt om 16:11 · niets voor jou" of "· 2 nieuwe to-do’s". Wacht een nieuwe to-do op een beter moment, zoals je ochtendoverzicht, dan staat er tot wanneer: "1 to-do wacht tot morgen 08:30".

Tik op de regel om elk e-mailgesprek, elke chat en elke melding te zien, met het icoon van de bron: wie schreef, het onderwerp of de eerste woorden, en de nieuwe to-do of waarom er niets nodig was, zoals "Alleen in cc, een collega antwoordt" of "Afspraak staat al voor donderdag". Een gesprek toont geen reden als de check alleen een vage gaf. Tik er een aan om het te lezen.

De eerste 10 staan er, een tik eronder toont de rest. Een getal na een naam, zoals (3), is hoeveel nieuwe berichten die chat heeft. Een melding op je telefoon over een bericht dat al in de lijst staat, zie je maar één keer. De regel blijft 12 uur na de check staan.

Hij telt alleen mail aan jou. Je eigen antwoorden worden gelezen voor context en beloftes, maar zijn geen nieuwe mail. De eigen e-mails van je Machine aan jou, zoals je ochtendoverzicht of een melding van een fix, worden nooit gelezen of getoond. Mail over betalingen, je proefperiode of een uitnodiging wordt gewoon gelezen.

## De knoppen

Een to-do toont zijn volgende stap, zoals **Doe het** of **Nakijken en versturen**, met **Snoozen** ernaast. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

**Wijzigingen vragen** zegt wat er anders moet: hoe het moet, of, zodra er een concept klaarstaat, wat erin moet veranderen. Is de rij op een telefoon vol, dan gaat **Snoozen** naar **…**. **Markeer als gedaan** (hij is geregeld) is er ook: in beeld bij een klare zonder concept, anders bovenaan onder **…**, ook bij een die jouw beslissing vraagt. Hij gaat meteen uit de lijst, met **Ongedaan maken** in de melding. Veeg de melding weg, of sleep hem weg met de muis, om hem eerder te sluiten. De wijziging blijft.

Wil je hem anders laten doen, zeg het dan in zijn **Chat**.

Onder **…** (op een telefoon schuift dat open vanaf de onderkant van het scherm):

- **Overdragen…**: geef hem aan een teamgenoot, aan [Claude Code of Codex](hand-to-agent.md) (die je ingesteld hebt), of [vraag iemand om een review](ask-to-review.md).
- **Herhalen…**: hij [komt terug in een ritme](recurring.md).
- **Niet nodig**: hij verdwijnt. Kies eventueel waarom: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel, of op **Naam** onder **Details**, om hem te hernoemen. Je titel blijft, ook als de to-do verandert.

Een gesloten to-do kan terugkomen met **Heropenen**. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van de ander. Je eigen antwoord brengt hem niet terug.

Een to-do die maar tot een bepaald moment telde, zoals een bevestiging voor een vergadering, sluit vanzelf zodra dat moment voorbij is. Hij gaat naar **Gedaan / afgewezen** met "Niet meer nodig" en wanneer het was. **Ongedaan maken** brengt hem een dag lang terug.

Voordat een bericht of overdracht voor iemand klaarstaat, kijkt je Machine je recente chats met de betrokkenen na, ook groepschats, en wacht tot Slack ze gelezen heeft. Toont een later bericht dat het al gedaan is, bijvoorbeeld omdat het al gevraagd is en ze ja zeiden, dan sluit de to-do vanzelf. **Ongedaan maken** brengt hem een dag lang terug.

Als een nieuwer bericht het plan verandert, zoals een feest dat naar een andere plek verhuist of een geschrapte boeking, werkt The Machine zijn to-do's zelf bij. Een die nog telt, volgt het nieuwe plan. Een waar niets meer te doen is, gaat naar **Gedaan / afgewezen** als "Niet nodig", zijn chat zegt "Bijgewerkt:" en waarom, en **Ongedaan maken** brengt hem een dag lang terug.

Bij je eerste to-do's staat onder de knoppen één korte regel met wat je moet weten: **Wijzigingen vragen** en **Niet nodig** als een to-do niet helemaal klopt, en bij je eerste klaarstaande concept dat er niets weggaat tot je op **Versturen** drukt. Een tip verdwijnt voorgoed zodra je die knop gebruikt of op × drukt, op al je apparaten.

Op je eerste dag zegt de bovenkant van To-do's hallo met je naam en wie het langst op je antwoord wacht. The Machine schrijft dat antwoord eerst, zodat het klaarstaat als je binnenkomt. Er gaat niets weg tot je het verstuurt. De regel verdwijnt na je eerste dag of je eerste besliste to-do.

Elke to-do begint met de titel. De regel eronder zegt over wie hij gaat, de organisatie als hij over een organisatie gaat (nooit alleen omdat iemand daar werkt), het project, Werk of Privé (onder **Alle**) en wanneer hij binnenkwam, en waar hij staat als de groep dat niet al zegt. Tik op een naam om de pagina in de Graph te openen.

Soms zegt een rustige regel onder de tekst wat niet bekend is, zoals "Laatste contact 12 dagen geleden via e-mail; niets sindsdien." Die staat er alleen als het laatste contact oud is of nog onbeantwoord, en noemt kanalen die niet gekoppeld zijn waar ze misschien geantwoord hebben, zoals WhatsApp. Je Machine bereidt voor met dezelfde feiten, dus hij zegt wat hij niet weet in plaats van te gokken.

Noemt de regel een kanaal dat niet gekoppeld is, dan opent Koppelen ernaast die koppeling.

Een titel zegt wat er moet gebeuren. Hij verandert alleen als dat verandert, zoals bij een nieuwe vraag. Een to-do die gedaan is houdt zijn titel, met eronder hoe hij afliep, zoals wat er verstuurd is of "Gedaan: Sam heeft dinsdag getekend".

Boven het concept noemt een rustige regel het bericht waar hij uit komt, met het logo van de dienst (Gmail, Slack, WhatsApp…). Tik erop om de thread te lezen. Het concept begint met het logo van waar het heen gaat, zo zie je vóór het lezen of het een Slack-antwoord of een e-mail is. Een stap zonder concept, zoals een overdracht, toont het logo op zijn knop.

Volgt het concept wat iemand anders in een ander bericht zei, zoals een voorstel van een collega in Slack, dan zegt een regel onder de to-do dat, zoals "Op basis van Sam in #ops". Tik erop om dat bericht hier te lezen, met Openen in Slack of Gmail erin. Is dat bericht de bron van de to-do zelf, dan toont de bronregel het al en komt er geen tweede regel.

Een chat (Slack, WhatsApp, Telegram, Intercom…) lees je als één gesprek, oudste eerst, elk bericht één keer; het bericht waar de to-do over gaat heeft een dun lijntje ernaast.

**Details** toont zijn naam, project en gebied (tik erop om het te wijzigen), je laatste notitie en het resultaat van een codeeragent. **Chat ›** aan het eind van die regel opent de chat. Een afgeronde to-do blijft kort: de titel, één regel en wat er verstuurd is; het bericht waar hij uit komt staat onder zijn **Details**.

Een to-do "Wacht op" (iemand heeft je iets beloofd) linkt naar je eigen laatste bericht aan die persoon, het bericht waarop je een antwoord verwacht: "E-mail aan Pat · di".

## Er zelf een maken

**Nieuwe to-do** (onder **Zoeken** op een computer) voegt een to-do toe voor wat dan ook. Aanmaken verstuurt niets. Zonder Werk of Privé komt hij waar hij hoort: volgens wie en waar hij over gaat, een bedrijf of mailbox die hij noemt, of de e-mail waarop hij opvolgt. Als niets het aangeeft, begint hij waar de meeste van je to-do's staan. The Machine zoekt die e-mail in je mailbox, ook oudere mail die nog niet binnengehaald is.

- **Deadline**: typ een dag of een tijd, zoals "morgen", "volgende vr", "3 nov", "15:00", "over 2 uur" of "morgen 9u". Engels werkt ook ("in 2 hours", "tomorrow 9"). Het agenda-icoon heeft snelle keuzes, zoals bij snoozen, en **Kies een datum**.
- **Bericht**: voeg het bericht toe waarover het gaat: een e-mail, Slack, Teams, WhatsApp, Telegram of elk ander bericht dat The Machine heeft. Zoek op tekst of afzender. Elk resultaat toont waar het vandaan komt, wie het stuurde en wanneer.
- **Bestanden**: tik op de paperclip in het vak, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon kun je ook een foto maken. Maximaal 5 bestanden, dezelfde soorten en groottes als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). × haalt er een weg.

De bestanden blijven bij de to-do: ze staan erop en in de chat ervan, en The Machine leest ze als hij eraan werkt. Alleen bestanden is genoeg: The Machine leest de tekst van een pdf of tekstbestand en vult de to-do daarmee in.
