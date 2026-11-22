---
title: To-do's
area: cards
summary: Eén to-do voor elke zaak waarvoor je iets moet doen, klaar om door jou goed te keuren. Lees wat de onderdelen van een to-do betekenen.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e7e5d78b3291e556
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do als er iets van je nodig is. Eén to-do per zaak, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze in groepen:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een issue, en die is uitgevoerd terwijl je weg was. Hij blijft daar staan totdat je op **Begrepen** tikt, maximaal één dag. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (een concept of resultaat is klaar, en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (eerst is je beslissing of antwoord nodig; als het werk is gestopt omdat alleen jij iets kunt aanleveren, zoals een feit, inloggegevens of een keuze, staat dat onder de titel), **Aan het voorbereiden…** (je Machine werkt eraan) of **Om te lezen** (een overzicht of briefing, waarover je niets hoeft te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws mee is gebeurd (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarbij iemand anders aan zet is (zie hieronder).
- **Komt later terug**: gesnoozede to-do's en to-do's waarop geen antwoord is gekomen op **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Lees [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het moment waarop ze zijn afgerond, zoals ‘5 minuten geleden afgerond’. To-do's die al afgerond lijken, zijn gemarkeerd als **Lijkt gedaan**.

Na het versturen verschijnt een korte melding met de bestemming van de to-do, zoals ‘Verstuurd. Verplaatst naar Gedaan.’ of ‘Verstuurd. Verplaatst naar Later tot ma.’ Een antwoord dat alleen belooft het werk te doen, zoals ‘Ik stuur het dinsdag’, laat de to-do open: ‘Verstuurd. Open gelaten.’ Met **Openen** ga je naar de to-do. Zoeken vindt to-do's op titel of op de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan to-do's met een verstreken deadline of een deadline uiterlijk morgen bovenaan, daarna vragen van je Fleet, vervolgens vervolgacties van een bord en dan de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem voorbereidt en wanneer hij is afgerond. Alleen de markering verandert. In de andere open groepen staan to-do's met een verstreken deadline of een deadline uiterlijk morgen bovenaan, en daarna de nieuwste. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat het werk af is, zoals ‘PR #3451 samengevoegd’, maar dat de to-do nog niet is gesloten. Met **Heropenen** zet je hem terug op je lijst. Je Machine leert ervan. Deze to-do's worden nooit als te laat getoond. Na een dag sluit hij vanzelf, met **Ongedaan maken** als optie. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld door te antwoorden in Gmail of Slack, sluit ook vanzelf.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: ‘Dit is Sam Lee niet.’ De afzender wordt weergegeven met diens eigen adres, nooit met de naam die diegene heeft gebruikt. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, bijvoorbeeld op een beoordeling of antwoord, staat **Wacht op:** met de volgende stap. De to-do staat ingeklapt onder **Wacht op anderen**, boven Komt later terug, totdat een nieuw bericht hem weer naar voren haalt. Dat gebeurt ook nadat je een vraag hebt teruggestuurd: de to-do komt terug op de ochtend voor de deadline, op de deadline zelf als die later vandaag is, of de volgende ochtend zodra de deadline is verstreken. Je ziet dan nog steeds op wie hij wacht.

Als een to-do gaat over een resultaat dat iemand anders moet aanleveren, zoals een ondertekend contract, staat dat bij **Details** onder **Klaar als**. Het versturen van jouw deel sluit de to-do niet af. Hij blijft onder **Wacht op anderen** staan totdat een bericht het resultaat bevestigt. Daarna sluit hij vanzelf, met **Ongedaan maken** als optie. Als er niets binnenkomt tegen de tijd dat je diegene moet herinneren, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Een to-do waar een week niets nieuws mee is gebeurd, wordt verplaatst van Voor jou naar **Ouder**, zodat nieuwe to-do's bovenaan staan als je een paar dagen weg bent geweest. Er is niets nieuws gebeurd als er geen nieuw bericht over de to-do is en jij er niets mee hebt gedaan, zoals een chatbericht sturen, iets bewerken of snoozen. Alleen bekijken telt niet.

Dringende to-do's, to-do's met een naderende deadline en to-do's die onderweg zijn om te worden verstuurd, blijven bij Voor jou staan. Met **Alles afwijzen** markeer je alle to-do's onder Ouder na één bevestiging als niet nodig, net als met **Niet nodig**, maar dan één voor één. Je kunt dit **Ongedaan maken**. Als er iets nieuws gebeurt met een to-do, komt hij weer bij Voor jou te staan.

Bij een to-do waar een week niemand iets mee heeft gedaan, verschijnt één keer de vraag **Nog nodig?**. Met **Niet nodig** sluit je de to-do, met **Ongedaan maken** als optie. Met **Houden** bewaar je hem en wordt de vraag niet opnieuw gesteld. Komt er de volgende week geen antwoord, dan wordt de to-do ingeklapt onder Komt later terug. Hij telt dan niet meer mee op het appicoon of in het ochtendoverzicht. Als je hem opent, een chatbericht stuurt, iets bewerkt of snoozet, of als er een nieuw bericht binnenkomt, komt hij weer terug.

Een project waar al een tijd niets is gebeurd en geen open to-do's meer bij staan, kan eens per week een to-do krijgen met één concrete volgende stap. Dit gebeurt maximaal drie keer per week. Lees [Projecten](projects.md).

Als je niets hoeft te doen, rust je Machine uit en is je lijst leeg. Tijdens een controle wordt hij wakker en laat hij dat weten. Als een controle is mislukt of is vertraagd, staat dat in de melding, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk toon je alle to-do's of alleen to-do's van één soort. Je telefoon en computer gebruiken dezelfde keuze. Als Werk of Privé is geselecteerd, brengt **Alles tonen** je terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, hoort niet bij Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook meteen naar de andere weergave: tik bij **Alleen privé** op **Werk** of **Alles tonen**.

De rij bovenaan de lijst toont de naam van je laatste ochtend- of avondoverzicht en wat daarin is meegeteld, zoals **Avondoverzicht van gisteren** · 12 afgerond, 3 open. Tik erop om het overzicht opnieuw te lezen. Met **Kopiëren** kopieer je het om ergens anders te plakken. Zodra je het opent of op de **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Als er geen recent overzicht is, zie je **Vandaag tot nu toe**: wat er vandaag is afgerond en wat nog openstaat, voor Werk en Privé, of alleen voor de weergave die je hebt gekozen.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Lees [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De toegang tot berichten die je Machine mag lezen en versturen, verhuist mee. Met **Ongedaan maken** in de melding zet je de to-do terug.

Als een to-do naar je andere gebied moet om verder te kunnen en alle berichten waar hij vandaan komt daar staan, wordt hij vanzelf verplaatst en gaat het werk verder. Anders zie je **Naar Werk verplaatsen** en wordt er niets verplaatst totdat je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt vanzelf verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd staat er geen Werk of Privé bij en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij vandaan komt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt aangemerkt, telt als Privé. Mail voor een ander bedrijf van jou komt bij de to-do's van dat bedrijf terecht. Een to-do over je privéleven, zoals familie die naar je werkadres schrijft, is vanaf het begin Privé.

Werk dat je op een persoonlijk account ontvangt, zoals een klant op WhatsApp of een bestelling in je persoonlijke mailbox, is vanaf het begin Werk. Een to-do die je zelf hebt verplaatst of ingesteld, blijft altijd staan waar je hem hebt neergezet. Werk of Privé bepaalt waar een to-do verschijnt en met wie hij wordt gedeeld, maar nooit waarvandaan hij antwoordt. Een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de mail binnenkwam. Hij verschijnt nooit in een Work Fleet of de Team Graph.

Als er twee of meer to-do's wachten, doorloopt **Doorlopen** in de kop van Voor jou ze één voor één, in de volgorde van de lijst. Je ziet elk concept volledig, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat op het scherm staat, snoozet `S`, slaat `→` over en stopt Esc. Onder de titel geeft de kop ook aan hoeveel tijd ze in je eigen tempo kosten, zoals ‘ongeveer 2 min’.

Een to-do die je iets vraagt, wordt overgeslagen. Daarvoor is een antwoord nodig, geen tik.

## Nu checken

Je Machine leest elke bron om de paar minuten, dag en nacht. Zodra er 40 berichten klaarstaan of het oudste bericht van iemand 15 minuten heeft gewacht, controleert hij wat er is binnengekomen. Nieuwsbrieven, meldingen en ontvangstbewijzen worden binnen een uur meegenomen bij de volgende controle.

's Nachts, van 00:00 tot 06:30, worden controles gepauzeerd. Nieuwe berichten worden nog steeds gelezen en bewaard, en om 06:30 tegelijk gecontroleerd, zodat je to-do's klaarstaan voordat je ochtendoverzicht verschijnt. Bij Koppelingen staat onder Controles: ‘Nachtpauze, haalt om 06:30 in’. Klikken, typen of scrollen in de app, iets schrijven in de chat of 's nachts op een to-do tikken, zorgt ervoor dat controles weer normaal lopen totdat je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** leest je Machine meteen alle bronnen. Als er niets openstaat, tik je op de regel van je Machine om die te bekijken, met **Details**. Daarmee open je Controles onder Koppelingen. Als er to-do's openstaan, staat de optie bovenaan op een computer. Een korte melding wordt daar alleen getoond als er een controle bezig is, is mislukt of is vertraagd. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare houden hun eigen tempo aan.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's een regel met wat er is gevonden in elke gecontroleerde bron, zoals ‘13 berichten gecontroleerd om 16:11 · niets nodig’ of ‘· 2 nieuwe to-do's’. Als een nieuwe to-do op een geschikter moment wacht, zoals je ochtendoverzicht, staat erbij tot wanneer: ‘1 to-do uitgesteld tot morgen 08:30’.

Tik op de regel om elk e-mailgesprek, elke chat en elke melding te bekijken, met het pictogram van de bron. Je ziet wie het bericht heeft geschreven, het onderwerp of de eerste woorden, en de nieuwe to-do of waarom er niets nodig was, zoals ‘Alleen in cc, een teamgenoot antwoordt’ of ‘Afspraak staat al voor donderdag’. Als de controle alleen een vage reden opleverde, wordt er bij een gesprek geen reden getoond. Tik op een gesprek om het te lezen.

De eerste 10 worden getoond. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle staan.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar gelden niet als nieuwe mail. E-mails die je Machine zelf naar je stuurt, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of vermeld. Mail over facturering, je proefperiode of een uitnodiging wordt gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met daarnaast **Snoozen**. Lees [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe het moet gebeuren, of, zodra een concept klaarstaat, wat daarin moet veranderen. **Markeren als gedaan** betekent dat je het hebt afgehandeld. Bij een klaargezette to-do zonder concept staat deze optie meteen in beeld; anders staat hij bovenaan onder **…**, ook bij een to-do waarvoor je eerst een beslissing moet nemen. De to-do verdwijnt meteen van de lijst. In de melding staat **Ongedaan maken**. Veeg de melding weg of sleep hem met de muis van het scherm om hem sneller te sluiten. De wijziging blijft bewaard.

Wil je dat het op een andere manier gebeurt, zeg dat dan in de **Chat** van de to-do.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om een beoordeling](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast schema terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt het ook in de chat vragen, bijvoorbeeld: ‘Hernoem dit naar …’. Je titel blijft staan.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van de ander, maar niet als jij zelf antwoordt. Je ziet dan wanneer de to-do is teruggekomen en hij wordt als nieuw gesorteerd. De chat gaat verder waar hij gebleven was, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals via automatische incasso of een opgeslagen kaart, worden geen to-do. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld een bevestiging van de afzender dat de betaling is ontvangen, wordt de to-do vanzelf gesloten. Je kunt dit een dag lang **Ongedaan maken**.

Een to-do die maar tot een bepaald moment relevant was, zoals een bevestiging voor een vergadering, wordt na dat moment vanzelf gesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet meer nodig’. Je kunt dit een dag lang **Ongedaan maken**.

Voordat een bericht of overdracht voor iemand als klaargezet wordt getoond, controleert je Machine je recente chats met de betrokkenen, ook groepschats, en wacht hij tot Slack ze heeft gelezen. Als een later bericht laat zien dat het al geregeld is, bijvoorbeeld omdat iemand is gevraagd en ja heeft gezegd, wordt de to-do vanzelf gesloten. Je kunt dit een dag lang **Ongedaan maken**.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie verhuist of een boeking vervalt, werkt The Machine zijn to-do's zelf bij. Een to-do die nog nodig is, volgt het nieuwe plan. Is er niets meer te doen, dan wordt hij verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet nodig’. In de chat staat ‘Bijgewerkt:’ met de reden. Je kunt dit een dag lang **Ongedaan maken**.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste opties: **Wijzigingen vragen** en **Niet nodig**. Ook staat erin dat er niets wordt verstuurd totdat je op **Versturen** drukt. De tip verdwijnt definitief zodra je de bijbehorende knop gebruikt of op × drukt.

Op je eerste dag heet de bovenkant van To-do's je welkom en staat erbij wie het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat als je binnenkomt.

Elke to-do begint met een titel. De regel eronder vermeldt op wie de to-do betrekking heeft, de organisatie als het daarover gaat (niet alleen omdat iemand er werkt), het project, Werk of Privé en wanneer de to-do is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en organisatie staat een foto of logo als dat in de Graph beschikbaar is, en anders staan de initialen er. Als een logo op klein formaat niet leesbaar is, bijvoorbeeld omdat het wit op een transparante achtergrond staat of een brede woordmarkering is, worden ook de initialen getoond.

Soms staat er een korte, gedempte melding over wat niet bekend is, zoals ‘Laatste contact 12 dagen geleden via e-mail; sindsdien niets.’ Die verschijnt als het laatste contact met iemand lang geleden was of op een antwoord wacht. Er worden ook kanalen genoemd die niet zijn gekoppeld, zoals WhatsApp. Je Machine vertelt wat hij niet weet in plaats van te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

Een titel zegt wat er moet gebeuren en verandert alleen als dat ook verandert. Een afgeronde to-do behoudt zijn titel, met daaronder hoe hij is afgerond, zoals ‘Gedaan: Sam heeft het dinsdag ondertekend’.

Boven het concept staat in een gedempte regel van welk bericht het afkomstig is, met het logo van de dienst. Tik erop om het gesprek te lezen. Bij het concept staat het logo van de plek waar het naartoe gaat. Zo zie je meteen of het om een Slack-antwoord of een e-mail gaat.

Als het concept voortbouwt op input van iemand anders, bijvoorbeeld een suggestie van een teamgenoot in Slack, staat dat in een regel, zoals ‘Gebaseerd op Sam in #ops’. Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt als één gesprek weergegeven, van oud naar nieuw: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan jouw berichten rechts, net als in de app. Het bericht van de to-do is gemarkeerd met ‘Deze to-do’ en opent in de weergave. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Bij een e-mail staat de rest van het gesprek ingeklapt erboven en eronder.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is binnengekomen. Op Android wordt de Gmail-app geopend als je die hebt.

Bij **Details** van een e-mail staat alleen informatie die niet in de kop staat, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets aan toe te voegen is, zijn er geen Details.

Bij een antwoord in een Slack-thread worden ook de berichten getoond die vóór het begin van de thread zijn verstuurd. Met de link naar het eigen bericht van een to-do open je dat bericht hier ook, met onderaan **Openen in Slack**.

Bij **Details** staan de naam, het project en het gebied (tik erop om ze te wijzigen), je laatste notitie en het resultaat van een codeeragent. De titel opent de chat. Een afgeronde to-do blijft kort; het bericht waar hij vandaan komt, staat onder **Details**.

Bij een to-do met ‘Wacht op’ staat een link naar je laatste bericht aan diegene, waarop je wacht: ‘E-mail aan Pat · di’.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor wat dan ook. Een to-do maken verstuurt niets. Als je geen **Werk** of **Privé** kiest, komt hij terecht waar hij hoort, op basis van wie en waarover hij gaat. Je Machine vindt ook de e-mail waarop de to-do een vervolg is, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, zoals ‘morgen’, ‘volgende vr’, ‘3 nov’, ‘14:00’ of ‘over 2 uur’. Dat kan ook in je eigen taal. Met het kalendericoon krijg je snelle opties en **Kies een datum**.
- **Herhaalt**: de to-do komt volgens een vast schema terug. Lees [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waar de to-do over gaat, maximaal 5.
- Berichticoon: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack-, Teams-, WhatsApp-, Telegram- of ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon maakt de camera ernaast een foto. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en The Machine leest ze wanneer hij eraan werkt. Alleen bestanden toevoegen is genoeg: de to-do wordt automatisch ingevuld op basis van een PDF of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op ware grootte te bekijken.
