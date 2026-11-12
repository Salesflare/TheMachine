---
title: Autre e-mail (IMAP)
area: connections
summary: Les e-mails de tout fournisseur avec IMAP, comme iCloud, Yahoo, Fastmail, Telenet ou votre propre domaine. Lecture seule pour l’instant.
covers: connector:imap
code: imap_mail.py, imap_presets.py, onboarding.py
order: 13
---
## Ce qu’elle lit

Votre boîte de réception et votre dossier Envoyés : les 7 derniers jours quand vous connectez, puis tout ce qui est nouveau. Les e-mails que vous envoyez comptent aussi : elle apprend ainsi comment vous écrivez et ce que vous avez promis. Les autres dossiers ne sont pas lus.

Rien ne change dans votre boîte. Les e-mails ne sont pas marqués comme lus.

## Ce qu’elle peut faire

Pour l’instant, elle lit seulement : elle ne peut pas encore envoyer depuis cette boîte. Une réponse préparée pour vous, vous la copiez dans votre logiciel de messagerie.

## La connecter

1. Dans le tableau de bord, ouvrez **Connexions**, puis **+ Ajouter**, et choisissez **Autre e-mail**.
2. Saisissez votre adresse e-mail et votre mot de passe.
3. Appuyez sur **Se connecter**.

Beaucoup de fournisseurs demandent un mot de passe d’application pour les logiciels de messagerie, pas votre mot de passe habituel. Créez-en un dans les réglages de compte de votre fournisseur :

- iCloud : un mot de passe pour app sur account.apple.com.
- Yahoo : Sécurité du compte, Générer un mot de passe d’application.
- Fastmail : Settings, Privacy and security, App passwords.
- Telenet : votre mot de passe habituel de la messagerie Telenet.
- Proton Mail : lancez Proton Mail Bridge sur le même ordinateur et utilisez le mot de passe affiché par Bridge.

Les réglages du serveur sont remplis pour la plupart des fournisseurs. Le vôtre n’est pas trouvé ? Ouvrez **Réglages du serveur** et saisissez ce que votre fournisseur indique pour les logiciels de messagerie : le serveur IMAP, le port et la sécurité (SSL/TLS ou STARTTLS). The Machine ne se connecte jamais sans TLS.

Gmail ou une messagerie Microsoft, même sur votre propre domaine ? Choisissez plutôt **Gmail** ou **Outlook**. Ils se connectent sans mot de passe.

## Quand elle s’arrête

- **Le serveur de messagerie a refusé le mot de passe** : vous l’avez changé, ou le mot de passe d’application a été supprimé. Connectez-la à nouveau avec le nouveau.
- **Le serveur de messagerie est injoignable** : elle réessaie toute seule. Si cela continue, vérifiez le nom du serveur dans Réglages du serveur.

## La retirer

**Connexions**, ouvrez le compte, **Détails**, puis **Déconnecter**. Elle arrête de lire, et ce qu’elle a déjà récupéré reste. Supprimez aussi le mot de passe d’application chez votre fournisseur.
