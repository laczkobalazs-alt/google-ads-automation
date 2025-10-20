# Google Ads Automation API - Részletes Dokumentáció

Ez a dokumentum részletes leírást ad a Google Ads Automation API végpontjairól, azok használatáról és a válaszok formátumáról.

Az API a [FastAPI](https://fastapi.tiangolo.com/) keretrendszerre épül, és interaktív dokumentációt biztosít a Swagger UI és ReDoc segítségével, amelyek az API indítása után a `/docs` és `/redoc` útvonalakon érhetők el.

## Alapok

- **Alap URL**: `http://localhost:8000` (alapértelmezett)
- **API prefix**: `/api/v1`
- **Hitelesítés**: Jelenleg nincs implementálva, de a jövőben OAuth2 alapú hitelesítés javasolt.

## Általános végpontok

### `GET /`

Főoldal, amely az API állapotát mutatja.

- **Válasz**:
```json
{
  "message": "Google Ads Automation API",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs"
}
```

### `GET /health`

Egészségügyi ellenőrzés, amely ellenőrzi az API állapotát és a Google Ads kliens konfigurációját.

- **Válasz**:
```json
{
  "status": "healthy",
  "google_ads_configured": true
}
```

## Kampányok (`/campaigns`)

### `GET /campaigns/list`

Lekérdezi az összes kampányt a megadott ügyfél fiókból.

- **Paraméterek**:
  - `customer_id` (string, kötelező): Google Ads ügyfél azonosító.
- **Válasz**: Kampányok listája `CampaignBase` séma szerint.

### `GET /campaigns/performance`

Lekérdezi a kampány(ok) teljesítményét a megadott időszakban.

- **Paraméterek**:
  - `customer_id` (string, kötelező): Google Ads ügyfél azonosító.
  - `campaign_id` (string, opcionális): Specifikus kampány azonosító.
  - `date_range` (string, opcionális): Dátum tartomány (pl. `LAST_30_DAYS`). Alapértelmezett: `LAST_30_DAYS`.
- **Válasz**: Kampány teljesítmény adatok listája `CampaignPerformance` séma szerint.

## Kulcsszavak (`/keywords`)

### `GET /keywords/performance`

Lekérdezi a kulcsszavak teljesítményét a megadott időszakban.

- **Paraméterek**:
  - `customer_id` (string, kötelező): Google Ads ügyfél azonosító.
  - `campaign_id` (string, opcionális): Specifikus kampány azonosító.
  - `date_range` (string, opcionális): Dátum tartomány. Alapértelmezett: `LAST_30_DAYS`.
- **Válasz**: Kulcsszó teljesítmény adatok listája `KeywordPerformance` séma szerint.

## Elemzés (`/analytics`)

### `GET /analytics/campaign-insights`

Kampány teljesítmény elemzés és betekintések.

- **Paraméterek**:
  - `customer_id`, `campaign_id`, `date_range`
  - `min_roas`, `max_cpa`, `min_ctr` (float, opcionális): Küszöbértékek az elemzéshez.
- **Válasz**: Elemzési eredmények, beleértve betekintéseket, összefoglalót és ajánlásokat.

### `GET /analytics/keyword-insights`

Kulcsszó teljesítmény elemzés és betekintések.

- **Paraméterek**:
  - `customer_id`, `campaign_id`, `date_range`
  - `min_impressions` (int, opcionális): Minimum megjelenítési szám a szűréshez.
- **Válasz**: Kulcsszó elemzési eredmények.

### `GET /analytics/compare-campaigns`

Kampányok összehasonlítása egy adott metrika alapján.

- **Paraméterek**:
  - `customer_id`, `date_range`
  - `metric` (string, opcionális): Összehasonlítási metrika (pl. `roas`, `ctr`). Alapértelmezett: `roas`.
- **Válasz**: Összehasonlítási eredmények.

### `POST /analytics/budget-allocation`

Optimális költségvetés elosztás számítása.

- **Paraméterek**:
  - `customer_id`, `date_range`
  - `total_budget` (float, kötelező): Teljes elérhető költségvetés.
  - `optimization_goal` (string, opcionális): Optimalizálási cél (pl. `maximize_conversions`).
- **Válasz**: Költségvetés elosztási javaslat.

## Automatizáció (`/automation`)

### `POST /automation/bid-optimization/create`

Létrehoz egy automatikus bid optimalizálási szabályt.

- **Request Body**: `BidOptimizationRequest` séma.
- **Válasz**: `APIResponse` a létrehozott szabály adataival.

### `POST /automation/bid-optimization/apply/{rule_id}`

Alkalmaz egy bid optimalizálási szabályt.

- **Path Paraméter**: `rule_id` (string, kötelező).
- **Query Paraméterek**: `customer_id`, `campaign_id`, `date_range`.
- **Válasz**: `APIResponse` az optimalizálási ajánlásokkal.

### `POST /automation/budget-optimization/create`

Létrehoz egy automatikus költségvetés optimalizálási szabályt.

- **Request Body**: `BudgetOptimizationRequest` séma.
- **Válasz**: `APIResponse` a létrehozott szabály adataival.

### `POST /automation/alert/create`

Létrehoz egy riasztási szabályt.

- **Query Paraméterek**: `customer_id`, `campaign_id`, `metric`, `threshold`, `condition`, `enabled`.
- **Válasz**: `APIResponse` a létrehozott szabály adataival.

### `POST /automation/alert/check`

Ellenőrzi a riasztási szabályokat.

- **Query Paraméterek**: `customer_id`, `date_range`.
- **Válasz**: Kiváltott riasztások listája.

### `GET /automation/rules`

Lekérdezi az automatizálási szabályokat.

- **Query Paraméterek**: `rule_type`, `enabled_only`.
- **Válasz**: Szabályok listája.

### `PUT /automation/rules/{rule_id}`

Frissít egy automatizálási szabályt.

- **Path Paraméter**: `rule_id`.
- **Query Paraméterek**: `enabled`, `target_roas`, `target_cpa`, `threshold`.
- **Válasz**: `APIResponse` a frissített szabály adataival.

### `DELETE /automation/rules/{rule_id}`

Töröl egy automatizálási szabályt.

- **Path Paraméter**: `rule_id`.
- **Válasz**: `APIResponse` a törlés eredményével.

### `GET /automation/history`

Lekérdezi az automatizálási történetet.

- **Query Paraméterek**: `rule_id`, `limit`.
- **Válasz**: Történeti rekordok listája.

