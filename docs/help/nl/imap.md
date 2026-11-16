---
title: Andere e-mail (IMAP)
area: connections
summary: E-mail van elke provider met IMAP, zoals iCloud, Yahoo, Fastmail, Telenet of je eigen domein.
covers: connector:imap
code: imap_mail.py, smtp_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
translated: a21e9d52d723f351
---
## Wat hij leest

Je inbox en de map Verzonden: de laatste 7 dagen wanneer je verbinding maakt, en daarna alle nieuwe e-mail. Ook de e-mail die je verstuurt telt mee, zodat hij leert hoe je schrijft en wat je hebt beloofd. Andere mappen worden niet gelezen.

Er wordt niets in je mailbox gewijzigd, behalve dat er een kopie komt van wat The Machine verstuurt in je map Verzonden. E-mail wordt niet als gelezen gemarkeerd.

## Wat hij kan doen

Hij verstuurt alleen e-mail nadat je op **Verzenden** drukt, via de mailserver van je provider (SMTP) met hetzelfde wachtwoord. Er komt een kopie in je map Verzonden. Antwoorden blijven in dezelfde e-mailthread en je handtekening is die uit **Instellingen**, of anders die onder je verzonden e-mail.

## Verbinden

1. Open in het dashboard **Koppelingen**, dan **E-mail**, en kies **Andere e-mail**.
2. Vul je e-mailadres en wachtwoord in.
3. Druk op **Verbinden**.

Veel providers vereisen voor e-mailapps een app-wachtwoord in plaats van je gewone wachtwoord. Maak er een aan in de accountinstellingen van je provider:

- iCloud: een app-specifiek wachtwoord op account.apple.com.
- Yahoo: Accountbeveiliging, App-wachtwoord genereren.
- Fastmail: Instellingen, Privacy en beveiliging, App-wachtwoorden.
- Telenet: je gewone Telenet-mailwachtwoord.
- Zoho Mail met tweestapsverificatie: een applicatiespecifiek wachtwoord in je Zoho-account, onder Beveiliging.
- Proton Mail: start Proton Mail Bridge op dezelfde computer en gebruik het wachtwoord dat Bridge toont. Dit werkt alleen als The Machine ook op die computer staat. The Machine toont de vingerafdruk van het certificaat van Bridge en vertrouwt alleen dat certificaat.

Voor de meeste providers worden de serverinstellingen ingevuld. Staat die van jou er niet bij? Open **Serverinstellingen** en vul de gegevens in die je provider voor e-mailapps opgeeft: de IMAP- en SMTP-servers, hun poorten en de beveiliging (SSL/TLS of STARTTLS). The Machine maakt nooit verbinding zonder TLS.

Gebruik je Gmail of Microsoft-e-mail, ook op je eigen domein? Kies dan **Gmail** of **Outlook**. Daarvoor meld je je aan zonder wachtwoord. Ook de servers die je invult bij Serverinstellingen worden daar gebruikt: Microsoft accepteert geen wachtwoorden meer van e-mailapps.

Heb je een adres van Microsoft 365 ingevuld? Het formulier herkent dit en toont **Aanmelden met Microsoft** in plaats van het wachtwoordveld. Daarmee open je het aanmeldscherm van Outlook. Wordt het adres niet binnen een paar seconden herkend? Dan blijft het wachtwoordformulier staan.

## Als de verbinding wegvalt

- **De mailserver weigerde het wachtwoord**: je hebt het gewijzigd of het app-wachtwoord is verwijderd. Maak opnieuw verbinding met het nieuwe wachtwoord.
- **De mailserver weigerde het wachtwoord voor verzending**: er is niets verstuurd. Maak opnieuw verbinding. Blijft de mailserver het wachtwoord weigeren, controleer dan de SMTP-server bij Serverinstellingen. Tot die tijd leest hij alleen e-mail.
- **De mailserver was niet bereikbaar**: hij probeert het vanzelf opnieuw. Blijft dit misgaan, controleer dan de servernaam bij Serverinstellingen.
- **Het certificaat van de mailserver is voor** een andere naam: bij gedeelde hosting reageert de server vaak met zijn eigen servernaam. Vul de getoonde naam in bij Serverinstellingen. The Machine slaat de certificaatcontrole nooit over.

## Verwijderen

**Koppelingen**, open het account, **Details** en daarna **Ontkoppelen**. Hij stopt met lezen en wat hij al heeft opgehaald, blijft staan. Verwijder ook het app-wachtwoord bij je provider.
