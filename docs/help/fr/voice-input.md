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

## La première fois

La première fois que vous touchez le micro, votre Machine prépare la voix. Elle télécharge le modèle vocal une seule fois, de 150 à 500 Mo, et affiche "Préparation de la voix…" avec l’avancement. Cela prend quelques minutes. Votre enregistrement attend et est transcrit dès que tout est prêt.

## Où va votre voix

Par défaut, votre enregistrement est transcrit sur votre Machine elle-même. Il ne la quitte jamais et il est supprimé dès que le texte est revenu. La reconnaissance vocale de votre navigateur n’est pas utilisée, car certains navigateurs envoient alors votre voix à leur éditeur.

Dans **Paramètres**, **Général**, sous **Saisie vocale**, vous pouvez choisir :

- **Transcrit** : **Sur cette Machine**, ou **Avec OpenAI**. OpenAI est plus rapide sur un petit serveur, mais votre enregistrement part chez OpenAI, avec votre propre clé. Il faut une clé API OpenAI dans OpenClaw. Une connexion ChatGPT ne suffit pas.
- **Précision** : **Plus précis** fonctionne le mieux pour la plupart des langues. **Plus rapide** va plus vite, mais se trompe sur plus de mots. Sur un serveur Standard, qui a moins de mémoire, **Plus rapide** est le choix par défaut.
- **Langue** : **Détecter** fonctionne pour toutes les langues de l’app. Choisir la vôtre est un peu plus rapide.

## Quand ça ne marche pas

- **Le micro est bloqué** : autorisez le micro pour ce site dans les paramètres de votre navigateur. Dans l’app sur téléphone, c’est dans les autorisations de l’app.
- **Aucun micro trouvé** : branchez-en un et réessayez.
- **Impossible de joindre votre Machine** : votre enregistrement est gardé et transcrit quand votre Machine est de retour. Pour essayer plus tôt, touchez **Essayer maintenant**.
- **Je n’ai rien compris** : parlez un peu plus près du micro, ou plus longtemps.
