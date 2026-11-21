#!/usr/bin/env python3
"""Copy a skill's references/BIBLIOGRAPHY.md into catalog/descriptions.json.

Reads the numbered entries ("1. Author. *Title*. Publisher, 2011. ISBN ... **V**. ...")
and replaces the skill's "bibliografia" list, so the catalog never drifts from the file.
conferida = status V (ISBN matched) or P (official page read). Section headings set the type.
Usage: python3 scripts/bib-to-catalog.py <skill> [<skill> ...]   (prints counts; --dry-run to only print)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def kind(heading):
    h = heading.lower()
    if 'vendor' in h or 'industry' in h or 'fornecedor' in h:
        return 'fornecedor'
    if 'book' in h:
        return 'livro'
    if any(w in h for w in ('law', 'legal', 'regulat', 'statute', 'standard')):
        return 'norma/lei'
    if any(w in h for w in ('official', 'documentation', 'platform', 'docs')):
        return 'doc oficial'
    if any(w in h for w in ('article', 'paper', 'stud', 'research', 'method', 'academic')):
        return 'artigo'
    return 'outro'


def parse(text):
    out, sect = [], 'outro'
    for line in text.splitlines():
        if line.startswith('#'):
            sect = kind(line)
            continue
        m = re.match(r'^\s*\d+\.\s+(.*)', line)
        if not m:
            continue
        body = m.group(1)
        st = re.search(r'\*\*([VPSU])\b', body)
        status = st.group(1) if st else 'U'
        t = re.search(r'\*([^*]+)\*', body.replace('**', '\x00\x00'))
        q = re.search(r'"([^"]+)"', body)
        first = min([x.start() for x in (t, q) if x] or [len(body)])
        if t and (not q or t.start() <= q.start()):
            title, author = t.group(1), body[:t.start()]
        elif q:
            title, author = q.group(1), body[:q.start()]
        else:
            title = re.split(r'\.\s+(?=https?://|\*\*|ISBN)', body)[0]
            author = ''
        author = author.strip().rstrip('.,').strip()
        title = title.replace('\x00', '').strip()
        year = re.search(r'\b(19|20)\d\d\b', body[first:] if author else body)
        link = re.search(r'ISBN[ :]*[\dXx-]{10,17}|DOI [^\s,;]+|https?://[^\s)]+', body)
        typ = sect
        if sect == 'outro' and re.search(r'ISBN', body):
            typ = 'livro'
        out.append({'autor': author or '(sem autor indicado)', 'titulo': title[:200],
                    'ano': year.group(0) if year else '',
                    'link': link.group(0).rstrip('.,') if link else '',
                    'tipo': typ, 'conferida': status in 'VP', 'status': status})
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry-run' in sys.argv
    path = os.path.join(ROOT, 'catalog', 'descriptions.json')
    desc = json.load(open(path))
    for name in args:
        bib = parse(open(os.path.join(ROOT, 'skills', name, 'references', 'BIBLIOGRAPHY.md')).read())
        entry = next(s for s in desc['skills'] if s['name'] == name)
        if not bib:
            print(f'{name}: no numbered entries found, catalog left unchanged (use the numbered V/P/S/U format)')
            continue
        entry['bibliografia'] = bib
        c = {k: sum(b['status'] == k for b in bib) for k in 'VPSU'}
        print(f'{name}: {len(bib)} fontes, ' + ', '.join(f'{k} {v}' for k, v in c.items()))
        if dry:
            for b in bib:
                print('  ', b['status'], b['tipo'], '|', b['autor'][:40], '|', b['titulo'][:60], '|', b['ano'], '|', b['link'][:50])
    if not dry:
        json.dump(desc, open(path, 'w'), ensure_ascii=False, indent=1)
        open(path, 'a').write('\n')


if __name__ == '__main__':
    main()
