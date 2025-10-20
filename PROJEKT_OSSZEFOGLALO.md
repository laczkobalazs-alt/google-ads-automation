# Google Ads Automation API - Projekt Összefoglaló

## Áttekintés

Sikeresen létrehoztunk egy átfogó **Google Ads adatelemző és automatizációs API szolgáltatást** Python nyelven, amely lehetővé teszi a Google Ads kampányok hatékony elemzését, optimalizálását és automatizálását. A projekt teljes mértékben működőképes és GitHub repository-ban elérhető.

**GitHub Repository**: [https://github.com/laczkobalazs-alt/google-ads-automation](https://github.com/laczkobalazs-alt/google-ads-automation)

## Főbb Funkciók

### 1. Adatelemzés

A rendszer részletes elemzési képességekkel rendelkezik, amelyek segítenek megérteni és optimalizálni a kampányok teljesítményét.

**Kampány teljesítmény elemzés** funkcióval azonosíthatók az alacsony ROAS-ú, magas CPA-jú vagy alacsony CTR-ű kampányok. Az elemzés automatikusan küszöbértékek alapján kategorizálja a kampányokat és ajánlásokat ad az optimalizáláshoz. A rendszer összefoglaló statisztikákat készít a teljes költségről, konverziókról és átlagos metrikákról.

**Kulcsszó teljesítmény elemzés** során a rendszer azonosítja a top teljesítő kulcsszavakat, amelyek a legtöbb konverziót generálják, valamint az alulteljesítőket, amelyek költenek de nem konvertálnak. Az alacsony Quality Score-ú kulcsszavak külön figyelmet kapnak, és a match type teljesítmény eloszlás is elemzésre kerül.

**Kampány összehasonlítás** lehetővé teszi különböző metrikák (ROAS, CTR, CPA) alapján a kampányok rangsorolását. A rendszer statisztikai elemzést végez átlag, medián és szórás számításával.

**Költségvetés elosztás optimalizálás** során a rendszer kiszámítja az optimális költségvetés elosztást a kampányok között, két fő cél alapján: konverziók maximalizálása vagy ROAS maximalizálása. A múltbeli teljesítmény alapján javaslatot tesz a költségvetés átcsoportosítására.

### 2. Automatizáció

Az automatizációs funkciók lehetővé teszik a kampányok önálló optimalizálását és folyamatos monitorozását.

**Bid optimalizálás** során szabályok hozhatók létre ROAS vagy CPA célok alapján. A rendszer automatikusan ajánlásokat ad a bid módosításokhoz a teljesítmény alapján, és történetet vezet az összes optimalizálási műveletről.

**Költségvetés optimalizálás** több kampány között osztja el optimálisan a rendelkezésre álló költségvetést. A teljesítmény alapú allokáció biztosítja, hogy a legjobban teljesítő kampányok több forráshoz jussanak.

**Riasztási rendszer** automatikusan figyeli a megadott metrikákat és riasztást küld, ha az értékek küszöb alá vagy fölé kerülnek. Teljesen konfigurálható küszöbértékekkel és feltételekkel működik, és támogatja a kampány-specifikus és globális riasztásokat is.

### 3. API Végpontok

A rendszer RESTful API-t biztosít az összes funkcióhoz, amely a következő kategóriákra oszlik:

**Campaigns** végpontok alatt található a kampányok listázása, teljesítmény lekérdezés dátum tartomány alapján, és részletes metrikák (impressions, clicks, CTR, CPC, conversions, ROAS).

**Keywords** végpontok lehetővé teszik a kulcsszó teljesítmény lekérdezést, Quality Score elemzést, és match type szerinti szűrést.

**Analytics** végpontok biztosítják a kampány és kulcsszó betekintéseket, kampány összehasonlítást, és költségvetés elosztási javaslatokat.

**Automation** végpontok alatt található a bid optimalizálási szabályok létrehozása és alkalmazása, költségvetés optimalizálási szabályok kezelése, riasztási szabályok létrehozása és ellenőrzése, valamint szabályok kezelése (CRUD műveletek) és automatizálási történet lekérdezése.

## Technológiai Stack

A projekt modern és bevált technológiákra épül:

**Python 3.11** biztosítja a fő programozási nyelvet, míg a **FastAPI** modern, gyors web framework-ként szolgál az API-khoz. A **Google Ads API** hivatalos integráció révén közvetlenül kapcsolódik a Google Ads rendszerhez.

Az adatfeldolgozást a **Pandas** és **NumPy** könyvtárak végzik, míg az **SQLAlchemy** opcionálisan elérhető az adattároláshoz. A **Loguru** gondoskodik a naplózásról és monitorozásról, a **Pydantic** pedig az adatvalidációról és sémákról.

## Projekt Struktúra

A projekt jól szervezett könyvtárstruktúrával rendelkezik:

```
google-ads-automation/
├── app/
│   ├── main.py              # FastAPI alkalmazás belépési pont
│   ├── config.py            # Konfigurációs beállítások
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/   # API végpontok
│   │       │   ├── campaigns.py
│   │       │   ├── keywords.py
│   │       │   ├── analytics.py
│   │       │   └── automation.py
│   │       └── models/      # Pydantic modellek
│   │           └── schemas.py
│   └── services/
│       ├── google_ads.py    # Google Ads API integráció
│       ├── analytics.py     # Elemzési szolgáltatások
│       └── automation.py    # Automatizációs szolgáltatások
├── docs/
│   └── API_DOCUMENTATION.md # Részletes API dokumentáció
├── requirements.txt         # Python függőségek
├── .env.example            # Környezeti változók példa
├── google-ads.yaml.example # Google Ads konfiguráció példa
└── README.md               # Projekt dokumentáció
```

## Telepítés és Használat

### Előfeltételek

A használathoz szükséges **Google Ads API hozzáférés**, amely a következőket foglalja magában:

- Google Ads Manager fiók létrehozása
- Developer Token megszerzése a Google Ads API Center-től
- OAuth2 credentials létrehozása a Google Cloud Console-on
- Google Ads API engedélyezése a projektben

### Gyors Kezdés

A projekt használatához először klónozd a repository-t:

```bash
git clone https://github.com/laczkobalazs-alt/google-ads-automation.git
cd google-ads-automation
```

Hozz létre virtuális környezetet:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
```

Telepítsd a függőségeket:

```bash
pip install -r requirements.txt
```

Konfiguráld a környezeti változókat:

```bash
cp .env.example .env
cp google-ads.yaml.example google-ads.yaml
# Szerkeszd a fájlokat a saját API hitelesítési adataiddal
```

Indítsd el az API-t:

```bash
uvicorn app.main:app --reload
```

Az API elérhető lesz a `http://localhost:8000` címen, az interaktív dokumentáció pedig a `http://localhost:8000/docs` címen.

## Használati Példák

### Kampány Teljesítmény Lekérdezése

```bash
curl -X GET "http://localhost:8000/api/v1/campaigns/performance?customer_id=1234567890&date_range=LAST_30_DAYS"
```

### Kampány Elemzés Betekintésekkel

```bash
curl -X GET "http://localhost:8000/api/v1/analytics/campaign-insights?customer_id=1234567890&min_roas=2.0&max_cpa=50.0"
```

### Bid Optimalizálási Szabály Létrehozása

```bash
curl -X POST "http://localhost:8000/api/v1/automation/bid-optimization/create" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "1234567890",
    "campaign_id": "987654321",
    "target_roas": 4.0,
    "enabled": true
  }'
```

### Riasztás Létrehozása

```bash
curl -X POST "http://localhost:8000/api/v1/automation/alert/create?customer_id=1234567890&metric=roas&threshold=2.0&condition=below"
```

## Következő Lépések

A projekt jelenleg működőképes alapot biztosít, de számos továbbfejlesztési lehetőség áll rendelkezésre:

**Éles használathoz** szükséges lépések közé tartozik a Google Ads API hozzáférés megszerzése és konfigurálása, OAuth2 hitelesítés implementálása az API biztonságához, valamint adatbázis integráció a történeti adatok tárolásához.

**Továbbfejlesztési lehetőségek** között szerepel a gépi tanulás alapú előrejelzések bevezetése, részletesebb riportok és vizualizációk készítése, webhook integráció külső rendszerekkel, multi-account kezelés támogatása, valamint dashboard UI fejlesztése a könnyebb használathoz.

**Automatizálási fejlesztések** terén érdemes lehet ütemezett automatikus futtatások beállítása, email/SMS értesítések integrálása, A/B tesztelés automatizálása, valamint szezonális optimalizálás implementálása.

## Támogatás és Dokumentáció

A projekt teljes dokumentációja elérhető a GitHub repository-ban:

- **README.md**: Általános projekt információk és telepítési útmutató
- **docs/API_DOCUMENTATION.md**: Részletes API dokumentáció
- **Interaktív dokumentáció**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc dokumentáció**: `http://localhost:8000/redoc`

## Összegzés

A Google Ads Automation API egy teljes körű megoldást nyújt a Google Ads kampányok kezelésére, amely egyesíti az adatelemzést, az automatizálást és a könnyű integrációt. A projekt moduláris felépítése lehetővé teszi a könnyű bővítést és testreszabást, míg a RESTful API biztosítja a rugalmas felhasználást különböző környezetekben.

A rendszer készen áll a használatra, és a megfelelő Google Ads API hitelesítési adatok beállítása után azonnal használható éles környezetben is. A jól dokumentált kód és az átlátható struktúra megkönnyíti a további fejlesztést és karbantartást.

---

**Készítette**: Manus AI  
**Dátum**: 2025. október 20.  
**Verzió**: 1.0.0

