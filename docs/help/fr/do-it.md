---
title: Faire et ce qui est envoyé
area: cards
summary: Faire prépare le travail. Rien n’est envoyé, payé ni modifié avant que vous approuviez cette étape.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: b1a9272a7629b74f
---
## Ce que fait Faire

**Faire** demande à votre Machine de préparer la tâche : rédiger une réponse, faire des recherches, remplir un formulaire. Elle utilise vos propres comptes et son propre navigateur, comme vous le feriez.

Pendant qu’elle travaille dans son navigateur, la tâche et son chat affichent cette page en direct, même entre les étapes, jusqu’à ce qu’elle ait terminé. Cliquez sur l’image pour ouvrir le navigateur. Dans la tâche, la page s’affiche en plus grand, avec **Arrêter** : une pression met immédiatement fin à cette exécution.

Avant une relance ou un transfert, elle vérifie s’il y a de nouvelles réponses, y compris celles d’un collègue. Si la tâche a déjà été traitée, elle vous l’indique. Si elle a modifié un document ou une page, la tâche contient un lien vers celui-ci.

## Rien n’est envoyé sans votre accord

- Une réponse revient sous forme de brouillon. **Vérifier et envoyer** l’ouvre, prête à être modifiée ; elle n’est envoyée que lorsque vous appuyez sur **Envoyer maintenant**.
- S’il y a deux e-mails ou plus dans une tâche, un seul bouton dans son chat permet de tous les vérifier. Ils s’affichent à tour de rôle avec **Suivant**, puis la dernière étape les envoie tous. Chaque e-mail n’apparaît comme envoyé qu’une fois qu’il l’est.
- Un e-mail s’affiche tel qu’il sera envoyé, avec le gras, les listes et les liens. Un message Slack ou un message de chat est en texte brut.
- **Demander des modifications** dans la même fenêtre : indiquez ce qu’il faut changer et votre Machine refait le brouillon.
- Une réponse répond au dernier e-mail du fil, et la source de la tâche ouvre cet e-mail.
- Une étape qui valide une action, comme envoyer un formulaire, payer ou réserver, attend votre confirmation ou que vous le demandiez dans le chat. Confirmer une étape ne débloque pas les autres : la tâche ne se termine que lorsque toutes les étapes sont faites.
- Dans le chat d’une tâche, un brouillon n’est jamais envoyé dans le même message que celui qui l’a rédigé.
- Tant que vous ne l’avez pas approuvé, la tâche reste sous **Pour vous**, avec le statut **Préparée**. La liste précise alors que rien ne sera envoyé avant votre approbation. Si la tâche attend encore quelque chose de vous, son statut est **Vous attend**. Elle indique qu’un brouillon a été envoyé uniquement une fois que c’est fait.
- Un long brouillon affiche ses 3 premières lignes. **Afficher plus**, ou appuyer sur le texte, permet de voir la suite ; **Vérifier et envoyer** affiche toujours le texte entier.

Selon la source, elle peut envoyer un e-mail, un message privé Slack, ou un message WhatsApp, Telegram, LinkedIn ou X. L’article de chaque connexion précise ce qu’elle peut envoyer.

## Modifier un e-mail

- Utilisez les boutons au-dessus du texte, ou `Ctrl B` pour le gras, `Ctrl I` pour l’italique et `Ctrl K` pour un lien (`⌘` sur Mac). Des boutons permettent aussi de créer une liste à puces ou numérotée.
- Un lien doit commencer par https://. Le texte collé est en texte brut, sans ses couleurs ni ses images.
- Le formatage non pris en charge dans les e-mails est d’abord supprimé, puis le message s’affiche tel qu’il sera envoyé. Appuyez de nouveau sur **Envoyer maintenant** pour l’envoyer.
- L’e-mail est envoyé exactement tel qu’il s’affiche, avec une copie en texte brut pour les applications de messagerie qui ne prennent pas en charge le formatage.

## Quand elle ne peut pas

- « Ce message ne peut pas être envoyé depuis ici. » signifie que vous devez copier le brouillon avec **Copier le brouillon**, puis l’envoyer vous-même.
- **Attend votre aide** signifie qu’elle a une question : **Répondre**. **Bloqué** signifie qu’elle s’est arrêtée sans poser de question ; la tâche vous en indique la raison.
- Si elle vous demande plusieurs choses, chaque question a ses propres choix ou un champ à remplir, parfois prérempli avec votre réponse précédente. **Répondre** envoie toutes vos réponses à la fois.
- S’il manque une information que vous seul avez, elle vous la demande et ne rédige que ce qui peut être envoyé sans cette information, par exemple une réponse qui confirme une date. Elle ne rédige pas une réponse qui dit seulement que vous reviendrez vers la personne.
- **Réessayer** relance la tâche. **Demander des modifications** permet de demander autre chose. Pour une tâche bloquée, **Réessayer** est l’action principale, et **Détails** montre ce qu’elle a tenté.
- Pendant la préparation, la tâche indique en une phrase simple ce que fait votre Machine, par exemple « Lecture des e-mails », « Lecture du PDF » ou « Rédaction du brouillon ». Les étapes détaillées restent dans le chat de la tâche.
- Une tâche marquée **En préparation…** démarre en quelques secondes. Si elle doit attendre, elle indique pourquoi et donne une estimation, par exemple « Démarre après la tâche en cours ».
- Un site vous demande de vous connecter : appuyez sur **Se connecter**, ou sur **Ouvrir le navigateur** pour vous connecter dans le navigateur. Elle reprend ensuite automatiquement. Sinon, appuyez sur **Continuer**.
- Un code envoyé sur votre téléphone ou une autorisation manquante arrête la tâche. Elle vous indique ce dont elle a besoin, puis vous propose **Continuer** ou **Réessayer**. Si une source n’est pas connectée, comme Slack, **Connecter Slack** apparaît dans la tâche. Elle reprend automatiquement une fois Slack connecté.
