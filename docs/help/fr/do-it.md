---
title: Faire et ce qui est envoyé
area: cards
summary: Faire prépare le travail. Rien n’est envoyé, payé ni modifié avant votre accord.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: d6651fe1eee401f4
---
## À quoi sert **Faire**

**Faire** demande à votre Machine de préparer la tâche : rédiger une réponse, chercher des informations, remplir un formulaire. Elle utilise vos propres comptes et son propre navigateur, comme vous le feriez.

Pendant qu’elle travaille dans son navigateur, la tâche et son chat affichent cette page en direct, même entre deux étapes, jusqu’à ce que la tâche soit terminée. Cliquez sur l’image pour ouvrir le navigateur. Dans la tâche, l’image s’affiche en plus grand, avec **Arrêter** : une seule pression interrompt immédiatement cette exécution.

Avant une relance ou un transfert, elle vérifie s’il y a de nouvelles réponses, y compris celles d’un collègue. Si la tâche est déjà traitée, elle vous le signale. Si elle a modifié un document ou une page, la tâche contient un lien vers cet élément.

Lorsqu’une tâche difficile aboutit sur un site ou dans un processus, votre Machine en conserve les étapes sous forme de compétence, sans aucune information personnelle. Les tâches suivantes sur ce site s’en servent comme guide, jamais comme autorisation : l’envoi ou le paiement attend toujours votre accord. Elles apparaissent dans **Paramètres > Compétences**, sous **Appris lors d’une tâche**.

## Rien n’est envoyé sans votre accord

- Une réponse est enregistrée comme brouillon. **Vérifier et envoyer** l’ouvre pour que vous puissiez la modifier. Elle n’est envoyée que lorsque vous appuyez sur **Envoyer maintenant**.
- S’il y a au moins deux e-mails dans une même tâche, un bouton dans le chat permet de tous les vérifier. Ils s’affichent l’un après l’autre avec **Suivant**. La dernière étape les envoie tous. Chaque e-mail n’est indiqué comme envoyé qu’une fois qu’il l’a été.
- Un e-mail s’affiche tel qu’il apparaîtra, avec le gras, les listes et les liens. Un message Slack ou un message de chat est en texte brut.
- **Demander des modifications** dans la même fenêtre : indiquez ce qu’il faut changer et votre Machine refait le brouillon.
- Une réponse répond au dernier e-mail du fil, et la source de la tâche ouvre cet e-mail.
- Une étape qui valide une action, comme envoyer un formulaire, payer ou réserver, attend votre confirmation ou votre demande dans le chat. La confirmation d’une étape laisse les autres en attente : la tâche ne se termine que lorsque toutes les étapes sont terminées.
- La tâche et son chat montrent ce qu’une telle étape enverra avant que vous appuyiez dessus. Une invitation de calendrier affiche son titre, son horaire, ses invités et indique si un lien de réunion est ajouté.
- Les calendriers connectés sont pris en compte lors de la recherche d’un créneau : elle consulte vos réunions prévues ces jours-là avant de vous proposer des horaires.
- Dans le chat d’une tâche, un brouillon n’est jamais envoyé dans le même message que celui qui l’a rédigé.
- Tant que vous n’avez pas donné votre accord, la tâche attend sous **Pour vous**, avec le statut **Préparée**. La liste indique une seule fois que rien ne sera envoyé avant votre accord. Une tâche qui attend encore quelque chose de votre part affiche **Vous attend**. Elle n’indique qu’un brouillon a été envoyé qu’une fois l’envoi effectué.
- Un long brouillon affiche ses 3 premières lignes. **Afficher plus**, ou un appui sur le texte, ouvre la suite. **Vérifier et envoyer** affiche toujours le texte en entier.

Selon la source, elle peut envoyer un e-mail, un message privé Slack, ou un message WhatsApp, Telegram, LinkedIn ou X. L’article consacré à chaque connexion indique ce qu’elle peut envoyer.

## Modifier un e-mail

- Utilisez les boutons au-dessus du texte, ou `Ctrl B` pour le gras, `Ctrl I` pour l’italique et `Ctrl K` pour un lien (`⌘` sur Mac). Des boutons permettent aussi de créer des listes à puces ou numérotées.
- Un lien doit commencer par https://. Le texte collé est inséré en texte brut, sans ses couleurs ni ses images.
- Les mises en forme incompatibles avec l’e-mail sont d’abord supprimées, puis le message affiche le résultat. Appuyez de nouveau sur **Envoyer maintenant** pour l’envoyer.
- L’e-mail est envoyé exactement comme il s’affiche, avec une copie en texte brut pour les applications de messagerie qui ne prennent pas en charge la mise en forme.

## En cas de problème

- « Impossible d’envoyer depuis ici. » signifie que vous devez copier le brouillon avec **Copier le brouillon**, puis l’envoyer vous-même.
- **Attend votre aide** signifie qu’une question vous est posée : **Répondre**. **Bloqué** signifie que la tâche s’est arrêtée sans poser de question. La tâche vous indique pourquoi.
- Plusieurs questions ? Chacune propose ses propres choix ou un champ de réponse court, parfois prérempli avec votre dernière réponse. **Répondre** envoie toutes vos réponses en même temps.
- Il manque une information que vous seule avez ? Elle vous la demande et ne rédige que ce qui peut être envoyé sans cette information, comme une réponse qui confirme une date. Elle ne rédige pas une réponse qui dit seulement que cela arrive.
- **Réessayer** relance la tâche. **Demander des modifications** permet de demander autre chose. Pour une tâche bloquée, **Réessayer** apparaît en premier et **Détails** indique ce qui a été tenté.
- Pendant la préparation, la tâche indique en une phrase simple ce que fait votre Machine, par exemple « Lecture des e-mails », « Lecture du PDF » ou « Rédaction du brouillon ». Les étapes détaillées restent dans le chat de la tâche.
- Une tâche marquée **En préparation…** démarre en quelques secondes. Si elle doit attendre, elle vous indique pourquoi et donne une estimation, par exemple « Démarre après la tâche en cours ».
- Un site vous demande de vous connecter : appuyez sur **Se connecter**, ou sur **Ouvrir le navigateur** et connectez-vous depuis celui-ci. La tâche reprend ensuite automatiquement. Si ce n’est pas le cas, appuyez sur **Continuer**.
- Un code envoyé sur votre téléphone ou une autorisation manquante arrête la tâche. Elle vous indique ce dont elle a besoin, puis affiche **Continuer** ou **Réessayer**. Si une source n’est pas connectée, comme Slack, **Connecter Slack** s’affiche dans la tâche. Elle reprend automatiquement une fois Slack connecté.
