---
title: Autre e-mail (IMAP)
area: connections
summary: Les e-mails de tout fournisseur avec IMAP, comme iCloud, Yahoo, Fastmail, Telenet ou votre propre domaine.
covers: connector:imap
code: imap_mail.py, smtp_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
---
## Ce qu’elle lit

Votre boîte de réception et votre dossier Envoyés : les 7 derniers jours quand vous connectez, puis tout ce qui est nouveau. Les e-mails que vous envoyez comptent aussi : elle apprend ainsi comment vous écrivez et ce que vous avez promis. Les autres dossiers ne sont pas lus.

Rien ne change dans votre boîte, sauf une copie de ce que The Machine envoie, dans votre dossier Envoyés. Les e-mails ne sont pas marqués comme lus.

## Ce qu’elle peut faire

Elle envoie un e-mail seulement quand vous appuyez sur Envoyer, par le serveur de messagerie de votre fournisseur (SMTP) avec le même mot de passe. Une copie va dans votre dossier Envoyés. Les réponses restent dans leur conversation, et votre signature est celle des Paramètres, sinon celle qui termine vos e-mails envoyés.

## La connecter

1. Dans le tableau de bord, ouvrez **Connexions**, puis **+ Ajouter**, et choisissez **Autre e-mail**.
2. Saisissez votre adresse e-mail et votre mot de passe.
3. Appuyez sur **Se connecter**.

Beaucoup de fournisseurs demandent un mot de passe d’application pour les logiciels de messagerie, pas votre mot de passe habituel. Créez-en un dans les réglages de compte de votre fournisseur :

- iCloud : un mot de passe pour app sur account.apple.com.
- Yahoo : Sécurité du compte, Générer un mot de passe d’application.
- Fastmail : Settings, Privacy and security, App passwords.
- Telenet : votre mot de passe habituel de la messagerie Telenet.
- Zoho Mail avec l’authentification à deux facteurs : un mot de passe spécifique à l’application dans votre compte Zoho, Sécurité.
- Proton Mail : lancez Proton Mail Bridge sur le même ordinateur et utilisez le mot de passe affiché par Bridge. Cela ne fonctionne qu’avec The Machine sur ce même ordinateur. The Machine affiche l’empreinte du certificat de Bridge et ne fait confiance qu’à celui-ci.

Les réglages du serveur sont remplis pour la plupart des fournisseurs. Le vôtre n’est pas trouvé ? Ouvrez **Réglages du serveur** et saisissez ce que votre fournisseur indique pour les logiciels de messagerie : les serveurs IMAP et SMTP, leurs ports et leur sécurité (SSL/TLS ou STARTTLS). The Machine ne se connecte jamais sans TLS.

Gmail ou une messagerie Microsoft, même sur votre propre domaine ? Choisissez plutôt **Gmail** ou **Outlook**. Ils se connectent sans mot de passe. Leurs serveurs saisis dans Réglages du serveur y mènent aussi : Microsoft n’accepte plus les mots de passe des applications de messagerie.

## Quand elle s’arrête

- **Le serveur de messagerie a refusé le mot de passe** : vous l’avez changé, ou le mot de passe d’application a été supprimé. Connectez-la à nouveau avec le nouveau.
- **Le serveur de messagerie a refusé le mot de passe pour l’envoi** : rien n’a été envoyé. Reconnectez-la ; s’il refuse encore, vérifiez le serveur SMTP dans Réglages du serveur. D’ici là, elle lit seulement.
- **Le serveur de messagerie est injoignable** : elle réessaie toute seule. Si cela continue, vérifiez le nom du serveur dans Réglages du serveur.
- **Le certificat du serveur de messagerie est pour un autre nom** : un hébergement mutualisé répond souvent avec le nom de son propre serveur. Saisissez le nom affiché dans Réglages du serveur. The Machine ne saute jamais la vérification du certificat.

## La retirer

**Connexions**, ouvrez le compte, **Détails**, puis **Déconnecter**. Elle arrête de lire, et ce qu’elle a déjà récupéré reste. Supprimez aussi le mot de passe d’application chez votre fournisseur.
