"""Sending on Teams: one owner-approved reply in the Teams chat (1:1, group or meeting) its to-do came from, as the owner.
check() validates a draft (next_actions.validate); TeamsTransport sends an approved one through the connector's one write
(connectors/teams.py Sender, Microsoft Graph's POST /chats/{chat}/messages with ChatMessage.Send). Never a channel post,
never a browser. A connection from before ChatMessage.Send says it needs a Reconnect and sends nothing."""
import datetime

from machine.owner_error import OwnerError

FIELDS = {'kind', 'label', 'account_id', 'chat_id', 'body'}
MAX_LENGTH = 8000  # well under what Teams takes in one message


def check(value, config, teams_chats):
    """A Teams draft as the card keeps it. The chat is one of this to-do's own Teams messages' chats (teams_chats, built
    by the service: never a channel thread, which goes as before), on the connection it came in on, which can send. The
    to-do's area doesn't change where its chat lives."""
    if set(value) - FIELDS:
        raise OwnerError('Unsupported Teams fields; plain text in the task’s Teams chat only')
    account = next((a for a in config['accounts'] if a['id'] == value.get('account_id') and a.get('service') == 'teams'), None)
    if not account or account.get('shared'):
        raise OwnerError('Use the Teams account belonging to this task')
    chat = (teams_chats or {}).get(str(value.get('chat_id') or ''))
    if not chat or chat.get('account_id') != account['id']:
        raise ValueError('Reply only in a Teams chat from this task’s own messages (chat_id is its metadata.chat_id); '
                         'a reply in a Teams channel thread goes as before')
    if chat.get('can_send') is False:
        raise ValueError('This Teams connection can’t send yet: it needs a Reconnect. Put the reply text in body, leave '
                         'next_actions empty and set needs: Reconnect Microsoft Teams to send it')
    result = {'kind': 'teams', 'account_id': account['id'], 'chat_id': str(value['chat_id']),
              'to_name': chat.get('name') or 'Teams chat', 'max_length': MAX_LENGTH}
    if value.get('label'):
        if value['label'] != 'Send' and not value['label'].startswith('Send '):
            raise OwnerError('Teams button labels must say Send, such as Send reply')
        result['label'] = value['label']
    body = value.get('body')
    if not isinstance(body, str) or not body.strip() or len(body) > MAX_LENGTH or '\x00' in body:
        raise OwnerError(f'Provide the concrete Teams message, at most {MAX_LENGTH} characters')
    result['body'] = body.strip()
    return result


class TeamsTransport:
    """Posts one owner-approved reply through connectors/teams.py Sender. Checks read-only first. Graph has no
    idempotency key: an unclear outcome is looked for in the chat afterwards and never sent again."""

    RECONNECT = 'Reconnect Microsoft Teams to send replies. Nothing was sent.'
    REFUSED = {'teams_send_not_granted': RECONNECT, 'teams_not_granted': RECONNECT,
               'teams_send_shared': 'A Teams sign-in shared through your Fleet only reads. Nothing was sent.',
               'teams_signin_expired': 'Microsoft Teams needs you to sign in again. Reconnect it. Nothing was sent.',
               'teams_not_connected': 'Microsoft Teams isn’t connected anymore. Nothing was sent.',
               'teams_work_only': 'Teams needs a work or school account. Nothing was sent.',
               'account_identity_mismatch': 'Teams is signed in as someone else now. Nothing was sent.'}

    def __init__(self, config, connector, helpers):
        self.config, self.connector, self.helpers = config, connector, helpers

    def sender(self, action):
        account = next((a for a in self.config['accounts'] if a['id'] == action['account_id'] and a.get('service') == 'teams'), None)
        if not account:
            raise OwnerError('That Teams connection is gone. Nothing was sent.')
        try:
            return self.connector.Sender(self.config, account, self.helpers)
        except self.helpers.SourceError as error:
            raise ValueError(self.REFUSED.get(error.category, 'Teams replies are off. Nothing was sent.')) from None

    def preflight(self, action):
        if action['kind'] != 'teams':
            raise OwnerError('Only an owner-approved Teams reply can use the Teams transport')
        try:
            self.sender(action).ready(action['chat_id'])
        except self.helpers.SourceError as error:
            if error.category == 'teams_http' and error.status in (403, 404, 410):  # refused, not found or deleted
                raise ValueError('That Teams chat can’t be reached from here anymore. Nothing was sent.') from None
            raise ValueError(self.REFUSED.get(error.category, 'I couldn’t reach Teams. Nothing was sent; tap Send again.')) from None

    def send(self, action, job):
        import ms_graph
        try:
            sender = self.sender(action)
        except ValueError:
            return {'rejected': 'refused'}
        try:
            message = sender.post(action['chat_id'], action['body'])
        except self.helpers.SourceError as error:  # no token, so nothing went out
            return {'rejected': error.category} if error.category in self.REFUSED else {'not_sent': True}
        except ms_graph.GraphError as error:
            if error.status == 429:
                return {'not_sent': True}  # Teams refused it for now and posted nothing: send it again shortly
            if error.status and 400 <= error.status < 500 and error.status != 408:
                return {'rejected': error.status}  # refused; nothing was posted
            return {}  # a timeout or a server error: unknown, reconcile reads the chat, never resends
        except Exception:  # noqa: BLE001 - unknown outcome: never resent
            return {}
        if isinstance(message, dict) and message.get('id'):
            return {'message_id': f"teams:{action['chat_id']}:{message['id']}"}
        return {}

    def reconcile(self, action, job):
        try:
            since = datetime.datetime.fromisoformat(job['created_at']) - datetime.timedelta(seconds=60)
            found = self.sender(action).find(action['chat_id'], action['body'], since)
        except (ValueError, KeyError, TypeError, self.helpers.SourceError):
            return {}
        return {'message_id': f"teams:{action['chat_id']}:{found[0]}"} if len(found) == 1 else {}
