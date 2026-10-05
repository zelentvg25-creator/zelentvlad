# Персональний блог

## Запуск локально

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata app_blog/article_data.json
python manage.py runserver
```

Після запуску сайт доступний за адресою `http://127.0.0.1:8000/`, а панель адміністрування — `http://127.0.0.1:8000/admin/`.

Початкові категорії та статті збережені у `app_blog/article_data.json`. Локальна база даних і облікові записи адміністратора не додаються до репозиторію. Створіть адміністратора командою `python manage.py createsuperuser`.
