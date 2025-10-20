# Google Ads Automation API - Használati Útmutató

Ez az útmutató bemutatja, hogy mit tudsz csinálni a telepítés után, hogyan használd az API-t, és hogyan hozd ki belőle a legtöbbet.

---

## 📋 Tartalom

1. [Az API indítása](#1-az-api-indítása)
2. [Az interaktív dokumentáció használata](#2-az-interaktív-dokumentáció-használata)
3. [Első lépések - Adatok lekérdezése](#3-első-lépések---adatok-lekérdezése)
4. [Kampányok elemzése](#4-kampányok-elemzése)
5. [Automatizálás beállítása](#5-automatizálás-beállítása)
6. [Riasztások létrehozása](#6-riasztások-létrehozása)
7. [Költségvetés optimalizálás](#7-költségvetés-optimalizálás)
8. [Haladó használat](#8-haladó-használat)
9. [Tippek és trükkök](#9-tippek-és-trükkök)

---

## 1. Az API Indítása

### Minden alkalommal, amikor használni szeretnéd az API-t:

**1. Nyisd meg a terminált/parancssort**

**2. Lépj be a projekt mappába:**

**Windows:**
```cmd
cd %USERPROFILE%\Documents\google-ads-automation
```

**Mac/Linux:**
```bash
cd ~/Documents/google-ads-automation
```

**3. Aktiváld a virtuális környezetet:**

**Windows:**
```cmd
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

Látnod kell a `(venv)` feliratot a parancssor elején.

**4. Indítsd el az API-t:**

```bash
uvicorn app.main:app --reload
```

**5. Várd meg, amíg elindul:**

Látnod kell:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**6. Most már használhatod az API-t!**

- API: http://localhost:8000
- Dokumentáció: http://localhost:8000/docs

### Az API leállítása:

- Nyomd meg: **CTRL + C** a terminálban
- Vagy csak zárd be a terminál ablakot

---

## 2. Az Interaktív Dokumentáció Használata

Az API-nak van egy beépített, interaktív dokumentációs felülete, ahol minden végpontot ki tudsz próbálni közvetlenül a böngészőből!

### Hogyan használd:

**1. Nyisd meg a böngésződet:**
```
http://localhost:8000/docs
```

**2. Látnod fogsz 4 fő kategóriát:**
- 🟢 **Campaigns** - Kampányok kezelése
- 🔵 **Keywords** - Kulcsszavak elemzése
- 🟡 **Analytics** - Elemzési funkciók
- 🟣 **Automation** - Automatizálás

**3. Próbálj ki egy végpontot:**

Például a **GET /health** végpontot:

1. Kattints a **GET /health** sorra
2. Kattints a **"Try it out"** gombra
3. Kattints az **"Execute"** gombra
4. Görgess le, és látni fogod a választ!

**Példa válasz:**
```json
{
  "status": "healthy",
  "google_ads_configured": true
}
```

Ha `"google_ads_configured": true`, akkor minden rendben van! ✅

Ha `"google_ads_configured": false`, akkor ellenőrizd a `google-ads.yaml` fájlt. ❌

---

## 3. Első Lépések - Adatok Lekérdezése

### 3.1. Kampányok Listázása

Ez a legegyszerűbb művelet - lekérdezed az összes kampányodat.

**A dokumentációs felületen:**

1. Keresd meg: **GET /api/v1/campaigns/list**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Írd be a **customer_id**-t
   - Ez a Google Ads ügyfél azonosítód
   - 10 számjegy, kötőjelek nélkül
   - Például: `1234567890`
5. Kattints az **"Execute"** gombra

**Példa válasz:**
```json
[
  {
    "id": 12345678,
    "name": "Tavaszi Akció",
    "status": "ENABLED",
    "channel_type": "SEARCH",
    "bidding_strategy": "TARGET_CPA",
    "budget": 100.0
  },
  {
    "id": 87654321,
    "name": "Nyári Kampány",
    "status": "PAUSED",
    "channel_type": "DISPLAY",
    "bidding_strategy": "MAXIMIZE_CONVERSIONS",
    "budget": 50.0
  }
]
```

**Mit látsz:**
- **id**: Kampány azonosító
- **name**: Kampány neve
- **status**: Állapot (ENABLED = aktív, PAUSED = szünetel)
- **channel_type**: Típus (SEARCH = keresési, DISPLAY = display)
- **bidding_strategy**: Ajánlati stratégia
- **budget**: Napi költségvetés

### 3.2. Kampány Teljesítmény Lekérdezése

Most nézzük meg, hogy teljesítenek a kampányaid!

**A dokumentációs felületen:**

1. Keresd meg: **GET /api/v1/campaigns/performance**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki:
   - **customer_id**: A Google Ads ügyfél azonosítód
   - **date_range**: Válassz időszakot (pl. `LAST_30_DAYS`)
   - **campaign_id**: Hagyd üresen (így minden kampányt lekérdez)
5. Kattints az **"Execute"** gombra

**Lehetséges date_range értékek:**
- `LAST_7_DAYS` - Utolsó 7 nap
- `LAST_30_DAYS` - Utolsó 30 nap
- `THIS_MONTH` - Ez a hónap
- `LAST_MONTH` - Múlt hónap
- `THIS_YEAR` - Ez az év

**Példa válasz:**
```json
[
  {
    "campaign_id": 12345678,
    "campaign_name": "Tavaszi Akció",
    "impressions": 15000,
    "clicks": 450,
    "ctr": 0.03,
    "average_cpc": 1.25,
    "cost": 562.50,
    "conversions": 25,
    "conversions_value": 2500.0,
    "cost_per_conversion": 22.50,
    "conversion_rate": 0.0556,
    "roas": 4.44
  }
]
```

**Mit jelentenek az értékek:**
- **impressions**: Hányszor jelent meg a hirdetésed
- **clicks**: Hányszor kattintottak rá
- **ctr**: Kattintási arány (clicks / impressions)
- **average_cpc**: Átlagos kattintási költség
- **cost**: Összköltség
- **conversions**: Konverziók száma
- **conversions_value**: Konverziók értéke
- **cost_per_conversion**: Egy konverzió költsége
- **conversion_rate**: Konverziós arány
- **roas**: Return on Ad Spend (megtérülés)

### 3.3. Kulcsszavak Teljesítménye

**A dokumentációs felületen:**

1. Keresd meg: **GET /api/v1/keywords/performance**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki:
   - **customer_id**: A Google Ads ügyfél azonosítód
   - **date_range**: `LAST_30_DAYS`
5. Kattints az **"Execute"** gombra

**Példa válasz:**
```json
[
  {
    "campaign_id": 12345678,
    "campaign_name": "Tavaszi Akció",
    "ad_group_id": 98765432,
    "ad_group_name": "Cipők",
    "keyword": "női cipő",
    "match_type": "BROAD",
    "impressions": 5000,
    "clicks": 150,
    "ctr": 0.03,
    "average_cpc": 1.20,
    "cost": 180.0,
    "conversions": 8,
    "conversions_value": 800.0,
    "quality_score": 7
  }
]
```

---

## 4. Kampányok Elemzése

Most jön az igazán hasznos rész! Az API automatikusan elemzi a kampányaidat és ajánlásokat ad.

### 4.1. Kampány Betekintések (Insights)

Ez a funkció automatikusan azonosítja a problémákat és lehetőségeket.

**A dokumentációs felületen:**

1. Keresd meg: **GET /api/v1/analytics/campaign-insights**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki:
   - **customer_id**: A Google Ads ügyfél azonosítód
   - **date_range**: `LAST_30_DAYS`
   - **min_roas**: `2.0` (minimum elvárt ROAS)
   - **max_cpa**: `50.0` (maximum elfogadható CPA)
   - **min_ctr**: `0.01` (minimum elvárt CTR)
5. Kattints az **"Execute"** gombra

**Példa válasz:**
```json
{
  "insights": [
    {
      "type": "low_roas",
      "severity": "warning",
      "message": "2 kampány ROAS értéke a küszöb (2.0) alatt van",
      "affected_campaigns": ["Nyári Kampány", "Őszi Akció"],
      "metric_value": 1.5
    },
    {
      "type": "high_cpa",
      "severity": "warning",
      "message": "1 kampány CPA értéke a küszöb (50.0) felett van",
      "affected_campaigns": ["Téli Kampány"],
      "metric_value": 65.0
    }
  ],
  "summary": {
    "total_campaigns": 5,
    "total_cost": 2500.0,
    "total_conversions": 100,
    "total_clicks": 5000,
    "total_impressions": 150000,
    "average_roas": 3.2,
    "average_ctr": 0.033,
    "average_cpc": 0.50
  },
  "recommendations": [
    {
      "type": "roas_optimization",
      "message": "Fontold meg az alacsony ROAS-ú kampányok költségvetésének csökkentését vagy optimalizálását",
      "campaigns": ["Nyári Kampány", "Őszi Akció"]
    }
  ]
}
```

**Mit kapsz:**
- **insights**: Automatikusan azonosított problémák
- **summary**: Összefoglaló statisztikák
- **recommendations**: Konkrét ajánlások

### 4.2. Kulcsszó Betekintések

Hasonló elemzés a kulcsszavakra.

**A dokumentációs felületen:**

1. Keresd meg: **GET /api/v1/analytics/keyword-insights**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki:
   - **customer_id**: A Google Ads ügyfél azonosítód
   - **date_range**: `LAST_30_DAYS`
   - **min_impressions**: `100` (csak azokat elemzi, amiknek legalább 100 megjelenésük volt)
5. Kattints az **"Execute"** gombra

**Mit kapsz:**
- **top_performers**: A 10 legjobban teljesítő kulcsszó
- **underperformers**: Kulcsszavak, amik költenek de nem konvertálnak
- **insights**: Automatikus elemzés (pl. alacsony Quality Score)

### 4.3. Kampányok Összehasonlítása

**A dokumentációs felületen:**

1. Keresd meg: **GET /api/v1/analytics/compare-campaigns**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki:
   - **customer_id**: A Google Ads ügyfél azonosítód
   - **date_range**: `LAST_30_DAYS`
   - **metric**: `roas` (vagy `ctr`, `cost_per_conversion`)
5. Kattints az **"Execute"** gombra

**Példa válasz:**
```json
{
  "metric": "roas",
  "best_campaign": {
    "name": "Tavaszi Akció",
    "value": 5.2
  },
  "worst_campaign": {
    "name": "Téli Kampány",
    "value": 1.1
  },
  "average": 3.2,
  "median": 3.0,
  "std_dev": 1.5,
  "rankings": [
    {
      "campaign_name": "Tavaszi Akció",
      "roas": 5.2
    },
    {
      "campaign_name": "Nyári Kampány",
      "roas": 3.8
    }
  ]
}
```

---

## 5. Automatizálás Beállítása

Most jön az igazi varázslat! Beállítasz szabályokat, és az API automatikusan figyeli és optimalizálja a kampányaidat.

### 5.1. Bid Optimalizálási Szabály Létrehozása

Ez a szabály automatikusan ajánlásokat ad a bid (ajánlat) módosításához.

**A dokumentációs felületen:**

1. Keresd meg: **POST /api/v1/automation/bid-optimization/create**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki a Request body-t:

```json
{
  "customer_id": "1234567890",
  "campaign_id": "12345678",
  "target_roas": 4.0,
  "enabled": true
}
```

**Paraméterek magyarázata:**
- **customer_id**: Google Ads ügyfél azonosító
- **campaign_id**: A kampány azonosító, amit optimalizálni szeretnél
- **target_roas**: Cél ROAS érték (pl. 4.0 = 400% megtérülés)
- **target_cpa**: VAGY cél CPA érték (pl. 25.0)
- **enabled**: `true` = azonnal aktív, `false` = szünetel

5. Kattints az **"Execute"** gombra

**Példa válasz:**
```json
{
  "success": true,
  "message": "Bid optimalizálási szabály sikeresen létrehozva",
  "rule": {
    "rule_id": "bid_opt_1234567890_12345678_1729425600.0",
    "type": "bid_optimization",
    "customer_id": "1234567890",
    "campaign_id": "12345678",
    "target_roas": 4.0,
    "enabled": true,
    "created_at": "2025-10-20T10:00:00",
    "status": "active"
  }
}
```

**Mentsd el a `rule_id`-t!** Később szükséged lesz rá.

### 5.2. Bid Optimalizálás Alkalmazása

Most alkalmazzuk a szabályt és kérjünk ajánlásokat!

**A dokumentációs felületen:**

1. Keresd meg: **POST /api/v1/automation/bid-optimization/apply/{rule_id}**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki:
   - **rule_id**: Az előbb kapott rule_id
   - **customer_id**: `1234567890`
   - **campaign_id**: `12345678`
   - **date_range**: `LAST_7_DAYS`
5. Kattints az **"Execute"** gombra

**Példa válasz:**
```json
{
  "success": true,
  "message": "Bid optimalizálás sikeresen alkalmazva",
  "recommendations": [
    {
      "action": "decrease_bid",
      "reason": "ROAS (3.2) alacsonyabb mint a cél (4.0)",
      "adjustment_percent": -10,
      "priority": "high"
    }
  ],
  "rule": {
    "rule_id": "bid_opt_1234567890_12345678_1729425600.0",
    "last_run": "2025-10-20T10:05:00"
  }
}
```

**Mit jelent ez:**
- Az API azt javasolja, hogy csökkentsd a bid-et 10%-kal
- Mert a jelenlegi ROAS (3.2) alacsonyabb, mint a célod (4.0)
- Ez magas prioritású ajánlás

**Mit csinálj ezzel:**
- Menj a Google Ads felületére
- Keresd meg a kampányt
- Csökkentsd a bid-et 10%-kal
- Vagy hagyd, hogy később automatikusan történjen (ha implementálod)

---

## 6. Riasztások Létrehozása

A riasztások automatikusan figyelik a kampányaidat és jeleznek, ha valami nem stimmel.

### 6.1. Riasztási Szabály Létrehozása

**Példa: Riasztás, ha a ROAS 2.0 alá esik**

**A dokumentációs felületen:**

1. Keresd meg: **POST /api/v1/automation/alert/create**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki:
   - **customer_id**: `1234567890`
   - **campaign_id**: Hagyd üresen (minden kampányt figyel) VAGY add meg egy konkrét kampány ID-t
   - **metric**: `roas`
   - **threshold**: `2.0`
   - **condition**: `below`
   - **enabled**: `true`
5. Kattints az **"Execute"** gombra

**Más példák:**

**Riasztás, ha CPA 50 fölé megy:**
- metric: `cost_per_conversion`
- threshold: `50.0`
- condition: `above`

**Riasztás, ha CTR 1% alá esik:**
- metric: `ctr`
- threshold: `0.01`
- condition: `below`

### 6.2. Riasztások Ellenőrzése

Most nézzük meg, hogy van-e valami probléma!

**A dokumentációs felületen:**

1. Keresd meg: **POST /api/v1/automation/alert/check**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki:
   - **customer_id**: `1234567890`
   - **date_range**: `LAST_7_DAYS`
5. Kattints az **"Execute"** gombra

**Példa válasz:**
```json
[
  {
    "rule_id": "alert_1234567890_roas_1729425600.0",
    "campaign_id": 87654321,
    "campaign_name": "Nyári Kampány",
    "metric": "roas",
    "metric_value": 1.5,
    "threshold": 2.0,
    "condition": "below",
    "message": "ROAS (1.5) is below threshold (2.0)",
    "triggered_at": "2025-10-20T10:10:00"
  }
]
```

**Mit jelent ez:**
- A "Nyári Kampány" ROAS-a (1.5) a küszöb (2.0) alatt van
- Azonnal intézkedned kell!

**Mit csinálj:**
- Nézd meg a kampányt részletesen
- Ellenőrizd a kulcsszavakat
- Optimalizáld a hirdetéseket
- Vagy szüneteltess a kampányt

---

## 7. Költségvetés Optimalizálás

Az API kiszámítja, hogyan oszd el optimálisan a költségvetést a kampányaid között.

**A dokumentációs felületen:**

1. Keresd meg: **POST /api/v1/analytics/budget-allocation**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki:
   - **customer_id**: `1234567890`
   - **total_budget**: `1000.0` (mennyi a teljes havi költségvetésed)
   - **date_range**: `LAST_30_DAYS`
   - **optimization_goal**: `maximize_conversions` vagy `maximize_roas`
5. Kattints az **"Execute"** gombra

**Példa válasz:**
```json
{
  "optimization_goal": "maximize_conversions",
  "total_budget": 1000.0,
  "allocations": [
    {
      "campaign_id": 12345678,
      "campaign_name": "Tavaszi Akció",
      "current_budget": 300.0,
      "recommended_budget": 450.0,
      "change_percent": 50.0
    },
    {
      "campaign_id": 87654321,
      "campaign_name": "Nyári Kampány",
      "current_budget": 400.0,
      "recommended_budget": 350.0,
      "change_percent": -12.5
    },
    {
      "campaign_id": 11111111,
      "campaign_name": "Őszi Akció",
      "current_budget": 300.0,
      "recommended_budget": 200.0,
      "change_percent": -33.3
    }
  ]
}
```

**Mit jelent ez:**
- A "Tavaszi Akció" jól teljesít → növeld a költségvetést 450-re (+50%)
- A "Nyári Kampány" közepesen teljesít → csökkentsd 350-re (-12.5%)
- Az "Őszi Akció" gyengén teljesít → csökkentsd 200-ra (-33.3%)

---

## 8. Haladó Használat

### 8.1. Összes Automatizálási Szabály Lekérdezése

**A dokumentációs felületen:**

1. Keresd meg: **GET /api/v1/automation/rules**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki (opcionális):
   - **rule_type**: `bid_optimization`, `budget_optimization`, vagy `alert`
   - **enabled_only**: `true` (csak az aktív szabályok)
5. Kattints az **"Execute"** gombra

### 8.2. Szabály Módosítása

**A dokumentációs felületen:**

1. Keresd meg: **PUT /api/v1/automation/rules/{rule_id}**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki:
   - **rule_id**: A módosítandó szabály ID-ja
   - **enabled**: `false` (szüneteltetés) vagy `true` (aktiválás)
   - **target_roas**: Új ROAS cél (opcionális)
5. Kattints az **"Execute"** gombra

### 8.3. Szabály Törlése

**A dokumentációs felületen:**

1. Keresd meg: **DELETE /api/v1/automation/rules/{rule_id}**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki:
   - **rule_id**: A törlendő szabály ID-ja
5. Kattints az **"Execute"** gombra

### 8.4. Automatizálási Történet

Nézd meg, mit csinált az automatizálás eddig!

**A dokumentációs felületen:**

1. Keresd meg: **GET /api/v1/automation/history**
2. Kattints rá
3. Kattints a **"Try it out"** gombra
4. Töltsd ki (opcionális):
   - **rule_id**: Egy konkrét szabály története
   - **limit**: Hány rekordot mutasson (alapértelmezett: 100)
5. Kattints az **"Execute"** gombra

---

## 9. Tippek és Trükkök

### 💡 Napi Rutin

**Reggel:**
1. Indítsd el az API-t
2. Ellenőrizd a riasztásokat: `POST /api/v1/automation/alert/check`
3. Nézd meg a kampány betekintéseket: `GET /api/v1/analytics/campaign-insights`

**Este:**
4. Nézd meg a napi teljesítményt: `GET /api/v1/campaigns/performance` (date_range: `TODAY`)
5. Alkalmazd a bid optimalizálást: `POST /api/v1/automation/bid-optimization/apply/{rule_id}`

### 🎯 Ajánlott Küszöbértékek

**ROAS (Return on Ad Spend):**
- Minimum: 2.0 (200% megtérülés)
- Jó: 3.0-5.0
- Kiváló: 5.0+

**CPA (Cost Per Acquisition):**
- Függ az iparágadtól
- Általában: 20-50 EUR/USD
- Számítsd ki: Átlagos vásárlási érték × 0.3

**CTR (Click-Through Rate):**
- Minimum: 0.01 (1%)
- Jó: 0.02-0.05 (2-5%)
- Kiváló: 0.05+ (5%+)

### 🔄 Automatizálási Stratégia

**1. Kezdd kis lépésekkel:**
- Először csak riasztásokat állíts be
- Figyeld meg 1-2 hétig
- Aztán add hozzá a bid optimalizálást

**2. Ne automatizálj mindent egyszerre:**
- Válassz 1-2 fontos kampányt
- Teszteld rajtuk az automatizálást
- Ha működik, terjeszd ki a többire

**3. Rendszeresen ellenőrizd:**
- Hetente nézd meg a történetet
- Havi szinten értékeld az eredményeket
- Finomhangold a küszöbértékeket

### 📊 Riportolás

**Heti riport készítése:**

1. Kampány teljesítmény: `LAST_7_DAYS`
2. Kampány betekintések
3. Kulcsszó betekintések
4. Kiváltott riasztások

**Havi riport készítése:**

1. Kampány teljesítmény: `LAST_MONTH`
2. Kampány összehasonlítás (ROAS, CTR, CPA)
3. Költségvetés allokáció javaslat
4. Automatizálási történet

### ⚠️ Gyakori Hibák

**1. "Customer ID not found"**
- Ellenőrizd, hogy jó formátumban adtad meg (10 számjegy, kötőjelek nélkül)
- Ellenőrizd, hogy van hozzáférésed a fiókhoz

**2. "No data returned"**
- Lehet, hogy a kampány nem futott a megadott időszakban
- Próbálj hosszabb date_range-t (pl. `LAST_30_DAYS`)

**3. "API quota exceeded"**
- A Google Ads API-nak van napi limitje
- Várj egy kicsit, aztán próbáld újra
- Csökkentsd a lekérdezések gyakoriságát

---

## 🎓 Következő Lépések

**Ha már magabiztosan használod az API-t:**

1. **Integráld más rendszerekkel:**
   - Google Sheets export
   - Email értesítések
   - Slack/Discord webhook

2. **Fejlessz saját dashboard-ot:**
   - React/Vue.js frontend
   - Grafikonok és vizualizációk
   - Valós idejű monitoring

3. **Automatizáld a futtatást:**
   - Cron job beállítása
   - Ütemezett riportok
   - Automatikus bid módosítások

4. **Gépi tanulás:**
   - Előrejelzések
   - Anomália detektálás
   - Intelligens optimalizálás

---

## 📞 Segítség

Ha elakadtál vagy kérdésed van:

1. Nézd meg a dokumentációt: http://localhost:8000/docs
2. Olvasd el a README.md fájlt
3. Nézd meg a GitHub Issues-t
4. Kérdezz bátran! 😊

---

**Készítette:** Manus AI  
**Utolsó frissítés:** 2025. október 20.

