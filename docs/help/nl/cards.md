---
title: To-do's
area: cards
summary: Eén to-do voor elke zaak die aandacht van je vraagt, klaar om goed te keuren. Lees wat de onderdelen van een to-do betekenen.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 6cbbad37c4dfaf07
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do als er iets van je nodig is. Eén to-do per zaak, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze bij elkaar:

- **Net gedaan**: bovenaan staat de laatste stap die je hebt bevestigd, zoals een formulier of een issue dat is afgehandeld terwijl je weg was. Deze blijft maximaal een dag staan, totdat je op **Begrepen** tikt. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (het werk is gedaan en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (je moet eerst een beslissing nemen of antwoord geven), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of briefing waarover je niets hoeft te beslissen).
- **Wacht op anderen**: ingeklapte to-do's waarbij de volgende stap bij iemand anders ligt (zie hieronder).
- **Komt later terug**: to-do's die je hebt gesnoozed en to-do's waarop geen antwoord kwam op **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Bekijk [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, nieuwste eerst, met het tijdstip waarop ze zijn afgerond, zoals '5 minuten geleden gedaan'. To-do's die al afgerond lijken, zijn gemarkeerd als **Lijkt gedaan**.

Nadat je iets hebt verstuurd, staat er kort waar de to-do naartoe is verplaatst, zoals 'Verstuurd. Verplaatst naar Gedaan.' of 'Verstuurd. Verplaatst naar Later tot ma.'. Met **Openen** ga je naar de to-do. Met Zoeken vind je een to-do op titel of op de ontvanger, ook in Later en Gedaan.

Onder **Voor jou** staan eerst to-do's waarvan de deadline is verstreken of morgen valt, daarna vragen van je Fleet, vervolgens vervolgacties van een bord en dan de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem voorbereidt en wanneer hij klaar is. Alleen de markering verandert. In de andere open groepen staan to-do's waarvan de deadline is verstreken of morgen valt bovenaan, gevolgd door de rest, nieuwste eerst. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets is afgerond, bijvoorbeeld 'PR #3451 samengevoegd', maar dat het nog niet is afgesloten. Met **Heropenen** zet je de to-do terug op je lijst en leert je Machine ervan. Deze to-do's worden nooit als te laat weergegeven. Na een dag wordt de to-do automatisch afgesloten. Je kunt dat ongedaan maken met **Ongedaan maken**. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook automatisch afgesloten.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, bijvoorbeeld sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: 'Dit is niet Sam Lee.' De afzender wordt weergegeven met zijn eigen adres, nooit met de naam die hij heeft opgegeven. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Een to-do die nog op iemand anders wacht, bijvoorbeeld op een beoordeling of antwoord, vermeldt bij **Wacht op** welke stap dat is. De to-do staat ingeklapt onder **Wacht op anderen**, boven Komt later terug, totdat een nieuw bericht hem weer naar voren haalt. Hetzelfde geldt nadat je zelf een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline als die later vandaag valt, of de volgende ochtend als de deadline al verstreken is. Er staat dan ook op wie de to-do nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet opleveren, zoals een ondertekend contract, staat dat bij **Details** onder **Klaar als**. Je eigen deel versturen sluit de to-do niet af. Hij blijft onder **Wacht op anderen** staan totdat een bericht het resultaat laat zien. Daarna wordt hij automatisch afgesloten. Je kunt dat ongedaan maken met **Ongedaan maken**. Als er niets binnenkomt tegen de tijd dat je erachteraan moet, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Als een to-do een week onaangeroerd blijft, vraagt hij één keer: **Nog nodig?** Met **Niet nodig** sluit je hem af. Je kunt dit ongedaan maken met **Ongedaan maken**. Met **Houden** houd je de to-do en wordt de vraag niet opnieuw gesteld. Komt er nog een week geen antwoord, dan wordt de to-do ingeklapt onder Komt later terug. Hij telt dan niet meer mee op het appicoon en in het ochtendoverzicht. Als je de to-do opent, een chatbericht stuurt, hem bewerkt, snoozet of er een nieuw bericht binnenkomt, komt hij weer terug.

Een project dat een week stil ligt en geen openstaande to-do's heeft, kan één keer per week een to-do krijgen met één concrete volgende stap. Dat gebeurt maximaal drie keer per week. Bekijk [Projecten](projects.md).

Als er niets is dat je aandacht vraagt, wacht je Machine rustig op een lege lijst. Tijdens een controle wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk toon je alle to-do's of alleen to-do's van één type. Op je telefoon en computer geldt dezelfde keuze. Als Werk of Privé is geselecteerd, brengt **Alles tonen** je terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, valt niet onder Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook meteen over naar de andere weergave: tik onder **Alleen privé** op **Werk** of **Alles tonen**.

De bovenste rij in de lijst toont de naam van je laatste ochtend- of avondoverzicht en wat erin werd geteld, bijvoorbeeld **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om het overzicht opnieuw te lezen, met **Kopiëren** om het ergens te plakken. Zodra je het opent of op de **×** tikt, blijft het op al je apparaten staan totdat het volgende overzicht verschijnt.

Als er geen recent overzicht is, zie je **Vandaag tot nu toe**: wat vandaag is afgerond en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt geselecteerd.

Een to-do voor een project toont de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Bekijk [To-do's voor een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De toegang tot berichten die de to-do mag lezen en versturen, verhuist mee. Met **Ongedaan maken** in de melding verplaats je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle berichten waaruit hij is ontstaan daar staan, wordt hij automatisch verplaatst en gaat hij verder. Anders zie je **Naar Werk verplaatsen**. Er wordt niets verplaatst totdat je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt automatisch verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd valt hij niet onder Werk of Privé en blijft hij privé.

Een to-do kan altijd de berichten lezen waaruit hij is ontstaan. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt ingesteld, telt als Privé. Mail voor een ander bedrijf van jou gaat naar de to-do's van dat bedrijf. Een to-do over je privéleven, bijvoorbeeld familie die naar je werkadres mailt, valt vanaf het begin onder Privé.

Werk dat je via een persoonlijk account bereikt, zoals een klant via WhatsApp of een bestelling in je persoonlijke mailbox, valt vanaf het begin onder Werk. Een to-do die je zelf hebt verplaatst of aangemaakt, blijft altijd staan waar je hem hebt gezet. Werk of Privé bepaalt waar een to-do wordt weergegeven en met wie hij wordt gedeeld, nooit waar hij op berichten antwoordt. Een antwoord gaat altijd naar de plek waar het gesprek plaatsvindt, ook nadat een to-do is verplaatst, tenzij je een andere manier kiest.

Zo'n to-do onder Privé antwoordt nog steeds vanaf het werkadres waarop de e-mail is binnengekomen. Hij wordt nooit weergegeven in een Fleet voor Werk of in de Team Graph.

Als er twee of meer to-do's wachten, kun je met **Doorlopen** in de kop van Voor jou de to-do's één voor één afwerken, in de volgorde van de lijst. Je ziet elk concept volledig, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Druk op een computer op Enter om te versturen wat op het scherm staat, op `S` om te snoozen, op `→` om over te slaan en op Esc om te stoppen. Onder de titel vermeldt de kop ook hoelang de to-do's duren als je je eigen tempo aanhoudt, bijvoorbeeld 'ongeveer 2 min'.

Een to-do die je een vraag stelt, wordt niet meegenomen. Daarvoor is je antwoord nodig, niet een tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Hij controleert de binnengekomen berichten zodra er 40 berichten klaarstaan of het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en ontvangstbewijzen neemt hij mee bij de volgende controle, binnen een uur.

Tussen 00:00 en 06:30 liggen controles 's nachts stil. Nieuwe berichten worden nog steeds gelezen en bewaard, en om 06:30 samen gecontroleerd, zodat je to-do's klaarstaan voordat je ochtendoverzicht verschijnt. Bij Controles onder Koppelingen staat 'Nachtpauze, haalt de achterstand in om 06:30'. Klik, typ of scroll je in de app, schrijf je in de chat of tik je 's nachts op een to-do, dan worden de controles weer zoals gewoonlijk uitgevoerd totdat je een uur weg bent geweest. Met **Nu checken** controleer je altijd meteen.

Met **Nu checken** leest je Machine alle bronnen meteen. Als er niets openstaat, tik je op de regel van je Machine om die te bekijken, met **Details** om Controles onder Koppelingen te openen. Als er to-do's openstaan, staat de regel bovenaan op een computer. Een korte regel wordt daar alleen weergegeven als er een controle loopt of als er een is mislukt of te laat is. Je kunt er ook naar vragen in de chat.

LinkedIn, X en Salesflare houden hun eigen tempo aan.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's wat er is gevonden, uit alle bronnen die zijn gelezen. Bijvoorbeeld: '13 berichten gecontroleerd om 16:11 · niets vraagt je aandacht' of '· 2 nieuwe to-do's'. Als een nieuwe to-do moet wachten op een beter moment, zoals je ochtendoverzicht, staat erbij tot wanneer: '1 to-do uitgesteld tot morgen 08:30'.

Tik op de regel om alle e-mailthreads, chats en meldingen te zien, met het pictogram van de betreffende bron: wie het bericht heeft geschreven, het onderwerp of de eerste woorden, en de nieuwe to-do of de reden dat er niets nodig was. Bijvoorbeeld 'Alleen in cc, een teamgenoot antwoordt' of 'Vergadering staat al op donderdag'. Als de controle alleen een vage reden opleverde, wordt er geen reden bij de thread getoond. Tik erop om het bericht te lezen.

De eerste 10 worden weergegeven. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat bevat. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle staan.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails van The Machine zelf, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt gewoon gelezen.

## De knoppen

Een to-do toont de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met **Snoozen** ernaast. Bekijk [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets moet worden gedaan of, als er een concept klaarstaat, wat je daarin wilt aanpassen. **Markeer als gedaan** betekent dat de to-do is afgehandeld. Bij een klaargezette to-do zonder concept staat deze optie meteen in beeld. Anders staat hij bovenaan onder **…**, ook bij een to-do waarvoor je een beslissing moet nemen. De to-do verdwijnt meteen van de lijst. In de melding staat **Ongedaan maken**. Veeg de melding weg of sleep hem met de muis opzij om de to-do eerder af te sluiten. De wijziging blijft staan.

Wil je dat de to-do op een andere manier wordt afgehandeld, vertel dat dan in de **Chat**.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om iets te beoordelen](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast ritme terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. De titel die je kiest, blijft staan.

Met **Heropenen** zet je een afgesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van de ander, maar niet door je eigen antwoord.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals via automatische incasso of een opgeslagen kaart, worden geen to-do. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld doordat de afzender bevestigt dat je betaling is ontvangen, wordt de to-do automatisch afgesloten. Je kunt hem een dag lang terughalen met **Ongedaan maken**.

Een to-do die maar tot een bepaald moment belangrijk was, zoals een bevestiging vóór een vergadering, wordt na dat moment automatisch afgesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de status 'Niet meer nodig'. Je kunt hem een dag lang terughalen met **Ongedaan maken**.

Voordat een bericht of overdracht voor iemand als klaargezet wordt weergegeven, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als uit een later bericht blijkt dat het al is geregeld, bijvoorbeeld omdat iemand erom is gevraagd en ja heeft gezegd, wordt de to-do automatisch afgesloten. Je kunt hem een dag lang terughalen met **Ongedaan maken**.

Als een nieuwer bericht het plan verandert, bijvoorbeeld doordat een feest naar een andere locatie is verplaatst of een reservering is geannuleerd, werkt The Machine de to-do's zelf bij. Een to-do die nog steeds nodig is, volgt het nieuwe plan. Als er niets meer te doen is, wordt de to-do verplaatst naar **Gedaan / afgewezen** met de status 'Niet nodig'. In de chat staat 'Bijgewerkt:' met de reden. Je kunt de to-do een dag lang terughalen met **Ongedaan maken**.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**. Ook staat erin dat er niets wordt verstuurd voordat je op **Versturen** drukt. Een tip verdwijnt definitief zodra je de knop gebruikt of op × drukt.

Op je eerste dag heet de bovenkant van To-do's je welkom en staat er wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat wanneer je aankomt.

Elke to-do begint met de titel. Op de regel eronder staat op wie de to-do betrekking heeft, de organisatie als die relevant is (niet alleen omdat iemand er werkt), het project, Werk of Privé en wanneer de to-do is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en organisatie wordt een foto of logo getoond als die in de Graph staat. Anders worden de initialen getoond. Als een logo op klein formaat niet leesbaar zou zijn, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, worden ook de initialen getoond.

Soms staat er een subtiele regel met wat niet bekend is, zoals 'Laatste contact 12 dagen geleden via e-mail; sindsdien niets'. Deze verschijnt als het laatste contact met die persoon lang geleden was of onbeantwoord bleef. Ook worden niet-gekoppelde kanalen genoemd, zoals WhatsApp. Je Machine vertelt wat hij niet weet in plaats van te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

De titel zegt wat er moet gebeuren en verandert alleen als dat ook verandert. Een afgeronde to-do behoudt zijn titel, met daaronder hoe hij is afgerond, zoals 'Gedaan: Sam heeft het dinsdag ondertekend'.

Boven het concept staat een lichtgekleurde regel met de naam van het bericht waaruit de to-do is ontstaan en het logo van die dienst. Tik erop om de thread te lezen. Het concept toont het logo van de bestemming, zodat je meteen ziet of het om een antwoord in Slack of een e-mail gaat.

Als het concept is gebaseerd op iemands inbreng op een andere plek, bijvoorbeeld een suggestie van een teamgenoot in Slack, staat dat op een regel, zoals 'Gebaseerd op Sam in #ops'. Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, van oud naar nieuw: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je berichten rechts, net als in de app. Het bericht van de to-do is gemarkeerd met 'Deze to-do' en wordt meteen geopend. Met **Eerdere berichten tonen** voeg je oudere berichten toe. De rest van een e-mailthread wordt ingeklapt boven en onder het bericht weergegeven.

Onder **Details** van een e-mail staan alleen gegevens die niet in de kop staan, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets toe te voegen is, staat er niets.

Bij een antwoord in een Slack-thread wordt ook getoond wat er vóór de start van de thread is gezegd. Met de link van een to-do naar zijn eigen bericht open je het bericht hier ook, met **Openen in Slack** onderaan.

Onder **Details** staan de naam, het project en het gebied (tik op een onderdeel om het te wijzigen), je laatste notitie en het resultaat van een programmeeragent. Met de titel open je de chat. Een afgeronde to-do blijft ingeklapt. Het bericht waaruit hij is ontstaan, staat onder **Details**.

Bij een to-do met de status 'Wacht op' linkt je laatste bericht aan de ander naar het bericht waarop je wacht, bijvoorbeeld: 'E-mail aan Pat · di'.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor wat dan ook. Als je er een maakt, wordt er niets verstuurd. Als je geen **Werk** of **Privé** kiest, komt hij terecht waar hij hoort, op basis van wie en wat erin voorkomt. De to-do vindt ook de e-mail op waarop hij een vervolg is, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, zoals 'morgen', 'volgende vr', '3 nov', '14:00' of 'over 2 uur'. Dat kan ook in je eigen taal. Met het kalenderpictogram zie je snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt volgens een vast ritme terug. Bekijk [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waarop de to-do betrekking heeft, maximaal 5.
- Berichtenpictogram: voeg het bericht toe waarop de to-do betrekking heeft: een e-mail, Slack-, Teams-, WhatsApp- of Telegram-bericht, of een ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat zie je waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon kun je met de camera ernaast een foto maken. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (bekijk [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en The Machine leest ze wanneer hij eraan werkt. Je kunt ook alleen bestanden toevoegen. The Machine vult de to-do dan in op basis van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op volledig formaat te bekijken.
