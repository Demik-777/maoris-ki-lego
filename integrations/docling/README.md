# Docling — проверка документов для MDL

- Upstream: https://github.com/docling-project/docling
- Source license according to GitHub API (2026-11-08): MIT; stars: 70 277.
- Назначение: извлекать структуру PDF/таблиц/сканов для Maoris Back Office.
- Статус: **README reviewed, not installed / not run**.

## Изолированная установка для тестового окружения

```bash
python -m venv .venv-docling
. .venv-docling/bin/activate
python -m pip install --upgrade pip
python -m pip install docling
python -c "from docling.document_converter import DocumentConverter; print('import OK')"
```

Тяжёлые модели и OCR могут потребовать дополнительную память, дисковое место и загрузку весов. **Не использовать реальные счета, персональные данные или конфиденциальные договоры** в первоначальном тесте.

## Тест-кейсы

1. Текстовый PDF с 8 известными полями (дата, сумма, контрагент и пр.).
2. Табличный PDF с минимум 10 строками и 3 колонками.
3. Скан/фото на тестовых данных; проверить порядок чтения, кириллицу и немецкие умляуты.

Скрипт-проверка после установки (на заранее подготовленном `sample.pdf`):

```python
from docling.document_converter import DocumentConverter
doc = DocumentConverter().convert("sample.pdf")
print(doc.document.export_to_markdown()[:4000])
```

Записать долю распознанных полей, ошибки таблиц, секунды на файл, RAM и качество OCR. PASS = корректные существенные поля и таблицы на тестовом наборе. **Не подтверждено выполнением**.
