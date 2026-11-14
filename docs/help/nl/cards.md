---
title: To-do's
area: cards
summary: Eén to-do per zaak waarvoor je iets moet doen, klaar om door jou goedgekeurd te worden. Dit betekenen de onderdelen van een to-do.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 12be97d431968927
---
Je Machine leest alles wat nieuw binnenkomt en maakt alleen een to-do als er iets van je nodig is. Eén to-do per zaak, ongeacht hoeveel berichten erbij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze gegroepeerd:

- **Net gedaan**: bovenaan staat de laatste stap die je hebt bevestigd, zoals een formulier of een issue dat is verwerkt terwijl je weg was. Hij blijft maximaal een dag staan, totdat je op **Begrepen** tikt. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met het dringendste bovenaan. Bij elke to-do staat **Klaargezet** (het werk is gedaan en met **Doe het** of **Versturen** wordt het uitgevoerd), **Wacht op jou** (je moet eerst een beslissing nemen of antwoord geven), **Aan het voorbereiden…** (je Machine is ermee bezig) of **Om te lezen** (een overzicht of korte briefing, zonder beslissing).
- **Wacht op anderen**: ingeklapt staan hier to-do's waarvan de volgende stap bij iemand anders ligt (zie hieronder).
- **Komt later terug**: gesnoozede to-do's en to-do's waarop niemand heeft gereageerd op **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Zie [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en erbij wanneer ze zijn afgerond, zoals 'Gedaan 5 minuten geleden'. To-do's die al afgerond lijken, zijn gemarkeerd als **Lijkt gedaan**.

Nadat je iets verstuurt, staat er kort waar de to-do naartoe is gegaan, zoals 'Verstuurd. Verplaatst naar Gedaan.' of 'Verstuurd. Verplaatst naar Later tot ma.' Met **Openen** ga je naar de to-do. Met Zoeken vind je een to-do op titel of op de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan to-do's waarvan de deadline is verstreken of uiterlijk morgen valt bovenaan, gevolgd door vragen van je Fleet, daarna de follow-ups van een bord en dan de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek staan terwijl je Machine hem klaarmaakt en wanneer hij is afgerond. Alleen de markering verandert. In de andere open groepen staan to-do's waarvan de deadline is verstreken of uiterlijk morgen valt bovenaan, gevolgd door de rest, met de nieuwste bovenaan. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets is afgerond, zoals 'PR #3451 merged', maar dat de to-do nog niet is gesloten. Met **Heropenen** zet je hem terug op je lijst en leert je Machine ervan. Deze to-do's worden nooit als te laat getoond. Na een dag sluit hij vanzelf, met **Ongedaan maken** als optie. Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, sluit ook vanzelf.

Als een bericht afkomstig is van een adres dat lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, vermeldt de to-do dat duidelijk: 'Dit is Sam Lee niet.' De afzender wordt weergegeven met het eigen adres, nooit met de naam die diegene gebruikte. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Bij een to-do die nog op iemand anders wacht, zoals een beoordeling of antwoord, staat **Wacht op:** met de stap die nog moet gebeuren. De to-do staat ingeklapt onder **Wacht op anderen**, boven Komt later terug, totdat een nieuw bericht hem weer laat verschijnen. Hetzelfde geldt nadat je een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline zelf als die later vandaag valt, of de volgende ochtend als de deadline is verstreken. Er staat dan ook op wie hij nog wacht.

Gaat een to-do over een resultaat dat iemand anders moet opleveren, zoals een ondertekend contract, dan staat dat bij **Details** onder **Klaar als**. Als je jouw deel verstuurt, wordt de to-do niet gesloten. Hij blijft onder **Wacht op anderen** staan totdat een bericht het resultaat bevestigt. Daarna sluit hij vanzelf, met **Ongedaan maken** als optie. Als er niets binnenkomt tegen de tijd dat je diegene moet herinneren, verschijnt de to-do opnieuw met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Als niemand een week iets met een to-do heeft gedaan, vraagt hij één keer: **Nog nodig?** Met **Niet nodig** sluit je hem, met **Ongedaan maken** als optie. Met **Houden** blijft hij staan en vraagt hij het niet nog een keer. Als er daarna nog een week geen antwoord komt, wordt hij ingeklapt onder Komt later terug. Het aantal op het appicoon en in het ochtendoverzicht telt hem dan niet meer mee. Als je hem opent, een chatbericht stuurt, hem bewerkt of snoozet, of als er een nieuw bericht binnenkomt, verschijnt hij weer.

Eén keer per week kan een project waar al een tijdje niets in gebeurt en geen openstaande to-do's heeft, een to-do krijgen met één specifieke volgende stap. Dat gebeurt hooguit drie keer per week. Zie [Projecten](projects.md).

Als er niets van je nodig is, staat je Machine stil bij een lege lijst. Tijdens een controle wordt hij weer actief en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk toon je alle to-do's of alleen één soort. Op je telefoon en computer wordt dezelfde keuze gebruikt. Als Werk of Privé is geselecteerd, ga je met **Alles tonen** terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, hoort niet bij Werk of Privé en staat alleen onder Alle.

Met de regel bovenaan de lijst schakel je ook direct naar de andere weergave: **Alleen privé · Werk · Alles tonen**.

De rij bovenaan de lijst toont de naam van je laatste ochtend- of avondoverzicht en wat daarin is meegeteld, zoals **Avondoverzicht van gisteren** · 12 afgerond, 3 open. Tik erop om dat overzicht opnieuw te lezen en met **Kopiëren** ergens te plakken. Zodra je het opent of op **×** tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Als er geen recent overzicht is, staat er **Vandaag tot nu toe**: wat er vandaag is afgerond en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt geselecteerd.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Zie [To-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. De berichten die hij mag lezen en versturen, verhuizen mee. Met **Ongedaan maken** in de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle berichten waar hij vandaan komt daar staan, wordt hij automatisch daarheen verplaatst en gaat hij verder. Anders staat er **Naar Werk verplaatsen** en wordt er niets verplaatst totdat je erop tikt. Een to-do die je hebt toegevoegd zonder Werk of Privé te kiezen, wordt automatisch verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd hoort hij niet bij Werk of Privé en blijft hij privé.

Een to-do kan de berichten lezen waar hij vandaan komt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt ingesteld, telt als Privé. Mail voor een ander bedrijf van jou komt terecht bij de to-do's van dat bedrijf. Een to-do over je privéleven, zoals familie die naar je werkadres mailt, is vanaf het begin Privé.

Werk dat je via een persoonlijk account bereikt, zoals een klant op WhatsApp of een bestelling in je persoonlijke mailbox, is vanaf het begin Werk. Een to-do die je zelf hebt verplaatst of ingesteld, blijft altijd staan waar je hem hebt gezet. Werk of Privé bepaalt waar een to-do verschijnt en met wie hij wordt gedeeld, nooit waar hij op antwoordt. Een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de mail binnenkwam. Hij verschijnt nooit in een Werk-Fleet of de Team Graph.

Als er twee of meer to-do's wachten, kun je met **Doorlopen** in de kop van Voor jou de to-do's één voor één afwerken, in de volgorde van de lijst. Je ziet elk concept helemaal, met **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuur je met Enter wat op het scherm staat, snoozet `S`, slaat `→` over en stop je met Esc. Onder de titel staat in de kop ook hoelang ze ongeveer duren als je ze in je eigen tempo afwerkt, zoals 'ongeveer 2 min'.

Een to-do die je iets vraagt, wordt in geen van beide groepen opgenomen: hij wacht op je antwoord, niet op een tik.

## Nu checken

Je Machine leest elke paar minuten elke bron, dag en nacht. Hij controleert wat er is binnengekomen zodra er 40 berichten wachten of het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en betalingsbewijzen worden bij de volgende controle meegenomen, binnen een uur.

's Nachts, van 00:00 tot 06:30, pauzeren de controles. Nieuwe berichten worden nog steeds gelezen en bewaard, en om 06:30 tegelijk gecontroleerd, zodat je to-do's klaarstaan voordat je ochtendoverzicht verschijnt. Bij de controles onder Koppelingen staat 'Nachtpauze, haalt de achterstand om 06:30 in'. Open je de app, schrijf je iets in de chat of tik je 's nachts op een to-do, dan worden de controles weer normaal uitgevoerd totdat je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen gecontroleerd.

Met **Nu checken** leest je Machine meteen elke bron. Als er niets openstaat, tik je op de regel van je Machine om hem te bekijken, met **Details**. Daarmee open je Controles onder Koppelingen. Als er to-do's openstaan, staat de regel bovenaan op een computer. Een korte regel verschijnt alleen terwijl er een controle bezig is, of wanneer een controle is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare hebben hun eigen tempo.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's wat de controle heeft gevonden, uit elke gelezen bron. Bijvoorbeeld: '13 berichten gecontroleerd om 16:11 · niets nodig' of '· 2 nieuwe to-do's'. Als een nieuwe to-do wordt bewaard voor een beter moment, zoals je ochtendoverzicht, staat erbij tot wanneer: '1 to-do bewaard tot morgen 08:30'.

Tik op de regel om elke e-mailthread, chat en melding te bekijken, met het pictogram van de bron: wie het heeft geschreven, het onderwerp of de eerste woorden, en de nieuwe to-do of waarom er niets nodig was. Bijvoorbeeld: 'Alleen in cc, een teamgenoot antwoordt' of 'Afspraak al gepland voor donderdag'. Als de controle alleen een vage reden opleverde, staat er geen reden bij de thread. Tik op een thread om hem te lezen.

De eerste 10 worden getoond. Tik eronder om de rest te zien. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al in de lijst staat, wordt maar één keer getoond. De regel blijft 12 uur na de controle staan.

Alleen mail aan jou wordt meegeteld. Je eigen antwoorden worden gelezen voor context en beloftes, maar tellen niet als nieuwe mail. E-mails die The Machine zelf naar jou stuurt, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt wel gewoon gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met daarnaast **Snoozen**. Zie [Doe het](do-it.md) en [Snoozen](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe de taak moet worden uitgevoerd, of, zodra er een concept klaarstaat, wat daarin moet veranderen. Met **Markeer als gedaan** geef je aan dat het is afgehandeld. Bij een klaargezette to-do zonder concept staat deze knop meteen in beeld, anders bovenaan onder **…**. Dat geldt ook voor een to-do waarvoor je nog een beslissing moet nemen. De to-do verdwijnt meteen uit de lijst. In de melding staat **Ongedaan maken**. Veeg de melding weg of sleep hem met de muis naar de zijkant om hem eerder te sluiten. De wijziging blijft staan.

Wil je dat het op een andere manier gebeurt, zeg dat dan in de **Chat**.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om iets te beoordelen](ask-to-review.md).
- **Herhalen…**: de to-do [komt regelmatig terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert ervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je titel blijft behouden.

Met **Heropenen** zet je een gesloten to-do terug. Hij verschijnt ook vanzelf weer als er iets nieuws gebeurt, zoals een nieuw bericht van diegene, maar niet na je eigen antwoord.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, bijvoorbeeld via automatische incasso of een opgeslagen betaalkaart, worden dat niet. Als een latere e-mail laat zien dat de rekening is betaald, zoals een bevestiging van de afzender, sluit de to-do vanzelf. Met **Ongedaan maken** zet je hem een dag lang terug.

Een to-do die alleen tot een bepaald tijdstip nodig is, zoals een bevestiging vóór een vergadering, sluit vanzelf na dat tijdstip. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding 'Niet meer nodig'. Met **Ongedaan maken** zet je hem een dag lang terug.

Voordat een bericht of overdracht voor iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack die heeft gelezen. Als een later bericht laat zien dat het al is geregeld, bijvoorbeeld omdat iemand erom is gevraagd en ja heeft gezegd, sluit de to-do vanzelf. Met **Ongedaan maken** zet je hem een dag lang terug.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een boeking is geannuleerd, werkt The Machine de to-do's automatisch bij. Een to-do die nog nodig is, volgt het nieuwe plan. Als er niets meer te doen is, wordt hij verplaatst naar **Gedaan / afgewezen** met de melding 'Niet nodig'. In de chat staat 'Bijgewerkt:' met de reden. Met **Ongedaan maken** zet je hem een dag lang terug.

Bij je eerste to-do's verschijnt een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**, en de uitleg dat er niets wordt verstuurd totdat je op **Versturen** drukt. Een tip verdwijnt definitief zodra je de bijbehorende knop gebruikt of op × drukt.

Op je eerste dag staat er bovenaan To-do's een welkomstbericht. Het noemt degene die al het langst op je antwoord wacht. Dat antwoord wordt als eerste opgesteld, zodat het klaarstaat wanneer je aankomt.

Elke to-do begint met de titel. De regel eronder vermeldt over wie de to-do gaat, de organisatie als die relevant is (niet alleen omdat iemand daar werkt), het project, Werk of Privé en wanneer het bericht is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en organisatie staat de foto of het logo als dat beschikbaar is in de Graph, anders staan er initialen. Als een logo op klein formaat niet goed leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, worden ook initialen getoond.

Soms staat er een korte, gedempte regel met wat niet bekend is, zoals 'Laatste contact 12 dagen geleden via e-mail; sindsdien niets'. Die verschijnt als het laatste contact met die persoon lang geleden is of onbeantwoord bleef. Ook worden niet-gekoppelde kanalen vermeld, zoals WhatsApp. Je Machine zegt wat hij niet weet, in plaats van iets te gokken.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

Een titel beschrijft wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do houdt zijn titel, met daaronder hoe hij is afgerond, zoals 'Gedaan: Sam heeft het dinsdag ondertekend'.

Boven het concept staat een vage regel met het bericht waar het vandaan komt en het logo van die dienst. Tik erop om de thread te lezen. Bij het concept staat het logo van de plek waar het naartoe gaat, zodat je meteen ziet of het een Slack-antwoord of een e-mail is.

Als het concept is gebaseerd op iemands input ergens anders, zoals een suggestie van een teamgenoot in Slack, staat dat op een regel, zoals 'Gebaseerd op Sam in #ops'. Tik erop om dat bericht te lezen.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, met de oudste berichten eerst: de berichten vóór het bericht waar de to-do over gaat en de antwoorden erna. In WhatsApp, Telegram of Signal staan je berichten rechts, net als in de app. Het bericht waar de to-do over gaat, is gemarkeerd met 'Deze to-do' en wordt in beeld geopend. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Bij een e-mailthread staan de overige berichten ingeklapt erboven en eronder.

Bij **Details** van een e-mail staan alleen gegevens die niet in de kop staan, zoals volledige cc-adressen, bcc of een ander antwoordadres. Als er niets toe te voegen is, wordt er niets weergegeven.

Bij een antwoord in een Slack-thread zie je ook wat er vóór het begin van de thread is gezegd. De link van een to-do naar het bijbehorende bericht opent dat bericht hier ook, met **Openen in Slack** onderaan.

Onder **Details** staan de naam, het project en het gebied (tik op een ervan om die te wijzigen), je laatste notitie en het resultaat van een codeerassistent. Met **Chat ›** open je de chat. Een afgeronde to-do blijft kort. Het bericht waar hij vandaan komt, staat onder **Details**.

Een to-do met 'Wacht op' linkt naar je laatste bericht aan diegene, het bericht waarop je een antwoord verwacht: 'E-mail aan Pat · di'.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor wat dan ook. Als je er een maakt, wordt er niets verstuurd. Als je **Werk** of **Privé** niet selecteert, komt de to-do terecht waar hij hoort, op basis van wie en waarover hij gaat. Ook vindt hij de e-mail waar hij op volgt, zelfs als die ouder is.

- **Deadline**: typ een dag of tijd, zoals 'morgen', 'volgende vr', '3 nov', '14:00' of 'over 2 uur'. Dat kan ook in je eigen taal. Met het kalenderpictogram open je snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt regelmatig terug. Zie [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven op wie de to-do betrekking heeft, maximaal 5.
- Berichtpictogram: voeg het bericht toe waar de to-do over gaat: een e-mail, Slack-, Teams-, WhatsApp- of Telegram-bericht, of een ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat van welke bron het komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon kun je met de camera ernaast een foto maken. Maximaal 5 bestanden, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × verwijder je een bestand.

De bestanden blijven bij de to-do en The Machine leest ze wanneer hij eraan werkt. Alleen bestanden zijn al genoeg: The Machine vult de to-do in op basis van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding weergegeven. Tik erop om hem op ware grootte te bekijken.
