---
title: To-do's
area: cards
summary: Eén to-do per taak die je aandacht nodig heeft, klaar om door jou goedgekeurd te worden. Lees wat de onderdelen van een to-do betekenen.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: f77d6b07f6f94ce5
---
Je Machine leest alles wat nieuw is en maakt alleen een to-do als iets je aandacht nodig heeft. Eén to-do per onderwerp, hoeveel berichten er ook bij horen.

## Waar to-do's staan

Op de pagina **To-do's** staan ze in groepen:

- **Net gedaan**: bovenaan staat een laatste stap die je hebt bevestigd, zoals een formulier of een issue dat is afgehandeld terwijl je weg was. Hij blijft maximaal een dag staan, totdat je op **Begrepen** tikt. Je telefoon krijgt er ook een melding van.
- **Voor jou**: alles wat op jou wacht, met eerst wat uiterlijk morgen moet gebeuren. Bij elke to-do staat **Klaargezet** (een concept of resultaat is klaar, en met **Doe het** of **Versturen** voer je het uit), **Wacht op jou** (je moet eerst een beslissing nemen of antwoord geven; als het werk niet verder kan of niet gebruikt kan worden zonder iets wat alleen jij hebt, zoals een prijs, een feit of een keuze, staat onder de titel wat dat is), **Aan het voorbereiden…** (je Machine werkt eraan) of **Om te lezen** (een overzicht of briefing, zonder dat je iets hoeft te beslissen).
- **Ouder**: ingeklapte to-do's waar al een week niets nieuws over is gebeurd (zie hieronder).
- **Wacht op anderen**: ingeklapte to-do's waarbij de volgende stap bij iemand anders ligt (zie hieronder).
- **Komt later terug**: gesnoozede to-do's, berichten die [later worden verstuurd](send-later.md) en to-do's waarop niemand antwoordde op **Nog nodig?** (zie hieronder).
- **Beloftes**: wat jij hebt beloofd en wat anderen jou hebben beloofd. Lees meer over [Beloftes](promises.md).
- **Gedaan / afgewezen**: alle afgeronde to-do's, met de nieuwste bovenaan en het tijdstip waarop ze zijn afgerond, zoals ‘Gedaan: 5 minuten geleden’. To-do's die al afgerond lijken, zijn gemarkeerd met **Lijkt gedaan**.

Na het versturen staat er een korte melding met waar de to-do naartoe is verplaatst, zoals ‘Verstuurd. Verplaatst naar Gedaan.’ of ‘Verstuurd. Verplaatst naar Later tot ma.’ Als een antwoord alleen belooft dat het werk wordt gedaan, zoals ‘Ik stuur het dinsdag’, blijft de to-do open: ‘Verstuurd. Open gehouden.’ Met **Openen** ga je naar de to-do. Met Zoeken vind je een to-do op titel of op de ontvanger, ook in Later en Gedaan.

Bij **Voor jou** staan eerst de to-do's waarvan de deadline is verstreken of uiterlijk morgen valt, dan vragen van je Fleet, daarna vervolgacties van een bord en dan de rest. Binnen elke groep staan de nieuwste bovenaan. Een to-do blijft op dezelfde plek terwijl je Machine hem klaarmaakt en wanneer hij klaar is: alleen de markering verandert. In de andere open groepen staan eerst de to-do's waarvan de deadline is verstreken of uiterlijk morgen valt, daarna de rest, met de nieuwste bovenaan. De zijbalk houdt dezelfde volgorde aan.

**Lijkt gedaan** betekent dat je Machine ziet dat iets is afgerond, bijvoorbeeld ‘PR #3451 is samengevoegd’, maar dat het nog niet is gesloten. Met **Heropenen** zet je de to-do terug op je lijst en leert je Machine ervan. Deze to-do's worden nooit als te laat weergegeven. Als een bericht laat zien dat iets klaar is, wordt de to-do na een dag vanzelf gesloten. Je kunt dat ongedaan maken met **Ongedaan maken**. Anders wacht de to-do op **Als gedaan markeren**.

Een to-do die je zelf al hebt afgehandeld, bijvoorbeeld met een antwoord in Gmail of Slack, wordt ook vanzelf gesloten. Een antwoord waarin staat dat er een bestand is bijgevoegd terwijl dat niet zo is, sluit de to-do niet.

Als een bericht afkomstig is van een adres dat alleen lijkt op dat van iemand die je kent, zoals sam@acme-corp.example in plaats van sam@acmecorp.example, staat dat duidelijk bij de to-do: ‘Dit is niet Sam Lee.’ De persoon wordt weergegeven met het eigen e-mailadres, nooit met de naam die de afzender heeft gebruikt. Je Machine controleert zo'n bericht bij de persoon op het adres dat je al hebt, nooit bij de afzender.

Een to-do die nog op iemand anders wacht, bijvoorbeeld op een beoordeling of antwoord, vermeldt bij **Wacht op** welke stap dat is. De to-do staat ingeklapt in **Wacht op anderen**, boven Komt later terug, totdat een nieuw bericht hem weer terugbrengt. Hetzelfde geldt nadat je een vraag hebt teruggesteld: de to-do komt terug op de ochtend vóór de deadline, op de deadline zelf als die later vandaag is, of de volgende ochtend als de deadline al voorbij is. Er staat bij op wie de to-do nog wacht.

Als een to-do gaat over een resultaat dat iemand anders moet opleveren, zoals een ondertekend contract, zie je dat bij **Details** onder **Klaar als**. Als jij jouw deel verstuurt, wordt de to-do niet gesloten. Hij blijft in **Wacht op anderen** staan totdat een bericht het resultaat laat zien. Daarna wordt hij vanzelf gesloten. Je kunt dat ongedaan maken met **Ongedaan maken**. Als er niets binnenkomt tegen de tijd dat je iemand eraan moet herinneren, komt de to-do terug met **Schrijf een korte herinnering** in de chat. Vertel in de chat wat als afgerond telt om dit aan te passen.

Een to-do waar een week niets nieuws over is gebeurd, wordt verplaatst van Voor jou naar **Ouder**, zodat nieuwe to-do's bovenaan staan als je na een paar dagen weer terugkomt. Niets nieuws betekent dat er geen nieuw bericht over is en dat jij er niets mee hebt gedaan, zoals een chatbericht sturen, iets aanpassen of snoozen. Alleen de to-do bekijken telt niet.

Dringende to-do's, to-do's met een naderende deadline en to-do's waarvan iets onderweg is om te versturen, blijven in Voor jou staan. Met **Alles afwijzen** markeer je alle to-do's in Ouder in één keer als niet nodig, na één bevestiging. Dat werkt net als **Niet nodig** voor één to-do, en je kunt het ongedaan maken met **Ongedaan maken**. Als er iets nieuws gebeurt, komt de to-do terug in Voor jou.

Een to-do waar een week niemand iets mee heeft gedaan, vraagt één keer: **Nog nodig?** Met **Niet nodig** sluit je hem. Je kunt dat ongedaan maken met **Ongedaan maken**. Met **Houden** houd je de to-do en wordt dit nooit opnieuw gevraagd. Als je nog een week niet antwoordt, wordt de to-do ingeklapt onder Komt later terug. Hij telt dan niet meer mee voor het getal op het appicoon of in het ochtendoverzicht. Als je de to-do opent, een chatbericht stuurt, iets aanpast, snoozet of een nieuw bericht binnenkomt, komt hij weer terug.

Een project waar al een tijd niets is gebeurd en geen open to-do's heeft, kan één keer per week een to-do krijgen met één concrete volgende stap. Dat gebeurt maximaal drie keer per week. Lees meer over [Projecten](projects.md).

Als niets je aandacht nodig heeft, doet je Machine een dutje en blijft de lijst leeg. Tijdens een controle wordt hij wakker en laat hij dat weten. Als een controle is mislukt of te laat is, staat dat erbij, met **Nu checken** eronder.

Met **Alle**, **Werk** en **Privé** bovenaan de zijbalk geef je aan of alle to-do's of maar één soort wordt weergegeven. Op je telefoon en computer geldt dezelfde keuze. Als Werk of Privé is geselecteerd, ga je met **Alles tonen** terug naar alle to-do's. Een melding over je Machine zelf, zoals een onderdeel dat steeds opnieuw opstart, is niet Werk of Privé en wordt alleen weergegeven onder Alle.

Met de regel bovenaan de lijst schakel je ook meteen naar de andere weergave: tik onder **Alleen privé** op **Werk** of **Alles tonen**.

De rij bovenaan de lijst vermeldt je laatste ochtend- of avondoverzicht en hoeveel to-do's erin stonden, bijvoorbeeld **Avondoverzicht van gisteren** · 12 gedaan, 3 open. Tik erop om het overzicht opnieuw te lezen. Met **Kopiëren** plak je het ergens anders. Zodra je het overzicht opent of op × tikt, blijft het op al je apparaten staan tot het volgende overzicht.

Als er geen recent overzicht is, zie je **Vandaag tot nu toe**: wat er vandaag is afgerond en wat nog openstaat, voor Werk en Privé of alleen voor de weergave die je hebt gekozen.

Bij een to-do voor een project staat de projectnaam onder de titel. Tik erop om het project te openen. Met **Project** onder **Details** wijzig je het project of haal je de to-do eruit. Lees meer over [de to-do's van een project](projects.md#a-project-s-to-dos).

Met **Gebied** onder **Details** verplaats je een to-do naar je andere gebied. Ook de gegevens die de to-do mag lezen en versturen, verhuizen mee. Met **Ongedaan maken** in de melding zet je hem terug.

Als een to-do je andere gebied nodig heeft om verder te gaan en alle berichten waar hij vandaan komt daar staan, wordt hij vanzelf daarheen verplaatst en gaat het werk verder. Anders zie je **Naar Werk verplaatsen** en gebeurt er niets totdat je erop tikt. Een to-do die je toevoegt zonder Werk of Privé te kiezen, wordt automatisch verplaatst zodra duidelijk is waar hij thuishoort. Tot die tijd staat er niet bij of hij Werk of Privé is, en blijft hij privé.

Een to-do kan altijd de berichten lezen waar hij vandaan komt. Als hij andere berichten uit je andere gebied nodig heeft, vraagt hij dat met **Deze mail voor deze to-do gebruiken**. Een werkmailbox die je als Privé hebt aangemerkt, telt als Privé. Mail voor een ander bedrijf van je hoort bij de to-do's van dat bedrijf. Een to-do over je privéleven, zoals familie die naar je werkadres schrijft, is vanaf het begin Privé.

Werk dat je via een privéaccount bereikt, zoals een klant via WhatsApp, een bestelling in je privépostvak of een [belofte](promises.md) over werk, is vanaf het begin Werk.

Een to-do die je zelf hebt verplaatst of geplaatst, blijft altijd staan waar je hem hebt neergezet. Werk of Privé bepaalt waar een to-do wordt weergegeven en met wie hij wordt gedeeld, nooit waar hij op antwoordt: een antwoord gaat altijd naar de plek van het gesprek, ook na een verplaatsing, tenzij je een andere manier kiest.

Zo'n Privé-to-do antwoordt nog steeds vanaf het werkadres waarop de e-mail binnenkwam. Hij wordt nooit weergegeven in een Werk-Fleet of de Team-Graph.

Als er twee of meer to-do's wachten, ga je met **Doorlopen** in de kop van Voor jou één voor één door de lijst. Je ziet elke to-do in de volgorde van de lijst, met het volledige concept en de opties **Versturen** of **Doe het**, **Wijzigingen vragen**, **Snoozen** en **Overslaan**. Op een computer verstuurt Enter wat op het scherm staat, snoozet `S`, slaat `→` over en stopt Esc. In de kop staat hoelang het ongeveer duurt als je je eigen tempo aanhoudt, bijvoorbeeld ‘ongeveer 2 min’.

Aan het einde zie je hoeveel to-do's zijn verstuurd of gesloten en hoeveel er nog worden klaargemaakt.

Een to-do die jou iets vraagt, wordt niet meegenomen. Daarvoor moet je antwoord geven, niet alleen ergens op tikken.

## Nu checken

Je Machine leest elke paar minuten alle bronnen, dag en nacht. Hij controleert wat er is binnengekomen zodra er 40 berichten klaarstaan of zodra het oudste bericht van iemand 15 minuten heeft gewacht. Nieuwsbrieven, meldingen en ontvangstbewijzen worden bij de volgende controle meegenomen, binnen een uur.

's Nachts, van 00:00 tot 06:30, worden controles gepauzeerd. Nieuwe berichten worden nog steeds gelezen en bewaard, en om 06:30 in één keer gecontroleerd, zodat je to-do's klaarstaan vóór je ochtendoverzicht. Bij Controles onder Koppelingen staat ‘'s Nachts gepauzeerd, haalt de achterstand om 06:30 in’. Klik, typ of scroll in de app, schrijf in de chat of tik 's nachts op een to-do, en de controles lopen zoals gewoonlijk door totdat je een uur weg bent geweest. Met **Nu checken** wordt altijd meteen een controle gestart.

Met **Nu checken** worden alle bronnen meteen gelezen. Als er geen to-do's openstaan, tik je op de regel van je Machine om die te bekijken, met **Details**, waarmee Controles onder Koppelingen wordt geopend. Als er to-do's openstaan, staat de regel bovenaan op een computer. Je ziet hem alleen kort tijdens een controle, of als een controle is mislukt of te laat is. Je kunt het ook in de chat vragen.

LinkedIn, X en Salesflare volgen hun eigen tempo.

## Laatste controle

Na een controle waarbij nieuwe berichten zijn gelezen, staat er boven je to-do's wat er is gevonden, uit elke bron die is gelezen, bijvoorbeeld ‘13 berichten gecontroleerd om 16:11 · geen nieuwe to-do's’ of ‘· 2 nieuwe to-do's’. De melding gaat alleen over die controle. To-do's die al op je lijst stonden, blijven staan zoals ze zijn. Als een nieuwe to-do op een beter moment wordt getoond, bijvoorbeeld in je ochtendoverzicht, staat erbij tot wanneer hij wordt uitgesteld: ‘1 to-do uitgesteld tot morgen 08:30’.

Tik op de melding om alle e-mailthreads, chats en meldingen te zien, met het pictogram van de bron. Je ziet wie er heeft geschreven, het onderwerp of de eerste woorden, en de nieuwe to-do of de reden waarom er niets nodig was, bijvoorbeeld ‘Alleen in cc, een teamgenoot antwoordt’ of ‘Meeting staat al gepland voor donderdag’. Bij een thread wordt geen reden getoond als de controle slechts een vage reden gaf. Tik op een bericht om het te lezen, samen met de berichten eromheen.

De eerste 10 worden getoond. Tik eronder om de rest te bekijken. Een getal achter een naam, zoals (3), geeft aan hoeveel nieuwe berichten die chat heeft. Een telefoonmelding over een bericht dat al op de lijst staat, wordt maar één keer getoond. De melding blijft 12 uur na de controle staan.

Alleen e-mail aan jou telt mee. Je eigen antwoorden worden gelezen voor de context en beloftes, maar tellen niet als nieuwe e-mail. E-mails van The Machine aan jou, zoals je ochtendoverzicht of een melding over een oplossing, worden nooit gelezen of weergegeven. Mail over facturering, je proefperiode of een uitnodiging wordt zoals gewoonlijk gelezen.

## De knoppen

Bij een to-do staat de volgende stap, zoals **Doe het** of **Nakijken en versturen**, met **Snoozen** ernaast. Lees meer over [Doe het](do-it.md) en [Snooze](snooze.md).

Met **Wijzigingen vragen** geef je aan wat er moet veranderen: hoe iets moet worden gedaan, of, zodra een concept klaarstaat, wat er in het concept moet veranderen. Laat je tekst onafgemaakt staan, dan staat hij er nog als je terugkomt. Met **Annuleren** gooi je hem weg.

**Als gedaan markeren** betekent dat het is afgehandeld. De knop staat direct in beeld bij een klaargezette to-do zonder concept of bij een to-do die jou iets vraagt. Anders staat hij bovenaan onder **…**. De to-do verdwijnt meteen van de lijst, met **Ongedaan maken** in het bericht. Veeg het bericht weg of sleep het met de muis van het scherm om het eerder te sluiten. De wijziging blijft bewaard.

Wil je dat het op een andere manier wordt gedaan, zeg dat dan in de **Chat**. In het antwoord staat alleen wat er is veranderd, bijvoorbeeld dat de to-do is gesnoozed en tot wanneer. Als iets niet aangepast kon worden, zoals een deadline, staat dat erbij.

Onder **…**:

- **Overdragen…**: geef de to-do aan een teamgenoot, [Claude Code of Codex](hand-to-agent.md), of [vraag iemand om hem te beoordelen](ask-to-review.md).
- **Herhalen…**: de to-do [komt volgens een vast ritme terug](recurring.md).
- **Niet nodig**: de to-do verdwijnt. Je kunt eventueel een reden kiezen: **Niet relevant**, **Feiten kloppen niet** of **Al geregeld**. Je Machine leert hiervan.

Tik op de titel of op **Naam** onder **Details** om de naam te wijzigen. Je kunt het ook in de chat vragen, bijvoorbeeld: ‘Hernoem dit naar …’. De titel blijft van jou.

Met **Heropenen** zet je een gesloten to-do terug. Hij komt ook vanzelf terug als er iets nieuws gebeurt, zoals een nieuw bericht van die persoon, maar niet als jij zelf antwoordt. Daarna staat erbij wanneer de to-do is teruggekomen en wordt hij als nieuw gesorteerd. De chat gaat verder waar hij gebleven was, ook na weken.

Een rekening die je zelf nog moet betalen, uit welk land dan ook, wordt een to-do met het bedrag, de deadline en de betaalgegevens op de rekening. Rekeningen die automatisch worden betaald, zoals via automatische incasso of een opgeslagen kaart, worden dat niet. Als een latere e-mail laat zien dat de rekening is betaald, bijvoorbeeld doordat de afzender bevestigt dat de betaling is ontvangen, wordt de to-do vanzelf gesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Een to-do die maar tot een bepaald tijdstip belangrijk is, zoals een bevestiging vóór een meeting, wordt na dat tijdstip vanzelf gesloten. Hij wordt verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet meer nodig’. Met **Ongedaan maken** zet je hem een dag lang terug.

Voordat een bericht of overdracht voor iemand als klaar wordt weergegeven, controleert je Machine je recente chats met de betrokken personen, ook groepschats, en wacht hij tot Slack die heeft gelezen. Als een later bericht laat zien dat het al geregeld is, bijvoorbeeld omdat iemand was gevraagd en ja zei, wordt de to-do vanzelf gesloten. Met **Ongedaan maken** zet je hem een dag lang terug.

Als iemand anders in hetzelfde gesprek heeft geschreven nadat het concept is gemaakt, houdt **Versturen** het concept tegen: ‘Niet verstuurd: nieuw bericht in de thread’. Bij de to-do zie je dat bericht, met **Lezen** en **Opnieuw voor dit bericht**. Druk opnieuw op **Versturen** om je concept ongewijzigd te versturen.

Als een nieuwer bericht het plan verandert, bijvoorbeeld omdat een feest naar een andere locatie is verplaatst of een boeking is geannuleerd, werkt The Machine zijn to-do's zelf bij. Een to-do die nog nodig is, volgt het nieuwe plan. Als er niets meer te doen is, wordt de to-do verplaatst naar **Gedaan / afgewezen** met de melding ‘Niet nodig’. In de chat staat ‘Bijgewerkt:’ met de reden. Met **Ongedaan maken** zet je hem een dag lang terug.

Bij je eerste to-do's zie je een korte tip met de belangrijkste acties: **Wijzigingen vragen** en **Niet nodig**, en de uitleg dat er niets wordt verstuurd totdat je op **Versturen** drukt. De tip verdwijnt definitief zodra je de knop gebruikt of op × drukt.

Op je eerste dag begroet de bovenkant van To-do's je en staat er wie het langst op je antwoord wacht. Dat antwoord wordt als eerste klaargezet, zodat het klaarstaat zodra je aankomt.

Elke to-do begint met de titel. De regel eronder vermeldt over wie het gaat, de organisatie als die relevant is, het project, Werk of Privé en wanneer de to-do is binnengekomen. Tik op een naam om de pagina van die persoon in de Graph te openen.

Bij een naam en organisatie staat de foto of het logo als de Graph die heeft, anders de initialen. Een logo dat op die grootte niet goed leesbaar is, bijvoorbeeld witte tekst op een transparante achtergrond of een breed woordmerk, wordt ook vervangen door de beginletter.

Soms staat er een korte, gedempte regel met wat niet bekend is, bijvoorbeeld ‘Laatste contact 12 dagen geleden via e-mail; sindsdien niets’. Die wordt getoond als het laatste contact met die persoon lang geleden was of onbeantwoord bleef. Ook kan erop staan welke kanalen niet zijn gekoppeld, zoals WhatsApp. Je Machine zegt wat hij niet weet, in plaats van te gissen.

Als er een niet-gekoppeld kanaal wordt genoemd, opent **Koppelen** ernaast die koppeling.

De titel geeft aan wat er moet gebeuren en verandert alleen als dat verandert. Een afgeronde to-do houdt zijn titel, met daaronder hoe hij is afgerond, bijvoorbeeld ‘Gedaan: Sam heeft het dinsdag ondertekend’.

Boven het concept staat in een gedempte regel van welk bericht het afkomstig is, met het logo van die dienst. Tik erop om de thread te lezen. Bij het concept staat het logo van de plek waar het naartoe gaat, zodat je meteen ziet of het een Slack-antwoord of een e-mail is.

Als het concept voortkomt uit iemands reactie ergens anders, zoals een voorstel van een teamgenoot in Slack, staat dat erbij, bijvoorbeeld ‘Gebaseerd op Sam in #ops’. Tik erop om dat bericht te lezen. De regel verdwijnt zodra een update het concept vervangt.

Een chat (Slack, WhatsApp, Telegram, Intercom…) wordt weergegeven als één gesprek, van oud naar nieuw: de berichten vóór het bericht waar de to-do over gaat, en de antwoorden erna. In WhatsApp, Telegram of Signal staan je berichten rechts, net als in de app. Het bericht waar de to-do over gaat, is gemarkeerd met ‘Deze to-do’ en wordt geopend in beeld. Met **Eerdere berichten tonen** voeg je oudere berichten toe. Bij een e-mail wordt de rest van de thread ingeklapt erboven en eronder weergegeven.

Een bericht wordt op dezelfde manier geopend vanuit Zoeken, de Graph, antwoorden van Ask of de laatste controle. Het is gemarkeerd met ‘Dit bericht’ of ‘Nieuwe berichten’.

Met **Openen in Gmail** open je de e-mail in het Gmail-account waarop hij is binnengekomen. Op Android wordt hij geopend in de Gmail-app als je die hebt.

Bij **Details** van een e-mail staat alleen informatie die niet in de kop staat, zoals volledige Cc-adressen, Bcc of een ander antwoordadres. Als er niets aan toe te voegen is, staat er niets.

Bij een antwoord in een Slack-thread zie je ook wat er is gezegd voordat de thread begon. Een link van een to-do naar het bijbehorende bericht opent dat bericht hier ook, met onderaan **Openen in Slack**.

Bij **Details** staan de naam, het project en het gebied (tik erop om ze te wijzigen), je laatste notitie en het resultaat van een codeeragent. Met de titel open je de chat. Een afgeronde to-do blijft kort; het bericht waar hij vandaan komt staat onder **Details**.

Bij een to-do met ‘Wacht op’ staat een link naar je laatste bericht aan die persoon en naar het bericht waarop je wacht: ‘E-mail aan Pat · di’.

## Zelf een to-do maken

Met **Nieuwe to-do** (onder **Zoeken** op een computer, **+** op een telefoon of `N`) voeg je een to-do toe voor wat dan ook. Als je er een maakt, wordt er niets verstuurd. Als je geen **Werk** of **Privé** kiest, komt de to-do terecht waar hij thuishoort, op basis van wie en waar het over gaat. De to-do zoekt ook de e-mail op waar hij een vervolg op is, zelfs als die ouder is.

Sluit de to-do voordat je hem toevoegt en je tekst en keuzes staan er de volgende keer nog. Bestanden niet. Met **Weggooien** in het bericht verwijder je ze.

- **Deadline**: typ een dag of tijd, bijvoorbeeld ‘morgen’, ‘volgende vr’, ‘3 nov’, ‘14.00’ of ‘over 2 uur’. Dat kan ook in je eigen taal. Het kalendericoon bevat snelle keuzes en **Kies een datum**.
- **Herhaalt**: de to-do komt volgens een vast ritme terug. Lees meer over [Terugkerende to-do's](recurring.md).
- **Persoon**: koppel de personen of bedrijven waar de to-do over gaat, maximaal 5.
- Berichtenicoon: voeg het bericht toe waar de to-do over gaat, zoals een e-mail, Slack-, Teams-, WhatsApp-, Telegram- of ander bericht dat The Machine heeft. Zoek op tekst of afzender. Bij elk resultaat staat waar het vandaan komt, wie het heeft verstuurd en wanneer.
- **Bestanden**: tik op de paperclip, plak een screenshot of sleep bestanden naar het formulier. Op een telefoon maakt de camera ernaast een foto. Je kunt maximaal 5 bestanden toevoegen, net als in de chat (zie [Bestanden toevoegen](card-chat.md#add-files)). Met × haal je een bestand weer weg.

De bestanden blijven bij de to-do en je Machine leest ze wanneer hij eraan werkt. Alleen bestanden toevoegen is genoeg: de to-do wordt ingevuld aan de hand van een pdf- of tekstbestand. Een foto wordt als kleine afbeelding getoond. Tik erop om hem op ware grootte te zien.
