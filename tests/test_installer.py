"""install.sh / installer.py against a temporary HOME with stub openclaw and systemctl.
Nothing here touches the real user's systemd, OpenClaw or data directory."""
import builtins, json, os, re, shutil, socket, stat, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest import mock

import installer

ROOT = Path(__file__).resolve().parent.parent
REINDEX_RUNNING = installer.reindex_running  # the real one: InstallerTest.setUp turns it off for every other test
STUB = '''#!/bin/sh
echo "{name} $*" >> "{log}"
if [ "$*" = "$ASSISTANT_TEST_FAIL" ]; then echo "Synthetic failure" >&2; exit 1; fi
case "$*" in --version) echo "OpenClaw 2026.11.2 (test)";; *list-unit-files*) echo "openclaw-gateway.service enabled enabled";;
  "--user is-active "*) case " $ASSISTANT_TEST_ACTIVE " in *" $3 "*) echo active;; *) echo inactive; exit 3;; esac;; esac
exit 0
'''
ANSWERS = {'ASSISTANT_OWNER_NAME': 'Alex Owner', 'ASSISTANT_TELEGRAM_OWNER': '1000001',
           'ASSISTANT_TAILSCALE_OWNER': 'alex@example.com', 'ASSISTANT_DASHBOARD_HOST': 'machine.example-tailnet.ts.net',
           'ASSISTANT_TIMEZONE': 'Europe/Amsterdam', 'ASSISTANT_CONNECTORS': 'gmail,calendar,gateway',
           'ASSISTANT_EMAIL': 'alex@example.com', 'ASSISTANT_GOG_CLIENT': 'work', 'ASSISTANT_BOUNDARY': 'work:Acme'}


def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


class OpenClawUpdateNote(unittest.TestCase):
    def test_an_older_openclaw_gets_the_update_path_that_migrates_its_data(self):
        said = []
        versions = {'node': 'v24.22.1\n', 'openclaw': 'OpenClaw 2026.10.7 (abc)\n'}
        run = lambda args, **kw: subprocess.CompletedProcess(args, 0, versions.get(Path(args[0]).name, ''), '')
        for have, noted in (('2026.10.7', True), (installer.required_openclaw(), False)):
            versions['openclaw'] = f'OpenClaw {have} (abc)\n'
            said.clear()
            with mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer, 'say', side_effect=said.append), \
                    mock.patch.object(installer.shutil, 'which', side_effect=lambda name: f'/bin/{name}' if name in ('node', 'openclaw') else None), \
                    mock.patch.object(installer, 'resolve_tool', side_effect=lambda path: path), \
                    mock.patch.object(installer, 'openclaw_package_dir', return_value='/lib/openclaw'), \
                    mock.patch.object(installer.onboarding.portable, 'tailscale', return_value=None), \
                    mock.patch.object(installer.service, 'available', return_value=False):
                installer.check_prerequisites()
            text = '\n'.join(said)
            self.assertEqual(f'openclaw update --tag {installer.required_openclaw()}' in text, noted, text)
            self.assertEqual('openclaw doctor --fix' in text, noted)


class InstallerTest(unittest.TestCase):
    def test_plugin_enable_is_retried_while_the_gateway_applies_the_install(self):
        calls, tries = [], iter([1, 0])
        def run(command, **kwargs):
            calls.append(command[1:3])
            code = next(tries) if command[1:3] == ['plugins', 'enable'] else 0
            return subprocess.CompletedProcess(command, code, '', 'The CLI command failed.' if code else '')
        with mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer.time, 'sleep'), \
             mock.patch.object(installer, 'say'):
            self.assertTrue(installer.install_plugin({'openclaw': 'openclaw'}))
        self.assertEqual(calls.count(['plugins', 'enable']), 2)

    def test_an_unchanged_bridge_is_not_reinstalled_or_reloaded(self):
        calls = []
        def run(command, **kwargs):
            calls.append(command[1:3])
            return subprocess.CompletedProcess(command, 0, '', '')
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(installer, 'run', side_effect=run), \
                mock.patch.object(installer, 'say'):
            stamp = Path(tmp) / 'plugin-installed'
            facts = {'openclaw': 'openclaw', 'openclaw_version': '2026.11.2'}
            self.assertTrue(installer.install_plugin(facts, stamp=stamp))
            self.assertIn(['plugins', 'reload'], calls)
            calls.clear()
            self.assertTrue(installer.install_plugin(facts, stamp=stamp))  # an update that did not touch it
            self.assertEqual(calls, [])
            self.assertTrue(installer.install_plugin({**facts, 'openclaw_version': '2026.11.1'}, stamp=stamp))
            self.assertIn(['plugins', 'reload'], calls)  # a new OpenClaw gets it again
            calls.clear()
            self.assertTrue(installer.install_plugin(facts, reload=False, stamp=stamp))
            self.assertNotIn(['plugins', 'reload'], calls)

    def test_openclaw_background_turns_that_only_use_the_limits_are_turned_off_once_where_unset(self):
        # 2026-10-25: Skill Workshop reviews and the heartbeat spent a new owner's 5-hour ChatGPT window in minutes.
        calls = []
        def run(command, **kwargs):
            calls.append(command[1:])
            return subprocess.CompletedProcess(command, 0, '', '')
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer, 'say'):
            config, stamp = Path(tmp) / 'openclaw.json', Path(tmp) / 'data' / 'openclaw-quiet.json'
            config.write_text('{agents: {defaults: {utilityModel: "openai/gpt-6.1-sol"}}, // set by the owner\n}')
            with mock.patch.dict(os.environ, {'OPENCLAW_CONFIG_PATH': str(config)}):
                self.assertEqual(installer.quiet_openclaw({'openclaw': 'openclaw'}, stamp),
                                 ['agents.defaults.heartbeat.every', 'skills.workshop.autonomous.mode', 'mcp.sessionIdleTtlMs'])
                self.assertIn(['config', 'set', 'mcp.sessionIdleTtlMs', '1800000', '--strict-json'], calls)  # 2026-10-30: 256 live MCP runtimes
                self.assertIn(['config', 'set', 'skills.workshop.autonomous.mode', '"off"', '--strict-json'], calls)
                self.assertIn(['config', 'set', 'agents.defaults.heartbeat.every', '"0m"', '--strict-json'], calls)
                self.assertFalse(any('utilityModel' in c for call in calls for c in call))  # theirs stays
                calls.clear()
                # An update later, after the owner turned the heartbeat back on by removing the value: left alone
                self.assertEqual(installer.quiet_openclaw({'openclaw': 'openclaw'}, stamp), [])
                self.assertEqual(calls, [])

    def test_telegram_link_previews_go_off_once_telegram_is_set_up_and_only_where_unset(self):
        # Telegram's servers open the first link of a message for its preview: a link a model was talked into writing
        # (to-do text, an assistant reply) would reach that site with no tap. Off once Telegram is there.
        calls = []
        def run(command, **kwargs):
            calls.append(command[1:])
            return subprocess.CompletedProcess(command, 0, '', '')
        off = ['config', 'set', 'channels.telegram.linkPreview', 'false', '--strict-json']
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer, 'say'):
            config, stamp = Path(tmp) / 'openclaw.json', Path(tmp) / 'data' / 'openclaw-quiet.json'
            config.write_text('{}')
            with mock.patch.dict(os.environ, {'OPENCLAW_CONFIG_PATH': str(config)}):
                # No Telegram yet: nothing written under channels (a half-made channel), and not marked done
                self.assertNotIn('channels.telegram.linkPreview', installer.quiet_openclaw({'openclaw': 'openclaw'}, stamp))
                self.assertNotIn(off, calls)
                # Telegram set up later: the next install or update turns previews off
                config.write_text('{channels: {telegram: {botToken: "x"}}}')
                calls.clear()
                self.assertEqual(installer.quiet_openclaw({'openclaw': 'openclaw'}, stamp), ['channels.telegram.linkPreview'])
                self.assertIn(off, calls)
                # Once only: an owner who turns them back on keeps them
                config.write_text('{channels: {telegram: {botToken: "x", linkPreview: true}}}')
                calls.clear()
                self.assertEqual(installer.quiet_openclaw({'openclaw': 'openclaw'}, stamp), [])
                config.write_text('{channels: {telegram: {botToken: "x"}}}')
                self.assertEqual(installer.quiet_openclaw({'openclaw': 'openclaw'}, stamp), [])
                self.assertEqual(calls, [])
            # An owner who set it before any install: theirs stays
            stamp.unlink()
            config.write_text('{channels: {telegram: {botToken: "x", linkPreview: true}}}')
            with mock.patch.dict(os.environ, {'OPENCLAW_CONFIG_PATH': str(config)}):
                self.assertNotIn('channels.telegram.linkPreview', installer.quiet_openclaw({'openclaw': 'openclaw'}, stamp))
            self.assertNotIn(off, calls)

    def test_daily_memory_rules_go_into_the_workspace_agents_md_once_and_the_owners_edits_stay(self):
        # OpenClaw's own AGENTS.md names no single daily file and nothing about the session-memory hook's files
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(installer, 'say'):
            space, stamp = Path(tmp) / 'workspace', Path(tmp) / 'data' / 'memory-rules.json'
            agents = space / 'AGENTS.md'
            # No AGENTS.md yet (OpenClaw writes its own first): nothing written, and the next run tries again
            self.assertFalse(installer.memory_rules(space, stamp))
            self.assertFalse(agents.exists())
            self.assertFalse(stamp.exists())
            space.mkdir()
            stock = '# AGENTS.md - Your Workspace\n\n## Memory\n\n- **Daily notes:** `memory/YYYY-MM-DD.md` holds raw logs.\n'
            agents.write_text(stock)
            agents.chmod(0o644)
            self.assertTrue(installer.memory_rules(space, stamp))
            text = agents.read_text()
            self.assertTrue(text.startswith(stock))  # what was there stays, the rules come after it
            self.assertEqual(text.count(installer.MEMORY_RULES_BEGIN), 1)
            self.assertTrue(text.endswith(installer.MEMORY_RULES))
            self.assertEqual(stat.S_IMODE(agents.stat().st_mode), 0o644)
            for words in ('`memory/YYYY-MM-DD.md`', 'Append', 'session-memory', '`MEMORY.md`', '`memory/assistant/`'):
                self.assertIn(words, installer.MEMORY_RULES)
            self.assertNotIn('—', installer.MEMORY_RULES)
            # What the owner states that stays true is saved as a fact in The Machine, under Learning, with who it is
            # about; MEMORY.md and USER.md get no new ones and stay readable
            rule = next(line for line in installer.MEMORY_RULES.splitlines() if 'durable' in line.lower())
            for words in ('fact, decision or lasting preference', 'the owner states', '`assistant_signals` `remember_fact`', '`about`',
                          'person, organization or project', 'Learning', 'edit, undo or forget', 'Add no new ones to `MEMORY.md` or `USER.md`',
                          'keep reading both'):
                self.assertIn(words, rule)
            self.assertNotIn('go in `MEMORY.md`', installer.MEMORY_RULES)
            self.assertEqual(json.loads(stamp.read_text())['version'], installer.MEMORY_RULES_VERSION)
            # Rerun (every update on a hosted Machine): not again
            self.assertFalse(installer.memory_rules(space, stamp))
            self.assertEqual(agents.read_text(), text)
            # The owner edits them, or removes them: theirs stays, nothing comes back
            agents.write_text(text.replace('dated in the owner', 'dated in my'))
            self.assertFalse(installer.memory_rules(space, stamp))
            self.assertIn('dated in my', agents.read_text())
            agents.write_text(stock)
            self.assertFalse(installer.memory_rules(space, stamp))
            self.assertEqual(agents.read_text(), stock)
            # Rules already there (a lost stamp): not twice
            stamp.unlink()
            agents.write_text(text)
            self.assertFalse(installer.memory_rules(space, stamp))
            self.assertEqual(agents.read_text(), text)
            # An owner with their own rules for the hook's files: left as it is
            stamp.unlink()
            own = '# AGENTS.md\n\n- Daily notes go to `memory/daily/YYYY-MM-DD.md`; merge the Session-Memory hook files there.\n'
            agents.write_text(own)
            self.assertFalse(installer.memory_rules(space, stamp))
            self.assertEqual(agents.read_text(), own)
            self.assertTrue(stamp.exists())
            self.assertEqual(sorted(p.name for p in space.iterdir()), ['AGENTS.md'])  # no temp file left

    def test_an_earlier_memory_block_is_replaced_only_when_it_is_still_byte_for_byte_as_installed(self):
        before, now = installer.MEMORY_RULES_BEFORE[-1], installer.MEMORY_RULES
        self.assertEqual(len(set(installer.MEMORY_RULES_BEFORE)), len(installer.MEMORY_RULES_BEFORE))
        self.assertNotIn(now, installer.MEMORY_RULES_BEFORE)
        for block in (*installer.MEMORY_RULES_BEFORE, now):
            self.assertTrue(block.startswith(installer.MEMORY_RULES_BEGIN + '\n') and block.endswith(installer.MEMORY_RULES_END + '\n'))
        self.assertIn('Durable decisions and facts go in `MEMORY.md` and lasting preferences in `USER.md`', before)  # what #499 wrote
        stock = '# AGENTS.md - Your Workspace\n\n## Memory\n\n- **Daily notes:** `memory/YYYY-MM-DD.md` holds raw logs.\n'
        mine = '\n## My own rules\n\n- Answer in short lines.\n'
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(installer, 'say') as said:
            space, stamp = Path(tmp) / 'workspace', Path(tmp) / 'data' / 'memory-rules.json'
            space.mkdir()
            stamp.parent.mkdir()
            agents = space / 'AGENTS.md'

            def installed(text, mode=0o644, added=True):
                """A workspace an earlier version left: its AGENTS.md and the stamp that version wrote."""
                agents.write_bytes(text.encode())
                agents.chmod(mode)
                stamp.write_text(json.dumps({'added': added, 'at': '2026-11-03'}) + '\n')

            # 1. Untouched since the install (the owner wrote their own rules after it): the new block takes its place,
            # everything else stays byte for byte, and so do the file's mode and owner
            installed(stock + '\n' + before + mine, 0o600)
            owner = agents.stat()
            self.assertTrue(installer.memory_rules(space, stamp))
            self.assertEqual(agents.read_bytes(), (stock + '\n' + now + mine).encode())
            self.assertEqual(stat.S_IMODE(agents.stat().st_mode), 0o600)
            self.assertEqual((agents.stat().st_uid, agents.stat().st_gid), (owner.st_uid, owner.st_gid))
            self.assertEqual(sorted(p.name for p in space.iterdir()), ['AGENTS.md'])  # written whole, no temp file left
            self.assertEqual(json.loads(stamp.read_text()), {'added': True, 'version': installer.MEMORY_RULES_VERSION, 'replaced': True,
                                                             'at': json.loads(stamp.read_text())['at']})
            self.assertIn('Learning', said.call_args.args[0])
            # ...once: the owner editing the new block, or putting the old one back by hand, is theirs
            for theirs in (stock + '\n' + now.replace('edit, undo or forget', 'change') + mine, stock + '\n' + before + mine):
                agents.write_bytes(theirs.encode())
                self.assertFalse(installer.memory_rules(space, stamp))
                self.assertEqual(agents.read_bytes(), theirs.encode())

            # 2. Changed in any way: left completely alone, now and on every later run, also when put back later
            edits = {'a word changed': before.replace('dated in the owner', 'dated in my'),
                     'a line shortened': before.replace(', never only in a daily note', ''),
                     'a line removed': before.replace('- Results of to-dos stay in `memory/assistant/`; they are not daily notes.\n', ''),
                     'a space added': before.replace('## Daily memory', '## Daily memory '),
                     'the end marker gone': before.replace(installer.MEMORY_RULES_END + '\n', ''),
                     'other line ends': before.replace('\n', '\r\n'),
                     'there twice': before + '\n' + before}
            for what, block in edits.items():
                with self.subTest(what):
                    theirs = stock + '\n' + block + mine
                    installed(theirs)
                    self.assertFalse(installer.memory_rules(space, stamp))
                    self.assertEqual(agents.read_bytes(), theirs.encode())
                    self.assertEqual(json.loads(stamp.read_text())['replaced'], False)
                    agents.write_bytes((stock + '\n' + before + mine).encode())  # back as installed, by hand, after the check
                    self.assertFalse(installer.memory_rules(space, stamp))
                    self.assertEqual(agents.read_bytes(), (stock + '\n' + before + mine).encode())

            # 3. Removed by the owner: not added again, in either text
            installed(stock + mine)
            self.assertFalse(installer.memory_rules(space, stamp))
            self.assertEqual(agents.read_bytes(), (stock + mine).encode())
            # An owner who had their own rules for the hook's files and never got the block: nothing
            own = '# AGENTS.md\n\n- Merge the session-memory hook files into `memory/daily/`. Durable facts go in `MEMORY.md`.\n'
            installed(own, added=False)
            self.assertFalse(installer.memory_rules(space, stamp))
            self.assertEqual(agents.read_bytes(), own.encode())
            self.assertEqual(json.loads(stamp.read_text())['added'], False)
            # A file that can't be read is tried again next time, not marked as done
            installed(stock + '\n' + before)
            agents.write_bytes(b'\xff\xfe' + before.encode())
            self.assertFalse(installer.memory_rules(space, stamp))
            self.assertNotIn('version', json.loads(stamp.read_text()))
            # A write that fails leaves the file as it was, whole, and is tried again
            installed(stock + '\n' + before)
            with mock.patch.object(installer.os, 'replace', side_effect=OSError('disk full')):
                self.assertFalse(installer.memory_rules(space, stamp))
            self.assertEqual(agents.read_bytes(), (stock + '\n' + before).encode())
            self.assertEqual(sorted(p.name for p in space.iterdir()), ['AGENTS.md'])
            self.assertTrue(installer.memory_rules(space, stamp))
            self.assertEqual(agents.read_bytes(), (stock + '\n' + now).encode())

    def test_a_new_install_starts_at_thinking_low_only_where_unset_and_the_model_offers_it(self):
        listed = {'models': [{'provider': 'acme', 'id': 'lm-2', 'available': True, 'thinkingLevels': [{'id': 'low'}, {'id': 'medium'}]},
                             {'provider': 'acme', 'id': 'deep', 'available': True, 'thinkingLevels': [{'id': 'medium'}, {'id': 'high'}]},
                             {'provider': 'other', 'id': 'out', 'available': False, 'thinkingLevels': [{'id': 'low'}]}]}
        calls = []
        def run(command, **kwargs):
            calls.append(command[1:])
            out = json.dumps(listed) if command[1:4] == ['gateway', 'call', 'models.list'] else ''
            return subprocess.CompletedProcess(command, 0, out, '')
        low = ['config', 'set', 'agents.defaults.thinkingDefault', '"low"', '--strict-json']
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer, 'say'):
            config = Path(tmp) / 'openclaw.json'
            with mock.patch.dict(os.environ, {'OPENCLAW_CONFIG_PATH': str(config)}):
                for settings, expected in (({'model': {'primary': 'acme/lm-2'}}, True),
                                           ({'model': 'acme/lm-2', 'thinkingDefault': 'high'}, False),  # a level set stays
                                           ({'model': {'primary': 'acme/deep'}}, False),  # no low: its own default stays
                                           ({'model': {'primary': 'other/out'}}, False),  # not signed in (a hosted Machine before its sign-in)
                                           ({}, False)):
                    calls.clear()
                    config.write_text(json.dumps({'agents': {'defaults': settings}}))
                    self.assertEqual(installer.start_thinking({'openclaw': 'openclaw'}), expected, settings)
                    self.assertEqual(low in calls, expected, settings)
                self.assertFalse(installer.start_thinking({}))

    def test_only_a_first_install_sets_the_starting_thinking_level(self):
        import inspect
        source = inspect.getsource(installer.main)
        self.assertIn('fresh = not paths.config.exists()', source)
        self.assertLess(source.index('fresh = not paths.config.exists()'), source.index('setup_config('))
        self.assertIn('fresh, not args.no_start', source)
        self.assertIn('if fresh:\n        start_thinking(facts)', inspect.getsource(installer.prepare))

    def test_a_first_install_does_the_steps_without_answers_while_it_asks(self):
        """Bytecode, Node packages and the OpenClaw bridge go ahead while the questions are asked: their lines wait
        until after the questions, their programs never read the terminal, and OpenClaw is not called during pairing."""
        import threading
        asking, calls = threading.Event(), []

        def step(name):
            def inner(*args, **kwargs):
                asking.wait(5)  # only once the questions are under way
                installer.say(f'{name} done')
                calls.append((name, installer.run([sys.executable, '-c', 'import sys; print(sys.stdin.read())']).stdout))
                return True
            return inner
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        paths = mock.Mock(data=Path(folder.name) / 'data')
        printed = []
        with mock.patch.object(installer, 'precompile', step('bytecode')), mock.patch.object(installer, 'install_node_packages', step('node')), \
                mock.patch.object(installer, 'install_plugin', step('bridge')), mock.patch.object(installer, 'quiet_openclaw'), \
                mock.patch.object(installer, 'gateway_keep_retrying'), mock.patch.object(installer, 'memory_rules'), \
                mock.patch.object(installer, 'start_thinking') as thinking, mock.patch('builtins.print', lambda *a, **k: printed.append(' '.join(map(str, a)))):
            ahead = installer.Ahead(installer.prepare, {'node': 'node'}, paths, True, True, False, True)
            with installer.OPENCLAW_TURN:  # the questions pair Telegram: the steps ahead wait for it
                asking.set()
                installer.say('a question')
                self.assertEqual(calls, [])
            self.assertTrue(ahead.result())
        self.assertEqual([name for name, _ in calls], ['bytecode', 'node', 'bridge'])
        self.assertEqual({out for _, out in calls}, {'\n'})  # stdin was empty, not the terminal
        self.assertEqual(printed[0], 'a question')
        self.assertIn('bridge done', printed)
        thinking.assert_called_once()

    def test_a_failed_bridge_ahead_still_stops_the_install(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        paths = mock.Mock(data=Path(folder.name) / 'data')
        with mock.patch.object(installer, 'precompile'), mock.patch.object(installer, 'install_node_packages'), \
                mock.patch.object(installer, 'install_plugin', return_value=False), mock.patch.object(installer, 'quiet_openclaw') as quiet:
            self.assertFalse(installer.Ahead(installer.prepare, {'node': 'node'}, paths, True, True, False, True).result())
        quiet.assert_not_called()
        with mock.patch.object(installer, 'install_node_packages', side_effect=RuntimeError('boom')), self.assertRaises(RuntimeError):
            installer.Ahead(installer.prepare, {'node': 'node'}, paths, True, True, False).result()

    def gateway(self, reload_code=1, health=(), unit='openclaw-gateway.service', restart_code=0):
        """install_plugin against a fake OpenClaw whose reload fails and whose Gateway health answers `health` in turn."""
        calls, answers = [], iter(health)
        def run(command, **kwargs):
            calls.append(command)
            if command[1:3] == ['plugins', 'reload']:
                return subprocess.CompletedProcess(command, reload_code, '', '[openclaw] The CLI command failed.' if reload_code else '')
            if command[1:3] == ['gateway', 'health']:
                found = next(answers, None)
                return subprocess.CompletedProcess(command, 0 if found else 1, json.dumps(found) if found else '', '')
            if command[:3] == ['systemctl', '--user', 'restart']:
                return subprocess.CompletedProcess(command, restart_code, '', 'Job failed' if restart_code else '')
            return subprocess.CompletedProcess(command, 0, '', '')
        said = []
        tmp = Path(tempfile.mkdtemp(prefix='machine-plugin-'))
        self.addCleanup(shutil.rmtree, tmp, True)
        stamp = tmp / 'plugin-installed'
        with mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer.time, 'sleep'), \
                mock.patch.object(installer, 'say', side_effect=said.append), \
                mock.patch.object(installer.onboarding, 'gateway_units', return_value=[unit] if unit else []), \
                mock.patch.dict(os.environ, {'ASSISTANT_GATEWAY_WAIT': '60'}):
            ok = installer.install_plugin({'openclaw': 'openclaw', 'openclaw_version': '2026.11.2'}, stamp=stamp)
        return ok, calls, '\n'.join(said), stamp.exists()

    def swap(self, fail=(), breaks=None, reload_heals=False, busy=(), unit='openclaw-gateway.service', restart=True, wait='600'):
        """install_plugin against a fake Gateway with a model runtime: the plugin step `breaks` unpublishes it (as a
        swap OpenClaw could neither finish nor roll back does), a Gateway restart brings it back, a second reload only
        with `reload_heals`. `fail`: the plugin steps that fail. `busy`: what the memory index says in turn (None: nothing
        can tell), then nothing. The clock is a fake one that only time.sleep moves."""
        calls, state, looks, clock = [], {'models': True, 'reloads': 0}, iter(busy), [1000.0]
        self.clock = clock
        loaded = {'ok': True, 'plugins': {'loaded': [installer.PLUGIN_ID], 'errors': []}}
        def run(command, **kwargs):
            calls.append(' '.join(command[:1] + command[1:4]) if command[0] != 'openclaw' else ' '.join(command[1:3]))
            step = command[2] if command[1:2] == ['plugins'] else None
            code = 0
            if step == 'reload':
                state['reloads'] += 1
                if reload_heals and not state['models']:
                    state['models'] = True
                    return subprocess.CompletedProcess(command, 0, '', '')
            if step and step == breaks and (step != 'reload' or state['reloads'] == 1):
                state['models'] = False
            if step in fail:
                code = 1
            if command[1:4] == ['gateway', 'call', 'models.list']:
                code = 0 if state['models'] else 1
            if command[1:3] == ['gateway', 'health']:
                return subprocess.CompletedProcess(command, 0, json.dumps(loaded), '')
            if command[:3] == ['systemctl', '--user', 'restart']:
                state['models'] = True
            return subprocess.CompletedProcess(command, code, '', 'UNAVAILABLE: runtime owner was not published for main' if code else '')
        def index_busy():
            calls.append('index?')
            return next(looks, None)
        said = []
        tmp = Path(tempfile.mkdtemp(prefix='machine-swap-'))
        self.addCleanup(shutil.rmtree, tmp, True)
        stamp = tmp / 'plugin-installed'
        def sleep(seconds):
            clock[0] += seconds
        with mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer.time, 'sleep', side_effect=sleep) as slept, \
                mock.patch.object(installer.time, 'monotonic', side_effect=lambda: clock[0]), \
                mock.patch.object(installer, 'say', side_effect=said.append), mock.patch.object(installer, 'index_busy', side_effect=index_busy), \
                mock.patch.object(installer, 'gateway_started', return_value=None), \
                mock.patch.object(installer.onboarding, 'gateway_units', return_value=[unit] if unit else []), \
                mock.patch.dict(os.environ, {'ASSISTANT_GATEWAY_WAIT': '60', 'ASSISTANT_SWAP_WAIT': wait, 'ASSISTANT_PLUGIN_RETRY_WAIT': '0'}):
            ok = installer.install_plugin({'openclaw': 'openclaw', 'openclaw_version': '2026.11.2'}, stamp=stamp, restart=restart)
        self.waiting = (tmp / installer.BRIDGE_WAITING).exists()
        return ok, calls, '\n'.join(said), stamp.exists(), slept.call_count

    RESTART = 'systemctl --user restart openclaw-gateway.service'

    def idle(self, looks, wait='600', quiet=None, ports=None):
        """gateway_idle against an index that says looks(seconds since the start) at each look, on a fake clock that
        only time.sleep moves. Returns (idle, the seconds it took, what was said, the looks)."""
        clock, said, seen = [500.0], [], []
        def sleep(seconds):
            clock[0] += seconds
        def index_busy():
            seen.append(looks(clock[0] - 500.0))
            return seen[-1]
        env = {'ASSISTANT_SWAP_WAIT': wait, **({'ASSISTANT_SWAP_QUIET': quiet} if quiet else {})}
        with mock.patch.object(installer.time, 'sleep', side_effect=sleep), mock.patch.object(installer.time, 'monotonic', side_effect=lambda: clock[0]), \
                mock.patch.object(installer, 'say', side_effect=said.append), mock.patch.object(installer, 'index_busy', side_effect=index_busy), \
                mock.patch.dict(os.environ, env):
            os.environ.pop('ASSISTANT_SWAP_POLL', None)
            if not quiet:
                os.environ.pop('ASSISTANT_SWAP_QUIET', None)
            ok = installer.gateway_idle('the bridge goes in')
        return ok, clock[0] - 500.0, '\n'.join(said), seen

    def test_a_pause_in_the_memory_index_is_not_the_end_of_it(self):
        # What happened on a real Machine: a long run went quiet for 40 seconds between batches and then went on.
        ok, took, said, seen = self.idle(lambda t: t < 30 or 70 <= t < 100)
        self.assertTrue(ok)
        self.assertEqual(took, 160)  # 60 unbroken seconds after the last busy look, not after the first quiet one
        self.assertGreater(seen.count(False), 3)  # far more than three quiet looks went by in the pause
        self.assertEqual(said.count('waiting up to 10 min'), 1, said)
        ok, took, said, _ = self.idle(lambda t: 20 <= t < 50)  # the first look fell in a pause: the same stretch, started again
        self.assertTrue(ok)
        self.assertEqual(took, 110)
        self.assertIn('stays quiet for 60 s before the bridge goes in', said)
        self.assertIn('waiting up to 10 min', said)

    def test_an_unbroken_quiet_stretch_is_idle(self):
        ok, took, said, seen = self.idle(lambda t: False)  # an embedding server that is doing nothing
        self.assertTrue(ok)
        self.assertEqual((took, len(seen)), (60, 31))
        self.assertNotIn('waiting up to', said)
        self.assertIn('stays quiet for 60 s', said)
        ok, took, _, _ = self.idle(lambda t: t < 10, quiet='20')  # ASSISTANT_SWAP_QUIET
        self.assertEqual((ok, took), (True, 30))
        ok, took, _, _ = self.idle(lambda t: True if t < 10 else None)  # the server went away after its run: quiet from then on
        self.assertEqual((ok, took), (True, 70))

    def test_where_nothing_can_tell_there_is_no_wait(self):
        ok, took, said, seen = self.idle(lambda t: None)  # no embedding server on this computer: most installs
        self.assertEqual((ok, took, said, seen), (True, 0, '', [None]))

    def test_the_bound_ends_a_run_that_never_goes_quiet_for_long(self):
        ok, took, said, _ = self.idle(lambda t: True)
        self.assertFalse(ok)
        self.assertEqual(took, 600)
        ok, took, _, _ = self.idle(lambda t: t % 50 < 10)  # 40 second pauses for good: busy all the way to the bound
        self.assertFalse(ok)
        self.assertEqual(took, 600)
        ok, took, _, _ = self.idle(lambda t: t < 590)  # went quiet just before the bound: the stretch is let finish
        self.assertEqual((ok, took), (True, 650))
        ok, took, _, _ = self.idle(lambda t: t < 590 or 620 <= t)  # and one that broke after the bound ends it
        self.assertEqual((ok, took), (False, 620))
        ok, took, _, _ = self.idle(lambda t: 40 <= t, wait='30')  # the bound counts from the first busy look
        self.assertEqual((ok, took), (False, 70))

    def test_the_bridge_goes_in_only_once_the_memory_index_has_stopped(self):
        ok, calls, said, stamped, slept = self.swap(busy=[True, True, False, True] + [False] * 31)
        self.assertTrue(ok, said)
        self.assertTrue(stamped)
        self.assertEqual(calls[:36], ['index?'] * 35 + ['plugins install'], calls)  # a quiet look between batches is not idle
        self.assertEqual(slept, 34)
        self.assertEqual(said.count('waiting up to 10 min'), 1, said)
        self.assertNotIn(self.RESTART, calls)
        ok, calls, said, _, slept = self.swap()  # nothing here can tell (no local embedding server): no wait
        self.assertTrue(ok, said)
        self.assertEqual((calls[:2], slept), (['index?', 'plugins install'], 0))

    def test_an_index_that_starts_between_the_swap_and_the_reload_is_waited_for_too(self):
        ok, calls, said, stamped, _ = self.swap(busy=[None, True, True])  # nothing to see at the swap, a run by the reload
        self.assertTrue(ok, said)
        self.assertTrue(stamped)
        between = calls[calls.index('plugins enable'):calls.index('plugins reload')]
        self.assertEqual(between.count('index?'), 2 + 31, calls)  # a full minute after the last busy look
        self.assertEqual(self.clock[0] - 1000.0, 4 + 60)
        self.assertEqual(said.count('  OpenClaw is building its memory index; waiting up to 10 min for it before reloading the bridge.'), 1, said)
        ok, calls, said, stamped, _ = self.swap(busy=[None] + [True] * 50, wait='0')  # still running at the bound
        self.assertTrue(ok, said)  # this install may restart the Gateway: it goes on, the check after the reload covers it
        self.assertIn('going on', said)
        self.assertIn('plugins reload', calls)
        ok, calls, said, stamped, _ = self.swap(busy=[None] + [True] * 50, wait='0', restart=False)
        self.assertEqual(ok, installer.WAITING)  # the bridge waits; the install goes on
        self.assertFalse(stamped)  # not reloaded is not installed: the next run does it
        self.assertTrue(self.waiting)
        self.assertIn('plugins install', calls)
        self.assertFalse([c for c in calls if c.startswith(('plugins reload', 'systemctl'))], calls)
        self.assertIn('linked but not reloaded', said)
        self.assertIn('the next nightly update tries again by itself', said)
        self.assertNotIn('openclaw memory status', said)

    def test_the_reload_that_brings_models_back_waits_for_the_same_quiet(self):
        # The swap went in during a pause the first check could not see (None), the index went on and the install failed.
        ok, calls, said, _, _ = self.swap(fail=['install'], breaks='install', reload_heals=True, busy=[None, True, True] + [False] * 15 + [True])
        self.assertFalse(ok)
        after = calls[calls.index('plugins install'):calls.index('plugins reload')]
        self.assertEqual(after.count('index?'), 18 + 31, calls)  # 30 quiet seconds did not do: a full minute after the last busy look
        self.assertEqual(self.clock[0] - 1000.0, 36 + 60)
        self.assertIn('  OpenClaw is building its memory index; waiting up to 10 min for it before reloading the bridge.', said)
        self.assertIn('Reloaded the bridge: model calls work again', said)
        self.assertNotIn(self.RESTART, calls)

    def test_an_index_that_never_stops_is_waited_for_only_so_long(self):
        ok, calls, said, stamped, _ = self.swap(busy=[True] * 50, wait='0')
        self.assertTrue(ok, said)  # this install may restart the Gateway: it goes on, the checks after each step cover it
        self.assertIn('going on', said)
        self.assertIn('plugins install', calls)
        ok, calls, said, stamped, _ = self.swap(busy=[True] * 50, wait='0', restart=False)
        self.assertEqual(ok, installer.WAITING)  # not a failed install: the bridge waits, everything else goes on
        self.assertFalse(stamped)
        self.assertTrue(self.waiting)  # the nightly update tries again
        self.assertFalse([c for c in calls if c.startswith(('plugins', 'systemctl'))], calls)
        self.assertIn('nothing in OpenClaw was changed', said)
        self.assertIn('Everything else is updated', said)
        self.assertIn('the next nightly update tries again by itself', said)
        self.assertNotIn('openclaw memory status', said)  # that command does not show the run that indexes
        ok, _, _, stamped, _ = self.swap(busy=[True] * 50, wait='0', unit=None)  # no Gateway service to restart: the same
        self.assertEqual((ok, stamped, self.waiting), (installer.WAITING, False, True))
        ok, _, _, stamped, _ = self.swap()  # a swap that goes in leaves nothing waiting
        self.assertEqual((ok, stamped, self.waiting), (True, True, False))
        ok, _, _, stamped, _ = self.swap(fail=['install'])  # one that failed is tried again by the nightly update too
        self.assertEqual((ok, stamped, self.waiting), (False, False, True))

    def test_a_bridge_that_waits_for_the_index_lets_the_rest_of_the_install_go_on(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        paths = mock.Mock(data=Path(folder.name) / 'data')
        with mock.patch.object(installer, 'install_node_packages'), mock.patch.object(installer, 'install_plugin', return_value=installer.WAITING), \
                mock.patch.object(installer, 'quiet_openclaw') as quiet, mock.patch.object(installer, 'gateway_keep_retrying'), \
                mock.patch.object(installer, 'memory_rules'):
            self.assertTrue(installer.prepare({'node': 'node'}, paths, False, True, False))
        quiet.assert_called_once()

    def test_a_rebuild_of_the_memory_index_counts_as_running_while_its_database_is_written(self):
        # A real Machine, 2026-11-10: the embedding server was quiet for a minute, the rebuild went on from its cache,
        # and the swap failed on OpenClaw's 5 second stop.
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        agent = Path(folder.name) / 'agents/main/agent'
        agent.mkdir(parents=True)
        (agent / 'openclaw-agent.sqlite').write_text('the real one')
        still = subprocess.CompletedProcess([], 0, '  10     1 openclaw-gateway gateway run', '')  # no embedding server at all
        with mock.patch.dict(os.environ, {'OPENCLAW_STATE_DIR': folder.name}), mock.patch.object(installer, 'run', return_value=still), \
                mock.patch.object(installer, 'reindex_running', REINDEX_RUNNING):
            os.environ.pop('ASSISTANT_EMBEDDING_PORTS', None)
            os.environ.pop('ASSISTANT_REINDEX_FRESH', None)
            self.assertFalse(installer.reindex_running())
            self.assertIsNone(installer.index_busy())  # no rebuild, nothing to ask: as before
            shadow = agent / 'openclaw-agent.sqlite.memory-reindex-0a1b2c3d-wal'
            shadow.write_text('rows')
            self.assertTrue(installer.reindex_running())
            self.assertIs(installer.index_busy(), True)
            old = shadow.stat().st_mtime - 50  # as long between two writes as a running rebuild was seen to take
            os.utime(shadow, (old, old))
            self.assertTrue(installer.reindex_running())
            old -= 3600  # left behind by a Gateway that stopped mid-rebuild
            os.utime(shadow, (old, old))
            self.assertFalse(installer.reindex_running())
            self.assertIsNone(installer.index_busy())
            os.environ['ASSISTANT_REINDEX_FRESH'] = '7200'
            self.assertTrue(installer.reindex_running())
        with mock.patch.dict(os.environ, {'OPENCLAW_STATE_DIR': str(Path(folder.name) / 'none')}):
            self.assertFalse(REINDEX_RUNNING())  # no OpenClaw state here

    def fake_openclaw(self, provider='local', agent_dir=None):
        """A fake OpenClaw state folder with openclaw.json saying `provider` for memory search, and `agent_dir` as the
        agentDir of a second agent. Returns (state folder, the default agent's folder)."""
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        state = Path(folder.name)
        agent = state / 'agents/main/agent'
        agent.mkdir(parents=True)
        (agent / 'openclaw-agent.sqlite').write_text('the real one')
        settings = {'memory': {'search': {'provider': provider}}}
        if agent_dir:
            settings['agents'] = {'list': [{'id': 'main'}, {'id': 'work', 'agentDir': str(agent_dir)}]}
        (state / 'openclaw.json').write_text(json.dumps(settings))
        return state, agent

    def test_a_rebuild_on_local_embeddings_is_found_where_openclaw_keeps_the_agent(self):
        elsewhere = Path(tempfile.mkdtemp(prefix='machine-agent-'))
        self.addCleanup(shutil.rmtree, elsewhere, True)
        state, agent = self.fake_openclaw(agent_dir=elsewhere)
        with mock.patch.dict(os.environ, {'OPENCLAW_STATE_DIR': str(state)}), mock.patch.object(installer, 'reindex_running', REINDEX_RUNNING):
            for key in ('ASSISTANT_REINDEX_FRESH', 'OPENCLAW_CONFIG_PATH'):
                os.environ.pop(key, None)
            self.assertEqual(installer.agent_dirs(), [agent, elsewhere])
            self.assertTrue(installer.local_memory_search())
            self.assertFalse(installer.local_rebuild())
            shadow = elsewhere / 'openclaw-agent.sqlite.memory-reindex-0a1b2c3d'  # an agent with its own agentDir
            shadow.write_text('rows')
            self.assertTrue(installer.local_rebuild())
            old = shadow.stat().st_mtime - 3600  # left behind by a Gateway that stopped mid-rebuild
            os.utime(shadow, (old, old))
            self.assertFalse(installer.local_rebuild())
            self.assertTrue(shadow.exists())  # only looked at, never removed
            (agent / 'openclaw-agent.sqlite.memory-reindex-4e5f-wal').write_text('rows')
            self.assertTrue(installer.local_rebuild())
            for provider in ('none', 'openai'):  # a hosted Machine (none), or a remote provider: not this guard
                (state / 'openclaw.json').write_text(json.dumps({'memory': {'search': {'provider': provider}}}))
                self.assertFalse(installer.local_rebuild())
            (state / 'openclaw.json').write_text(json.dumps({'agents': {'defaults': {'memorySearch': {'provider': 'local'}}}}))
            self.assertTrue(installer.local_rebuild())

    def test_a_rebuild_on_local_embeddings_is_waited_for_longer(self):
        self.addCleanup(setattr, installer, 'REBUILD_OUTLASTED', False)
        with mock.patch.object(installer, 'local_rebuild', return_value=True), mock.patch.dict(os.environ, {'ASSISTANT_REBUILD_WAIT': '1200'}):
            ok, took, said, _ = self.idle(lambda t: t < 900)  # past the usual 10 minutes, done within 20
            self.assertEqual((ok, took), (True, 960))
            self.assertIn('rebuilding its memory index on local embeddings; waiting up to 20 min', said)
            self.assertIn('a Gateway stop or plugin swap during a rebuild hangs until it ends', said)
            self.assertNotIn('waiting up to 10 min', said)
            ok, took, _, _ = self.idle(lambda t: True)
            self.assertEqual((ok, took), (False, 1200))
            ok, took, said, seen = self.idle(lambda t: True)  # outlasted once in this run: not waited for again
            self.assertEqual((ok, took, seen), (False, 0, []))

    def test_a_rebuild_on_local_embeddings_is_never_swapped_into_or_restarted_through(self):
        # A real Machine, 2026-11-10: the swap went on after the wait, failed on "plugin service stop timed out ...
        # memory-core-index", and the Gateway restart after it hung for its whole TimeoutStopSec and was killed.
        self.addCleanup(setattr, installer, 'REBUILD_OUTLASTED', False)
        with mock.patch.object(installer, 'local_rebuild', return_value=True), mock.patch.dict(os.environ, {'ASSISTANT_REBUILD_WAIT': '0'}):
            ok, calls, said, stamped, _ = self.swap(busy=[True] * 50, wait='0')  # a Gateway this install may restart
            self.assertEqual(ok, installer.WAITING)
            self.assertFalse(stamped)
            self.assertTrue(self.waiting)  # the next install or nightly update tries again
            self.assertFalse([c for c in calls if c.startswith(('plugins', 'systemctl'))], calls)
            self.assertIn('nothing in OpenClaw was changed', said)
            self.assertNotIn('going on', said)
            ok, calls, said, stamped, _ = self.swap(busy=[None] + [True] * 50, wait='0')  # one that started after the swap
            self.assertEqual((ok, stamped, self.waiting), (installer.WAITING, False, True))
            self.assertIn('plugins install', calls)
            self.assertFalse([c for c in calls if c.startswith(('plugins reload', 'systemctl'))], calls)
            self.assertIn('linked but not reloaded', said)
        ok, calls, said, _, _ = self.swap(busy=[True] * 50, wait='0')  # any other index run: as before
        self.assertTrue(ok, said)
        self.assertIn('going on', said)

    def test_the_gateway_is_not_restarted_during_a_rebuild_on_local_embeddings(self):
        calls = []
        def run(command, **kwargs):
            calls.append(' '.join(command[:3]))
            return subprocess.CompletedProcess(command, 0, '{"ok": true, "plugins": {"loaded": ["%s"]}}' % installer.PLUGIN_ID, '')
        said = []
        with mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer, 'say', side_effect=said.append), \
                mock.patch.object(installer.onboarding, 'gateway_units', return_value=['openclaw-gateway.service']), \
                mock.patch.object(installer, 'local_rebuild', return_value=True), mock.patch.object(installer, 'gateway_idle', return_value=False) as idle:
            self.assertFalse(installer.load_in_gateway('openclaw', 'reload failed'))
            idle.assert_called_once()
            self.assertFalse([c for c in calls if c.startswith('systemctl')], calls)
            self.assertIn('Not restarting openclaw-gateway.service', '\n'.join(said))
            self.assertIn('systemctl --user restart openclaw-gateway.service', '\n'.join(said))
            idle.return_value = True  # the rebuild ended within the wait: the restart goes on
            self.assertTrue(installer.load_in_gateway('openclaw', 'reload failed'))
            self.assertIn('systemctl --user restart', calls)
            calls.clear()
            idle.return_value = False
            for recovery in (True, lambda: True):  # no models: still running at the cap, restarted anyway
                self.assertTrue(installer.load_in_gateway('openclaw', 'the Gateway cannot run models', recovery=recovery))
                self.assertEqual(calls.count('systemctl --user restart'), 1, calls)
                calls.clear()
            self.assertIn('restarting openclaw-gateway.service anyway', '\n'.join(said))
            self.assertFalse(installer.load_in_gateway('openclaw', 'reload failed', recovery=lambda: False))  # models work: planned
            self.assertNotIn('systemctl --user restart', calls)

    def test_a_failed_swap_during_a_rebuild_still_gets_its_recovery_restart(self):
        # The swap went in during a pause nothing could see (None); the rebuild went on, the install failed and took the
        # models with it. The reload cannot go in during the rebuild; the restart that brings models back must.
        self.addCleanup(setattr, installer, 'REBUILD_OUTLASTED', False)
        rebuild = iter([False] + [True] * 200)  # nothing at the first look, a rebuild from then on
        with mock.patch.object(installer, 'local_rebuild', side_effect=lambda: next(rebuild, True)), \
                mock.patch.dict(os.environ, {'ASSISTANT_REBUILD_WAIT': '0'}):
            ok, calls, said, stamped, _ = self.swap(fail=['install'], breaks='install', busy=[None] + [True] * 50, wait='0')
        self.assertFalse(ok)
        self.assertNotIn('plugins reload', calls)  # no reload into the rebuild
        self.assertIn(self.RESTART, calls)  # but the recovery restart happens
        self.assertIn('restarting openclaw-gateway.service anyway', said)
        self.assertIn('Model calls work again', said)
        self.assertNotIn('NOT FIXED', said)

    def openclaw_has(self, record=None, plugin=None, loaded=True, hooks=True, inspect_code=0):
        """A fake OpenClaw whose own record of the bridge is `record` and `plugin` over a good one. Returns (run, calls)."""
        root = str(ROOT / 'openclaw-plugin')
        found = {'plugin': {'id': installer.PLUGIN_ID, 'rootDir': root, 'enabled': True, 'status': 'loaded', **(plugin or {})},
                 'install': {'source': 'path', 'sourcePath': root, 'installPath': root, **(record or {})}}
        calls = []
        def run(command, **kwargs):
            calls.append(command[1:3])
            if command[1:3] == ['plugins', 'inspect']:
                return subprocess.CompletedProcess(command, inspect_code, json.dumps(found), '')
            if command[1:3] == ['gateway', 'health']:
                return subprocess.CompletedProcess(command, 0, json.dumps({'ok': True, 'plugins': {'loaded': [installer.PLUGIN_ID] if loaded else []}}), '')
            return subprocess.CompletedProcess(command, 0, '', '')
        settings = {'plugins': {'entries': {installer.PLUGIN_ID: {'enabled': True, 'hooks': {'allowConversationAccess': hooks}}}}}
        return run, calls, settings

    def test_a_new_openclaw_around_an_unchanged_bridge_it_already_runs_needs_no_swap(self):
        facts, newer = {'openclaw': 'openclaw', 'openclaw_version': '2026.11.2'}, {'openclaw': 'openclaw', 'openclaw_version': '2026.11.3'}
        cases = (({}, False), ({'record': {'sourcePath': '/somewhere/else'}}, True), ({'record': {'source': 'npm'}}, True),
                 ({'plugin': {'enabled': False}}, True), ({'plugin': {'status': 'error'}}, True), ({'plugin': {'rootDir': '/somewhere/else'}}, True),
                 ({'loaded': False}, True), ({'hooks': False}, True), ({'inspect_code': 1}, True))
        for case, swapped in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                stamp = Path(tmp) / 'plugin-installed'
                run, calls, settings = self.openclaw_has(**case)
                with mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer, 'say') as say, \
                        mock.patch.object(installer, 'index_busy', return_value=None), mock.patch.object(installer.time, 'sleep'), \
                        mock.patch.object(installer.onboarding, 'openclaw_settings', return_value=settings):
                    self.assertTrue(installer.install_plugin(facts, stamp=stamp))
                    calls.clear()
                    self.assertTrue(installer.install_plugin(newer, stamp=stamp))  # OpenClaw was updated, the bridge was not
                    self.assertEqual(['plugins', 'install'] in calls, swapped, calls)
                    self.assertEqual(['plugins', 'reload'] in calls, swapped, calls)
                    self.assertFalse((Path(tmp) / installer.BRIDGE_WAITING).exists())
                    if not swapped:
                        self.assertIn('already loaded by this OpenClaw', say.call_args[0][0])
                    calls.clear()
                    self.assertTrue(installer.install_plugin(newer, stamp=stamp))  # and the stamp is up to date either way
                    self.assertEqual(calls, [])

    def test_a_stamp_from_before_its_parts_were_kept_still_counts_and_gets_them(self):
        facts = {'openclaw': 'openclaw', 'openclaw_version': '2026.11.2'}
        run, calls, settings = self.openclaw_has()
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer, 'say'), \
                mock.patch.object(installer, 'index_busy', return_value=None), mock.patch.object(installer.time, 'sleep'), \
                mock.patch.object(installer.onboarding, 'openclaw_settings', return_value=settings):
            stamp = Path(tmp) / 'plugin-installed'
            stamp.write_text(installer.plugin_fingerprint(facts) + '\n')  # as every install before this one wrote it
            self.assertTrue(installer.install_plugin(facts, stamp=stamp))
            self.assertEqual(calls, [])  # the same bridge: no swap because the stamp grew
            self.assertEqual(installer.read_stamp(stamp), (installer.plugin_fingerprint(facts), installer.bridge_parts(facts)))
            stamp.write_text('0' * 64 + '\n')  # an old stamp that does not match cannot say what changed: the usual swap
            self.assertTrue(installer.install_plugin(facts, stamp=stamp))
            self.assertIn(['plugins', 'install'], calls)
            self.assertNotIn(['plugins', 'inspect'], calls)
            calls.clear()
            changed = {**installer.bridge_parts(facts), 'files': '0' * 64}  # the bridge's own files changed: always a swap
            stamp.write_text('0' * 64 + '\n' + json.dumps(changed) + '\n')
            self.assertTrue(installer.install_plugin(facts, stamp=stamp))
            self.assertIn(['plugins', 'reload'], calls)
            self.assertNotIn(['plugins', 'inspect'], calls)

    def old_stamp_install(self, stamp_text, started, case=None):
        """install_plugin over a stamp written as `stamp_text` (None: no stamp), with plugin-waiting set, on a Gateway
        that started `started` seconds after the bridge's files last changed (negative: before)."""
        facts = {'openclaw': 'openclaw', 'openclaw_version': '2026.11.2'}
        run, calls, settings = self.openclaw_has(**(case or {}))
        tmp = Path(tempfile.mkdtemp(prefix='machine-stamp-'))
        self.addCleanup(shutil.rmtree, tmp, True)
        stamp, waiting = tmp / 'plugin-installed', tmp / installer.BRIDGE_WAITING
        if stamp_text is not None:
            stamp.write_text(stamp_text)
        waiting.write_text(installer.plugin_fingerprint(facts) + '\n')
        with mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer, 'say') as say, \
                mock.patch.object(installer, 'index_busy', return_value=None), mock.patch.object(installer.time, 'sleep'), \
                mock.patch.object(installer.onboarding, 'openclaw_settings', return_value=settings), \
                mock.patch.object(installer, 'bridge_changed_at', return_value=5000.0), \
                mock.patch.object(installer, 'gateway_started', return_value=5000.0 + started):
            self.assertTrue(installer.install_plugin(facts, stamp=stamp))
        return calls, stamp, waiting.exists(), ' '.join(c[0][0] for c in say.call_args_list), facts

    def test_an_old_stamp_over_a_bridge_the_gateway_already_runs_needs_no_swap(self):
        # A real Machine, 2026-11-10: a one-line stamp from before the bridge last changed, a Gateway that had the
        # current files loaded, and four live swaps that failed during drain and took model calls down.
        for text in ('0' * 64 + '\n', None):  # a one-line stamp that does not match, and no stamp at all
            with self.subTest(stamp=text):
                calls, stamp, waiting, said, facts = self.old_stamp_install(text, started=60)
                self.assertNotIn(['plugins', 'install'], calls)
                self.assertNotIn(['plugins', 'reload'], calls)
                self.assertIn(['plugins', 'inspect'], calls)
                self.assertEqual(installer.read_stamp(stamp), (installer.plugin_fingerprint(facts), installer.bridge_parts(facts)))
                self.assertFalse(waiting)  # the nightly update has nothing left to do
                self.assertIn('already loaded as it is by the running Gateway', said)

    def test_an_old_stamp_over_changed_files_still_swaps(self):
        # The files changed after the Gateway started: what it runs is older than the folder, whatever inspect says.
        calls, stamp, waiting, said, facts = self.old_stamp_install('0' * 64 + '\n', started=-60)
        self.assertIn(['plugins', 'install'], calls)
        self.assertIn(['plugins', 'reload'], calls)
        self.assertNotIn(['plugins', 'inspect'], calls)
        self.assertEqual(installer.read_stamp(stamp)[1], installer.bridge_parts(facts))
        self.assertFalse(waiting)
        for case in ({'loaded': False}, {'plugin': {'status': 'error'}}, {'record': {'sourcePath': '/somewhere/else'}}, {'hooks': False}):
            with self.subTest(case=case):  # a Gateway newer than the files that does not have this bridge in: swap
                calls, *_ = self.old_stamp_install('0' * 64 + '\n', started=60, case=case)
                self.assertIn(['plugins', 'install'], calls)
        with mock.patch.object(installer, 'bridge_changed_at', return_value=5000.0), \
                mock.patch.object(installer, 'gateway_started', return_value=None), mock.patch.object(installer, 'bridge_in_openclaw') as inspect:
            self.assertFalse(installer.gateway_runs_these_files('openclaw'))  # no Gateway process found: no proof
        inspect.assert_not_called()

    def test_the_gateway_start_comes_from_the_process_list(self):
        listing = ('    1-02:03:04 /usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789\n'
                   '         00:03 openclaw gateway health --json\n'
                   '      10:00:00 /usr/bin/python3 assistant.py\n')
        with mock.patch.object(installer, 'run', return_value=subprocess.CompletedProcess([], 0, listing, '')), \
                mock.patch.object(installer.time, 'time', return_value=1_000_000.0):
            self.assertEqual(installer.gateway_started(), 1_000_000.0 - (86400 + 2 * 3600 + 3 * 60 + 4))  # the oldest one
        for stdout in ('      10:00:00 /usr/bin/python3 assistant.py\n', '  soon /x/openclaw gateway\n'):
            with mock.patch.object(installer, 'run', return_value=subprocess.CompletedProcess([], 0, stdout, '')):
                self.assertIsNone(installer.gateway_started())
        self.assertEqual([installer.elapsed_seconds(t) for t in ('00:07', '01:00:07', '2-00:00:07', 'x', '1:2:3:4')], [7, 3607, 172807, None, None])

    def test_a_failed_swap_whose_recovery_reload_loaded_the_bridge_counts_as_in(self):
        # The reload that brings models back reads the linked folder: the bridge is in, and the nightly run would only
        # repeat the swap that failed.
        run, calls, settings = self.openclaw_has()
        def failing(command, **kwargs):
            if command[1:3] == ['plugins', 'install']:
                calls.append(command[1:3])
                return subprocess.CompletedProcess(command, 1, '', 'Plugin operation failed during drain')
            if command[1:4] == ['gateway', 'call', 'models.list']:
                calls.append(command[1:3])
                return subprocess.CompletedProcess(command, 1 if ['plugins', 'reload'] not in calls else 0, '', '')
            return run(command, **kwargs)
        facts = {'openclaw': 'openclaw', 'openclaw_version': '2026.11.2'}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(installer, 'run', side_effect=failing), mock.patch.object(installer, 'say'), \
                mock.patch.object(installer, 'index_busy', return_value=None), mock.patch.object(installer.time, 'sleep'), \
                mock.patch.object(installer, 'gateway_started', return_value=None), \
                mock.patch.object(installer.onboarding, 'openclaw_settings', return_value=settings):
            stamp = Path(tmp) / 'plugin-installed'
            self.assertTrue(installer.install_plugin(facts, stamp=stamp))
            self.assertEqual(installer.read_stamp(stamp)[1], installer.bridge_parts(facts))
            self.assertFalse((Path(tmp) / installer.BRIDGE_WAITING).exists())
            self.assertEqual(calls.count(['plugins', 'install']), 1)

    def test_a_failed_plugin_install_that_took_the_model_runtime_down_gets_it_back(self):
        ok, calls, said, stamped, _ = self.swap(fail=['install'], breaks='install')
        self.assertFalse(ok)  # the bridge did not go in: still a failed install, tried again next time
        self.assertFalse(stamped)
        after = calls[calls.index('plugins install'):]
        self.assertLess(after.index('plugins reload'), after.index(self.RESTART), calls)  # one reload first, then the restart
        self.assertEqual(after.count('plugins reload'), 1)
        self.assertEqual(calls[-2:], ['gateway call', 'plugins inspect'], calls)  # checked again after the restart, then whether it is in
        self.assertIn('cannot run models', said)
        self.assertIn('Model calls work again', said)
        self.assertIn('run ./install.sh again', said)
        self.assertNotIn('plugins enable', calls)
        ok, calls, said, _, _ = self.swap(fail=['install'], breaks='install', reload_heals=True)
        self.assertFalse(ok)
        self.assertNotIn(self.RESTART, calls)  # the reload was enough
        self.assertIn('Reloaded the bridge: model calls work again', said)

    def test_the_model_runtime_is_checked_after_every_plugin_step(self):
        for step in ('install', 'enable', 'reload'):
            with self.subTest(step=step):
                ok, calls, said, stamped, _ = self.swap(breaks=step)  # the step itself reports success
                self.assertIn(self.RESTART, calls)
                self.assertIn(f'After the plugin {step}, the OpenClaw Gateway cannot run models', said)
                self.assertTrue(ok, said)
                self.assertTrue(stamped)
        ok, calls, said, stamped, _ = self.swap()
        self.assertEqual([c for c in calls if c.startswith(('plugins', 'gateway call'))],
                         ['plugins install', 'gateway call', 'plugins enable', 'gateway call', 'plugins reload', 'gateway call'], calls)
        self.assertNotIn(self.RESTART, calls)

    def test_where_the_owner_restarts_the_gateway_themself_it_ends_with_the_one_command(self):
        for case in ({'fail': ['install'], 'breaks': 'install'}, {'breaks': 'reload'}, {'fail': ['reload']}):
            with self.subTest(case=case):
                ok, calls, said, stamped, _ = self.swap(restart=False, **case)
                self.assertFalse(ok)
                self.assertFalse(stamped)  # nothing recorded as installed
                self.assertFalse([c for c in calls if c.startswith('systemctl')], calls)
                self.assertIn('Restart it: systemctl --user restart openclaw-gateway.service', said)
                if case.get('breaks'):
                    self.assertIn('NOT FIXED: the OpenClaw Gateway cannot run models', said)

    def test_without_a_gateway_service_a_lost_model_runtime_ends_with_the_openclaw_command(self):
        ok, calls, said, stamped, _ = self.swap(fail=['install'], breaks='install', unit=None)
        self.assertFalse(ok)
        self.assertIn('NOT FIXED', said)
        self.assertIn('Restart it: openclaw gateway restart', said)

    def test_gateway_restarts_are_the_owners_when_the_config_says_so(self):
        config = self.tmp / 'config.json'
        paths = mock.Mock(config=config)
        self.assertTrue(installer.may_restart_gateway(paths))  # no config yet
        config.write_text('{"port": 1}')
        self.assertTrue(installer.may_restart_gateway(paths))
        config.write_text('{"gateway_restart": false}')
        self.assertFalse(installer.may_restart_gateway(paths))

    def test_the_memory_index_is_read_from_the_gateways_own_embedding_server(self):
        ps = '\n'.join(('  10     1 openclaw-gateway gateway run',
                        '  20    10 /opt/llama/llama-server --models-preset /x/preset.ini --port 4100',
                        '  21    20 /opt/llama/llama-server --embeddings --host 127.0.0.1 --metrics --port 4101 -m /x/e.gguf',
                        '  30     1 /opt/llama/llama-server --embeddings --host 127.0.0.1 --metrics --port 4999',  # someone else's
                        '  31    10 /opt/llama/llama-server --host 127.0.0.1 --metrics --port 4102'))  # a chat model
        metrics = {4101: '# HELP llamacpp:requests_processing Number of requests processing.\nllamacpp:requests_processing 1\n'
                         'llamacpp:requests_deferred 3\nllamacpp:prompt_tokens_total 9\n'}
        class Answer:
            def __init__(self, text): self.text = text
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self, n=-1): return self.text.encode()
        def urlopen(url, timeout=None):
            port = int(url.split(':')[2].split('/')[0])
            if port not in metrics:
                raise OSError('refused')
            return Answer(metrics[port])
        with mock.patch.object(installer, 'run', return_value=subprocess.CompletedProcess([], 0, ps, '')), \
                mock.patch.object(installer, 'reindex_running', return_value=False), \
                mock.patch.object(installer.urllib.request, 'urlopen', side_effect=urlopen), mock.patch.dict(os.environ):
            os.environ.pop('ASSISTANT_EMBEDDING_PORTS', None)
            self.assertEqual(installer.gateway_embedding_ports(), [4101])
            self.assertIs(installer.index_busy(), True)
            metrics[4101] = 'llamacpp:requests_processing 0\nllamacpp:requests_deferred 0\n'
            self.assertIs(installer.index_busy(), False)
            metrics[4101] = 'something else\n'
            self.assertIsNone(installer.index_busy())
            del metrics[4101]
            self.assertIsNone(installer.index_busy())
        with mock.patch.object(installer, 'run', return_value=subprocess.CompletedProcess([], 127, '', 'no ps')), \
                mock.patch.object(installer, 'reindex_running', return_value=False):
            self.assertIsNone(installer.index_busy())

    def embedding_servers(self, pages, ports='8792'):
        """index_busy with no Gateway embedding server, against fake servers: pages[(port, path)] is what one answers."""
        asked = []
        class Answer:
            def __init__(self, text): self.text = text
            def __enter__(self): return self
            def __exit__(self, *a): return False
            def read(self, n=-1): return self.text.encode()
        def urlopen(url, timeout=None):
            asked.append(url)
            host, path = url.split('//')[1].split('/', 1)
            if (int(host.split(':')[1]), '/' + path) not in pages:
                raise OSError('refused')
            return Answer(pages[(int(host.split(':')[1]), '/' + path)])
        with mock.patch.object(installer, 'run', return_value=subprocess.CompletedProcess([], 0, '  10     1 openclaw-gateway gateway run', '')), \
                mock.patch.object(installer.urllib.request, 'urlopen', side_effect=urlopen), \
                mock.patch.object(installer, 'reindex_running', return_value=False), \
                mock.patch.dict(os.environ, {'ASSISTANT_EMBEDDING_PORTS': ports}):
            return installer.index_busy(), asked

    def test_an_embedding_server_the_gateway_did_not_start_is_asked_by_its_port(self):
        busy = 'llamacpp:requests_processing 1\nllamacpp:requests_deferred 0\n'
        still = 'llamacpp:requests_processing 0\nllamacpp:requests_deferred 0\n'
        self.assertEqual(self.embedding_servers({(8792, '/metrics'): busy}), (True, ['http://127.0.0.1:8792/metrics']))
        self.assertIs(self.embedding_servers({(8792, '/metrics'): still})[0], False)
        self.assertIs(self.embedding_servers({(8792, '/metrics'): still, (8793, '/metrics'): busy}, ports=' 8792, 8793 ,')[0], True)
        self.assertEqual(self.embedding_servers({(8792, '/metrics'): busy}, ports=''), (None, []))  # not set: as before
        # Only port numbers, only on this computer: anything else is skipped, never asked.
        found, asked = self.embedding_servers({(8792, '/metrics'): busy}, ports='example.com:80,8792@example.com,-1,0,99999,8792/x,\u00b2,0x10')
        self.assertEqual((found, asked), (None, []))
        found, asked = self.embedding_servers({(8792, '/metrics'): busy}, ports='example.com:80,8792')
        self.assertIs(found, True)
        self.assertTrue(all(url.startswith('http://127.0.0.1:8792/') for url in asked), asked)

    def test_an_embedding_server_without_metrics_is_read_from_its_slots(self):
        slots = lambda *working: json.dumps([{'id': n, 'is_processing': one, 'n_ctx': 2048} for n, one in enumerate(working)])
        found, asked = self.embedding_servers({(8792, '/slots'): slots(False, True)})
        self.assertIs(found, True)
        self.assertEqual(asked, ['http://127.0.0.1:8792/metrics', 'http://127.0.0.1:8792/slots'])  # /metrics first
        self.assertIs(self.embedding_servers({(8792, '/slots'): slots(False, False)})[0], False)
        self.assertIs(self.embedding_servers({(8792, '/metrics'): 'not counts\n', (8792, '/slots'): slots(True)})[0], True)
        found, asked = self.embedding_servers({(8792, '/metrics'): 'llamacpp:requests_processing 0\n', (8792, '/slots'): slots(True)})
        self.assertEqual((found, len(asked)), (False, 1))  # a /metrics that says is the answer
        for unreadable in ('[]', '{"error": "slots are off"}', '[{"id": 0}]', 'not json', '[1, "x"]', 'null'):
            self.assertIsNone(self.embedding_servers({(8792, '/slots'): unreadable})[0], unreadable)
        self.assertIsNone(self.embedding_servers({})[0])  # nothing answers on that port

    def test_a_reload_without_a_running_gateway_starts_it_and_checks_the_bridge_loaded(self):
        loaded = {'ok': True, 'plugins': {'loaded': ['telegram', installer.PLUGIN_ID], 'errors': []}}
        ok, calls, said, stamped = self.gateway(health=[None, {'ok': True, 'plugins': {'loaded': ['telegram']}}, loaded])
        self.assertTrue(ok, said)
        self.assertTrue(stamped)
        self.assertIn(['systemctl', '--user', 'reset-failed', 'openclaw-gateway.service'], calls)
        self.assertIn(['systemctl', '--user', 'restart', 'openclaw-gateway.service'], calls)
        self.assertIn('loaded', said)

    def test_a_gateway_that_does_not_load_the_bridge_fails_with_its_reason(self):
        broken = {'ok': True, 'plugins': {'loaded': ['telegram'], 'errors': [{'id': installer.PLUGIN_ID, 'error': 'entry not found'}]}}
        ok, _, said, stamped = self.gateway(health=[broken])
        self.assertFalse(ok)
        self.assertFalse(stamped)
        self.assertIn('did not load ' + installer.PLUGIN_ID + ': entry not found', said)

    def test_a_gateway_that_does_not_start_fails_with_what_to_check(self):
        ok, _, said, _ = self.gateway(health=[], restart_code=1)
        self.assertFalse(ok)
        self.assertIn('Could not start the OpenClaw Gateway', said)
        with mock.patch.object(installer.time, 'time', side_effect=[0, 0, 100, 100]):
            ok, _, said, _ = self.gateway(health=[])
        self.assertFalse(ok)
        self.assertIn('did not come up', said)

    def test_without_a_gateway_service_the_saved_bridge_is_enough(self):
        ok, calls, said, stamped = self.gateway(health=[], unit=None)
        self.assertTrue(ok, said)
        self.assertFalse(stamped)  # not live yet: the next install reloads it
        self.assertNotIn('restart', [c[2] for c in calls if c[0] == 'systemctl'])
        self.assertIn('loads when it starts', said)

    def test_a_running_gateway_that_refuses_the_reload_without_a_service_fails(self):
        ok, _, said, _ = self.gateway(health=[{'ok': True, 'plugins': {'loaded': []}}], unit=None)
        self.assertFalse(ok)
        self.assertIn('plugin reload failed', said)

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='machine-install-'))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.home, self.bin, self.log = self.tmp / 'home', self.tmp / 'bin', self.tmp / 'calls.log'
        self.home.mkdir()
        self.bin.mkdir()
        # Never this computer's own OpenClaw: a memory index it is rebuilding would count as running in these tests
        rebuild = mock.patch.object(installer, 'reindex_running', return_value=False)
        rebuild.start()
        self.addCleanup(rebuild.stop)
        for name in ('openclaw', 'systemctl', 'journalctl'):
            path = self.bin / name
            path.write_text(STUB.format(log=self.log, name=name))
            path.chmod(0o755)
        package = self.tmp / 'lib/node_modules/openclaw'
        package.mkdir(parents=True)
        (package / 'package.json').write_text(json.dumps({'name':'openclaw','version':'2026.11.2'}))
        (self.bin / 'node').symlink_to(shutil.which('node'))
        self.data = self.home / '.local/share/personal-assistant'
        self.config = self.data / 'config.json'

    def env(self, **extra):
        env = {k: v for k, v in os.environ.items() if not k.startswith(('ASSISTANT_', 'OPENCLAW_'))}
        env.update(HOME=str(self.home), PATH=str(self.bin), ASSISTANT_PLUGIN_RETRY_WAIT='0',  # no real Gateway to wait for
                   ASSISTANT_SERVICE_MANAGER='systemd',  # the stubs are systemd's, also on macOS
                   ASSISTANT_FROM_MAIN='1')  # this checkout, not the newest signed release (test_release covers that)
        env.update(ANSWERS)
        env.update(extra)
        return env

    def install(self, *args, **extra):
        return subprocess.run([sys.executable, str(ROOT / 'installer.py'), '--non-interactive', '--health-timeout', '0', *args],
                              env=self.env(**extra), capture_output=True, text=True, timeout=120, stdin=subprocess.DEVNULL)

    def calls(self):
        return self.log.read_text().splitlines() if self.log.exists() else []

    def mode(self, path):
        return stat.S_IMODE(path.stat().st_mode)

    def test_non_interactive_install_writes_config_secrets_unit_plugin_and_cli(self):
        result = self.install('--no-start')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        config = json.loads(self.config.read_text())
        self.assertEqual((config['owner_name'], config['telegram_owner'], config['tailscale_owner']),
                         ('Alex Owner', '1000001', 'alex@example.com'))
        self.assertEqual(config['dashboard_host'], 'machine.example-tailnet.ts.net:8443')  # its own origin
        self.assertEqual(config['dashboard_path'], '/')
        self.assertEqual([a['id'] for a in config['accounts']], ['work-gmail', 'work-calendar', 'openclaw-gateway'])
        gmail = config['accounts'][0]
        self.assertEqual((gmail['email'], gmail['client'], gmail['boundary']), ('alex@example.com', 'work', 'work:Acme'))
        self.assertNotIn('exclude', gmail)
        self.assertEqual(config['app_dir'], str(ROOT))
        self.assertEqual(config['database'], str(self.data / 'events.sqlite'))
        self.assertFalse(config['delivery_enabled'])
        self.assertFalse(config['review_worker']['enabled'])
        self.assertTrue(Path(config['openclaw_package_dir'], 'package.json').exists())
        self.assertNotIn('~', json.dumps(config))
        self.assertEqual(self.mode(self.data), 0o700)
        for name in ('config.json', 'api-token', 'owner-token', 'vapid.json'):
            self.assertEqual(self.mode(self.data / name), 0o600, name)
        self.assertEqual(len((self.data / 'api-token').read_text()), 64)
        unit = (self.home / '.config/systemd/user/personal-assistant.service').read_text()
        self.assertIn(f'ExecStart={sys.executable} {ROOT}/assistant.py serve', unit)
        self.assertIn(f'WorkingDirectory={ROOT}', unit)
        self.assertEqual((self.home / '.local/bin/assistant').resolve(), ROOT / 'cli.py')
        cli = subprocess.run([sys.executable, str(self.home / '.local/bin/assistant'), '--help'], capture_output=True, text=True)
        self.assertIn('usage: assistant', cli.stdout, cli.stderr)
        calls = self.calls()
        self.assertIn(f'openclaw plugins install --link --force --accept-capabilities {ROOT}/openclaw-plugin', calls)
        self.assertIn('openclaw plugins enable personal-assistant-bridge', calls)
        # Without this OpenClaw skips the bridge's conversation hooks and reviews never bind to their run.
        self.assertIn('openclaw config set plugins.entries.personal-assistant-bridge.hooks.allowConversationAccess true --strict-json', calls)
        self.assertIn('systemctl --user daemon-reload', calls)
        self.assertFalse(any('enable personal-assistant.service' in c for c in calls), calls)  # --no-start
        self.assertIn('Next steps', result.stdout)
        self.assertIn('Connect Gmail: assistant connect gmail', result.stdout)
        self.assertIn('Connect Google Calendar: assistant connect calendar', result.stdout)
        self.assertNotIn('Connect Machine health', result.stdout)
        self.assertIn('assistant doctor', result.stdout)

    def test_the_gateway_unit_gets_a_drop_in_that_keeps_systemd_retrying_once(self):
        dropin = self.home / '.config/systemd/user/openclaw-gateway.service.d/keep-retrying.conf'
        result = self.install('--no-start')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        text = dropin.read_text()
        self.assertIn('[Unit]\nStartLimitIntervalSec=0\n', text)  # no start limit: systemd never gives up
        self.assertIn('[Service]\nRestartSec=15\n', text)
        self.assertIn('keeps retrying', result.stdout)
        result = self.install('--no-start')  # an update: same file, nothing said
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(dropin.read_text(), text)
        self.assertNotIn('keeps retrying', result.stdout)

    def test_the_retry_drop_in_goes_only_next_to_an_existing_gateway_unit_under_systemd(self):
        calls, said = [], []
        run = lambda command, **kwargs: calls.append(command) or subprocess.CompletedProcess(command, 0, '', '')
        paths = installer.Paths(self.home)
        units = self.home / '.config/systemd/user'
        with mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer, 'say', side_effect=said.append), \
                mock.patch.object(installer.service, 'manager', return_value='systemd'), \
                mock.patch.object(installer.onboarding, 'gateway_units', return_value=['openclaw-gateway.service', 'openclaw-node.service']):
            self.assertEqual(installer.gateway_keep_retrying(paths), [units / 'openclaw-gateway.service.d/keep-retrying.conf'])
            self.assertFalse((units / 'openclaw-node.service.d').exists())  # the node host is not the Gateway
            self.assertEqual(calls, [['systemctl', '--user', 'daemon-reload']])
            calls.clear()
            self.assertEqual(installer.gateway_keep_retrying(paths), [])  # already there: no write, no reload
            self.assertEqual(calls, [])
            (units / 'openclaw-gateway.service.d/keep-retrying.conf').write_text('[Unit]\nStartLimitIntervalSec=60\n')
            self.assertEqual(len(installer.gateway_keep_retrying(paths)), 1)  # an older or edited one is put back
            self.assertEqual((units / 'openclaw-gateway.service.d/keep-retrying.conf').read_text(), installer.GATEWAY_RETRY_TEXT)
        shutil.rmtree(units)
        for manager, found in (('systemd', []), ('launchd', ['openclaw-gateway.service'])):
            with self.subTest(manager=manager), mock.patch.object(installer, 'run', side_effect=run), \
                    mock.patch.object(installer.service, 'manager', return_value=manager), \
                    mock.patch.object(installer.onboarding, 'gateway_units', return_value=found):
                self.assertEqual(installer.gateway_keep_retrying(paths), [])  # no unit yet / launchd's KeepAlive retries
                self.assertFalse(units.exists())

    def test_the_retry_drop_in_never_goes_outside_the_user_units_folder(self):
        run = lambda command, **kwargs: subprocess.CompletedProcess(command, 0, '', '')
        paths = installer.Paths(self.home)
        odd = ['../../evil-gateway.service', 'openclaw-gateway/../x.service', 'openclaw-gateway..service', 'openclaw-gateway.socket']
        with mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer, 'say'), \
                mock.patch.object(installer.service, 'manager', return_value='systemd'), \
                mock.patch.object(installer.onboarding, 'gateway_units', return_value=odd + ['openclaw-gateway@main.service']):
            self.assertEqual(installer.gateway_keep_retrying(paths),
                             [self.home / '.config/systemd/user/openclaw-gateway@main.service.d/keep-retrying.conf'])
        self.assertFalse((self.home / 'evil-gateway.service.d').exists())
        self.assertEqual(sorted(p.name for p in (self.home / '.config/systemd/user').iterdir()), ['openclaw-gateway@main.service.d'])

    def test_rerun_upgrades_without_clobbering_config_or_secrets(self):
        self.assertEqual(self.install('--no-start').returncode, 0)
        token = (self.data / 'api-token').read_text()
        vapid = (self.data / 'vapid.json').read_text()
        config = json.loads(self.config.read_text())
        config['owner_name'] = 'Changed By Hand'
        config['accounts'][0]['exclude'] = [{'senders': ['noise@example.com']}]
        config['port'] = free_port()
        del config['weekly_recap']
        self.config.write_text(json.dumps(config))
        result = self.install(ASSISTANT_OWNER_NAME='Someone Else', ASSISTANT_CONNECTORS='gateway')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        again = json.loads(self.config.read_text())
        self.assertEqual(again['owner_name'], 'Changed By Hand')
        self.assertEqual(again['accounts'][0]['exclude'], [{'senders': ['noise@example.com']}])
        self.assertEqual(len(again['accounts']), 3)
        self.assertEqual(again['weekly_recap'], {'enabled': True, 'weekday': 5, 'at': '16:00'})  # missing default restored
        self.assertEqual(self.mode(self.config), 0o600)
        self.assertEqual((self.data / 'api-token').read_text(), token)
        self.assertEqual((self.data / 'vapid.json').read_text(), vapid)
        self.assertIn('Keeping existing', result.stdout)
        self.assertIn('already present, unchanged', result.stdout)
        calls = self.calls()
        self.assertIn('systemctl --user enable personal-assistant.service', calls)
        self.assertIn('systemctl --user restart personal-assistant.service', calls)
        self.assertIn('not answering yet', result.stdout)  # nothing listens on the free port
        before = self.config.read_text()
        self.assertEqual(self.install().returncode, 1)
        self.assertEqual(self.config.read_text(), before)

    def test_telegram_is_optional(self):
        result = self.install('--no-start', ASSISTANT_TELEGRAM_OWNER='')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('No Telegram', result.stdout)
        config = json.loads(self.config.read_text())
        self.assertEqual(config['telegram_owner'], '')
        self.assertNotIn('telegram_account', config)

    def test_missing_answers_fail_clearly_without_writing(self):
        result = self.install('--no-start', ASSISTANT_TAILSCALE_OWNER='')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('tailscale', result.stdout + result.stderr)
        self.assertFalse(self.config.exists())
        result = self.install('--no-start', ASSISTANT_TELEGRAM_OWNER='@alex')
        self.assertIn('numeric chat ID', result.stdout + result.stderr)
        result = self.install('--no-start', ASSISTANT_CONNECTORS='gmail,fax')
        self.assertIn('Unknown sources: fax', result.stdout + result.stderr)

    def test_upgrades_never_take_the_examples_identity(self):
        self.assertEqual(self.install('--no-start').returncode, 0)
        config = json.loads(self.config.read_text())
        for key in ('dashboard_host', 'timezone'):
            del config[key]
        self.config.write_text(json.dumps(config))
        result = self.install('--no-start')
        again = json.loads(self.config.read_text())
        self.assertNotIn('dashboard_host', again)
        self.assertEqual(again['timezone'], installer.local_timezone())
        self.assertIn('dashboard_host is empty', subprocess.run(
            [sys.executable, str(ROOT / 'cli.py'), '--config', str(self.config), 'doctor'], env=self.env(), capture_output=True, text=True).stdout)

    def test_bad_answers_and_a_missing_tailscale_fail_before_writing(self):
        result = self.install('--no-start', ASSISTANT_TIMEZONE='Mars/Olympus')
        self.assertIn('Unknown time zone', result.stdout + result.stderr)
        result = self.install('--no-start', ASSISTANT_TAILSCALE_OWNER='')
        self.assertIn('FAIL  tailscale', result.stdout)
        self.assertIn('https://tailscale.com/download', result.stdout)
        self.assertFalse(self.config.exists())

    def test_a_personal_setup_a_named_bot_and_no_gateway_unit(self):
        home = Path(tempfile.mkdtemp(prefix='machine-wizard-'))
        self.addCleanup(shutil.rmtree, home, True)
        (home / '.openclaw').mkdir()
        (home / '.openclaw/openclaw.json').write_text(json.dumps({'channels': {'telegram': {'accounts': {
            'family': {'botToken': 'x', 'allowFrom': ['5']}, 'mine': {'botToken': 'y', 'allowFrom': ['tg:1000001']}}}}}))
        replies = iter(['Alex Owner', 'alex', '1000001', 'alex@example.com', 'https://box', 'box.example-tailnet.ts.net',
                        'Mars/Olympus', 'Europe/Brussels', 'gmail,fax', 'gmail,gateway', 'nope', 'alex@gmail.com', ''])
        with mock.patch.dict(os.environ, {'HOME': str(home)}, clear=False), \
             mock.patch.dict(os.environ, {k: '' for k in installer.ENV.values()}), \
             mock.patch.object(builtins, 'input', lambda prompt='': next(replies)), \
             mock.patch.object(installer.onboarding, 'gateway_unit', return_value=None), \
             mock.patch.object(installer, 'say') as said:
            values = installer.answers(True, {})
            config = installer.new_config(values, {}, installer.Paths(home))
        self.assertEqual(next(replies, 'done'), 'done')
        said = ' '.join(str(c.args[0]) for c in said.call_args_list)
        for problem in ('not a Telegram user ID', 'a host name', 'unknown time zone', 'unknown: fax', 'an email address', 'skipped the Gateway'):
            self.assertIn(problem, said)
        self.assertEqual((values['telegram_owner'], values['timezone'], values['boundary']), ('1000001', 'Europe/Brussels', 'personal:me'))
        self.assertEqual([(a['id'], a['boundary']) for a in config['accounts']], [('personal-gmail', 'personal:me')])
        self.assertEqual(config['telegram_account'], 'mine')

    def test_tagged_machines_spaces_and_the_cli_path(self):
        status = {'Self': {'UserID': 7, 'DNSName': 'box.example-tailnet.ts.net.'}, 'User': {'7': {'LoginName': 'tagged-devices'}}}
        with mock.patch.object(installer, 'run', return_value=subprocess.CompletedProcess([], 0, json.dumps(status), '')):
            self.assertEqual(installer.tailscale_identity('tailscale'), {'tailscale_owner': '', 'dashboard_host': 'box.example-tailnet.ts.net:8443'})
        self.assertEqual([installer.dashboard_address(h) for h in ('m.tail.ts.net', 'https://m.tail.ts.net/', 'm.tail.ts.net:443', 'my.example.com')],
                         ['m.tail.ts.net:8443', 'm.tail.ts.net:8443', 'm.tail.ts.net:443', 'my.example.com'])
        unit = installer.unit_text({}, {'python': '/opt/my python/bin/python3'}, '/tmp/c.json')
        self.assertIn('ExecStart="/opt/my python/bin/python3" ', unit)
        self.assertIn('Environment="PATH=', unit)
        result = self.install('--no-start')
        self.assertIn('is not on your PATH', result.stdout)
        self.assertIn(str(self.home / '.local/bin/assistant'), result.stdout)

    def test_missing_openclaw_is_reported_with_a_fix(self):
        (self.bin / 'openclaw').unlink()
        result = self.install('--no-start')
        self.assertEqual(result.returncode, 1)
        self.assertIn('FAIL  openclaw CLI not found', result.stdout)
        self.assertIn('npm install -g openclaw@2026.11.2', result.stdout)
        self.assertFalse(self.config.exists())

    def test_without_openclaw_it_offers_to_install_it_and_walks_through_its_setup(self):
        settings = self.tmp / 'openclaw/openclaw.json'
        npm_prefix = self.tmp / 'root-owned'  # npm's global folder, not ours: install into ~/.local, never sudo
        npm_prefix.mkdir(); npm_prefix.chmod(0o555); self.addCleanup(npm_prefix.chmod, 0o755)
        ran, said = [], []

        class UI(installer.onboarding.UI):
            def __init__(self, answers): self.answers = answers
            def say(self, text=''): said.append(text)
            def yes(self, prompt, default=True):
                said.append(prompt)
                return self.answers.pop(0)

        def run(args, check=False, **kwargs):
            ran.append(args)
            name = Path(args[0]).name
            if name == 'node':
                return subprocess.CompletedProcess(args, 0, 'v24.22.1\n', '')
            if args[1:] == ['prefix', '-g']:
                return subprocess.CompletedProcess(args, 0, f'{npm_prefix}\n', '')
            if args[1:3] == ['install', '-g']:
                binary = Path(args[args.index('--prefix') + 1]) / 'bin/openclaw'
                binary.parent.mkdir(parents=True, exist_ok=True); binary.write_text('#!/bin/sh\n'); binary.chmod(0o755)
                return subprocess.CompletedProcess(args, 0, '', 'npm warn install-scripts Run `npm install -g --allow-scripts=esbuild,koffi,openclaw`'
                                                   ' to allow these scripts once\n')
            if args[1:] == ['onboard', '--install-daemon']:  # OpenClaw's own wizard: model, Gateway, Telegram bot
                settings.parent.mkdir(exist_ok=True)
                settings.write_text(json.dumps({'channels': {'telegram': {'botToken': 'x'}}}))
            return subprocess.CompletedProcess(args, 0, '', '')

        which = lambda name: {'node': str(self.bin / 'node'), 'npm': str(self.bin / 'npm')}.get(name)
        with mock.patch.dict(os.environ, {'HOME': str(self.home), 'OPENCLAW_CONFIG_PATH': str(settings), 'PATH': str(self.bin)}), \
             mock.patch.object(installer, 'run', side_effect=run), mock.patch.object(installer.shutil, 'which', side_effect=which), \
             mock.patch.object(installer, 'say'), mock.patch.object(installer.openclaw_pin, 'check') as pinned:
            installer.offer_openclaw(UI([False]))  # no: nothing installed
            self.assertFalse(any(a[1:3] == ['install', '-g'] for a in ran))
            pinned.side_effect = installer.openclaw_pin.PinMismatch('the registry checksum does not match')
            installer.offer_openclaw(UI([True]))  # a checksum that doesn't match the pin: nothing installed either
            self.assertFalse(any(a[1:3] == ['install', '-g'] for a in ran))
            self.assertIn('was not installed: the registry checksum does not match', '\n'.join(said))
            pinned.side_effect = None
            installer.offer_openclaw(UI([True, True]))
            pinned.assert_called_with('2026.11.2')
            self.assertIn(str(self.home / '.local/bin'), os.environ['PATH'])  # the rest of this run finds it
        local = self.home / '.local'
        self.assertIn([str(self.bin / 'npm'), 'install', '-g', 'openclaw@2026.11.2', '--prefix', str(local)], ran)
        # npm 11 held back the install scripts: the install runs again with exactly those allowed, as npm says (no rebuild)
        self.assertIn([str(self.bin / 'npm'), 'install', '-g', 'openclaw@2026.11.2', '--prefix', str(local), '--allow-scripts=esbuild,koffi,openclaw'], ran)
        self.assertFalse(any('rebuild' in a for a in ran))
        self.assertIn([str(local / 'bin/openclaw'), 'onboard', '--install-daemon'], ran)
        self.assertIn([str(local / 'bin/openclaw'), 'health'], ran)
        self.assertFalse(any('channels' in a for a in ran))  # the wizard already added the bot
        text = '\n'.join(said)
        self.assertIn('Install OpenClaw 2026.11.2 now? (runs: npm install -g openclaw@2026.11.2 --prefix', text)
        self.assertIn('@BotFather', text)
        self.assertIn('Gateway: say yes to running it as a service', text)

        # Set up, but no Telegram bot: only that step. Set up with a bot: not a single question.
        settings.write_text(json.dumps({'gateway': {}}))
        (self.bin / 'openclaw').chmod(0o755)
        ran.clear(); said.clear()
        which = lambda name: str(self.bin / name) if name == 'openclaw' else None
        with mock.patch.dict(os.environ, {'OPENCLAW_CONFIG_PATH': str(settings)}), mock.patch.object(installer, 'run', side_effect=run), \
             mock.patch.object(installer.shutil, 'which', side_effect=which):
            installer.offer_openclaw(UI([True]))
            self.assertEqual(ran[:1], [[str(self.bin / 'openclaw'), 'channels', 'add', '--channel', 'telegram']], said)
            settings.write_text(json.dumps({'channels': {'telegram': {'accounts': {'work': {'botToken': 'x'}}}}}))
            ran.clear(); said.clear()
            installer.offer_openclaw(UI([]))
            self.assertEqual((ran, said), ([], []))

    def test_without_node_it_says_what_to_install_first(self):
        said = []
        ui = installer.onboarding.UI(); ui.say = said.append
        ui.yes = mock.Mock(side_effect=AssertionError('nothing to ask'))
        with mock.patch.object(installer.shutil, 'which', return_value=None):
            installer.offer_openclaw(ui)
        self.assertIn('Node.js', said[0])
        self.assertIn('nodejs.org', said[0])

    def test_failed_install_steps_exit_nonzero(self):
        for command in ('plugins install --link --force --accept-capabilities ' + str(ROOT / 'openclaw-plugin'),
                        'plugins enable personal-assistant-bridge',
                        'config set plugins.entries.personal-assistant-bridge.hooks.allowConversationAccess true --strict-json',
                        'plugins reload personal-assistant-bridge --wait',
                        '--user daemon-reload', '--user enable personal-assistant.service',
                        '--user restart personal-assistant.service'):
            with self.subTest(command=command):
                result = self.install(ASSISTANT_TEST_FAIL=command, ASSISTANT_GATEWAY_WAIT='0')
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        result = self.install('--no-start', ASSISTANT_TEST_FAIL='--user daemon-reload')
        self.assertEqual(result.returncode, 1, result.stdout)

    def test_an_install_that_may_not_restart_the_gateway_fails_plainly_and_records_nothing(self):
        first = self.install()  # nothing answers the health check here, so its exit code says nothing
        stamp = self.data / 'plugin-installed'
        self.assertTrue(stamp.exists(), first.stdout + first.stderr)
        stamp.unlink()  # as after an update that changed the bridge
        self.config.write_text(json.dumps({**json.loads(self.config.read_text()), 'gateway_restart': False}))
        self.log.unlink()
        (self.bin / 'openclaw').write_text(f'''#!/bin/sh
echo "openclaw $*" >> "{self.log}"
case "$*" in
  --version) echo "OpenClaw 2026.11.2 (test)";;
  "plugins install"*) echo "Plugin replacement failed and its previous instance could not be restored" >&2; exit 1;;
  "gateway call models.list"*) echo "UNAVAILABLE: runtime owner was not published for main" >&2; exit 1;;
  "gateway health"*) echo '{{"ok": true, "plugins": {{"loaded": []}}}}';;
esac
exit 0
''')
        result = self.install()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('NOT FIXED: the OpenClaw Gateway cannot run models', result.stdout)
        self.assertIn('Restart it: systemctl --user restart openclaw-gateway.service', result.stdout)
        self.assertFalse(stamp.exists())
        calls = self.calls()
        self.assertIn('openclaw plugins reload personal-assistant-bridge --wait', calls)  # the one retry
        self.assertFalse([c for c in calls if c.startswith('systemctl') and 'openclaw-gateway' in c and ' restart ' in c], calls)
        self.assertNotIn('systemctl --user restart personal-assistant.service', calls)  # the install stopped there
        config = json.loads(self.config.read_text())
        self.assertIs(config['gateway_restart'], False)  # the choice survives the install

    def test_a_bridge_left_waiting_is_put_in_by_the_run_the_nightly_update_makes(self):
        self.assertEqual(self.install('--no-start').returncode, 0)
        self.log.unlink()
        result = self.install('--if-bridge-waits')  # nothing waits: nothing runs, nothing is said
        self.assertEqual((result.returncode, result.stdout, self.calls()), (0, '', []), result.stderr)
        (self.data / 'plugin-waiting').write_text('x\n')
        self.install('--if-bridge-waits')  # nothing answers the health check here, so its exit code says nothing
        self.assertIn(f'openclaw plugins install --link --force --accept-capabilities {ROOT}/openclaw-plugin', self.calls())
        self.assertIn('openclaw plugins reload personal-assistant-bridge --wait', self.calls())
        self.assertTrue((self.data / 'plugin-installed').exists())
        self.assertFalse((self.data / 'plugin-waiting').exists())

    def test_the_nightly_run_leaves_a_bridge_the_gateway_already_runs_alone(self):
        self.assertEqual(self.install('--no-start').returncode, 0)
        stamp = self.data / 'plugin-installed'
        stamp.write_text('0' * 64 + '\n')  # a one-line stamp from before the bridge last changed
        (self.data / 'plugin-waiting').write_text('x\n')
        root = str(ROOT / 'openclaw-plugin')
        found = {'plugin': {'rootDir': root, 'enabled': True, 'status': 'loaded'}, 'install': {'source': 'path', 'sourcePath': root}}
        (self.bin / 'openclaw').write_text(f'''#!/bin/sh
echo "openclaw $*" >> "{self.log}"
case "$*" in
  --version) echo "OpenClaw 2026.11.2 (test)";;
  "plugins inspect"*) echo '{json.dumps(found)}';;
  "gateway health"*) echo '{{"ok": true, "plugins": {{"loaded": ["{installer.PLUGIN_ID}"]}}}}';;
esac
exit 0
''')
        # A Gateway that started a moment ago, well after this checkout's bridge files were written
        (self.bin / 'ps').write_text('#!/bin/sh\necho "  00:01 /usr/bin/node /usr/lib/node_modules/openclaw/dist/index.js gateway --port 18789"\n')
        (self.bin / 'ps').chmod(0o755)
        (self.home / '.openclaw').mkdir(exist_ok=True)
        (self.home / '.openclaw/openclaw.json').write_text(json.dumps(
            {'plugins': {'entries': {installer.PLUGIN_ID: {'enabled': True, 'hooks': {'allowConversationAccess': True}}}}}))
        self.log.unlink()
        result = self.install('--if-bridge-waits')
        self.assertIn('already loaded as it is by the running Gateway', result.stdout, result.stdout + result.stderr)
        self.assertFalse([c for c in self.calls() if c.startswith(('openclaw plugins install', 'openclaw plugins reload'))], self.calls())
        self.assertFalse((self.data / 'plugin-waiting').exists())
        self.assertEqual(len(stamp.read_text().splitlines()), 2)

    def test_activation_is_explicit_and_preserves_existing_choices(self):
        self.assertEqual(self.install('--no-start').returncode, 0)
        with mock.patch.dict(os.environ, self.env(), clear=True), mock.patch.object(installer, 'health', return_value=True):
            self.assertEqual(installer.main(['--non-interactive', '--activate']), 0)
        activated = json.loads(self.config.read_text())
        self.assertTrue(activated['delivery_enabled'])
        self.assertTrue(activated['review_worker']['enabled'])
        self.assertEqual(self.install('--no-start').returncode, 0)
        self.assertTrue(json.loads(self.config.read_text())['delivery_enabled'])

    def test_a_first_install_takes_the_signed_release_or_installs_nothing(self):
        env = {k: v for k, v in self.env().items() if k != 'ASSISTANT_FROM_MAIN'}
        with mock.patch.dict(os.environ, env, clear=True), mock.patch.object(installer, 'to_signed_release', return_value=False):
            self.assertEqual(installer.main(['--non-interactive', '--no-start']), 1)
        self.assertFalse(self.config.exists())  # refused: nothing written
        with mock.patch.dict(os.environ, env, clear=True), mock.patch.object(installer, 'to_signed_release', return_value=True), \
                mock.patch.object(installer.os, 'execv', side_effect=SystemExit(0)) as again:
            with self.assertRaises(SystemExit):
                installer.main(['--non-interactive', '--no-start'])
        again.assert_called_once_with(sys.executable, [sys.executable, str(ROOT / 'installer.py'), '--non-interactive', '--no-start'])
        with mock.patch.dict(os.environ, env, clear=True), mock.patch.object(installer, 'to_signed_release') as signed, \
                mock.patch.object(installer, 'health', return_value=True):
            self.assertEqual(installer.main(['--non-interactive', '--no-start', '--from-main']), 0)
        signed.assert_not_called()

    def test_failed_uninstall_never_purges_running_service_data(self):
        self.assertEqual(self.install('--no-start').returncode, 0)
        result = self.install('--uninstall', '--purge', ASSISTANT_TEST_FAIL='--user disable --now personal-assistant.service')
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertTrue(self.config.exists())
        self.assertTrue((self.home / '.config/systemd/user/personal-assistant.service').exists())

    def test_removed_source_is_rejected_without_rewriting_private_config(self):
        self.assertEqual(self.install('--no-start').returncode, 0)
        config = json.loads(self.config.read_text())
        config['accounts'].append({'id':'work-feed','service':'rss','transport':'http','boundary':'work','url':'https://example.com/feed.xml'})
        self.config.write_text(json.dumps(config))
        self.assertEqual(self.install('--no-start').returncode, 0, 'connector plugins are supported sources')
        config = json.loads(self.config.read_text())
        config['accounts'].append({'id':'old-source','service':'unsupported'})
        self.config.write_text(json.dumps(config))
        before = self.config.read_text()
        result = self.install('--no-start')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Unsupported sources', result.stderr)
        self.assertEqual(self.config.read_text(), before)

    def test_a_self_hosted_install_updates_itself_daily_from_signed_releases_only(self):
        units = self.home / '.config/systemd/user'
        self.assertEqual(self.install('--no-start').returncode, 0)
        update = (units / 'the-machine-update.service').read_text()
        self.assertIn(f'{ROOT}/scripts/release.py update --install', update)
        self.assertIn('OnCalendar=', (units / 'the-machine-update.timer').read_text())
        self.assertNotIn('systemctl --user enable --now the-machine-update.timer', self.calls())  # --no-start
        self.install()
        self.assertIn('systemctl --user enable --now the-machine-update.timer', self.calls())
        config = json.loads(self.config.read_text())
        self.config.write_text(json.dumps({**config, 'auto_update': False}))
        self.assertEqual(self.install('--no-start').returncode, 0)
        self.assertIn('systemctl --user disable --now the-machine-update.timer', self.calls())
        self.assertFalse((units / 'the-machine-update.timer').exists())
        self.config.write_text(json.dumps(config))
        self.assertEqual(self.install('--no-start').returncode, 0)
        self.assertEqual(self.install('--uninstall').returncode, 0)
        self.assertFalse((units / 'the-machine-update.service').exists())
        self.assertFalse((units / 'the-machine-update.timer').exists())

    def machine_units(self):
        """Units as onboarding and signal_setup write them, plus ones an install must leave alone."""
        units = self.home / '.config/systemd/user'
        units.mkdir(parents=True, exist_ok=True)
        mirror = lambda name: f'[Service]\nExecStart={sys.executable} {ROOT}/{name} --store /tmp/store follow\n'
        for unit, text in (('the-machine-personal-telegram.service', mirror('telegram_mirror.py')),
                           ('the-machine-personal-signal.service', mirror('signal_mirror.py')),
                           ('the-machine-second-telegram.service', mirror('telegram_mirror.py')),  # not running
                           ('the-machine-wacli-x.service', '[Service]\nExecStart=/opt/wacli --store /tmp/w sync --follow\n'),
                           ('openclaw-gateway.service', f'[Service]\nExecStart=/usr/bin/node {ROOT}/openclaw-root.mjs gateway\n'),
                           ('cdp-relay.service', f'[Service]\nExecStart=/usr/bin/env node {ROOT}/deploy/cdp-relay.mjs\n')):
            (units / unit).write_text(text)
        return ' '.join(('personal-assistant.service', 'the-machine-personal-telegram.service', 'the-machine-personal-signal.service',
                         'the-machine-wacli-x.service', 'openclaw-gateway.service', 'cdp-relay.service'))

    def test_an_update_restarts_every_running_machine_unit_after_the_service(self):
        self.assertEqual(self.install('--no-start').returncode, 0)
        active = self.machine_units()
        self.log.unlink()
        result = self.install(ASSISTANT_TEST_ACTIVE=active)
        calls = self.calls()
        service = calls.index('systemctl --user restart personal-assistant.service')
        for unit in ('the-machine-personal-telegram.service', 'the-machine-personal-signal.service'):
            self.assertGreater(calls.index(f'systemctl --user restart {unit}'), service, unit)
            self.assertIn(f'{unit}: restarted on this release', result.stdout)
        # not running: not started either
        self.assertIn('systemctl --user is-active the-machine-second-telegram.service', calls)
        self.assertFalse([c for c in calls if 'second-telegram' in c and 'is-active' not in c], calls)
        # its own program, set up by hand, or OpenClaw's: never asked, never restarted
        for unit in ('the-machine-wacli-x.service', 'cdp-relay.service', 'the-machine-update.service'):
            self.assertFalse([c for c in calls if c.endswith(' ' + unit)], unit)
        self.assertFalse([c for c in calls if 'openclaw-gateway' in c and re.search(r'\b(is-active|restart|try-restart|start|stop|kill)\b', c)], calls)

    def test_a_machine_unit_that_does_not_restart_shows_in_the_health_lines(self):
        self.assertEqual(self.install('--no-start').returncode, 0)
        active = self.machine_units()
        result = self.install(ASSISTANT_TEST_ACTIVE=active, ASSISTANT_TEST_FAIL='--user restart the-machine-personal-signal.service')
        self.assertIn('Health: the-machine-personal-signal.service did not restart and may run the previous release;'
                      ' check systemctl --user status the-machine-personal-signal.service', result.stdout)
        self.assertIn('systemctl --user restart the-machine-personal-telegram.service', self.calls())  # the others still go
        self.assertNotIn('Health: the-machine-personal-telegram.service', result.stdout)

    def test_machine_units_are_found_by_their_launchd_agents_too(self):
        agents = self.home / 'Library/LaunchAgents'
        agents.mkdir(parents=True)
        with mock.patch.object(installer.service, 'manager', return_value='launchd'):
            paths = installer.Paths(self.home)
            for unit, program in ((installer.UNIT_NAME, [sys.executable, str(ROOT / 'assistant.py'), 'serve']),
                                  ('the-machine-personal-telegram.service', [sys.executable, str(ROOT / 'telegram_mirror.py'), 'follow']),
                                  ('the-machine-wacli-x.service', ['/opt/wacli', 'sync'])):
                installer.service.definition_path(unit, self.home).write_text(
                    installer.service.plist_text(program, unit=unit, base=self.home))
            self.assertEqual(installer.machine_units(paths), ['the-machine-personal-telegram.service'])

    def test_hosted_machines_get_no_update_timer(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(installer, 'HOSTED_AGENT', Path(tmp)), \
                mock.patch.object(installer.service, 'manager', return_value='systemd'), \
                mock.patch.object(installer, 'run') as ran, mock.patch.object(installer, 'say'):
            paths = installer.Paths(Path(tmp) / 'home')
            self.assertIsNone(installer.install_updates({}, {'systemctl': 'systemctl'}, paths, start=True))
            ran.assert_not_called()
            self.assertFalse((paths.unit.parent / installer.UPDATE_TIMER).exists())

    def test_uninstall_keeps_data_and_purge_removes_it(self):
        self.assertEqual(self.install('--no-start').returncode, 0)
        result = self.install('--uninstall')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.home / '.config/systemd/user/personal-assistant.service').exists())
        self.assertFalse((self.home / '.local/bin/assistant').exists())
        self.assertTrue(self.config.exists())
        calls = self.calls()
        self.assertIn('systemctl --user disable --now personal-assistant.service', calls)
        self.assertIn('openclaw plugins uninstall personal-assistant-bridge --force --keep-files', calls)
        self.assertTrue((ROOT / 'openclaw-plugin/index.ts').exists())
        self.assertEqual(self.install('--uninstall', '--purge').returncode, 0)
        self.assertFalse(self.data.exists())
        self.assertNotEqual(self.install('--purge').returncode, 0)


class WizardTest(unittest.TestCase):
    def test_node_versions_match_the_pinned_openclaw_engine_range(self):
        for text, runs, installs in [('22.13.0',False,False),('24.15.9',False,False),('24.16.0',True,False),
                                     ('24.22.0',True,False),('24.22.1',True,True),('25.8.0',False,False),
                                     ('26.0.9',False,False),('26.1.0',True,False),('26.12.0',True,False),
                                     ('26.12.1',True,True),('27.0.0',True,True)]:
            with self.subTest(version=text):
                version = installer.version_tuple(text)
                self.assertEqual(installer.supported_node(version), runs)
                self.assertEqual(installer.supported_node(version, installer.OPENCLAW_NODE_FLOORS), installs)

    def test_a_node_too_old_for_the_pinned_openclaw_is_not_offered_the_install(self):
        said = []
        ui = type('UI', (), {'say': lambda self, text: said.append(text), 'yes': lambda self, *a: self.fail('asked')})()
        node = lambda args, **kwargs: subprocess.CompletedProcess(args, 0, 'v24.21.0\n', '')
        with mock.patch.object(installer.shutil, 'which', side_effect=lambda name: '/usr/bin/' + name if name in ('node', 'npm') else None), \
             mock.patch.object(installer, 'resolve_tool', side_effect=lambda binary: binary), mock.patch.object(installer, 'run', side_effect=node):
            installer.offer_openclaw(ui)
        self.assertIn('It needs Node.js >=24.22.1 <25 or >=26.12.1 with npm first', '\n'.join(said))

    def test_mise_shim_uses_the_installed_executable_and_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()  # macOS: /var is /private/var
            shim = root / 'shims/openclaw'
            binary = root / 'node/26.1/bin/openclaw'
            package = binary.parent.parent / 'lib/node_modules/openclaw'
            package.mkdir(parents=True)
            binary.parent.mkdir(parents=True)
            binary.write_text('stub')
            (package / 'package.json').write_text('{"name":"openclaw"}')
            with mock.patch.object(installer.shutil, 'which', return_value='/bin/mise'), \
                 mock.patch.object(installer, 'run', return_value=subprocess.CompletedProcess([],0,str(binary)+'\n','')):
                resolved = installer.resolve_tool(str(shim))
            self.assertEqual(resolved, str(binary))
            self.assertEqual(installer.openclaw_package_dir(resolved), package)

    def test_interactive_answers_build_the_config(self):
        home = Path(tempfile.mkdtemp(prefix='machine-wizard-'))
        self.addCleanup(shutil.rmtree, home, True)
        replies = iter(['Alex Owner', '1000001', 'alex@example.com', 'box.example-tailnet.ts.net', 'Europe/Amsterdam',
                        'gmail,android,whatsapp', 'alex@example.com', 'work:Acme'])
        with mock.patch.dict(os.environ, {'HOME': str(home)}, clear=False), \
             mock.patch.dict(os.environ, {k: '' for k in installer.ENV.values()}), \
             mock.patch.object(builtins, 'input', lambda prompt='': next(replies)), \
             mock.patch.object(installer, 'say'):
            paths = installer.Paths(home)
            values = installer.answers(True, {})
            config = installer.new_config(values, {}, paths)
        self.assertEqual(next(replies, 'done'), 'done')
        self.assertEqual([a['id'] for a in config['accounts']], ['work-gmail', 'personal-android', 'personal-whatsapp'])
        self.assertEqual(config['accounts'][0]['client'], 'default')
        self.assertTrue(installer.onboarding.missing(config, config['accounts'][1]))  # assistant connect android picks the phone
        self.assertEqual(config['accounts'][1]['boundary'], 'personal:phone')
        self.assertEqual(config['accounts'][2]['store'], str(home / '.local/share/wacli'))
        self.assertEqual(config['credentials']['gog-password'], str(home / '.local/share/personal-assistant/gog-password'))
        self.assertEqual(config['dashboard_host'], 'box.example-tailnet.ts.net:8443')

    def test_wizard_defaults_come_from_what_openclaw_already_knows(self):
        home = Path(tempfile.mkdtemp(prefix='machine-wizard-'))
        self.addCleanup(shutil.rmtree, home, True)
        (home / '.openclaw').mkdir()
        (home / '.openclaw/openclaw.json').write_text(json.dumps({'commands': {'ownerAllowFrom': ['telegram:2000002']}}))
        replies = iter([''] * 7)
        with mock.patch.dict(os.environ, {'HOME': str(home)}, clear=False), \
             mock.patch.dict(os.environ, {k: '' for k in installer.ENV.values()}), \
             mock.patch.object(builtins, 'input', lambda prompt='': next(replies)), \
             mock.patch.object(installer, 'tailscale_identity', return_value={'tailscale_owner': 'a@b.c', 'dashboard_host': 'h.ts.net'}), \
             mock.patch.object(installer.onboarding, 'owner_name', return_value='Alex Owner'), \
             mock.patch.object(installer.onboarding, 'gateway_unit', return_value='openclaw-gateway.service'), \
             mock.patch.object(installer, 'say'):
            values = installer.answers(True, {})
        self.assertEqual((values['telegram_owner'], values['owner_name'], values['connectors']), ('2000002', 'Alex Owner', 'gateway'))

    def test_guided_setup_connects_then_offers_preview_and_activation(self):
        home = Path(tempfile.mkdtemp(prefix='machine-guided-'))
        self.addCleanup(shutil.rmtree, home, True)
        with mock.patch.dict(os.environ, {'HOME': str(home), 'OPENCLAW_WORKSPACE': str(home / 'ws')}), \
             mock.patch.object(installer.onboarding, 'gateway_unit', return_value='openclaw-gateway.service'):
            paths = installer.Paths(home)
            values = {**{k: '' for k in installer.ENV}, 'owner_name': 'Alex', 'telegram_owner': '1000001', 'tailscale_owner': 'a@b.c',
                      'dashboard_host': 'h.ts.net', 'timezone': 'UTC', 'connectors': 'gmail,gateway', 'email': 'alex@acme.test',
                      'gog_client': 'default', 'boundary': 'work:Acme', 'whatsapp_store': ''}
            installer.write_private(paths.config, json.dumps(installer.new_config(values, {}, paths)))
            asked, connected = [], []

            class UI(installer.onboarding.UI):
                def say(self, text=''): asked.append(text)
                def yes(self, prompt, default=True):
                    asked.append(prompt)
                    return not prompt.startswith('Make the dashboard')

            def connect(path, name, ui, account_id=None, restart=True):
                connected.append((name, account_id, restart))
                config = json.loads(Path(path).read_text())
                installer.write_private(Path(config['credentials']['gog-password']), 'x')
                return next(a for a in config['accounts'] if a['id'] == account_id)  # as onboarding.connect does
            with mock.patch.object(installer.onboarding, 'connect', side_effect=connect), \
                 mock.patch.object(installer.onboarding, 'restart_and_sync') as sync, \
                 mock.patch.object(installer.onboarding, 'serve_dashboard') as serve, \
                 mock.patch.object(installer.subprocess, 'call', return_value=0) as preview, \
                 mock.patch.object(installer, 'run', return_value=subprocess.CompletedProcess([], 0)), \
                 mock.patch.object(installer, 'say'):
                config = installer.guided(paths, '2026-01-01T00:00:00+00:00', UI())
        self.assertEqual(connected, [('gmail', 'work-gmail', False)])
        self.assertEqual(sync.call_args.args[1], ['work-gmail', 'openclaw-gateway'])
        serve.assert_called_once()
        self.assertTrue((home / 'ws/USER.md').exists())
        calls = [c.args[0] for c in preview.call_args_list]
        self.assertEqual([c[4] for c in calls], ['profile', 'preview'])  # profile reads the first sync, before the preview
        self.assertEqual(calls[0][-2:], ['--workspace', str(home / 'ws')])
        self.assertEqual(preview.call_args.args[0][-1], 'preview')
        self.assertTrue(config['delivery_enabled'] and config['review_worker']['enabled'])
        self.assertTrue(json.loads(paths.config.read_text())['delivery_enabled'])
        self.assertLess(next(i for i, a in enumerate(asked) if 'preview' in str(a)), next(i for i, a in enumerate(asked) if 'Turn on' in str(a)))

    def test_example_config_covers_every_connector(self):
        example = json.loads((ROOT / 'config.example.json').read_text())
        self.assertEqual(sorted(a['id'] for a in example['accounts']), sorted(installer.CONNECTORS.values()))


if __name__ == '__main__':
    unittest.main()
