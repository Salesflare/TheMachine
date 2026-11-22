---
title: Faire et ce qui est envoyé
area: cards
summary: Faire prépare le travail. Rien n’est envoyé, payé ni modifié tant que vous n’avez pas approuvé cette étape.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: a403aa339eba78aa
---
## Ce que fait l’action Faire

**Faire** demande à votre Machine de préparer la tâche : rédiger une réponse, rechercher des informations, remplir un formulaire. Elle utilise vos comptes et son propre navigateur, comme vous le feriez.

Pendant qu’elle travaille dans son navigateur, la tâche et son chat affichent cette page en direct, même entre les étapes, jusqu’à ce qu’elle ait terminé. Cliquez sur l’image pour ouvrir le navigateur. Dans la tâche, il s’affiche en plus grand, avec **Arrêter** : une seule pression met fin à cette exécution.

Avant une relance ou un transfert, elle vérifie s’il y a de nouvelles réponses, y compris celles d’un collègue. Si la tâche a déjà été traitée, elle vous l’indique. Si elle a modifié un document ou une page, la tâche contient un lien vers cet élément.

Quand une tâche complexe aboutit sur un site ou dans un processus, votre Machine enregistre les étapes sous forme de compétence, sans aucune information personnelle. Les tâches suivantes sur ce site s’en servent comme guide, jamais comme autorisation : l’envoi ou le paiement attend toujours votre accord. Elles apparaissent dans **Paramètres > Compétences**, sous **Appris lors d’une tâche**.

## Rien n’est envoyé sans votre accord

- Une réponse est créée sous forme de brouillon. **Vérifier et envoyer** l’ouvre pour que vous puissiez le modifier. Il n’est envoyé que lorsque vous appuyez sur **Envoyer maintenant**.
- Pour deux e-mails ou plus dans une même tâche, un bouton dans le chat permet de tous les vérifier. Ils s’affichent l’un après l’autre avec **Suivant**. La dernière étape les envoie tous. Chaque e-mail n’est indiqué comme envoyé qu’une fois qu’il l’a été.
- Un e-mail s’affiche tel qu’il apparaîtra, avec le gras, les listes et les liens. Un message Slack ou un message de chat s’affiche en texte brut.
- **Demander des modifications** dans la même fenêtre : dites quoi modifier et votre Machine refait le brouillon.
- Une réponse répond au dernier e-mail de la conversation, et la source de la tâche ouvre cet e-mail.
- Une étape qui valide une action, comme envoyer, payer ou réserver, attend votre confirmation ou que vous le demandiez dans le chat. La confirmation d’une étape laisse les autres en attente : la tâche ne se termine que lorsque toutes les étapes sont terminées.
- La tâche et son chat affichent ce qu’une telle étape enverra avant que vous appuyiez dessus. Une invitation d’agenda affiche son titre, son heure, ses invités et indique si un lien de réunion est ajouté.
- Les agendas connectés sont pris en compte lors de la recherche d’un horaire : elle consulte vos réunions pour les jours concernés avant de vous proposer des horaires.
- Dans le chat d’une tâche, un brouillon n’est jamais envoyé dans le même message que celui qui l’a rédigé.
- Tant que vous n’avez pas approuvé le résultat, la tâche reste dans **Pour vous**, avec le statut **Préparée**. La liste précise que rien ne sera envoyé avant votre approbation. **Préparée** signifie qu’un brouillon ou un résultat est prêt à être approuvé. Si le travail se termine sans résultat parce qu’elle a besoin de vous (pour une décision, une information manquante, une connexion ou un choix), la tâche affiche plutôt **Vous attend**, avec une ligne précisant ce dont elle a besoin. Il en va de même pour la notification et le récap du matin. Un brouillon n’est indiqué comme envoyé qu’une fois réellement envoyé.
- Un long brouillon affiche ses 3 premières lignes. **Afficher plus**, ou toucher le texte, ouvre la suite. **Vérifier et envoyer** affiche toujours l’intégralité du brouillon.

Selon la source, elle peut envoyer un e-mail, un message privé Slack ou un message WhatsApp, Telegram, LinkedIn ou X. L’article consacré à chaque connexion précise ce qu’elle peut envoyer.

## Modifier un e-mail

- Utilisez les boutons au-dessus du texte, ou `Ctrl B` pour le gras, `Ctrl I` pour l’italique et `Ctrl K` pour un lien (`⌘` sur Mac). Des boutons permettent aussi de créer une liste à puces ou numérotée.
- Un lien doit commencer par https://. Le texte collé est ajouté en texte brut, sans ses couleurs ni ses images.
- La mise en forme incompatible avec les e-mails est d’abord supprimée, et le message affiche le résultat final. Appuyez de nouveau sur **Envoyer maintenant** pour l’envoyer.
- L’e-mail est envoyé exactement comme il s’affiche, avec une copie en texte brut pour les applications de messagerie qui ne prennent pas en charge la mise en forme.

## En cas de problème

- « Impossible d’envoyer depuis ici. » signifie que vous pouvez copier le brouillon avec **Copier le brouillon** et l’envoyer vous-même.
- **Attend votre aide** signifie qu’elle a une question : **Répondre**. **Bloqué** signifie qu’elle s’est arrêtée sans poser de question. La tâche en indique la raison.
- Vous avez posé plusieurs questions ? Chacune propose ses propres choix ou un champ de réponse courte, parfois prérempli avec votre réponse précédente. **Répondre** envoie toutes les réponses ensemble.
- Il manque une information que vous seul avez ? Elle vous la demande et rédige uniquement ce qui peut être fait sans cette information, par exemple une réponse pour confirmer une date. Elle ne rédige pas une réponse qui dit seulement que l’information arrive.
- **Réessayer** relance la tâche. **Demander des modifications** permet de demander autre chose. Pour une tâche bloquée, **Réessayer** est proposé en premier et **Détails** affiche ce qu’elle a tenté.
- Elle est bloquée parce que l’exécution a échoué ? Après la mise à jour de votre Machine, elle réessaie cette tâche une fois automatiquement.
- Elle réessaie automatiquement une exécution ayant échoué au maximum deux fois. Ensuite, elle attend un nouvel élément, comme un nouveau message ou un message de votre part dans son chat, ou que vous appuyiez sur **Réessayer**.
- Pendant la préparation, la tâche indique brièvement ce que fait votre Machine, par exemple « Lecture de l’e-mail », « Lecture du PDF » ou « Rédaction du brouillon ». Les étapes détaillées restent dans le chat de la tâche.
- Une tâche avec le statut **En préparation…** démarre en quelques secondes. Si elle doit attendre, elle explique pourquoi et indique une estimation, par exemple « Démarre après la tâche en cours ».
- Une tâche que votre Machine prépare avant que vous la demandiez peut attendre pour économiser votre utilisation. Le bouton **Faire** reste affiché : appuyez dessus pour démarrer immédiatement, avant les autres tâches. Rien n’est envoyé sans votre accord. Si vous avez atteint la limite d’utilisation de votre forfait IA, Faire vous l’indique et la tâche démarre à la réinitialisation de la limite.
- Un site vous demande de vous connecter : appuyez sur **Se connecter**, ou sur **Ouvrir le navigateur** pour vous connecter depuis celui-ci. Elle reprend ensuite automatiquement. Si ce n’est pas le cas, appuyez sur **Continuer**.
- Un code envoyé sur votre téléphone ou une autorisation manquante peut l’arrêter. La tâche indique ce dont elle a besoin, puis affiche **Continuer** ou **Réessayer**. Si une source n’est pas connectée, comme Slack, **Connecter Slack** s’affiche dans la tâche. Elle reprend automatiquement une fois Slack connecté.
