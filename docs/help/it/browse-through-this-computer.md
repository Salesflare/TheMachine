---
title: Naviga tramite l'app desktop
area: troubleshooting
summary: Fai passare il browser della tua Machine ospitata dal computer su cui è in esecuzione l'app desktop, così i siti vedono la tua connessione internet.
code: desktop/src/exit.rs, desktop/src/settings.rs
keywords: desktop app, exit node, home internet, office, ip address, linkedin, sign in, proxy
order: 5
translated: 6da69c78d7e60574
---
Alcuni siti, come LinkedIn, non consentono di accedere da un browser nel cloud. Se hai effettuato l'accesso nell'[app desktop](desktop-app.md), il browser della tua Machine ospitata può passare da quel computer. Così i siti vedono la connessione internet di casa o dell'ufficio, non quella di un centro dati.

## Attivala

È attiva per impostazione predefinita quando è disponibile sulla tua Machine. Nelle **Impostazioni** dell'app desktop, l'opzione è **Consenti alla mia Machine di navigare tramite questo computer**. Disattivala e il browser della tua Machine tornerà subito a connettersi direttamente.

Quando il browser della tua Machine la usa, il riquadro del robot e l'icona dell'app nella barra dei menu o nella barra delle applicazioni mostrano **La tua Machine sta navigando tramite questo computer**.

## Cosa passa da qui

Solo il browser della tua Machine, diretto ai siti web: le porte 80 e 443 degli indirizzi pubblici su internet. L'app non si connette mai a questo computer, alla rete di casa o dell'ufficio né ad altri indirizzi privati, e non apre porte sul computer. Il traffico è limitato a 4 MB/s in download, 1 MB/s in upload e 2 GB al giorno.

## Quando il computer è spento

Il browser della tua Machine si connette direttamente dalla tua Machine e torna a passare dal computer non appena l'app è di nuovo in esecuzione.
