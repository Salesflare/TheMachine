---
title: Faire, et ce qui est envoyé
area: cards
summary: Faire prépare le travail. Rien n’est envoyé, payé ou modifié avant votre approbation.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: 54e03fdaf3c3365b
---
## Ce que fait **Faire**

**Faire** demande à votre Machine de préparer la tâche : rédiger une réponse, faire des recherches, remplir un formulaire. Elle utilise vos comptes et son propre navigateur, comme vous le feriez.

Pendant qu’elle travaille dans son navigateur, la tâche et son chat affichent cette page en direct, même entre les étapes, jusqu’à ce qu’elle ait terminé. Cliquez sur l’image pour ouvrir le navigateur. Dans la tâche, la page s’affiche en plus grand, avec **Arrêter** : une seule pression met immédiatement fin à cette exécution.

Avant de poursuivre ou de transférer la tâche, elle vérifie s’il y a de nouvelles réponses, y compris celles d’un collègue. Si la tâche a déjà été traitée, elle vous l’indique. Si elle a modifié un document ou une page, la tâche contient un lien vers celui-ci.

Quand elle réussit une tâche complexe sur un site ou dans un processus, votre Machine enregistre les étapes sous forme de compétence, sans les détails de qui que ce soit. Les tâches suivantes sur ce site s’en servent comme guide, jamais comme autorisation : l’envoi ou le paiement attend toujours votre accord. Elles apparaissent dans **Paramètres > Compétences**, avec la mention **Appris lors d’une tâche**.

## Rien n’est envoyé sans votre accord

- Une réponse revient sous forme de brouillon. **Vérifier et envoyer** l’ouvre pour que vous puissiez le modifier. Elle n’est envoyée que lorsque vous appuyez sur **Envoyer maintenant**.
- S’il y a au moins deux e-mails dans une tâche, un bouton dans son chat permet de tous les vérifier. Ils s’affichent l’un après l’autre avec **Suivant**, et la dernière étape les envoie tous. Chaque e-mail n’est marqué comme envoyé qu’une fois qu’il l’a été.
- Un e-mail s’affiche tel qu’il apparaîtra, avec le texte en gras, les listes et les liens. Un message Slack ou un message de chat est en texte brut.
- **Demander des modifications** dans la même fenêtre : indiquez ce qu’il faut changer et votre Machine refait le brouillon.
- Une réponse répond au dernier e-mail du fil, et la source de la tâche ouvre cet e-mail.
- Une étape qui valide une action, comme envoyer un formulaire, payer ou réserver, attend votre confirmation ou votre demande dans le chat. La confirmation d’une étape laisse les autres en attente : la tâche ne se termine que lorsque toutes les étapes sont terminées.
- La tâche et son chat indiquent ce qu’une telle étape envoie avant que vous appuyiez dessus. Une invitation de calendrier affiche son titre, son horaire, ses invités et indique si un lien de réunion est ajouté.
- Les calendriers connectés sont pris en compte lors de la recherche d’un horaire : votre Machine consulte vos réunions pour les jours concernés avant de vous proposer des horaires.
- Dans le chat d’une tâche, un brouillon n’est jamais envoyé dans le même message que celui qui l’a rédigé.
- En attendant votre approbation, la tâche reste dans **Pour vous**, avec le statut **Préparée**. La liste indique une seule fois que rien ne sera envoyé avant votre approbation. Une tâche qui attend toujours quelque chose de votre part affiche **Vous attend**. Elle indique qu’un brouillon a été envoyé uniquement après son envoi.
- Un long brouillon affiche ses 3 premières lignes. **Afficher plus**, ou un appui sur le texte, affiche la suite. **Vérifier et envoyer** affiche toujours le texte complet.

Selon la source, elle peut envoyer un e-mail, un message privé Slack ou un message WhatsApp, Telegram, LinkedIn ou X. L’article consacré à chaque connexion indique ce qu’elle peut envoyer.

## Modifier un e-mail

- Utilisez les boutons au-dessus du texte, ou `Ctrl B` pour le gras, `Ctrl I` pour l’italique et `Ctrl K` pour un lien (`⌘` sur Mac). Des boutons permettent aussi de créer une liste à puces ou numérotée.
- Un lien doit commencer par https://. Le texte collé est ajouté en texte brut, sans ses couleurs ni ses images.
- Les mises en forme incompatibles avec l’e-mail sont d’abord supprimées, puis le message affiche le résultat. Appuyez de nouveau sur **Envoyer maintenant** pour l’envoyer.
- L’e-mail est envoyé exactement comme il s’affiche, avec une copie en texte brut pour les applications de messagerie qui n’affichent pas la mise en forme.

## Quand ça ne fonctionne pas

- « Impossible d’envoyer depuis ici. » signifie que vous devez copier le brouillon avec **Copier le brouillon** et l’envoyer vous-même.
- **Attend votre aide** signifie qu’elle a une question : **Répondre**. **Bloqué** signifie qu’elle s’est arrêtée sans poser de question. La tâche vous indique pourquoi.
- Plusieurs questions ? Chacune propose ses propres choix ou un champ à remplir, parfois avec la réponse précédente déjà saisie. **Répondre** envoie toutes les réponses en même temps.
- Il manque une information que vous seul avez ? Elle vous la demande et ne rédige que ce qui peut l’être sans cette information, comme une réponse confirmant une date. Elle ne rédige pas une réponse qui dit seulement que l’information suivra.
- **Réessayer** relance la tâche. **Demander des modifications** permet de demander autre chose. Pour une tâche bloquée, **Réessayer** est proposé en premier, et **Détails** indique ce qu’elle a essayé.
- La tâche est bloquée parce que l’exécution elle-même a échoué ? Après la mise à jour de votre Machine, elle réessaie automatiquement cette tâche une fois.
- Elle réessaie automatiquement une exécution en échec au maximum deux fois. Ensuite, elle attend un nouvel élément, comme un nouveau message ou votre message dans son chat, ou que vous appuyiez sur **Réessayer**.
- Pendant la préparation, la tâche indique en une phrase ce que fait votre Machine, par exemple « Lecture des e-mails », « Lecture du PDF » ou « Rédaction du brouillon ». Les étapes détaillées restent dans le chat de la tâche.
- Une tâche marquée **En préparation…** démarre en quelques secondes. Si elle doit attendre, elle vous indique pourquoi et donne une estimation, par exemple « Démarre après la tâche en cours ».
- Une tâche préparée par votre Machine avant que vous la demandiez peut attendre pendant qu’elle économise votre quota d’utilisation. Le bouton **Faire** reste affiché : appuyez dessus pour la lancer immédiatement, avant les autres tâches. Rien n’est envoyé sans votre accord. Si votre forfait d’IA a atteint sa limite d’utilisation, Faire vous l’indique et la tâche démarre une fois la limite réinitialisée.
- Un site vous demande de vous connecter : appuyez sur **Se connecter**, ou sur **Ouvrir le navigateur** et connectez-vous. Elle reprend ensuite automatiquement. Si ce n’est pas le cas, appuyez sur **Continuer**.
- Un code envoyé sur votre téléphone ou une autorisation manquante l’arrête. La tâche indique ce dont elle a besoin, puis affiche **Continuer** ou **Réessayer**. Si une source n’est pas connectée, comme Slack, **Connecter Slack** s’affiche dans la tâche. Elle reprend automatiquement une fois Slack connecté.
