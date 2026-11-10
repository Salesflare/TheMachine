"""Office files a preparation makes or sends stay valid (office_files.py): an invoice workbook made from last month's
keeps every namespace Excel needs, a workbook rewritten through an XML library is caught before it leaves, and an email
attachment goes out under the name the recipient should see. Made-up files only; nothing is sent."""
import io
import json
import re
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock
from xml.etree import ElementTree

import next_actions
import office_files

MAIN = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
SHEET = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
         f'<worksheet xmlns="{MAIN}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
         'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" mc:Ignorable="x14ac xr" '
         'xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac" '
         'xmlns:xr="http://schemas.microsoft.com/office/spreadsheetml/2014/revision" xr:uid="{00000000-0001-0000-0000-000000000000}">'
         '<dimension ref="A1:D5"/><sheetData>'
         '<row r="1" x14ac:dyDescent="0.25"><c r="A1" t="s"><v>0</v></c><c r="B1" s="1"><v>45716</v></c></row>'
         '<row r="2"><c r="A2" t="s"><v>1</v></c><c r="B2"><v>41</v></c></row>'
         '<row r="4"><c r="B4"><v>500.5</v></c><c r="D4"><f>B4*2</f><v>1001</v></c></row>'
         '</sheetData><pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/></worksheet>')
PARTS = {
    '[Content_Types].xml': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
    '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
    '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
    '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>',
    '_rels/.rels': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>',
    'xl/workbook.xml': f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<workbook xmlns="{MAIN}" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Invoice" sheetId="1" r:id="rId1"/></sheets>'
    '<calcPr calcId="191029"/></workbook>',
    'xl/_rels/workbook.xml.rels': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>',
    'xl/worksheets/sheet1.xml': SHEET,
    'xl/sharedStrings.xml': f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<sst xmlns="{MAIN}" count="2" uniqueCount="2">'
    '<si><t>Invoice date</t></si><si><t>Invoice number</t></si></sst>',
    'xl/styles.xml': f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<styleSheet xmlns="{MAIN}"><fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
    '<fills count="1"><fill><patternFill patternType="none"/></fill></fills><borders count="1"><border/></borders>'
    '<cellStyleXfs count="1"><xf/></cellStyleXfs><cellXfs count="2"><xf/><xf numFmtId="14" applyNumberFormat="1"/></cellXfs></styleSheet>',
}


def workbook(path, parts=PARTS):
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, text in parts.items():
            z.writestr(name, text)
    return path


def read(path, part):
    with zipfile.ZipFile(path) as z:
        return z.read(part).decode('utf-8')


class OfficeFiles(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        self.template = workbook(self.dir / '2025-02 invoice Acme - 41.xlsx')

    def test_last_months_invoice_is_sound(self):
        self.assertEqual(office_files.problems(self.template), [])

    def test_a_workbook_rewritten_by_an_xml_library_is_caught(self):
        # What went wrong: each sheet read with ElementTree and written back. Excel then calls the file corrupt (the
        # mc:Ignorable prefixes lose their declarations); LibreOffice still opens it, so reopening it there proves nothing.
        root = ElementTree.fromstring(SHEET.encode())
        broken = dict(PARTS, **{'xl/worksheets/sheet1.xml': ElementTree.tostring(root, encoding='unicode')})
        found = office_files.problems(workbook(self.dir / 'broken.xlsx', broken))
        self.assertTrue(found)
        self.assertTrue(any('ns0' in f or 'prefix' in f for f in found), found)

    def test_an_undeclared_compatibility_prefix_is_named(self):
        broken = dict(PARTS, **{'xl/worksheets/sheet1.xml': SHEET.replace(' xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac"', '')
                                .replace(' x14ac:dyDescent="0.25"', '')})
        found = office_files.problems(workbook(self.dir / 'broken.xlsx', broken))
        self.assertEqual(found, ['xl/worksheets/sheet1.xml names the prefix x14ac without declaring it (Excel, Word and PowerPoint refuse this)'])

    def test_a_part_with_entities_is_refused_unread(self):
        # A file from someone else's email is untrusted: no DTD, so no entity expansion
        bomb = '<?xml version="1.0"?><!DOCTYPE s [<!ENTITY a "aaaaaaaaaa"><!ENTITY b "&a;&a;&a;&a;&a;">]>' + f'<sst xmlns="{MAIN}">&b;</sst>'
        found = office_files.problems(workbook(self.dir / 'bomb.xlsx', dict(PARTS, **{'xl/sharedStrings.xml': bomb})))
        self.assertTrue(any(f.startswith('xl/sharedStrings.xml is not valid XML') for f in found), found)

    def test_missing_parts_and_damaged_files(self):
        parts = dict(PARTS)
        del parts['xl/styles.xml']
        found = office_files.problems(workbook(self.dir / 'parts.xlsx', parts))
        self.assertIn('lists a part that is missing (xl/styles.xml)', found)
        self.assertIn('xl/_rels/workbook.xml.rels points to a missing part (xl/styles.xml)', found)
        (self.dir / 'cut.xlsx').write_bytes(self.template.read_bytes()[:200])
        self.assertEqual(office_files.problems(self.dir / 'cut.xlsx'), ['is not a valid Office file (not a zip package)'])
        (self.dir / 'empty.docx').write_bytes(b'')
        self.assertEqual(office_files.problems(self.dir / 'empty.docx'), ['is empty'])
        (self.dir / 'locked.xlsx').write_bytes(office_files.OLE + b'\0' * 100)  # a password-protected file is left alone
        self.assertEqual(office_files.problems(self.dir / 'locked.xlsx'), [])

    def test_pdfs(self):
        (self.dir / 'a.pdf').write_bytes(b'<html>not a pdf</html>')
        self.assertEqual(office_files.problems(self.dir / 'a.pdf'), ['is not a PDF'])
        (self.dir / 'b.pdf').write_bytes(b'%PDF-1.7\n1 0 obj\n')
        self.assertEqual(office_files.problems(self.dir / 'b.pdf'), ['is cut off (no end of file)'])

    def test_next_months_invoice_changes_only_its_cells(self):
        out = self.dir / 'work' / 'next.xlsx'
        office_files.set_cells(self.template, out, {'B1': '2025-03-31', 'B2': '42', 'B4': '250.25', 'A5': 'Hosting share - March & co'})
        self.assertEqual(office_files.problems(out), [])
        sheet = read(out, 'xl/worksheets/sheet1.xml')
        self.assertTrue(sheet.startswith(SHEET[:SHEET.index('<sheetData>')]), 'the root, its namespaces and everything before the cells stay as they were')
        self.assertIn('<c r="B1" s="1"><v>45747</v></c>', sheet)  # a date keeps its date style
        self.assertIn('<c r="B2"><v>42</v></c>', sheet)
        self.assertIn('<c r="B4"><v>250.25</v></c><c r="D4"><f>B4*2</f></c>', sheet)  # last month's result goes: worked out on open
        self.assertIn('<row r="4">', sheet)
        self.assertRegex(sheet, r'</row><row r="5"><c r="A5" t="inlineStr"><is><t>Hosting share - March &amp; co</t></is></c></row></sheetData>')
        self.assertIn('fullCalcOnLoad="1"', read(out, 'xl/workbook.xml'))  # D4 shows 500.5 when it opens
        with zipfile.ZipFile(self.template) as a, zipfile.ZipFile(out) as b:
            for name in a.namelist():
                if name not in ('xl/worksheets/sheet1.xml', 'xl/workbook.xml'):
                    self.assertEqual(a.read(name), b.read(name), name)

    def test_text_numbers_and_new_cells_in_a_row(self):
        out = self.dir / 'next.xlsx'
        office_files.set_cells(self.template, out, {'C2': "'00042", 'A2': 'Invoice no.', 'B1': ''}, sheet='Invoice')
        sheet = read(out, 'xl/worksheets/sheet1.xml')
        self.assertIn('<c r="A2" t="inlineStr"><is><t>Invoice no.</t></is></c><c r="B2"><v>41</v></c><c r="C2" t="inlineStr"><is><t>00042</t></is></c>', sheet)
        self.assertIn('<c r="B1" s="1"/>', sheet)

    def test_what_set_cells_refuses(self):
        out = self.dir / 'next.xlsx'
        for values, sheet, said in (({'D4': '3'}, None, 'D4 has a formula'), ({'b2': '1'}, None, 'is not a cell like B2'),
                                    ({'B2': '1'}, 'Other', 'No sheet named Other; this workbook has Invoice'), ({}, None, 'at least one cell')):
            with self.assertRaises(ValueError) as caught:
                office_files.set_cells(self.template, out, values, sheet=sheet)
            self.assertIn(said, str(caught.exception))
        with self.assertRaises(ValueError):
            office_files.set_cells(self.template, self.dir / 'next.pdf', {'B2': '1'})
        self.assertFalse(out.exists())


class Attachments(unittest.TestCase):
    """The email next action refuses a file that would not open, and a working name the recipient would see."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.job = root / 'workspace/data/assistant-attachments/job1'
        self.notes = root / 'workspace/memory/assistant'
        self.job.mkdir(parents=True)
        self.notes.mkdir(parents=True)
        self.config = {'attachment_sources': [str(self.job.parent), str(self.notes)], 'attachment_dir': str(root / 'store')}

    def store(self, path):
        with mock.patch.object(next_actions.mail_attachments, 'open_root', return_value=None):
            return next_actions.store_attachments([str(path)], self.config)

    def test_a_sound_file_under_its_own_name(self):
        good = workbook(self.job / '2025-03 invoice Acme - 42.xlsx')
        self.assertEqual(self.store(good)[0]['name'], '2025-03 invoice Acme - 42.xlsx')

    def test_a_broken_workbook_is_refused(self):
        root = ElementTree.fromstring(SHEET.encode())
        broken = workbook(self.job / 'invoice 42.xlsx', dict(PARTS, **{'xl/worksheets/sheet1.xml': ElementTree.tostring(root, encoding='unicode')}))
        with self.assertRaises(ValueError) as caught:
            self.store(broken)
        self.assertIn('invoice 42.xlsx would not open', str(caught.exception))
        self.assertIn('assistant xlsx-set', str(caught.exception))

    def test_a_working_name_is_refused(self):
        pdf = self.notes / '250402-acme-march-42.pdf'
        pdf.write_bytes(b'%PDF-1.4\n%%EOF\n')
        with mock.patch.object(office_files, 'pdf_problems', return_value=[]), self.assertRaises(ValueError) as caught:
            self.store(pdf)
        self.assertIn('250402-acme-march-42.pdf is a working name', str(caught.exception))
        named = self.notes / 'Acme plan.md'  # memory/assistant itself is fine; only the yymmdd- working names are not
        named.write_text('# Plan\n')
        self.assertEqual(self.store(named)[0]['name'], 'Acme plan.md')


if __name__ == '__main__':
    unittest.main()
