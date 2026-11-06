"""Mail signatures in the service (signatures.py keeps them): Settings' view of each mailbox's signature, the one the
mailbox itself has (Gmail's own, or Outlook's from its sent mail) and the owner's changes. Moved out of assistant.App
as is. A mixin of assistant.App (APP_MIXINS)."""
import ms_graph
import next_actions
import signatures
from sources import credential, gog_read


class SignaturesApp:
    ACTIONS = {}  # its actions are still App.action's own branches

    def signature_view(self):
        """Each mailbox's signature for Settings: the owner's own, or the one imported from the mailbox (cleaned HTML),
        and where it came from: owner, imported (Gmail's own), detected (Outlook's sent mail) or '' (none yet)."""
        return [{'account_id': a['id'], 'email': a.get('email', ''), 'service': a.get('service', 'gmail'),
                 'html': (entry or {}).get('html', ''), 'source': (entry or {}).get('source', ''),
                 'saveable': bool(signatures.path(self.config))}
                for a in self.config.get('accounts', []) if next_actions.mail_account(a)
                for entry in [signatures.get(self.config, a['id'])]]

    def mailbox_signature(self, account):
        """The signature the mailbox itself has, cleaned: Gmail's own (sendAs, read with gmail.readonly, the scope the
        send check already uses), or for Outlook, which has no signature API, the one its sent mail ends with."""
        if account.get('service') == 'outlook':
            try:
                return signatures.detect(ms_graph.sent_bodies(self.config, credential, account),
                                         (str(self.config.get('owner_name') or '').split() or [''])[0]), 'detected'
            except ms_graph.GraphError as error:
                raise ValueError(f'Outlook could not be read now ({error})') from None
        try:
            send_as = (getattr(self, 'mail_read', None) or gog_read)(
                self.config, account, 'gmail', 'v1', 'gmail.users.settings.sendAs.get',
                {'userId': 'me', 'sendAsEmail': account['email']}, 'https://www.googleapis.com/auth/gmail.readonly')
        except Exception:
            raise ValueError('Gmail could not be read now; try again in a minute') from None
        return signatures.clean((send_as or {}).get('signature') or ''), 'imported'

    def signature_action(self, name, args):
        account = next((a for a in self.config.get('accounts', []) if a['id'] == args.get('account_id') and next_actions.mail_account(a)), None)
        if not account:
            raise ValueError('Choose one of your Gmail or Outlook accounts')
        if name == 'detect_signature':
            # Import: kept as the mailbox's signature unless the owner has their own, which stays.
            found, source = self.mailbox_signature(account)
            if signatures.path(self.config):
                signatures.save(self.config, account['id'], found, source)
            return {'html': found, 'found': bool(signatures.text(found).strip() or '<img' in found), 'source': source,
                    'signatures': self.signature_view()}
        if args.get('use_mailbox') is True:
            # Back to the mailbox's own: the owner's version goes, and the mailbox's is imported again.
            signatures.remove(self.config, account['id'])
            try:
                found, source = self.mailbox_signature(account)
                signatures.save(self.config, account['id'], found, source)
            except ValueError:
                pass  # read again at the next send
            return self.signature_view()
        # Judged once cleaned: a signature pasted from Outlook or Word carries markup that cleaning drops; cut short, it
        # would be stored broken.
        value = str(args.get('html') or '')
        if len(value) > signatures.MAX_PASTED or len(signatures.clean(value, signatures.MAX_PASTED, None)) > signatures.MAX_HTML:
            raise ValueError('That signature is too long')
        signatures.save(self.config, account['id'], value, 'owner')
        return self.signature_view()
