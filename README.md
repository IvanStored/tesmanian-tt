# Python Automation Masters TT

Сайт: https://www.tesmanian.com/

Що треба реалізувати:

1. Скрипт, який скрапить сайт 24/7 з інтервалом у 15 секунд.
2. Логін має бути один раз (або коли отримуємо unauthirized error), щоб нас не запідозрили у спамі
3. На виході мають бути тільки нові результати (у порівняня з попередньою перевіркою 15 сек тому) у телеграм канал. Відсилати потрібно title статті і посилання на неї.


## Installation:


```sh
git clone https://github.com/IvanStored/tesmanian-tt.git
cd tesmanian-tt
python -m venv venv
venv/scripts/activate
pip install -r requirements.txt
docker compose up --build
```