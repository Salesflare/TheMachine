---
title: Verhuizen naar een andere computer
area: getting-started
summary: Exporteer alles wat je Machine weet in één versleuteld bestand en importeer het op een andere Machine, gehost of je eigen.
covers: moving
code: moving.py, cli.py, machine/app/export.py
site: Export everything, Delete it now, Download
order: 5
---
Alles wat je AI leert, is van jou: berichten, gesprekken, to-do's met hun geschiedenis, concepten, de Graph, herinneringen, skills en agenttaken. Je kunt het allemaal meenemen, ook als je stopt met The Machine.

## Exporteren

Op je eigen computer:

1. Druk in **Instellingen** › **Algemeen** › **Exporteren** op **Exporteren** naast Alles.
2. Kies eventueel een wachtwoordzin. Zonder krijg je een exportcode: schrijf hem op, de import heeft hem nodig.
3. Zet eventueel **Sleutels en tokens meenemen** aan (vraagt een wachtwoordzin), dan hoef je je bronnen niet opnieuw te koppelen.
4. Druk op **Export starten** en dan op **Downloaden**. Het bestand wordt na 24 uur verwijderd, of meteen met **Verwijderen**.

Op een gehoste Machine opent **Exporteren** naast Alles je accountpagina. Druk op **Alles exporteren** en dan op **Downloaden**. Je Machine verwijdert het bestand na 24 uur, of meteen met **Nu verwijderen**.

Het bestand is altijd versleuteld. Na een export toont Instellingen wat erin zit, met aantallen, en wat er niet in zit en waarom. Aanmeldingen bij Google en Microsoft via de gehoste dienst vragen aan de andere kant altijd een nieuwe aanmelding.

## Importeren

1. Druk in **Instellingen** › **Algemeen** › **Exporteren** op **Bestand kiezen** naast Importeren en kies de export.
2. Typ de wachtwoordzin of exportcode en druk op **Openen**. The Machine controleert eerst het hele bestand.
3. Gehost: druk op **Nu importeren**. The Machine herstart er binnen een paar minuten mee. Op je eigen computer: druk op **Vervangen door deze export** en dan op **Vervangen**. The Machine herstart ermee binnen een minuut of twee, en Instellingen toont **Geïmporteerd**.

De import vervangt wat die Machine nu heeft en bewaart daar eerst een kopie van. Niets wat klaarstond, gaat vanzelf de deur uit: verzendingen in de wachtrij wachten tot je ze opnieuw verstuurt.

Gevorderd: op een computer waar The Machine zonder servicebeheer draait, toont Instellingen de commando's. Je kunt ze ook zelf uitvoeren: `assistant service stop`, `assistant import --staged --force`, `assistant service start`.

Op een nieuwe computer [installeer je eerst The Machine](self-hosted-setup.md). Zeg daarna je gehoste abonnement op als je het niet meer nodig hebt: zie [Opzeggen of verwijderen](cancel-and-delete.md).
