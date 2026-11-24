---
title: To-do's
area: cards
summary: Eén to-do voor elke taak die je aandacht nodig heeft, klaar om door jou goedgekeurd te worden. Lees wat de onderdelen van een to-do betekenen.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 32c3a3e62b74548f
---
Je Machine leest alle nieuwe berichten en maakt alleen een to-do aan als iets je aandacht nodig heeft. Eén to-do per kwestie, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze in groepen:

- **Net gedaan**: bovenaan staat de laatste stap die je hebt bevestigd, bijvoorbeeld een formulier of een probleem dat is afgehandeld terwijl je weg was. Dit blijft maximaal een dag staan, tot je op **Begrepen** tikt. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met eerst wat uiterlijk morgen moet gebeuren. Bij elke to-do staat **Klaargezet** (een concept of resultaat is klaar; met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (je moet eerst een beslissing nemen of antwoord geven; als het werk niet verder kan of niet gebruikt kan worden zonder iets wat alleen jij hebt, zoals een prijs, een feit of een keuze, staat er onder de titel wat dat is), **Aan het voorbereiden…** (je Machine werkt eraan) of **Om te lezen** (een overzicht of briefing, zonder dat je iets hoeft te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws over is gebeurd (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarvoor iemand anders aan zet is (zie hieronder).
- **Komt later terug**: gesnoozede to-do's en to-do's waarop geen antwoord is gekomen op **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het tijdstip waarop ze zijn afgerond, bijvoorbeeld ‘5 minuten geleden gedaan’. To-do's die al afgerond lijken, zijn gemarkeerd als **Lijkt gedaan**.

Na het versturen staat er kort waar de to-do naartoe is verplaatst, bijvoorbeeld ‘Verstuurd. Verplaatst naar Gedaan.’ of ‘Verstuurd. Verplaatst naar Later tot ma.’ Een antwoord waarin je alleen belooft het werk te doen, zoals ‘Ik stuur het dinsdag’, laat de to-do openstaan: ‘Verstuurd. Opengehouden.’ Met **Openen** ga je naar de to-do. Zoeken vindt to-do's op titel of op de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan eerst to-do's waarvan de deadline is verstreken of uiterlijk morgen is, daarna vragen van je Fleet, vervolgacties van een bord en vervolgens de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek terwijl je Machine hem voorbereidt en wanneer hij klaar is. Alleen de markering verandert. In de andere open groepen staan to-do's waarvan de deadline is verstreken of uiterlijk morgen is bovenaan, gevolgd door de rest, nieuwste eerst. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets klaar is, bijvoorbeeld ‘PR #3451 is samengevoegd’, maar dat het nog niet is gesloten. Met **Heropenen** zet je het terug in je lijst. Je Machine leert daarvan. Deze to-do's worden nooit als te laat weergegeven. Als een bericht laat zien dat het klaar is, wordt het na een dag vanzelf gesloten. Je kunt dat ongedaan maken met **Ongedaan maken**. Anders wacht het tot je op **Als gedaan markeren** tikt.

Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook vanzelf gesloten. Een antwoord waarin staat dat er een bestand is bijgevoegd terwijl dat niet zo is, sluit de to-do niet.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, bijvoorbeeld sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: ‘Dit is Sam Lee niet.’ De afzender wordt weergegeven met het eigen adres, nooit met de naam die hij heeft gebruikt. Je Machine controleert zo'n bericht bij de persoon van wie je het adres al hebt, nooit bij de afzender.

Bij een to-do waarvoor iemand anders aan zet is, bijvoorbeeld voor een review of antwoord, staat **Wacht op:** met de volgende stap. De to-do staat ingeklapt in **Wacht op anderen**, boven Komt later terug, tot een nieuw bericht hem weer naar voren haalt. Dat gebeurt ook nadat je zelf een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline als die later vandaag valt, of de volgende ochtend als de deadline al voorbij is. Er staat dan op wie de to-do nog wacht.

Als een to-do draait om een resultaat dat iemand anders oplevert, zoals een ondertekend contract, staat dat bij **Details** onder **Klaar als**. Je eigen deel versturen sluit de to-do niet. Hij blijft in **Wacht op anderen** staan tot een bericht laat zien dat het resultaat er is. Daarna wordt hij vanzelf gesloten. Je kunt dat ongedaan maken met **Ongedaan maken**. Als er niets binnenkomt vóór het tijd is om erachteraan te gaan, komt de to-do terug en staat **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Als er een week niets nieuws over een to-do is gebeurd, verhuist hij van Voor jou naar **Ouder**. Zo staan nieuwe to-do's bovenaan als je na een paar dagen terugkomt. Er is niets nieuws gebeurd als er geen nieuw bericht over de to-do is en jij er niets mee hebt gedaan, zoals een chatbericht sturen, hem bewerken of snoozen. Alleen bekijken telt niet.

Dringende to-do's, to-do's met een naderende deadline en to-do's waarvan het versturen bezig is, blijven in Voor jou staan. Met **Alles afwijzen** markeer je in één keer alle to-do's in Ouder als niet nodig. Je bevestigt dit één keer. Dit werkt net als **Niet nodig**, waarmee je to-do's één voor één afwijst. Je kunt dit ongedaan maken met **Ongedaan maken**. Als er iets nieuws gebeurt, komt de to-do terug in Voor jou.

Als niemand een to-do een week heeft aangeraakt, vraagt hij één keer: **Nog nodig?** Met **Niet nodig** sluit je de to-do. Je kunt dit ongedaan maken met **Ongedaan maken**. Met **Houden** blijft de to-do staan en wordt dit nooit meer gevraagd. Als er nog een week geen antwoord komt, wordt de to-do ingeklapt in Komt later terug. Hij telt dan niet meer mee voor het getal op het appicoon en het ochtendoverzicht. Als je de to-do opent, een chatbericht stuurt, hem bewerkt of snoozet, of als er een nieuw bericht binnenkomt, komt hij weer terug.

Een project dat een week stil heeft gelegen en geen open to-do's heeft, kan één keer per week een to-do krijgen met een specifieke volgende stap. Dit gebeurt maximaal drie keer per week. Zie [Projecten](projects.md).

Als er niets is dat je aandacht nodig heeft, doet je Machine een dutje en blijft de lijst leeg. Tijdens het controleren wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk toon je alle to-do's of alleen één soort. Op je telefoon en computer geldt dezelfde keuze. Als Werk of Privé is geselecteerd, brengt **Alles tonen** je terug naar alle to-do's. Een melding over je Machine zelf, bijvoorbeeld een onderdeel dat steeds opnieuw opstart, valt niet onder Werk of Privé en staat alleen bij Alle.

Met de regel bovenaan de lijst schakel je ook direct naar de andere optie. Tik onder **Alleen privé** op **Werk** of **Alles tonen**.

De balk bovenaan de lijst toont je laatste ochtend- of avondoverzicht en wat daarin is meegeteld, bijvoorbeeld **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om het overzicht opnieuw te lezen. Met **Kopiëren** kun je het overal plakken. Zodra je het opent of op de **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Als er geen recent overzicht is, staat er **Vandaag tot nu toe**: wat er vandaag is gedaan en wat nog openstaat, voor Werk en Privé of alleen voor de optie die je hebt geselecteerd.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Zie [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De bronnen waaruit hij mag lezen en waarnaar hij mag versturen, verhuizen mee. Met **Ongedaan maken** bij de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te kunnen en alle berichten waar hij uit voortkomt daar staan, verhuist hij vanzelf naar dat gebied en gaat hij verder. Anders staat er **Naar Werk verplaatsen** en gebeurt er niets tot je erop tikt. Een to-do die je zelf hebt toegevoegd zonder Werk of Privé te kiezen, verhuist vanzelf zodra duidelijk is waar hij thuishoort. Tot die tijd valt hij niet onder Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij uit voortkomt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij met **Deze mail voor deze to-do gebruiken** om toestemming. Een werkmailbox die je als Privé hebt gemarkeerd, telt als Privé. Mail voor een ander bedrijf van jou komt bij de to-do's van dat bedrijf terecht. Een to-do over je privéleven, bijvoorbeeld een familielid dat naar je werkadres mailt, valt vanaf het begin onder Privé.

Werk dat je via een persoonlijk account bereikt, zoals een klant op WhatsApp, een bestelling in je persoonlijke mailbox of een [belofte](promises.md) over werk, valt vanaf het begin onder Werk.

Een to-do die je zelf hebt verplaatst of geplaatst, blijft altijd staan waar je hem hebt neergezet. Werk of Privé bepaalt waar een to-do verschijnt en met wie hij wordt gedeeld, nooit waar hij op antwoorden reageert. Een antwoord gaat altijd naar de plek waar het gesprek plaatsvindt, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n to-do onder Privé reageert nog steeds vanaf het werkadres waarop de e-mail is binnengekomen en verschijnt nooit in een Werk-Fleet of Team-Graph.

Als er twee of meer to-do's op je wachten, doorloopt **Doorlopen** in de kop van Voor jou ze één voor één, in de volgorde van de lijst. Je ziet elk concept volledig, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Druk op een computer op Enter om te versturen wat op het scherm staat, op `S` om te snoozen, op `→` om over te slaan en op Esc om te stoppen. In de kop staat hoelang ze duren in jouw tempo, bijvoorbeeld ‘ongeveer 2 min’.

Aan het einde staat hoeveel to-do's zijn verstuurd of gesloten en hoeveel er nog worden voorbereid.

Een to-do die je een vraag stelt, wordt niet meegenomen. Daarvoor is je antwoord nodig, niet een tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert wat er is binnengekomen zodra er 40 berichten klaarstaan of het oudste bericht van iemand al 15 minuten wacht. Nieuwsbrieven, meldingen en ontvangstbewijzen worden meegenomen bij de volgende controle, binnen een uur.

's Nachts, van 00:00 tot 06:30, worden controles gepauzeerd. Nieuwe berichten worden nog wel gelezen en bewaard, en om 06:30 samen gecontroleerd, zodat je to-do's klaarstaan vóór je ochtendoverzicht. Bij Controles onder Koppelingen staat dan ‘'s Nachts gepauzeerd, haalt de achterstand om 06:30 in’. Als je 's nachts in de app klikt, typt of scrolt, in de chat schrijft of op een to-do tikt, worden controles zoals gewoonlijk uitgevoerd tot je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** worden alle bronnen meteen gelezen. Als er geen open to-do's zijn, tik je op de regel van je Machine om hem te zien, met **Details**. Daarmee open je Controles onder Koppelingen. Als er open to-do's zijn, staat de regel bovenaan op een computer. Een korte melding wordt alleen weergegeven terwijl er een controle bezig is, of wanneer die is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare hebben hun eigen tempo.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's wat er is gevonden in alle gelezen bronnen, bijvoorbeeld ‘13 berichten gecontroleerd om 16:11 · geen nieuwe to-do's’ of ‘· 2 nieuwe to-do's’. Dit geldt alleen voor die controle. To-do's die al op je lijst stonden, blijven staan zoals ze zijn. Als een nieuwe to-do wacht op een beter moment, bijvoorbeeld je ochtendoverzicht, staat erbij tot wanneer: ‘1 to-do uitgesteld tot morgen 08:30’.

Tik op de regel om elk e-mailgesprek, elke chat en elke melding te zien, met het pictogram van de bron. Je ziet wie het bericht heeft geschreven, het onderwerp of de eerste woorden, en de nieuwe to-do of de reden waarom er niets nodig was, bijvoorbeeld ‘Alleen in cc, een teamgenoot antwoordt’ of ‘Afspraak staat al voor donderdag gepland’. Bij een gesprek wordt geen reden weergegeven als de controle alleen een vage reden opleverde. Tik op een bericht om het te lezen, samen met de berichten eromheen.

De eerste 10 worden weergegeven. Tik onderaan om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer weergegeven. De regel blijft 12 uur na de controle staan.

Alleen mail aan jou telt mee. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails van The Machine zelf, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met **Snoozen** ernaast. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe de taak moet worden uitgevoerd, of, zodra een concept klaarstaat, wat daarin moet veranderen. **Als gedaan markeren** betekent dat de taak is afgehandeld. Deze optie staat direct in beeld bij een klaargezette to-do zonder concept of bij een to-do die je iets vraagt. Anders staat hij bovenaan onder **…**. De to-do verdwijnt meteen uit de lijst. In de melding kun je dit ongedaan maken met **Ongedaan maken**. Veeg de melding weg of sleep hem met de muis van het scherm om hem eerder te sluiten. De wijziging blijft bewaard.

Wil je dat de taak op een andere manier wordt uitgevoerd, vertel dat dan in de **Chat**. In het antwoord staat alleen wat er is veranderd, bijvoorbeeld dat de to-do is gesnoozed en tot wanneer. Als iets niet kon worden aangepast, zoals een deadline, staat dat erbij.

Onder **…**:

- **Overdragen…**: geef de taak aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om een review](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast ritme terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert hiervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt dit ook in de chat vragen, bijvoorbeeld: ‘Hernoem dit naar …’. De titel blijft staan.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van de ander, maar niet na je eigen antwoord. Er staat dan wanneer hij is teruggekomen en hij wordt gesorteerd als een nieuwe to-do. De chat gaat verder waar hij was gebleven, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals via automatische incasso of een opgeslagen kaart, worden dat niet. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld een bevestiging van de afzender, wordt de to-do vanzelf gesloten. Je kunt hem een dag lang terugzetten met **Ongedaan maken**.

Een to-do die maar tot een bepaald tijdstip relevant was, bijvoorbeeld een bevestiging vóór een meeting, wordt na dat tijdstip vanzelf gesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet langer nodig’. Je kunt hem een dag lang terugzetten met **Ongedaan maken**.

Voordat een bericht of overdracht aan iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de betrokkenen, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat de taak al is afgehandeld, bijvoorbeeld omdat iemand erom is gevraagd en ja heeft gezegd, wordt de to-do vanzelf gesloten. Je kunt hem een dag lang terugzetten met **Ongedaan maken**.

Als iemand anders in hetzelfde gesprek heeft geschreven nadat je concept was gemaakt, houdt **Versturen** het tegen: ‘Niet verstuurd: nieuw bericht in het gesprek’. Bij de to-do staat dat bericht met **Lezen** en **Opnieuw voor dit bericht**. Druk nogmaals op **Versturen** om je concept ongewijzigd te versturen.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een boeking is geannuleerd, werkt The Machine zijn to-do's zelf bij. Een to-do die nog steeds nodig is, volgt het nieuwe plan. Is er niets meer te doen, dan wordt de to-do verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet nodig’. In de chat staat ‘Bijgewerkt:’ met de reden. Je kunt de to-do een dag lang terugzetten met **Ongedaan maken**.

Bij je eerste to-do's verschijnt een korte tip over de belangrijkste opties: **Wijzigingen vragen** en **Niet nodig**. Ook staat erin dat er niets wordt verstuurd tot je op **Versturen** drukt. De tip verdwijnt voorgoed zodra je de knop gebruikt of op × drukt.

Op je eerste dag heet de bovenkant van To-do's je welkom en wordt vermeld wie al het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat wanneer je begint.

Elke to-do begint met de titel. De regel eronder vermeldt over wie de to-do gaat, welke organisatie erbij hoort als het om een organisatie gaat (niet alleen omdat iemand er werkt), het project, Werk of Privé en wanneer de to-do is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en een organisatie staat een foto of logo als die in de Graph beschikbaar is. Anders staan er initialen. Als een logo op dit formaat niet leesbaar zou zijn, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, wordt ook de beginletter weergegeven.

Soms staat er een rustige melding met iets wat niet bekend is, bijvoorbeeld ‘Laatste contact 12 dagen geleden via e-mail; sindsdien niets’. Dit wordt weergegeven als het laatste contact lang geleden was of onbeantwoord bleef, en vermeldt kanalen die niet zijn gekoppeld, zoals WhatsApp. Je Machine vertelt wat hij niet weet, in plaats van te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast de bijbehorende koppeling.

De titel vermeldt wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do behoudt zijn titel, met daaronder hoe hij is afgerond, bijvoorbeeld ‘Gedaan: Sam heeft het dinsdag ondertekend’.

Boven het concept staat een vage regel met het bericht waar het uit voortkomt en het logo van de dienst. Tik erop om het gesprek te lezen. Bij het concept staat het logo van de plek waar het naartoe gaat, zodat je meteen ziet of het een Slack-antwoord of een e-mail is.

Als het concept is gebaseerd op input van iemand anders, bijvoorbeeld een suggestie van een teamgenoot in Slack, staat dat erbij, bijvoorbeeld ‘Gebaseerd op Sam in #ops’. Tik erop om dat bericht te lezen. De regel verdwijnt wanneer een update het concept vervangt.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt als één gesprek weergegeven, met de oudste berichten eerst: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je eigen berichten rechts, net als in de app. Het bericht van de to-do is gemarkeerd met ‘Deze to-do’ en wordt geopend in beeld. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Bij een e-mail staat de rest van het gesprek ingeklapt erboven en eronder.

Een bericht wordt op dezelfde manier geopend vanuit zoeken, de Graph, antwoorden van Ask of de laatste controle. Het is gemarkeerd als ‘Dit bericht’ of ‘Nieuwe berichten’.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waar hij is binnengekomen. Op Android opent hij in de Gmail-app als je die hebt.

Bij **Details** van een e-mail staat alleen informatie die niet in de kop staat, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets toe te voegen is, wordt er niets weergegeven.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. Via de link van een to-do naar het bijbehorende bericht open je het bericht hier ook, met **Openen in Slack** onderaan.

Bij **Details** staan de naam, het project en het gebied (tik erop om ze te wijzigen), je laatste notitie en het resultaat van een codeeragent. Tik op de titel om de chat te openen. Een afgeronde to-do blijft compact. Het bericht waar hij uit voortkomt staat onder **Details**.

Een to-do met ‘Wacht op’ bevat een link naar je laatste bericht aan de ander, het bericht waarop je wacht: ‘E-mail aan Pat · di’.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor alles wat je wilt. Er wordt niets verstuurd als je een to-do aanmaakt. Als je geen **Werk** of **Privé** kiest, komt de to-do terecht waar hij thuishoort, op basis van wie en wat erbij hoort. Je Machine zoekt ook de e-mail op waarop de to-do voortbouwt, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, zoals ‘morgen’, ‘volgende vr’, ‘3 nov’, ‘14:00’ of ‘over 2 uur’. Dat kan ook in je eigen taal. Met het kalenderpictogram zie je snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt volgens een vast ritme terug. Zie [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waar de to-do over gaat, maximaal 5.
- Berichtpictogram: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack-, Teams-, WhatsApp- of Telegram-bericht, of een ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een schermafbeelding of sleep bestanden naar het formulier. Op een telefoon kun je met de camera ernaast een foto maken. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en The Machine leest ze wanneer hij eraan werkt. Alleen bestanden toevoegen is genoeg: je Machine vult de to-do in op basis van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op volledige grootte te bekijken.
