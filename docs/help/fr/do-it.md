---
title: Faire, et ce qui est envoyé
area: cards
summary: Faire prépare le travail. Rien n’est envoyé, payé ou modifié avant que vous approuviez l’étape.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: b0f79ee45009cfde
---
## Ce que fait Faire

**Faire** demande à votre Machine de préparer la tâche : rédiger une réponse, faire des recherches, remplir un formulaire. Elle utilise vos comptes et son propre navigateur, comme vous le feriez.

Pendant qu’elle travaille dans son navigateur, la tâche et son chat affichent la page en direct, y compris entre les étapes, jusqu’à ce que le travail soit terminé. Cliquez sur l’image pour ouvrir le navigateur. Dans la tâche, elle s’affiche en plus grand, avec **Arrêter** : une pression met immédiatement fin à cette exécution.

Avant un suivi ou un transfert, elle vérifie s’il y a de nouvelles réponses, y compris celles d’un collègue. Si la tâche a déjà été traitée, elle vous l’indique. Si elle a modifié un document ou une page, la tâche contient un lien vers cet élément.

Quand une tâche complexe aboutit sur un site ou dans un processus, votre Machine conserve les étapes sous forme de compétence, sans aucune donnée personnelle. Les tâches suivantes sur ce site s’en servent comme guide, jamais comme autorisation : l’envoi ou le paiement attend toujours votre accord. Vous les trouverez dans **Paramètres > Compétences**, sous **Appris lors d’une tâche**.

## Rien n’est envoyé sans votre accord

- Une réponse est préparée sous forme de brouillon. **Vérifier et envoyer** l’ouvre pour que vous puissiez la modifier. Elle est envoyée uniquement lorsque vous appuyez sur **Envoyer maintenant**.
- Pour au moins deux e-mails dans une même tâche, un bouton dans son chat permet de tous les vérifier. Ils s’affichent l’un après l’autre avec **Suivant**. La dernière étape les envoie tous. Chaque e-mail n’apparaît comme envoyé qu’une fois qu’il l’a été.
- Un e-mail s’affiche tel qu’il sera envoyé, avec le texte en gras, les listes et les liens. Un message Slack ou un message de chat s’affiche en texte brut.
- **Demander des modifications** dans la même fenêtre : indiquez ce qu’il faut changer et votre Machine reprend le brouillon.
- Une réponse répond au dernier e-mail de la conversation, et la source de la tâche ouvre cet e-mail.
- Une étape qui confirme une action, comme envoyer un formulaire, payer ou réserver, attend votre confirmation ou votre demande dans le chat. Confirmer une étape ne valide pas les autres : la tâche se termine uniquement une fois toutes les étapes effectuées.
- La tâche et son chat indiquent ce qu’une telle étape enverra avant que vous appuyiez dessus. Une invitation d’agenda affiche son titre, son horaire, ses invités et précise si un lien de réunion est ajouté.
- Les agendas connectés sont pris en compte dans la recherche d’un horaire : elle consulte vos réunions pour ces jours avant de vous proposer des heures.
- Dans le chat d’une tâche, un brouillon n’est jamais envoyé dans le même message que celui qui l’a rédigé.
- Tant que vous n’avez pas donné votre accord, la tâche reste dans **Pour vous**, avec le statut **Préparée**. La liste indique alors une seule fois que rien ne sera envoyé avant votre accord. **Préparée** signifie qu’un brouillon ou un résultat est prêt à être approuvé. Si le travail se termine sans résultat parce qu’il a besoin de vous, par exemple pour prendre une décision, fournir une information manquante, vous connecter ou faire un choix, la tâche affiche plutôt **Vous attend**, avec une ligne précisant ce dont elle a besoin. C’est aussi le cas si elle s’est contentée de répondre ou d’expliquer (« Réponse donnée. Rien de fait pour l’instant. »), avec **Faire** en premier. Il en va de même pour sa notification et le récap du matin. Elle indique qu’un brouillon a été envoyé uniquement une fois qu’il l’a été.
- Un long brouillon affiche ses 3 premières lignes. **Afficher plus**, ou un appui sur le texte, ouvre le reste. **Vérifier et envoyer** affiche toujours le brouillon en entier.

Selon la source, elle peut envoyer un e-mail, un message privé Slack ou un message WhatsApp, Telegram, LinkedIn ou X. L’article de chaque connexion précise ce qu’elle peut envoyer.

## Modifier un e-mail

- Utilisez les boutons au-dessus du texte, ou `Ctrl B` pour le gras, `Ctrl I` pour l’italique et `Ctrl K` pour un lien (`⌘` sur Mac). Des boutons permettent aussi de créer une liste à puces ou numérotée.
- Un lien doit commencer par https://. Le texte collé est inséré en texte brut, sans ses couleurs ni ses images.
- Le formatage incompatible avec l’envoi d’un e-mail est d’abord supprimé. Le message affiche alors le résultat. Appuyez de nouveau sur **Envoyer maintenant** pour l’envoyer.
- L’e-mail est envoyé exactement comme affiché, avec une copie en texte brut pour les applications de messagerie qui ne prennent pas en charge le formatage.

## Si elle ne peut pas le faire

- « Impossible d’envoyer ceci depuis ici. » signifie que vous devez copier le brouillon avec **Copier le brouillon**, puis l’envoyer vous-même.
- Si **Vous attend** s’affiche et qu’il n’y a rien à envoyer, ouvrir ou lire, l’action proposée en premier est **Répondre**. Indiquez ce dont la tâche a besoin pour qu’elle continue. Pour une étape que vous seul pouvez effectuer, comme un paiement dans votre banque, l’action proposée en premier est **Marquer comme fait**.
- **Attend votre aide** signifie qu’elle a une question : **Répondre**. **Bloqué** signifie qu’elle s’est arrêtée sans poser de question. La tâche vous en indique la raison.
- Vous avez posé plusieurs questions ? Chacune propose ses propres choix ou un champ à remplir, parfois prérempli avec votre dernière réponse. **Répondre** les envoie toutes ensemble.
- Il lui manque une information que vous seul avez ? Elle vous la demande et prépare uniquement ce qu’elle peut faire sans, par exemple une réponse pour confirmer une date. Elle ne rédige pas une réponse qui dit seulement que cette information suivra.
- **Réessayer** relance la tâche. **Demander des modifications** permet de demander autre chose. Pour une tâche bloquée, **Réessayer** apparaît en premier, et **Détails** indique ce qu’elle a tenté.
- La tâche est bloquée parce que l’exécution a échoué ? Après une mise à jour de votre Machine, elle réessaie une fois toute seule.
- Elle réessaie automatiquement une exécution échouée au maximum deux fois. Ensuite, elle attend un nouvel élément, comme un nouveau message ou votre réponse dans son chat, ou que vous appuyiez sur **Réessayer**.
- Pendant la préparation, la tâche indique en termes simples ce que fait votre Machine, par exemple « Lecture des e-mails », « Lecture du PDF » ou « Rédaction du brouillon ». Les étapes détaillées restent dans le chat de la tâche.
- Une tâche marquée **En préparation…** démarre en quelques secondes. Si elle doit attendre, elle indique pourquoi et donne une estimation, par exemple « Démarre après la tâche en cours ».
- Une tâche préparée par votre Machine avant que vous la demandiez peut attendre pendant qu’elle économise votre quota. **Faire** reste affiché : appuyez dessus pour la démarrer immédiatement, avant les autres tâches. Rien n’est envoyé sans votre accord. Si la limite d’utilisation de votre forfait IA est atteinte, Faire vous l’indique et la tâche démarre lorsque la limite est réinitialisée.
- Un site vous demande de vous connecter : appuyez sur **Se connecter**, ou sur **Ouvrir le navigateur** pour vous connecter dans le navigateur. La tâche reprend ensuite toute seule. Si ce n’est pas le cas, appuyez sur **Continuer**.
- Un code envoyé sur votre téléphone ou une autorisation manquante l’arrête. La tâche indique ce dont elle a besoin, puis affiche **Continuer** ou **Réessayer**. Si une source n’est pas connectée, comme Slack, **Connecter Slack** apparaît dans la tâche. Elle continue toute seule une fois Slack connecté.
