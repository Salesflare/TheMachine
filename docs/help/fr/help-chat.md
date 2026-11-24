---
title: Demander de l’aide
area: getting-started
summary: Posez vos questions sur le fonctionnement de The Machine. Les réponses s’appuient sur ces pages d’aide et contiennent des liens.
covers: help-chat
code: help_chat.py, dashboard.html
order: 6
translated: 85d9614a8670bdf4
---
Cliquez sur **Aide** en bas de la barre latérale, au-dessus de **Paramètres**, et posez votre question avec vos propres mots, par exemple : « Comment mettre une tâche en attente ? ». Appuyez sur Entrée pour envoyer votre question, ou sur Shift+Enter pour ajouter une ligne. Aide répond dans la langue de votre application ou dans celle que vous utilisez pour écrire. Les liens vers les pages d’aide s’ouvrent directement dans le panneau, dans cette langue.

## D’où viennent les réponses

Aide consulte les pages d’aide correspondant à votre question et le code de l’application pour les sujets qu’elles ne couvrent pas. Si ces résultats portent sur un autre sujet, elle relance une recherche avec d’autres termes. Chaque réponse renvoie vers les pages utilisées.

Cette fonction utilise le modèle de votre Machine dans un chat court et séparé. Sous la zone de message, vous pouvez choisir un autre modèle ou un autre niveau de réflexion pour ce chat avec Aide (voir [Modèle](model.md)). Seuls votre question et les pages correspondantes sont transmis : aucun de vos messages, aucune information sur les personnes ni aucun paramètre.

Les réponses s’adaptent à votre niveau : elles sont formulées simplement pour la plupart des personnes et plus en détail si vos questions sont techniques. Aide estime votre niveau à partir de votre configuration, de votre rôle et de votre façon de poser vos questions. Seule cette estimation est transmise.

Aide indique d’abord ce que The Machine sait déjà faire et ne suggère une compétence que si aucune fonction intégrée ne convient. Voir [Personnaliser](personalize.md).

## Ce que voit l’équipe

Pour améliorer l’aide, votre Machine compte quelques mots qui indiquent le sujet de chaque question, par exemple « mettre une tâche en attente ». Elle ne transmet jamais votre question ni la réponse, ni aucun nom, adresse ou numéro : seulement des mots tirés de ces pages d’aide. Une fois par jour, ces compteurs sont envoyés à l’équipe The Machine, sans être associés à votre compte.

Pour arrêter cet envoi, désactivez **Partager ce qu’on demande à l’aide** dans **Paramètres**, sous **Sécurité**, dans la section **L’équipe The Machine**, ou choisissez le niveau de sécurité **Prudent** ([niveau de sécurité](security-levels.md)). Cette option nécessite [The Machine Network](/network). Les données qui n’ont pas encore été envoyées sont supprimées.

## Ce qu’Aide ne peut pas faire

Aide répond aux questions. Elle ne peut pas consulter vos données et ne modifie rien : elle vous indique plutôt où cliquer.

Si votre description évoque un dysfonctionnement plutôt qu’une question sur la marche à suivre, la réponse se termine par **Signaler ce bug**. Ce bouton ouvre **Signaler un bug** avec un bref résumé de ce que vous avez fait, de ce à quoi vous vous attendiez et de ce qui s’est passé. Le signalement au support est déjà coché. Vous pouvez tout modifier. Rien n’est envoyé tant que vous n’appuyez pas sur **Envoyer**.

**Signaler un bug** est aussi un onglet à part entière dans le même panneau. Voir [Contacter le support](get-support.md#report-a-bug).
