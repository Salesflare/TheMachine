---
title: Andere e-mail (IMAP)
area: connections
summary: Mail van elke provider met IMAP, zoals iCloud, Yahoo, Fastmail, Telenet of je eigen domein.
covers: connector:imap
code: imap_mail.py, smtp_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
translated: 85e7bf625f96964a
---
## Wat het leest

Je inbox en je map Verzonden: de laatste 7 dagen als je koppelt, daarna alles wat nieuw is. Mail die je verstuurt telt ook, zo leert hij hoe je schrijft en wat je beloofd hebt. Andere mappen worden niet gelezen.

Er verandert niets in je mailbox, behalve een kopie van wat The Machine verstuurt, in je map Verzonden. Mail wordt niet als gelezen gemarkeerd.

## Wat het kan doen

Het verstuurt mail pas als je op Versturen drukt, via de mailserver van je provider (SMTP) met hetzelfde wachtwoord. Een kopie komt in je map Verzonden. Antwoorden blijven in hun gesprek, en je handtekening is die uit Instellingen, anders die waarmee je verzonden mail eindigt.

## Koppelen

1. Open in het dashboard **Koppelingen**, dan **E-mail**, en kies **Andere e-mail**.
2. Vul je e-mailadres en wachtwoord in.
3. Druk op **Verbinden**.

Veel providers willen een app-wachtwoord voor mailprogramma's, niet je gewone wachtwoord. Maak er een aan in de accountinstellingen van je provider:

- iCloud: een app-specifiek wachtwoord op account.apple.com.
- Yahoo: Accountbeveiliging, App-wachtwoord genereren.
- Fastmail: Settings, Privacy and security, App passwords.
- Telenet: je gewone wachtwoord van je Telenet-mail.
- Zoho Mail met tweestapsverificatie: een app-specifiek wachtwoord in je Zoho-account, bij Beveiliging.
- Proton Mail: laat Proton Mail Bridge op dezelfde computer draaien en gebruik het wachtwoord dat Bridge toont. Dat werkt alleen met The Machine op diezelfde computer. The Machine toont de vingerafdruk van het certificaat van Bridge en vertrouwt alleen dat.

De serverinstellingen worden voor de meeste providers ingevuld. Die van jou niet gevonden? Open **Serverinstellingen** en typ wat je provider opgeeft voor mailprogramma's: de IMAP- en SMTP-server, hun poorten en beveiliging (SSL/TLS of STARTTLS). The Machine maakt nooit verbinding zonder TLS.

Gmail of mail van Microsoft, ook op je eigen domein? Kies dan **Gmail** of **Outlook**. Die melden zich aan zonder wachtwoord. Typ je hun servers in Serverinstellingen, dan gaat het ook daarheen: Microsoft neemt geen wachtwoorden van mailprogramma’s meer aan.

## Als het stopt

- **De mailserver weigerde het wachtwoord**: je hebt het gewijzigd, of het app-wachtwoord is verwijderd. Koppel opnieuw met het nieuwe.
- **De mailserver weigerde het wachtwoord om te verzenden**: er is niets verzonden. Koppel opnieuw; blijft hij weigeren, kijk dan de SMTP-server na in Serverinstellingen. Tot dan leest hij alleen.
- **De mailserver was niet bereikbaar**: hij probeert het zelf opnieuw. Blijft het mislukken, kijk dan de servernaam na in Serverinstellingen.
- **Het certificaat van de mailserver is voor een andere naam**: bij gedeelde hosting antwoordt vaak de eigen server van de host. Typ de getoonde naam in Serverinstellingen. The Machine slaat de certificaatcontrole nooit over.

## Verwijderen

**Koppelingen**, open het account, **Details**, dan **Ontkoppelen**. Het stopt met lezen en wat al binnen is, blijft. Verwijder het app-wachtwoord ook bij je provider.
