"""What an error report's message may say (error_feed.normalize): the words errors are written in, the error types
and the services, safe_word, which checks one word against them, and the patterns for a domain and for the whole
message's shape. Plain data and one function, importing only re.

The control plane keeps a byte-for-byte copy (themachine-cloud's cloud/error_words.py, which its tests compare with this
file), so a word added here is also allowed there: change it here, then copy it over."""
import re


# Capitalized words an error message is written in. Any other capitalized word could be a name, so it goes (<word>).
WORDS = set('''A An The No Not Cannot Could Failed Failure Invalid Unexpected Unknown Missing Expected Bad Too Unable
Internal Bearer Error Errors Exception Timeout Timed Connection Network Request Response Object Value Key Index Type Attribute
Name Module Import Syntax Reference Range Abort Aborted Permission Denied Access Refused Reset Closed Broken Pipe File
Directory Database Table Column Row Query Operation Unsupported Undefined Null None True False NaN Infinity Uncaught
Promise Load Loading Script Network Fetch JSON HTTP HTTPS API URL SQL TLS SSL EOF UTF ASCII CSRF CORS DOM OK Is Was
Got Has Have Must Should Only Already Empty Out Of In On At For To From With Without And Or If Then Else Unhandled
Rejection Maximum Minimum Call Stack Size Exceeded Assertion Decode Encode Unicode Recursion Overflow Memory Zero
Division Lookup Stop Iteration Generator Runtime Not Implemented Gateway Machine Machines OpenClaw Telegram Gmail Google
Microsoft Outlook Slack WhatsApp Telegram Zoom Calendar Drive Network Fleet Graph Card Cards Chat Review Preparation Sync Token Tokens
Expired Authentication Auth Rate Limit Quota Service Unavailable Forbidden Unauthorized Server Client Found Read Write Socket'''.split())
TYPES = {'str', 'int', 'float', 'bool', 'bytes', 'dict', 'list', 'tuple', 'set', 'frozenset', 'NoneType', 'object', 'type',
         'function', 'method', 'module', 'datetime', 'date', 'Path', 'Row', 'Connection', 'Cursor', 'undefined', 'null',
         'number', 'string', 'boolean', 'symbol', 'bigint', 'Array', 'Object', 'Promise', 'Response', 'Element', 'HTMLElement',
         'Node', 'Window', 'Document'}
TYPE_NAME = re.compile(r'[A-Z][A-Za-z0-9]*(?:Error|Exception|Warning|Interrupt|Exit|Iteration|Type)')
SAFE_WORDS = {w.lower() for w in WORDS | TYPES} | set('''such attribute properties reading after s person email lookup delivery status android feed jwt parse reply draft rejected open cannot send see role has no name known next failed down gone error unavailable request response local at remote retry code result received returned does did not exist is was are been have network reach body text get set null sent timeout connection refused deprecation validation sync unknown outcome exceeded exception quota limit read write pending range invalid empty function expected dict list index key and or of the a an to from for in on with without by it its this that too many client server call file os errno'''.split())
# The words Python, the browser, SQLite and HTTP write their errors in: never a person's or a customer's, and without
# them a report says "<word> is not <word>" where it should say "database is locked" (2026-10-28)
SAFE_WORDS |= set('''defined locked column table constraint unique operand unsupported values value unpack literal base depth
maximum minimum recursion expecting line char column evaluating attempting resource fetch object readonly database disk full
denied permission directory closed reset peer broken pipe decode encode codec byte bytes position start end out memory
argument arguments positional keyword unexpected missing required takes given were but callable iterable subscriptable
hashable serializable json http https url ssl certificate verify handshake host resolution temporary failure aborted abort
operation cancelled canceled interrupted process exited signal killed terminated command found module property setting
undefined assignment before referenced variable global access initialization declaration token input syntax storage
transaction inactive version blocked because document focused allowed agent context changed load loading chunk script
dynamically imported worker service registration timed seconds deadline eof occurred violation protocol would block
temporarily unavailable try again files header headers content length type mismatch got instead must be should can could
convert float int string number nan infinity zero division modulo non iterator generator already executing running event
loop thread lock schema row rows query sql near incomplete bindings supplied current statement uses parameter parameters
foreign check integrity image malformed attempt gateway bad internal unauthorized forbidden conflict payload large
unprocessable entity rate limited later upstream proxy gaierror sqlite3 subprocess returned nonzero exit status
when while during into than as if then else only all any some more less same other one first last
'''.split())
# and a browser's (the dashboard, sw.js): "Failed to execute 'querySelector'", "Invalid time value", "Failed to register a ServiceWorker"
SAFE_WORDS |= set('''execute valid selector constant time match pattern register fetching date'''.split())
# Our own error codes with a word that isn't above (imap_no_inbox arrived as "<word>"): each only as a whole, exactly as
# the source raises it, so its words alone ("inbox") and anything else next to them still go. tests/test_error_codes.py
# reads every code in the source and says which belong here.
CODES = set('''auth.test caldav caldav_auth_failed caldav_bad_answer caldav_failed caldav_no_calendar caldav_not_configured
caldav_not_found caldav_password_missing caldav_plaintext_refused caldav_rate_limited caldav_redirect_refused
caldav_tls_failed caldav_too_big caldav_unreachable calendar_plaintext_refused code_wrong conversations.info
docs_drive_kind docs_edit_unsupported docs_file_kind docs_files_not_granted docs_find_empty docs_sheets docs_slides
docs_google_broker_not_configured docs_not_connected docs_writes_unsupported
email_setup_required ews ews_auth_failed ews_bad_answer ews_failed ews_not_configured ews_not_found
ews_password_missing ews_plaintext_refused ews_rate_limited ews_redirect_refused ews_refused ews_tls_failed ews_too_big
ews_unreachable exchange_online google_broker_not_configured google_meet_not_connected google_scope_not_granted
google_signin_expired_run_gog_auth_add ical_time ics ics_auth_failed ics_failed ics_gone ics_link_missing
ics_not_a_calendar ics_not_found ics_plaintext_refused ics_rate_limited ics_redirect_refused ics_tls_failed ics_too_big
ics_unreachable imap_no_folder imap_no_inbox imap_not_configured imap_password_missing imap_plaintext_refused
imap_uidvalidity_reset invalid_client_metadata invalid_grant invalid_redirect_uri linear_credential_unwritable
linear_graphql_error linear_invalid_viewer linear_writes_unsupported linkedin_security_check
microsoft_broker_not_configured microsoft_graph_not_configured microsoft_scope_not_granted missing_history_id
no_lasting_access not_installed not_set_up notion_credential_unwritable notion_invalid_me notion_owner_unknown
openclaw_add_failed password_wrong qr_expired repeated_graph_page rss_invalid_item rss_invalid_xml rss_redirects
salesforce_broker_not_configured salesforce_invalid_opportunity salesforce_invalid_task sent_message_not_confirmed
shortcut_credential_unwritable slack_accesslimited slack_broker_not_configured slack_channel_not_found
slack_ekm_access_denied slack_enterprise_is_restricted slack_fatal_error slack_not_authed slack_not_in_channel
slack_org_login_required slack_team_access_not_granted slack_token_revoked slack_two_factor_setup_required
slack_user_not_visible smtp_not_configured smtp_password_missing smtp_plaintext_refused stripe_broker_not_configured
teams_not_connected teams_not_granted teams_send_not_granted teams_work_only telegram_app_blocked unexpected_graph_link
unknown_purpose unsupported_grant_type users.conversations users.info web_page_redirects x_invalid_item
zoom_broker_not_configured'''.split())
SAFE_CODES = CODES | {'android_feed_unavailable', 'delivery_outcome_unknown', 'conversations.history', 'HTTP_'}
# The services a source error names (SourceError categories: salesflare:HTTP_401, trello_http, google_meet_invalid_page)
SERVICES = set('''gmail calendar outlook slack salesflare hubspot pipedrive intercom stripe zoom trello shortcut github google
meet linkedin x rss whatsapp android docs journal maton telegram openclaw gog wacli microsoft gbrain codex claude openai
anthropic crm imap smtp graph fleet notion granola jira linear asana airtable teams salesforce web'''.split())
# Words those codes are made of besides (each part of a snake_case or dotted code must be a known word or service)
SAFE_WORDS |= set('''invalid page cursor broker credential unreachable signin expired unreadable http missing timezone window feed
advancing opportunities join disabled method note transcript ratelimited browser busy reader signed story member move history workspace
search board action summary user host conference artifact maton shared replies off region profile conversation
conversations parts identity mismatch entry encoding transport source content message person mention account scope
notifications notification offline snapshot query unreachable stopped collector unsupported download no too large robots address html
response timestamp media payment redirect required answered stalled unlinked outdated logged'''.split())
# The phase a failed review names (review.REVIEW_FAILURE_PHASES): "model" arrived as "<word>" (2026-11-22)
SAFE_WORDS |= set('''model bridge queue provider tool draining'''.split())
SAFE_TYPES = set('''Error Exception Warning BaseException RuntimeError ValueError TypeError KeyError IndexError AttributeError NameError ImportError ModuleNotFoundError SyntaxError ReferenceError RangeError AbortError TimeoutError ConnectionError ConnectionResetError ConnectionRefusedError BrokenPipeError FileNotFoundError PermissionError OSError IOError EOFError UnicodeError UnicodeDecodeError UnicodeEncodeError RecursionError OverflowError MemoryError ZeroDivisionError AssertionError LookupError StopIteration SystemExit KeyboardInterrupt NotImplementedError OperationalError DatabaseError IntegrityError HttpError SourceError BrokerError'''.split())
SAFE_TYPES |= set('''NetworkError QuotaExceededError NotAllowedError NotFoundError InvalidStateError SecurityError DataError
DataCloneError TransactionInactiveError VersionError ConstraintError NotSupportedError DOMException UnknownError
InvalidAccessError NotReadableError EncodingError HTTPError URLError JSONDecodeError IsADirectoryError NotADirectoryError
FileExistsError ProgrammingError InterfaceError CalledProcessError TimeoutExpired SSLError SSLCertVerificationError
CancelledError InvalidURL RemoteDisconnected IncompleteRead ChildProcessError ProcessLookupError BlockingIOError
InterruptedError ConnectionAbortedError UnboundLocalError IndentationError ResourceWarning DeprecationWarning UserWarning
RuntimeWarning ArithmeticError BufferError SystemError EvalError URIError AggregateError InternalError ExceptionGroup
GeneratorExit StopAsyncIteration UnsupportedOperation BadZipFile ParseError ChunkLoadError TargetClosedError ProtocolError
ReadTimeout ConnectTimeout'''.split())


def safe_word(word):
    if word.lower() in SAFE_WORDS or word.lower() in SERVICES or word in SAFE_CODES or word in SAFE_TYPES:
        return True
    parts = [p for p in re.split(r'[_.]', word.lower()) if p]  # a code: salesflare_invalid_json, trello_http
    return len(parts) > 1 and all(p in SAFE_WORDS or p in SERVICES for p in parts)


# A bare domain name in a message (taken out as <url>). Not the two Slack methods that look like one, as a whole.
DOMAIN = re.compile(r'(?i)\b(?!(?-i:users|conversations)\.(?-i:info)(?![\w.-]))[\w-]+(?:\.[\w-]+)*\.(?:com|org|net|io|ai|be|nl|de|fr|uk|eu|co|app|dev|computer|me|info|biz|us|ca|es|it|ch|at|se|no|dk|fi|pl|pt|br|au|in|jp|cloud|tech|so|ly|xyz)\b(?![\w(])')
# What a sent message may look like, checked last (and again by the control plane): placeholders, plain ASCII words and
# a little punctuation, nothing else
SHAPE = re.compile(r'(?:<[a-z]{1,8}>|…|[A-Za-z_][A-Za-z0-9_$.]{0,39}|[.,:;()\[\]{}=<>!?+*/#&|%"\-]| )*')
