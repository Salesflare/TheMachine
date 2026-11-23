"""A new post (X, LinkedIn, a forum), which The Machine has no send of its own for: the one step that posts it, told wherever a
run goes another way (next_actions.py, machine/app/card_actions.py). Imports nothing of The Machine's."""
import re

LAYER = 0  # how a new post goes out (a leaf)


def post_step(label, url='<the page where it is written>'):
    """How a run offers something that gets posted where The Machine has no send of its own: the last step the owner
    confirms, done in this Machine's browser (PREPARATION.md, The last step)."""
    return ('offer it as the last step, which the owner confirms and this Machine’s browser then does (no browser or sign-in needed to save it): '
            f'{{kind:finish,label:{label},url:{url},message:<exactly the text to post>,to_name:<the account it goes out from>,'
            'preview:<what goes out, from which account>,instructions:<switch to that account, enter exactly the text, post once>}')


def undelivered(kinds, outcome, needs, act, waiting):
    """A routine's draft (its `act`, post or send) that a result hands over as ready with nothing (the `kinds` of its actions) that posts
    or sends it: the owner would be left with Mark done on something that never went out. A question to them first is fine,
    and so is a channel The Machine can't post on: an Open link to its page, or (checked) words that say what they do."""
    if (act not in ('post', 'send') or outcome != 'needs_you' or str(needs or '').rstrip().endswith('?')
            or any(k in (*waiting, 'open') for k in kinds)):
        return []
    return ['nothing in next_actions ' + ('posts' if act == 'post' else 'sends') + ' this draft: use the send action for its channel, or, with none, '
            + post_step('Publish post' if act == 'post' else 'Send message')
            + '. Where no page takes it, or this Machine can’t do it there, add an Open link to the page where they do, or with no page save with checked:true and needs that says where and how they '
            + ('post it' if act == 'post' else 'send it')]


# Pages that only open a post already filled in, for the owner to check and post themselves in their own browser.
COMPOSERS = re.compile(r'https://(?:[a-z0-9-]+\.)*(?:(?:x|twitter)\.com/(?:intent/(?:post|tweet)|compose/(?:post|tweet)|share)'
                       r'|linkedin\.com/(?:sharing/share-offsite|shareArticle|feed/?\?(?:[^#]*&)?shareActive)'
                       r'|facebook\.com/sharer|threads\.(?:net|com)/intent/post|bsky\.app/intent/compose|reddit\.com/(?:r/[^/]+/)?submit)\b', re.I)
