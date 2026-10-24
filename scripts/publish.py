# -*- coding: utf-8 -*-
"""Автопубликация колод MemFlow Hub из GitHub issues.
Env: ISSUE_TITLE, ISSUE_BODY, ISSUE_USER, ISSUE_NUM. Заголовок должен начинаться с [deck]."""
import json, os, re, sys, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECKS = os.path.join(ROOT, 'decks')
CATALOG = os.path.join(ROOT, 'catalog.json')

TRANSLIT = {
    'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e','ж':'zh','з':'z','и':'i','й':'y',
    'к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f',
    'х':'h','ц':'ts','ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya'
}

def slugify(name: str) -> str:
    s = ''.join(TRANSLIT.get(ch, ch) for ch in name.lower())
    s = re.sub(r'[^a-z0-9-]+', '-', s).strip('-')
    return (s[:40] or 'deck')

def sanitize(d: dict, author: str) -> dict:
    name = str(d.get('name') or 'Deck').strip()[:60] or 'Deck'
    raw_cards = d.get('cards')
    if not isinstance(raw_cards, list) or not raw_cards:
        raise ValueError('cards должен быть непустым массивом')
    if len(raw_cards) > 500:
        raw_cards = raw_cards[:500]
    cards = []
    for c in raw_cards:
        if not isinstance(c, dict):
            continue
        front, back = str(c.get('front') or '')[:300], str(c.get('back') or '')[:300]
        if not front.strip() or not back.strip():
            continue
        card = {'front': front, 'back': back}
        if c.get('type') in ('basic', 'input', 'cloze'):
            card['type'] = c['type']
        tags = c.get('tags')
        if isinstance(tags, list):
            clean = [str(t)[:40] for t in tags[:8] if str(t).strip()]
            if clean:
                card['tags'] = clean
        img = str(c.get('img') or '')
        if img.startswith('http') and len(img) <= 300:
            card['img'] = img
        cards.append(card)
    if not cards:
        raise ValueError('нет ни одной валидной карточки (нужны front и back)')
    return {'name': name, 'author': author,
            'date': datetime.date.today().isoformat(),
            'cards': cards}

def rebuild_catalog():
    entries = []
    for f in sorted(glob.glob(os.path.join(DECKS, '*.json'))):
        try:
            with open(f, encoding='utf-8') as fh:
                d = json.load(fh)
            tags = []
            for c in d.get('cards', []):
                for tg in c.get('tags', []):
                    if tg not in tags:
                        tags.append(tg)
                    if len(tags) >= 2:
                        break
                if len(tags) >= 2:
                    break
            entries.append({'file': 'decks/' + os.path.basename(f),
                            'name': d.get('name', '?'),
                            'cards': len(d.get('cards', [])),
                            'author': d.get('author', ''),
                            'date': d.get('date', ''),
                            'tags': tags})
        except Exception:
            continue
    entries.sort(key=lambda x: (x['date'] or '', x['name']), reverse=True)
    with open(CATALOG, 'w', encoding='utf-8') as fh:
        json.dump(entries, fh, ensure_ascii=False, indent=1)
    return len(entries)

def main():
    title = os.environ.get('ISSUE_TITLE', '')
    body = os.environ.get('ISSUE_BODY', '') or ''
    user = os.environ.get('ISSUE_USER', 'anon')
    num = os.environ.get('ISSUE_NUM', '0')
    if not title.startswith('[deck]'):
        print('не issue колоды — пропускаю')
        return
    m = re.search(r'```json\s*(\{.*?\})\s*```', body, re.S) or re.search(r'```\s*(\{.*?\})\s*```', body, re.S)
    raw = m.group(1) if m else body
    try:
        d = json.loads(raw)
    except Exception:
        print('::error::в теле issue нет валидного JSON-блока'); sys.exit(1)
    try:
        deck = sanitize(d, user)
    except ValueError as e:
        print('::error::' + str(e)); sys.exit(1)

    slug = slugify(deck['name'])
    path = os.path.join(DECKS, slug + '.json')
    if os.path.exists(path):
        try:
            with open(path, encoding='utf-8') as fh:
                old = json.load(fh)
            if old.get('author') != user:
                path = os.path.join(DECKS, '{}-i{}.json'.format(slug, num))
        except Exception:
            pass
    os.makedirs(DECKS, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(deck, fh, ensure_ascii=False, indent=1)
    total = rebuild_catalog()
    print('опубликована {}: {} карточек; в каталоге {} колод'.format(
        os.path.basename(path), len(deck['cards']), total))

if __name__ == '__main__':
    main()
