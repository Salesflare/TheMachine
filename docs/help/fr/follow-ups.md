---
title: Relances
area: graph
summary: Relance d’elle-même quand quelqu’un ne répond pas, pour tout un tableau ou un seul projet. Demande d’abord, sauf si vous dites autrement.
covers: follow-ups
code: follow_ups.py, assistant.py, dashboard.html
order: 4
---
Quand une personne d’un tableau ne répond plus, votre Machine rédige la relance pour vous, avec votre ton et dans la même conversation. Désactivé tant que vous ne l’activez pas. Si l’une de vos compétences correspond au tableau, les brouillons la suivent, y compris pour ce qui vient en premier dans l’e-mail.

## L’activer

**⋯** sur un tableau, puis **Relances…**, et cochez **Relancer sans réponse**. Cela vaut pour tous les projets de ce tableau. Ou touchez **Relances désactivées** sous le nom du tableau, ou **Les relancer** dans une étape avec des projets sans réponse depuis plus de 10 jours.

Pour un seul projet : **Relances…** dans le **⋯** de sa carte ou sur sa page. **Pour ce projet** choisit **Activé**, **Désactivée** ou le réglage du tableau. Le réglage propre d’un projet l’emporte sur celui du tableau.

## Réglages

- Attendre 3 à 7 jours sans réponse. Après l’attente la plus courte, une relance est rédigée. La plus longue est la limite à laquelle elle part, même quand votre utilisation est serrée.
- Relancer au moins 1 fois et au plus 3 fois. Le minimum part toujours. Entre les deux, elle rédige quand même chaque relance. Si elle pense qu’il vaut mieux arrêter, le brouillon dit pourquoi (« The Machine s’arrêterait ici : 9 e-mails sans réponse depuis août ») et n’est pas coché : envoyez-le, ignorez-le ou choisissez **Arrêter les relances ici**. Demandez-en une quand même dans le chat d’une relance et elle l’écrit. Jamais plus que le maximum.
- **Étapes** : **Toutes les étapes ouvertes**, donc ni la dernière étape du tableau ni Au point mort ou refusé. **Personnaliser** active ou désactive des étapes et donne à une étape sa propre attente.
- **Canaux** : ceux qui sont connectés et peuvent envoyer. Une relance part sur le même canal que le dernier message. **Changer de canal sans réponse** essaie le suivant autorisé.
- **Déplacer vers « Au point mort ou refusé » après la dernière** : activé quand le tableau a cette ligne.

## Demander ou envoyer seule

**Me demander avant d’envoyer** est le réglage par défaut : les brouillons attendent dans vos tâches. **Envoyer sans demander** est un oui permanent pour ce tableau ou ce projet. Ce qui sort de l’ordinaire vous attend quand même, tout comme ce qui échoue. En mode Prudent, elle demande toujours. Une relance ne part jamais deux fois.

Juste avant l’envoi, le fil est vérifié à nouveau, et si quelqu’un a écrit depuis le brouillon, elle ne part pas : « Non envoyé : nouveau message dans le fil ».

## Les vérifier

Les relances d’un tableau arrivent en une seule tâche, jamais une par e-mail. Pendant la rédaction, elle indique « Rédaction de 3 relances… », puis « 8 relances prêtes pour Alpha testers ».

**Vérifier** les affiche en entier, les unes sous les autres : un seul défilement suffit pour tout lire. **Envoyer**, **Modifier** et **Ignorer** apparaissent sur la relance en cours. Au clavier, j et k (ou les flèches) pour se déplacer, Entrée envoie, e modifie, s ignore et c réécrit. **Envoyer tout ce qui est coché** envoie celles encore cochées.

**Ignorer** décoche un brouillon et le place en bas, marqué Ignorée avec **Annuler** ; il n’est vraiment ignoré qu’à la fermeture de la vérification. Une relance ignorée revient avec **Récupérer** dans les relances du projet ou sur sa tâche dans Fait, tant qu’aucune relance plus récente n’est venue. La relance d’un seul projet est une tâche normale.

**Modifier…** réécrit tous les brouillons cochés, ou seulement celui en cours, comme vous le demandez ; rien n’est envoyé, et **Annuler la modification** rétablit l’ancien texte. Tant que la zone de modification est ouverte ou qu’une réécriture tourne, rien ne part, et un brouillon qui a changé s’affiche d’abord à nouveau.

Quand plusieurs partent à la suite, aussi avec Envoyer sans demander, chaque boîte mail en envoie une toutes les 30 à 45 secondes, et la tâche montre où on en est : « Envoi de 3 sur 8… ». **Arrêter l’envoi** arrête le reste : celle déjà en route part quand même, les autres reviennent en brouillons dans la vérification, à envoyer plus tard (« Envoi arrêté. Envoyées : 1. 11 gardées en brouillons. »).

## E-mails envoyés avant votre Machine

Les e-mails envoyés depuis une autre app, avant que votre Machine lise cette boîte, comptent aussi. Elle lit la conversation (ou, si elle ne peut pas, les e-mails précédents cités dans votre dernier), donc trois e-mails sans réponse comptent pour trois, et « Pas de réponse depuis » compte à partir du premier. Si le maximum est déjà atteint, elle n’en rédige pas d’autre.

## Quand elles s’arrêtent

Les relances s’arrêtent quand la personne répond, quand le projet est gagné, perdu, archivé ou déplacé vers une étape fermée, et quand vous en mettez une en attente ou l’ignorez. Avant de rédiger, votre Machine vérifie s’il y a du nouveau dans la conversation, pour ne pas relancer quelqu’un qui a déjà répondu ailleurs.

**Mettre en pause** dans **Relances…** suspend un tableau ou un projet sans désactiver les relances : rien n’est rédigé ni envoyé, aucune série ne se termine, et les tâches ouvertes restent ouvertes. Choisissez un jour de reprise, ou touchez **Reprendre** quand vous voulez. L’attente reprend là où elle était, et ce qui était dû arrive une par une. Entre-temps, il affiche **En pause**.

Après la dernière relance sans réponse, le projet affiche « Pas de réponse après 3 relances » et passe à Au point mort ou refusé si c’est activé. Arrêtées avant qu’une ne parte, il affiche « Relances arrêtées » et reste dans son étape.

Si son e-mail a été rejeté et qu'il existe une autre adresse, la relance y va ("Rejetée, maintenant à <adresse>"). Un brouillon dont l'adresse est rejetée avant l'envoi est retenu : "Non envoyé : <adresse> a été rejetée", et passe à son autre adresse, où il attend ton envoi.

Sans autre adresse, les relances passent sur LinkedIn ou WhatsApp quand c'est autorisé et que vous y échangez. Sinon elles s'arrêtent avec "E-mail non distribué". Quand le projet compte, tu reçois un to-do pour trouver une nouvelle adresse.

## Où les voir

L’en-tête du tableau indique « Relances activées, la prochaine jeu. ». La carte d’un projet montre sa prochaine relance, ou qu’une relance est prête. La page du projet liste ce qui est parti, y compris ce qui a été envoyé automatiquement.

Les relances attendent quand votre Machine est occupée par vos tâches ou proche de sa limite d’utilisation, puis rattrapent leur retard. Sur un tableau partagé, seule la Machine du propriétaire du projet relance.
