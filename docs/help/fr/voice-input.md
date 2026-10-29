---
title: Saisie vocale
area: cards
summary: Parlez au lieu de taper. Ce que vous dites arrive dans la zone de message pour que vous le vérifiiez. Rien n’est envoyé.
covers: voice-input
code: voice_input.py, voice_worker.py, dashboard.html
order: 7
keywords: voice, dictate, dictation, speak, talk, microphone, mic, speech, transcribe
---
## Parler au lieu de taper

Touchez le micro dans une zone de message : le chat d’une tâche, **Nouvelle tâche**, **Aide**, ou la zone pour modifier un brouillon. Parlez, puis touchez la coche. Ou maintenez le micro pendant que vous parlez et relâchez quand vous avez fini.

Pendant qu’elle écoute, la zone affiche un minuteur. Touchez la croix pour arrêter sans rien garder. Un enregistrement dure au plus 2 minutes ; à 2 minutes, il s’arrête tout seul et elle écrit ce que vous avez dit.

Ce que vous avez dit arrive dans la zone, là où était votre curseur. Rien n’est envoyé : relisez, modifiez ce que vous voulez et envoyez-le vous-même.

## Où va votre voix

Dans **Paramètres**, **Général**, sous **Saisie vocale**, une courte ligne indique lequel est utilisé.

- **Automatique** (par défaut) : quand OpenAI est configuré dans OpenClaw, votre enregistrement est transcrit par OpenAI. C’est une clé API, ou une connexion ChatGPT si votre forfait permet l’audio. Sans OpenAI, il est transcrit sur votre Machine elle-même et ne la quitte jamais.
- **Sur cette Machine** : toujours sur votre Machine, même quand OpenAI est configuré.
- **Avec OpenAI** : toujours OpenAI.

Un enregistrement est supprimé dès que le texte est revenu.

## Préparation

Pour transcrire elle-même la parole, votre Machine a besoin d’un modèle vocal de 150 à 500 Mo. Elle le télécharge en arrière-plan, en priorité basse, une fois configurée, sa première revue terminée et après un moment de calme. Pendant ce temps, les paramètres affichent **Préparation en cours (en arrière-plan)**. Elle ne le fait jamais quand OpenAI est utilisé.

Tant qu’elle n’est pas prête, **Automatique** utilise la reconnaissance vocale de votre navigateur s’il en a une, et l’indique sous la zone. Certains navigateurs l’envoient à leur éditeur. Avec **Sur cette Machine**, votre enregistrement attend, et la zone affiche « Préparation de la voix… » avec le temps restant.

## Paramètres

- **Transcrit** : **Automatique**, **Sur cette Machine** ou **Avec OpenAI**.
- **Précision** (sur votre Machine uniquement) : **Plus précis** fonctionne le mieux pour la plupart des langues. **Plus rapide** va plus vite mais se trompe sur plus de mots. Sur un serveur Standard, qui a moins de mémoire, **Plus rapide** est le réglage par défaut.
- **Langue** : **Détecter** fonctionne pour toutes les langues de l’app. Choisir la vôtre est un peu plus rapide.

Pour parler à voix haute avec The Machine, voyez [Parler en direct](talk-live.md).

## Quand ça ne marche pas

- **Le micro est bloqué** : autorisez le micro pour ce site dans les paramètres de votre navigateur. Dans l’app sur téléphone, c’est dans les autorisations de l’app.
- **Aucun micro trouvé** : branchez-en un et réessayez.
- **Impossible de joindre votre Machine** : votre enregistrement est gardé et transcrit quand votre Machine est de retour. Pour essayer plus tôt, touchez **Essayer maintenant**.
- **Je n’ai rien compris** : parlez un peu plus près du micro, ou plus longtemps.
