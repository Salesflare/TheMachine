---
title: Autre e-mail (IMAP)
area: connections
summary: Les e-mails de n’importe quel fournisseur compatible avec IMAP, comme iCloud, Yahoo, Fastmail, Telenet ou votre propre domaine.
covers: connector:imap
code: imap_mail.py, smtp_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
translated: a21e9d52d723f351
---
## Ce que lit votre Machine

Votre boîte de réception et votre dossier Envoyés : les 7 derniers jours au moment de la connexion, puis tous les nouveaux e-mails. Les e-mails que vous envoyez comptent aussi. Votre Machine apprend ainsi votre façon d’écrire et ce que vous avez promis. Elle ne lit pas les autres dossiers.

Rien ne change dans votre boîte aux lettres, à part l’ajout d’une copie des e-mails envoyés par The Machine dans votre dossier Envoyés. Les e-mails ne sont pas marqués comme lus.

## Ce qu’elle peut faire

Elle envoie des e-mails uniquement après que vous avez appuyé sur **Envoyer**, via le serveur de messagerie de votre fournisseur (SMTP) et avec le même mot de passe. Une copie est enregistrée dans votre dossier Envoyés. Les réponses conservent le fil de discussion. Votre signature est celle définie dans **Paramètres**, ou, à défaut, celle qui figure à la fin de vos e-mails envoyés.

## Connecter votre compte

1. Dans le tableau de bord, ouvrez **Connexions**, puis **E-mail**, et choisissez **Autre e-mail**.
2. Saisissez votre adresse e-mail et votre mot de passe.
3. Appuyez sur **Connecter**.

De nombreux fournisseurs exigent un mot de passe d’application pour les applications de messagerie, plutôt que votre mot de passe habituel. Créez-en un dans les paramètres de votre compte chez votre fournisseur :

- iCloud : un mot de passe spécifique à l’application sur account.apple.com.
- Yahoo : Sécurité du compte, Générer un mot de passe d’application.
- Fastmail : Settings, Privacy and security, App passwords.
- Telenet : votre mot de passe habituel pour la messagerie Telenet.
- Zoho Mail avec l’authentification à deux facteurs : un mot de passe spécifique à l’application dans votre compte Zoho, sous Security.
- Proton Mail : lancez Proton Mail Bridge sur le même ordinateur et utilisez le mot de passe affiché par Bridge. Cela fonctionne uniquement si The Machine se trouve sur ce même ordinateur. The Machine affiche l’empreinte du certificat de Bridge et ne fait confiance qu’à celui-ci.

Les paramètres du serveur sont préremplis pour la plupart des fournisseurs. Le vôtre n’est pas détecté ? Ouvrez **Réglages du serveur** et saisissez les informations fournies par votre fournisseur pour les applications de messagerie : les serveurs IMAP et SMTP, leurs ports et le type de sécurité (SSL/TLS ou STARTTLS). The Machine ne se connecte jamais sans TLS.

Vous utilisez Gmail ou la messagerie Microsoft, y compris avec votre propre domaine ? Choisissez plutôt **Gmail** ou **Outlook**. La connexion se fait sans mot de passe. Les serveurs saisis dans **Réglages du serveur** s’appliquent aussi à ces options : Microsoft n’accepte plus les mots de passe des applications de messagerie.

Vous avez saisi une adresse Microsoft 365 ? Le formulaire l’indique et affiche **Se connecter avec Microsoft** à la place du champ de mot de passe. La page de connexion Outlook s’ouvre. Si l’adresse n’est pas détectée en quelques secondes, le formulaire de mot de passe reste affiché.

## En cas de problème

- **Le serveur de messagerie a refusé le mot de passe** : vous l’avez modifié ou le mot de passe d’application a été supprimé. Reconnectez votre compte avec le nouveau mot de passe.
- **Le serveur de messagerie a refusé le mot de passe pour l’envoi** : aucun e-mail n’a été envoyé. Reconnectez votre compte. Si le refus persiste, vérifiez le serveur SMTP dans **Réglages du serveur**. En attendant, votre Machine ne fait que lire les e-mails.
- **Le serveur de messagerie est injoignable** : votre Machine réessaie automatiquement. Si le problème persiste, vérifiez le nom du serveur dans **Réglages du serveur**.
- **Le certificat du serveur de messagerie est destiné à** un autre nom : les hébergements mutualisés répondent souvent avec leur propre nom de serveur. Saisissez le nom indiqué dans **Réglages du serveur**. The Machine ne contourne jamais la vérification du certificat.

## Supprimer la connexion

Dans **Connexions**, ouvrez le compte, puis **Détails** et **Déconnecter**. Votre Machine cesse de lire les e-mails, mais conserve ceux qu’elle a déjà importés. Supprimez aussi le mot de passe d’application chez votre fournisseur.
