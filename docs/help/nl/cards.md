---
title: To-do's
area: cards
summary: Eén to-do per zaak die je aandacht nodig heeft, klaar om door jou goedgekeurd te worden. Dit betekenen de onderdelen van een to-do.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: cd59c14a7a27491d
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do als iets je aandacht nodig heeft. Eén to-do per zaak, hoeveel berichten die ook omvat.

## Waar to-do's staan

Op de pagina **To-do's** staan ze bij elkaar:

- **Voor jou**: alles wat op jou wacht, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (het werk is gedaan en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (je moet eerst een beslissing nemen of antwoord geven) of **Aan het voorbereiden…** (je Machine is ermee bezig).
- **Net gedaan**: een laatste stap die je hebt bevestigd, zoals een formulier of issue, is uitgevoerd terwijl je weg was. De to-do blijft hier staan totdat je op **Begrepen** tikt, maximaal één dag. Je telefoon krijgt er ook een melding van.
- **Komt later terug**: to-do's die zijn gesnoozed en to-do's waarop je geen antwoord gaf bij **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: elke afgeronde to-do, met de nieuwste bovenaan en erbij wanneer die is afgerond, zoals 'Gedaan 5 minuten geleden'. To-do's die al afgerond lijken, krijgen het label **Lijkt gedaan**.

Nadat je iets hebt verstuurd, staat er kort waar de to-do terechtkwam, zoals 'Verstuurd. Verplaatst naar Gedaan.' of 'Verstuurd. Verplaatst naar Later tot ma.'. Met **Openen** ga je naar de to-do. Je kunt zoeken op de titel van een to-do of op de persoon aan wie die is verstuurd, ook in Later en Gedaan.

Bij **Voor jou** staan eerst de to-do's waarvan de deadline is verstreken of morgen valt, dan vragen van je Fleet en daarna de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine die voorbereidt en wanneer die klaar is. Alleen het label verandert. In de andere open groepen staan to-do's waarvan de deadline is verstreken of morgen valt bovenaan, gevolgd door de rest, met de nieuwste eerst. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets is afgerond, zoals 'PR #3451 samengevoegd', maar dat de to-do nog niet is gesloten. Met **Heropenen** zet je die terug op je lijst en leert je Machine ervan. Deze to-do's worden nooit als te laat weergegeven. Na een dag wordt de to-do vanzelf gesloten, met **Ongedaan maken** als optie. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook vanzelf gesloten.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: 'Dit is niet Sam Lee.' Je ziet de afzender onder het eigen adres, nooit onder de naam die diegene heeft gebruikt. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, bijvoorbeeld voor een review of antwoord, staat **Wacht op:** met die stap. De to-do staat ingeklapt bij **Wacht op anderen**, boven Komt later terug, totdat een nieuw bericht de to-do weer opent. Dat gebeurt ook nadat jij een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline zelf als die later vandaag valt, of de volgende ochtend als de deadline al verstreken is. Je ziet dan op wie de to-do nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet opleveren, zoals een ondertekend contract, zie je dat bij **Details** onder **Klaar als**. Als je jouw deel verstuurt, wordt de to-do niet gesloten. Die blijft bij **Wacht op anderen** staan totdat een bericht het resultaat bevestigt. Daarna wordt de to-do vanzelf gesloten, met **Ongedaan maken** als optie. Als er niets binnenkomt tegen de tijd dat je diegene een herinnering wilt sturen, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Als niemand een week iets met een to-do heeft gedaan, vraagt die één keer: **Nog nodig?** Met **Niet nodig** sluit je de to-do, met **Ongedaan maken** als optie. Met **Houden** houd je de to-do. De vraag wordt dan niet opnieuw gesteld. Als je nog een week niet reageert, wordt de to-do ingeklapt bij Komt later terug. De badge op het app-icoon en het ochtendoverzicht tellen die dan niet meer mee. Als je de to-do opent, een chatbericht stuurt, iets bewerkt, de to-do snoozet of er een nieuw bericht binnenkomt, komt die weer terug.

Een project waar een week niets is gebeurd en waarvoor geen open to-do's zijn, kan één keer per week een to-do krijgen met één concrete volgende stap. Dat gebeurt maximaal drie keer per week. Zie [Projecten](projects.md).

Als niets je aandacht nodig heeft, doet je Machine een dutje en is je lijst leeg. Tijdens een controle wordt je Machine wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk toon je alle to-do's of alleen één soort. Op je telefoon en computer staat dezelfde keuze geselecteerd. Als Werk of Privé is geselecteerd, ga je met **Alles tonen** terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, is niet Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook direct over naar de andere weergave: **Alleen privé · Werk · Alles tonen**.

De rij bovenaan de lijst vermeldt de naam van je laatste ochtend- of avondoverzicht en wat erin is geteld, zoals **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om het overzicht opnieuw te lezen. Met **Kopiëren** kun je het overal plakken. Zodra je het opent of op de **×** tikt, staat het op al je apparaten totdat het volgende overzicht verschijnt.

Als er geen recent overzicht is, zie je **Vandaag tot nu toe**: wat er vandaag is gedaan en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt gekozen.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** kun je het project wijzigen of verwijderen. Zie [To-do's voor een project](projects.md#a-projects-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De toegang tot berichten die de to-do mag lezen en versturen, verhuist mee. Met **Ongedaan maken** in de melding verplaats je de to-do terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle berichten waarop die is gebaseerd daar staan, wordt de to-do vanzelf verplaatst en gaat hij verder. Anders zie je **Naar Werk verplaatsen** en wordt er niets verplaatst totdat je erop tikt. Een to-do die je toevoegt zonder Werk of Privé te kiezen, wordt vanzelf verplaatst zodra duidelijk is waar die thuishoort. Tot die tijd staat er geen Werk of Privé bij en blijft de to-do privé.

Een to-do kan altijd de berichten lezen waarop die is gebaseerd. Als de to-do andere berichten uit je andere gebied nodig heeft, vraagt hij je om **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt gelabeld, telt als Privé. Mail voor een ander bedrijf van jou komt terecht bij de to-do's van dat bedrijf. Een to-do over je privéleven, zoals familie die naar je werkadres mailt, is vanaf het begin Privé.

Werk dat via een persoonlijk account bij je binnenkomt, zoals een klant op WhatsApp of een bestelling in je persoonlijke mailbox, is vanaf het begin Werk. Een to-do die je zelf hebt verplaatst of aangemaakt, blijft altijd staan waar je die hebt neergezet. Werk of Privé bepaalt waar een to-do wordt weergegeven en met wie die wordt gedeeld, maar niet waarvandaan die antwoordt. Een antwoord gaat altijd naar de plek waar het gesprek plaatsvindt, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen. Hij wordt nooit weergegeven in een Werk-Fleet of de Team Graph.

Als er twee of meer to-do's zijn waarop je actie moet ondernemen, kun je met **Doorlopen** in de kop van Voor jou de to-do's één voor één afwerken, in de volgorde van de lijst. Je ziet telkens het volledige concept, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat er op het scherm staat, met `S` snooze je, met `→` sla je over en met Esc stop je. Onder de titel staat in de kop ook hoelang het ongeveer duurt als je je eigen tempo aanhoudt, zoals 'ongeveer 2 min'.

Een to-do die je iets vraagt, wordt niet meegenomen in deze twee groepen: die wacht op je antwoord, niet op een tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert wat er is binnengekomen zodra er 40 berichten zijn of zodra het oudste bericht van iemand er 15 minuten staat. Nieuwsbrieven, meldingen en betalingsbewijzen worden meegenomen bij de volgende controle, binnen een uur.

's Nachts worden controles gepauzeerd, van 00:00 tot 06:30. Nieuwe berichten worden nog steeds gelezen en bewaard, en om 06:30 samen gecontroleerd, zodat je to-do's klaarstaan voordat je ochtendoverzicht verschijnt. Bij Controles onder Koppelingen staat 'Gepauzeerd voor de nacht, haalt om 06:30 de achterstand in'. Open de app, schrijf in de chat of tik 's nachts op een to-do en de controles worden weer zoals gebruikelijk uitgevoerd, totdat je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** leest je Machine meteen elke bron. Als er geen open to-do's zijn, tik je op de regel van je Machine om die te zien, met **Details**. Daarmee open je Controles onder Koppelingen. Als er open to-do's zijn, staat de regel bovenaan op een computer. Er staat alleen een korte regel als er een controle bezig is of als die is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare hebben hun eigen tempo.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's een regel met wat er is gevonden, van elke gelezen bron. Bijvoorbeeld: '13 berichten gecontroleerd om 16:11 · niets nodig' of '· 2 nieuwe to-do's'. Als een nieuwe to-do wacht op een beter moment, bijvoorbeeld je ochtendoverzicht, staat erbij tot wanneer: '1 to-do uitgesteld tot morgen 08:30'.

Tik op de regel om elke e-mailthread, chat en melding te bekijken, met het pictogram van de bron erbij: wie het bericht heeft geschreven, het onderwerp of de eerste woorden, en de nieuwe to-do of waarom er niets nodig was. Bijvoorbeeld: 'Alleen in cc, een teamgenoot antwoordt' of 'Afspraak staat al voor donderdag'. Bij een thread staat er geen reden als de controle alleen een vage reden opleverde. Tik op een bericht om het te lezen.

De eerste 10 resultaten worden getoond. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle staan.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails die The Machine zelf naar je stuurt, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met **Snoozen** ernaast. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe het moet worden gedaan of, zodra er een concept klaarstaat, wat daarin moet veranderen. **Markeer als gedaan** betekent dat de to-do is afgehandeld. Bij een to-do die klaarstaat zonder concept zie je deze optie meteen. Anders staat die bovenaan onder **…**, ook bij een to-do waarvoor je eerst een beslissing moet nemen. De to-do verdwijnt meteen van de lijst, met **Ongedaan maken** in de melding. Veeg de melding weg of sleep die met de muis weg om de to-do eerder te sluiten. De wijziging blijft bewaard.

Wil je het op een andere manier laten doen? Zeg dat dan in de **Chat**.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om een review](ask-to-review.md).
- **Herhalen…**: de to-do [komt op vaste momenten terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. De titel blijft staan.

Met **Heropenen** open je een gesloten to-do opnieuw. Die komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van die persoon, maar niet als jij zelf antwoordt.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens die op de rekening staan. Rekeningen die automatisch worden betaald, zoals een automatische incasso of een opgeslagen betaalkaart, worden geen to-do. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld doordat de afzender bevestigt dat de betaling is ontvangen, wordt de to-do vanzelf gesloten. Je kunt die een dag lang terughalen met **Ongedaan maken**.

Een to-do die alleen tot een bepaald moment belangrijk is, zoals een bevestiging vóór een afspraak, wordt na dat moment vanzelf gesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding 'Niet meer nodig'. Je kunt die een dag lang terughalen met **Ongedaan maken**.

Voordat een bericht of overdracht voor iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de mensen erin, ook groepschats, en wacht hij totdat Slack ze heeft gelezen. Als een later bericht laat zien dat het al is geregeld, bijvoorbeeld omdat iemand erom was gevraagd en ja heeft gezegd, wordt de to-do vanzelf gesloten. Je kunt die een dag lang terughalen met **Ongedaan maken**.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een boeking is geannuleerd, werkt The Machine de to-do's zelf bij. Een to-do die nog nodig is, volgt het nieuwe plan. Als er niets meer te doen is, wordt die verplaatst naar **Gedaan / afgewezen** met de melding 'Niet nodig'. In de chat staat dan 'Bijgewerkt:' met de reden erbij. Je kunt de to-do een dag lang terughalen met **Ongedaan maken**.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste opties: **Wijzigingen vragen** en **Niet nodig**. Ook staat erin dat er niets wordt verstuurd totdat je op **Versturen** tikt. De tip verdwijnt voorgoed zodra je de knop gebruikt of op × tikt.

Op je eerste dag zie je bovenaan To-do's een begroeting en de naam van degene die het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat wanneer je aankomt.

Elke to-do begint met de titel. Op de regel eronder staat over wie de to-do gaat, de organisatie als die relevant is (niet alleen omdat iemand daar werkt), het project, Werk of Privé en wanneer de to-do is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en organisatie staat een foto of logo als de Graph die heeft. Anders worden de initialen getoond. Een logo dat op dat formaat niet goed leesbaar is, zoals witte tekst op een transparante achtergrond of een breed woordmerk, wordt ook vervangen door de beginletter.

Soms staat er een subtiele regel met wat niet bekend is, zoals 'Laatste contact 12 dagen geleden via e-mail; sindsdien niets'. Die wordt getoond als het laatste contact oud is of onbeantwoord bleef. Er staan ook kanalen bij die niet gekoppeld zijn, zoals WhatsApp. Je Machine zegt wat hij niet weet in plaats van te gissen.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

De titel zegt wat er moet gebeuren en verandert alleen als dat ook verandert. Een afgeronde to-do houdt zijn titel, met daaronder hoe die is afgerond, zoals 'Gedaan: Sam heeft het dinsdag ondertekend'.

Boven het concept staat een subtiele regel met het bericht waarop het is gebaseerd en het logo van de betreffende dienst. Tik erop om de thread te lezen. Het concept toont het logo van de plek waar het naartoe gaat, zodat je meteen ziet of het bijvoorbeeld om een Slack-antwoord of een e-mail gaat.

Als het concept is gebaseerd op informatie van iemand anders, bijvoorbeeld een suggestie van een teamgenoot in Slack, staat dat op een regel, zoals 'Gebaseerd op Sam in #ops'. Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, met de oudste berichten eerst: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je berichten rechts, net als in de app. Bij het bericht van de to-do staat 'Deze to-do' en het wordt geopend in de weergave. Met **Eerdere berichten tonen** voeg je oudere berichten toe. De rest van een e-mailthread wordt ingeklapt boven en onder de e-mail weergegeven.

Bij **Details** van een e-mail zie je alleen informatie die niet in de kop staat, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets extra's is, wordt er niets getoond.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. Met de link van een to-do naar het bijbehorende bericht open je het hier ook, met **Openen in Slack** onderaan.

Bij **Details** zie je de naam, het project en het gebied (tik erop om het te wijzigen), je laatste notitie en het resultaat van een codeerassistent. Met **Chat ›** open je de chat. Een afgeronde to-do blijft kort. Het bericht waarop de to-do is gebaseerd, staat onder **Details**.

Een to-do met 'Wacht op' bevat een link naar je laatste bericht aan die persoon, het bericht waarop je wacht: 'E-mail aan Pat · di'.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer) voeg je een to-do toe voor wat dan ook. Als je een to-do maakt, wordt er niets verstuurd. Als je Werk of Privé niet kiest, komt de to-do terecht waar die thuishoort, op basis van wie en waarover die gaat. Je Machine zoekt ook de e-mail op waar de to-do een vervolg op is, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, zoals 'morgen', 'volgende vr', '3 nov', '14:00' of 'over 2 uur'. Dat kan ook in je eigen taal. Met het kalenderpictogram zie je snelle opties en **Kies een datum**.
- **Bericht**: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack-, Teams-, WhatsApp-, Telegram- of ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat zie je waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een schermafbeelding of sleep bestanden naar het formulier. Op een telefoon kun je met de camera ernaast een foto maken. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en The Machine leest ze wanneer hij eraan werkt. Alleen bestanden zijn al genoeg: The Machine vult de to-do in op basis van een PDF- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om die op ware grootte te bekijken.
