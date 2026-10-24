# ☁️ MemFlow Hub — колоды сообщества

Каталог готовых колод для [MemFlow](https://uwsqq.github.io/memflow/) (spaced repetition, FSRS-17).
Скачивай в один клик или публикуй свои колоды — они сразу доступны всем.

**🔗 Открыть: [uwsqq.github.io/memflow-hub](https://uwsqq.github.io/memflow-hub/)**

## Как скачать колоду
Кнопка **«➕ В MemFlow»** на карточке колоды — колода автоматически добавится в приложение
(откроется сайт MemFlow с параметром `#url=…` и импортирует JSON).

## Как опубликовать колоду
1. Открой [хаб](https://uwsqq.github.io/memflow-hub/) → секция **«📤 Публиковать колоду»**.
2. Вставь ссылку `#deck=…` из кнопки «Поделиться» в MemFlow (или JSON `{"name":…,"cards":[…]}`).
3. Нажми «Открыть GitHub с готовым issue» — бот опубликует колоду автоматически (Issue → Action → коммит → сайт обновляется).

Ограничения: до 500 карточек, `front`/`back` ≤ 300 символов, картинки только по http(s).

## Добавить колоду вручную (PR)
Положи `decks/<slug>.json` (`{"name","author","date","cards":[{"front","back","tags"?}]}`)
и перегенерируй `catalog.json` (или открой issue — бот сделает сам).

## Лицензия
Все колоды — [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/), если автор не указал иное.
