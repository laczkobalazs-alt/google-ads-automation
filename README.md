# Google Ads Automation API

Egy átfogó Google Ads adatelemző és automatizációs API szolgáltatás, amely lehetővé teszi a kampányok hatékony elemzését, optimalizálását és automatizálását.

## Funkciók

### Adatelemzés
- **Kampány teljesítmény elemzés**: Részletes riportok a kampányok teljesítményéről
- **Kulcsszó teljesítmény elemzés**: Kulcsszavak hatékonyságának mérése és értékelése
- **Költségvetés elemzés**: ROI és költséghatékonyság elemzése
- **Trend elemzés**: Időbeli trendek és minták felismerése

### Automatizáció
- **Automatikus ajánlat (bid) optimalizálás**: Intelligens ajánlat kezelés a jobb eredményekért
- **Költségvetés optimalizálás**: Automatikus költségvetés allokáció
- **Hirdetés szöveg A/B tesztelés**: Automatizált tesztelés és optimalizálás
- **Riasztások és értesítések**: Automatikus figyelmeztetések teljesítmény változásokról

## Technológiai stack

- **Python 3.11+**: Fő programozási nyelv
- **FastAPI**: Modern, gyors web framework API-khoz
- **Google Ads API**: Hivatalos Google Ads integráció
- **Pandas**: Adatelemzés és feldolgozás
- **SQLite/PostgreSQL**: Adattárolás és történeti adatok

## Telepítés

### Előfeltételek

1. **Python 3.11 vagy újabb** telepítése
2. **Google Ads API hozzáférés** beállítása:
   - Google Ads Manager fiók
   - Developer Token
   - OAuth2 hitelesítési adatok

### Lépések

1. Repository klónozása:
```bash
git clone https://github.com/laczkobalazs-alt/google-ads-automation.git
cd google-ads-automation
```

2. Virtuális környezet létrehozása:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# vagy
venv\Scripts\activate  # Windows
```

3. Függőségek telepítése:
```bash
pip install -r requirements.txt
```

4. Környezeti változók beállítása:
```bash
cp .env.example .env
# Szerkeszd a .env fájlt a saját API hitelesítési adataiddal
```

5. API indítása:
```bash
uvicorn app.main:app --reload
```

Az API elérhető lesz a `http://localhost:8000` címen.

## Konfiguráció

### Google Ads API beállítása

1. **Developer Token megszerzése**:
   - Lépj be a [Google Ads API Center](https://ads.google.com/aw/apicenter)-be
   - Kérj Developer Token-t (ez eltarthat néhány napig)

2. **OAuth2 credentials létrehozása**:
   - Menj a [Google Cloud Console](https://console.cloud.google.com/)-ra
   - Hozz létre egy új projektet
   - Engedélyezd a Google Ads API-t
   - Hozz létre OAuth2 credentials-t (Desktop app típus)
   - Töltsd le a `credentials.json` fájlt

3. **Konfiguráció**:
   - Másold a `google-ads.yaml.example` fájlt `google-ads.yaml` névre
   - Töltsd ki a szükséges adatokat

## API Dokumentáció

Az API indítása után a dokumentáció elérhető:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Használat

### Példa: Kampány teljesítmény lekérdezése

```bash
curl -X GET "http://localhost:8000/api/v1/campaigns/performance?customer_id=1234567890&date_range=LAST_30_DAYS"
```

### Példa: Automatikus bid optimalizálás bekapcsolása

```bash
curl -X POST "http://localhost:8000/api/v1/automation/bid-optimization" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "1234567890",
    "campaign_id": "987654321",
    "target_roas": 4.0,
    "enabled": true
  }'
```

## Projekt struktúra

```
google-ads-automation/
├── app/
│   ├── main.py              # FastAPI alkalmazás belépési pont
│   ├── config.py            # Konfigurációs beállítások
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/   # API végpontok
│   │   │   └── models/      # Pydantic modellek
│   ├── services/
│   │   ├── google_ads.py    # Google Ads API integráció
│   │   ├── analytics.py     # Elemzési szolgáltatások
│   │   └── automation.py    # Automatizációs szolgáltatások
│   └── utils/               # Segédfunkciók
├── tests/                   # Tesztek
├── docs/                    # Dokumentáció
├── requirements.txt         # Python függőségek
├── .env.example            # Környezeti változók példa
├── google-ads.yaml.example # Google Ads konfiguráció példa
└── README.md               # Ez a fájl
```

## Fejlesztés alatt

Ez a projekt aktív fejlesztés alatt áll. Az alábbi funkciók hamarosan érkeznek:
- [ ] Gépi tanulás alapú előrejelzések
- [ ] Részletesebb riportok és vizualizációk
- [ ] Webhook integráció
- [ ] Multi-account kezelés
- [ ] Dashboard UI

## Licenc

MIT License

## Kapcsolat

Ha kérdésed van vagy segítségre van szükséged, nyiss egy issue-t a GitHub-on.

