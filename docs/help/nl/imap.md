---
title: Andere e-mail (IMAP)
area: connections
summary: Mail van elke provider met IMAP, zoals iCloud, Yahoo, Fastmail, Telenet of je eigen domein. Leest voorlopig alleen.
covers: connector:imap
code: imap_mail.py, imap_presets.py, onboarding.py
order: 13
---
## Wat het leest

Je inbox en je map Verzonden: de laatste 7 dagen als je koppelt, daarna alles wat nieuw is. Mail die je verstuurt telt ook, zo leert hij hoe je schrijft en wat je beloofd hebt. Andere mappen worden niet gelezen.

Er verandert niets in je mailbox. Mail wordt niet als gelezen gemarkeerd.

## Wat het kan doen

Voorlopig leest het alleen: versturen vanuit deze mailbox kan nog niet. Een antwoord dat voor je klaarstaat kopieer je zelf naar je mailprogramma.

## Koppelen

1. Open in het dashboard **Koppelingen**, dan **+ Toevoegen**, en kies **Andere e-mail**.
2. Vul je e-mailadres en wachtwoord in.
3. Druk op **Verbinden**.

Veel providers willen een app-wachtwoord voor mailprogramma's, niet je gewone wachtwoord. Maak er een aan in de accountinstellingen van je provider:

- iCloud: een app-specifiek wachtwoord op account.apple.com.
- Yahoo: Accountbeveiliging, App-wachtwoord genereren.
- Fastmail: Settings, Privacy and security, App passwords.
- Telenet: je gewone wachtwoord van je Telenet-mail.
- Proton Mail: laat Proton Mail Bridge op dezelfde computer draaien en gebruik het wachtwoord dat Bridge toont.

De serverinstellingen worden voor de meeste providers ingevuld. Die van jou niet gevonden? Open **Serverinstellingen** en typ wat je provider opgeeft voor mailprogramma's: de IMAP-server, poort en beveiliging (SSL/TLS of STARTTLS). The Machine maakt nooit verbinding zonder TLS.

Gmail of mail van Microsoft, ook op je eigen domein? Kies dan **Gmail** of **Outlook**. Die melden zich aan zonder wachtwoord.

## Als het stopt

- **De mailserver weigerde het wachtwoord**: je hebt het gewijzigd, of het app-wachtwoord is verwijderd. Koppel opnieuw met het nieuwe.
- **De mailserver was niet bereikbaar**: hij probeert het zelf opnieuw. Blijft het mislukken, kijk dan de servernaam na in Serverinstellingen.

## Verwijderen

**Koppelingen**, open het account, **Details**, dan **Ontkoppelen**. Het stopt met lezen en wat al binnen is, blijft. Verwijder het app-wachtwoord ook bij je provider.
