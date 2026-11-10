from app.core.config import get_settings
from pathlib import Path
from app.services.ingestion import load_file
settings = get_settings()

print(f"App Name: {settings.app_name}")
print(f"App Environment: {settings.openai_api_key}")

#Test code
#docs = load_file(Path("data/sample_kb/company_it_handbook.md"))
#print(docs)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)