# We Are Sales Force

Satış gücü yönetimi için açık başvuru kaynağı — **www.wearesalesforce.com**

- `content/` – Rehber modülleri, yazılar, sözlük ve hakkında sayfası (TR/EN, Markdown + YAML)
- `tools.py`, `assets/tools.js` – Etkileşimli araçlar
- `build.py` – Statik site üreticisi → `dist/`
- `docs/` – GitHub Pages'in yayınladığı derlenmiş site (`build.py` çıktısının kopyası)

## Güncelleme

```bash
pip install markdown pyyaml
python3 build.py && rm -rf docs && cp -r dist docs
```

Hazırlayan: Bora Özkalp
