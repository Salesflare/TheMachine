"""Office files a preparation makes or sends (docs/usage.md, office-check and xlsx-set): changed so they stay valid, and checked before they leave.

Excel, Word and PowerPoint files are zip packages of XML parts. Reading a part into an XML library and writing it back
renames or drops namespace declarations that Excel needs (the mc:Ignorable prefixes such as x14ac), and Excel then calls
the file corrupt while LibreOffice still opens it. So:

- set_cells changes an .xlsx by editing only the text of the cells it sets; every other byte of the package stays as it
  was. A cell keeps its style (a date stays a date); formulas are never overwritten and recalculate when the file opens.
- problems lists what would make a file fail to open: the package, its XML, its declared prefixes, the parts its content
  types and relationships name; for a PDF its header and end, and pdfinfo when it is installed.

`assistant xlsx-set` and `assistant office-check` run these; an email attachment that has problems is refused
(next_actions.store_attachments)."""
import datetime as dt
import io
import posixpath
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree


OOXML = ('.xlsx', '.xlsm', '.xltx', '.xltm', '.docx', '.docm', '.dotx', '.dotm', '.pptx', '.pptm', '.potx', '.potm')
OLE = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'  # an encrypted (password) Office file or an old .xls/.doc: not a zip, left as is
_MC = re.compile(rb'\bmc:(?:Ignorable|ProcessContent|MustUnderstand)="([^"]*)"')
_PROBLEMS_MAX = 8


def problems(path, data=None):
    """What would keep this file from opening, in plain words; [] when it looks sound (or is a kind not checked here).
    data: its bytes when they are not the file's own (an attachment kept sealed on disk)."""
    path = Path(path)
    if data is None:
        try:
            data = path.read_bytes()
        except OSError as error:
            return [f'cannot be read ({error.strerror or error})']
    if not data:
        return ['is empty']
    suffix = path.suffix.lower()
    if suffix in OOXML:
        return [] if data.startswith(OLE) else package_problems(data)
    if suffix == '.pdf':
        return pdf_problems(path, data)
    return []


def package_problems(data):
    from connectors.docs import parse_xml  # noqa: PLC0415 - refuses any DTD: a file from someone else's email is untrusted
    found = []
    try:
        package = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile:
        return ['is not a valid Office file (not a zip package)']
    with package:
        names = set(package.namelist())
        bad = package.testzip()
        if bad:
            return [f'has a damaged part ({bad})']
        for required in ('[Content_Types].xml', '_rels/.rels'):
            if required not in names:
                found.append(f'misses {required}')
        for name in sorted(names):
            if not name.endswith(('.xml', '.rels')):
                continue
            raw = package.read(name)
            try:
                parse_xml(raw)
            except ElementTree.ParseError as error:
                found.append(f'{name} is not valid XML ({error})')
                continue
            for prefixes in _MC.findall(raw):
                for prefix in prefixes.split():
                    if b'xmlns:' + prefix + b'=' not in raw:
                        found.append(f'{name} names the prefix {prefix.decode()} without declaring it (Excel, Word and PowerPoint refuse this)')
            if re.search(rb'<ns\d+:', raw):
                found.append(f'{name} was rewritten by an XML library (ns0: prefixes); make the file again from the original')
        if '[Content_Types].xml' in names:
            try:
                types = parse_xml(package.read('[Content_Types].xml'))
                for override in types:
                    part = (override.get('PartName') or '').lstrip('/')
                    if override.tag.endswith('Override') and part and part not in names:
                        found.append(f'lists a part that is missing ({part})')
            except ElementTree.ParseError:
                pass
        for rels in sorted(n for n in names if n.endswith('.rels')):
            try:
                root = parse_xml(package.read(rels))
            except ElementTree.ParseError:
                continue
            base = posixpath.dirname(posixpath.dirname(rels))
            for rel in root:
                target = rel.get('Target') or ''
                if rel.get('TargetMode') == 'External' or not target or '://' in target:
                    continue
                part = posixpath.normpath(target.lstrip('/') if target.startswith('/') else posixpath.join(base, target))
                if part not in names:
                    found.append(f'{rels} points to a missing part ({part})')
    return found[:_PROBLEMS_MAX]


def pdf_problems(path, data):
    if not data.startswith(b'%PDF-'):
        return ['is not a PDF']
    if b'%%EOF' not in data[-2048:]:
        return ['is cut off (no end of file)']
    tool = shutil.which('pdfinfo')
    if tool:
        try:
            with tempfile.NamedTemporaryFile(suffix='.pdf') as copy:
                copy.write(data)
                copy.flush()
                done = subprocess.run([tool, copy.name], capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired):
            return []
        if done.returncode:
            return [f'does not open ({(done.stderr or "pdfinfo failed").strip().splitlines()[-1][:200]})']
    return []


# --- changing cells in an .xlsx --------------------------------------------------------------------------------------

_REF = re.compile(r'^([A-Z]{1,3})([1-9][0-9]{0,6})$')
_NUMBER = re.compile(r'^-?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][-+]?[0-9]+)?$')
_DATE = re.compile(r'^([0-9]{4})-([0-9]{2})-([0-9]{2})$')
_FORMULA_RESULT = re.compile(r'(<f\b[^>]*/>|<f\b[^>]*>[^<]*</f>)<v>[^<]*</v>')
_CALC_AFTER = ('oleSize', 'customWorkbookViews', 'pivotCaches', 'smartTagPr', 'smartTagTypes', 'webPublishing',
               'fileRecoveryPr', 'webPublishObjects', 'extLst')


def _col(letters):
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n


def _escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def _sheet_part(package, sheet):
    """The worksheet part for a sheet name (None: the first sheet)."""
    workbook = package.read('xl/workbook.xml').decode('utf-8')
    sheets = re.findall(r'<sheet\b[^>]*/?>', workbook)
    if not sheets:
        raise ValueError('This workbook has no sheets')
    chosen = sheets[0]
    if sheet is not None:
        chosen = next((s for s in sheets if re.search(r'\bname="' + re.escape(_escape(sheet)) + '"', s)), None)
        if chosen is None:
            names = [re.search(r'\bname="([^"]*)"', s).group(1) for s in sheets]
            raise ValueError(f'No sheet named {sheet}; this workbook has {", ".join(names)}')
    rid = re.search(r'\br:id="([^"]+)"', chosen) or re.search(r'\b\w+:id="([^"]+)"', chosen)
    rels = package.read('xl/_rels/workbook.xml.rels').decode('utf-8')
    rel = next((r for r in re.findall(r'<Relationship\b[^>]*/?>', rels) if f'Id="{rid.group(1)}"' in r), None) if rid else None
    target = re.search(r'\bTarget="([^"]+)"', rel or '')
    if not target:
        raise ValueError('Cannot find that sheet in the workbook')
    t = target.group(1)
    return t.lstrip('/') if t.startswith('/') else posixpath.normpath(posixpath.join('xl', t))


def _cell_xml(ref, attrs, value, base):
    """A cell with this value, keeping its other attributes (its style) but not its old type."""
    attrs = re.sub(r'\s+t="[^"]*"', '', attrs)
    text = str(value)
    if text == '':
        return f'<c r="{ref}"{attrs}/>'
    if text.startswith("'"):
        text = text[1:]
    elif _NUMBER.match(text):
        return f'<c r="{ref}"{attrs}><v>{text}</v></c>'
    elif (d := _DATE.match(text)):
        serial = (dt.date(int(d[1]), int(d[2]), int(d[3])) - base).days
        return f'<c r="{ref}"{attrs}><v>{serial}</v></c>'
    space = ' xml:space="preserve"' if text != text.strip() or '\n' in text else ''
    return f'<c r="{ref}"{attrs} t="inlineStr"><is><t{space}>{_escape(text)}</t></is></c>'


def _set_cell(xml, ref, value, base):
    letters, row = _REF.match(ref).groups()
    rows = re.compile(r'<row\b[^>]*?\br="' + row + r'"[^>]*?(?:/>|>.*?</row>)', re.S)
    found = rows.search(xml)
    if not found:  # a new row, in its place among the others
        data = re.search(r'<sheetData\s*/>|<sheetData\b[^>]*>', xml)
        if not data:
            raise ValueError('This sheet has no cell data')
        new_row = f'<row r="{row}">{_cell_xml(ref, "", value, base)}</row>'
        if data.group(0).endswith('/>'):
            return xml[:data.start()] + f'<sheetData>{new_row}</sheetData>' + xml[data.end():]
        at = xml.index('</sheetData>', data.end())
        for later in re.finditer(r'<row\b[^>]*?\br="([0-9]+)"', xml[data.end():at]):
            if int(later.group(1)) > int(row):
                at = data.end() + later.start()
                break
        return xml[:at] + new_row + xml[at:]
    row_xml = found.group(0)
    if row_xml.endswith('/>'):
        row_xml = row_xml[:-2] + '></row>'
    cell = re.search(r'<c\s[^>]*?\br="' + ref + r'"([^>]*?)(?:/>|>(.*?)</c>)', row_xml, re.S)
    if cell:
        attrs = re.sub(r'\s*\br="' + ref + '"', '', cell.group(0)[2:cell.group(0).index('>')].rstrip('/'))
        attrs = (' ' + attrs.strip()) if attrs.strip() else ''
        if cell.group(2) and '<f' in cell.group(2):
            raise ValueError(f'{ref} has a formula; set the cells it uses instead, and it recalculates when the file opens')
        row_xml = row_xml[:cell.start()] + _cell_xml(ref, attrs, value, base) + row_xml[cell.end():]
    else:
        at = row_xml.index('</row>')
        for other in re.finditer(r'<c\s[^>]*?\br="([A-Z]+)[0-9]+"', row_xml):
            if _col(other.group(1)) > _col(letters):
                at = other.start()
                break
        row_xml = row_xml[:at] + _cell_xml(ref, '', value, base) + row_xml[at:]
    return xml[:found.start()] + row_xml + xml[found.end():]


def _recalculate_on_open(workbook):
    """Formulas show their new results when the file opens (Excel, LibreOffice): fullCalcOnLoad on calcPr."""
    calc = re.search(r'<calcPr\b[^>]*?/?>', workbook)
    if calc:
        tag = re.sub(r'\s+fullCalcOnLoad="[^"]*"', '', calc.group(0))
        tag = tag[:-2].rstrip() + ' fullCalcOnLoad="1"/>' if tag.endswith('/>') else tag[:-1].rstrip() + ' fullCalcOnLoad="1">'
        return workbook[:calc.start()] + tag + workbook[calc.end():]
    at = workbook.rindex('</workbook>')
    for name in _CALC_AFTER:
        m = re.search(r'<' + name + r'\b', workbook)
        if m:
            at = m.start()
            break
    return workbook[:at] + '<calcPr fullCalcOnLoad="1"/>' + workbook[at:]


def set_cells(source, target, values, sheet=None):
    """Write a copy of the .xlsx source to target with these cells set ({'B2': '2025-03-31', 'C3': 'Text', 'D4': '12.5'}).

    A number stays a number, YYYY-MM-DD becomes a date (the cell's own format shows it), a leading ' keeps the rest as
    text, and '' clears the cell. Only the cell text changes; everything else in the package stays byte for byte, and the
    copy is checked (problems) before it is kept. ValueError says what is wrong."""
    source, target = Path(source), Path(target)
    if source.suffix.lower() not in ('.xlsx', '.xlsm', '.xltx', '.xltm') or target.suffix.lower() != source.suffix.lower():
        raise ValueError('xlsx-set changes an Excel file (.xlsx) into a new file of the same kind')
    if not values:
        raise ValueError('Give at least one cell, like B2=2025-03-31')
    for ref in values:
        if not _REF.match(ref):
            raise ValueError(f'{ref} is not a cell like B2')
    try:
        package = zipfile.ZipFile(source)
    except (OSError, zipfile.BadZipFile):
        raise ValueError(f'{source.name} is not an Excel file that can be opened') from None
    with package:
        part = _sheet_part(package, sheet)
        xml = package.read(part).decode('utf-8')
        workbook = package.read('xl/workbook.xml').decode('utf-8')
        base = dt.date(1904, 1, 1) if re.search(r'\bdate1904="(?:1|true)"', workbook) else dt.date(1899, 12, 30)
        for ref, value in values.items():
            xml = _set_cell(xml, ref, value, base)
        sheets = {n: package.read(n).decode('utf-8') for n in package.namelist() if re.fullmatch(r'xl/worksheets/[^/]+\.xml', n)}
        sheets[part] = xml
        # A formula's stored result is last month's: drop it so it is worked out again when the file opens. Excel does
        # that for fullCalcOnLoad; LibreOffice (and so a PDF made with it) only for a formula without a stored result.
        fresh = {n: _FORMULA_RESULT.sub(r'\1', text) for n, text in sheets.items()}
        replace = {n: text.encode('utf-8') for n, text in fresh.items() if n == part or text != sheets[n]}
        if any(text != sheets[n] for n, text in fresh.items()):
            replace['xl/workbook.xml'] = _recalculate_on_open(workbook).encode('utf-8')
        out = io.BytesIO()
        with zipfile.ZipFile(out, 'w') as copy:
            for info in package.infolist():
                copy.writestr(info, replace.get(info.filename, package.read(info)), compress_type=info.compress_type)
    data = out.getvalue()
    found = package_problems(data)
    if found:
        raise ValueError(f'The changed file would not open: {"; ".join(found)}')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return target
