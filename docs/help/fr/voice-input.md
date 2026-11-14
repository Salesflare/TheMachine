---
title: Saisie vocale
area: cards
summary: Parlez au lieu de taper. Vos paroles s’affichent dans le champ de message pour que vous puissiez les vérifier. Rien n’est envoyé.
covers: voice-input
code: voice_input.py, voice_worker.py, dashboard.html
order: 7
keywords: voice, dictate, dictation, speak, talk, microphone, mic, speech, transcribe
translated: f311b21bb4996eb4
---
## Parlez au lieu de taper

Touchez le micro dans un champ de message : le chat d’une tâche, **Nouvelle tâche**, **Aide** ou le champ où modifier un brouillon. Parlez, puis touchez la coche. Vous pouvez aussi maintenir le micro enfoncé pendant que vous parlez, puis le relâcher quand vous avez terminé.

Pendant l’écoute, un minuteur et le texte reconnu s’affichent dans le champ. Touchez la croix pour arrêter sans rien conserver. L’enregistrement s’arrête automatiquement au bout de 2 minutes.

Le texte s’affiche dans le champ, à l’endroit où se trouvait le curseur. Rien n’est envoyé : relisez-le, modifiez-le à votre guise, puis envoyez-le vous-même.

## Où votre voix est traitée

Choisissez cette option dans **Paramètres**, **Général**, sous **Saisie vocale**. Une courte phrase indique laquelle est utilisée.

- **Automatique** (par défaut) : OpenAI transcrit l’enregistrement lorsque votre Machine utilise OpenAI (avec une clé OpenAI ou un forfait ChatGPT qui permet le traitement audio). Sinon, votre Machine le fait elle-même et l’enregistrement ne la quitte jamais.
- **Sur cette Machine** : toujours sur votre Machine, même si OpenAI est configuré.
- **Avec OpenAI** : toujours avec OpenAI.

L’enregistrement est supprimé dès que le texte est récupéré.

## Préparation

Pour transcrire la parole elle-même, votre Machine télécharge d’abord un modèle vocal (150 à 500 MB) en arrière-plan, lorsque l’activité est faible. Pendant ce temps, les Paramètres affichent **Préparation en arrière-plan**. Cette étape est ignorée si OpenAI est utilisé.

En attendant, **Automatique** utilise la reconnaissance vocale intégrée à votre navigateur, si celui-ci en propose une, et l’indique sous le champ. Certains navigateurs envoient l’enregistrement à leur éditeur. Si vous choisissez **Sur cette Machine**, votre enregistrement est mis en attente. Le champ affiche alors « Préparation de la saisie vocale… » avec le temps restant.

## Paramètres

- **Transcrit** : **Automatique**, **Sur cette Machine** ou **Avec OpenAI**.
- **Précision** (sur votre Machine uniquement) : **Plus précis** donne les meilleurs résultats pour la plupart des langues. **Plus rapide** est plus rapide, mais fait davantage d’erreurs. C’est l’option par défaut sur une Machine Standard.
- **Langue** : **Détecter** fonctionne avec toutes les langues de l’application. Choisir la vôtre est légèrement plus rapide.

Pour parler à The Machine à voix haute, consultez [Parler en direct](talk-live.md).

## En cas de problème

- **Le microphone est bloqué** : autorisez l’accès au microphone pour ce site dans les paramètres de votre navigateur. Dans l’application mobile, cette autorisation se trouve dans les réglages de l’application.
- **Aucun microphone détecté** : connectez-en un, puis réessayez.
- **Impossible de joindre votre Machine** : votre enregistrement est conservé et transcrit lorsque votre Machine est de nouveau disponible. Pour réessayer plus tôt, touchez **Essayer maintenant**.
- **Aucune parole détectée** : rapprochez-vous du micro ou parlez un peu plus longtemps.
