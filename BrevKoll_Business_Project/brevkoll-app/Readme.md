# Myndighetsbrev ✉️

Helps immigrants in Sweden understand letters from Försäkringskassan, Arbetsförmedlingen,
Migrationsverket and other authorities. Upload a PDF/photo or paste text → get a simple
summary, actions, deadlines, key Swedish terms and a full translation in 19 languages.

## Run locally

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...        # or put it in .streamlit/secrets.toml
streamlit run app.py
```

`.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

## How it works
- PDFs and images go straight to Claude (reads scanned letters, no separate OCR needed).
- One call returns structured JSON: sender, summary, actions, deadlines, terms, contact, full translation.
- RTL languages (Arabic, Dari, Persian, Pashto, Sorani) render right-to-left.

## Before going public
- **GDPR**: letters contain personnummer and sensitive data (health, migration). Don't log or store
  uploads, write a privacy notice, and check your API provider's data-retention terms.
- **Not legal advice**: keep the disclaimer; deadlines (e.g. överklagande) matter a lot.
- **Ideas for v2**: text-to-speech of the summary (many users read poorly in any language),
  calendar export for deadlines, "draft a reply in Swedish", Swedish UI text translated too.
