# .env Fájl Beállítása - Részletes Útmutató

Ez az útmutató lépésről-lépésre megmutatja, hogyan hozd létre és töltsd ki a `.env` fájlt.

---

## Mi az a .env fájl?

A `.env` fájl egy **konfigurációs fájl**, amely tartalmazza az API hitelesítési adataidat és egyéb beállításokat. Ez a fájl **NEM kerül fel a GitHub-ra** (biztonsági okokból), ezért neked kell létrehoznod.

---

## 1. LÉPÉS: .env Fájl Létrehozása

### Windows-on:

**1. Nyisd meg a Command Prompt-ot (cmd)**

**2. Lépj be a projekt mappába:**
```cmd
cd %USERPROFILE%\Documents\google-ads-automation
```

**3. Másold át a példa fájlt:**
```cmd
copy .env.example .env
```

**4. Ha sikerült, látnod kell:**
```
1 file(s) copied.
```

### Mac/Linux-on:

**1. Nyisd meg a Terminal-t**

**2. Lépj be a projekt mappába:**
```bash
cd ~/Documents/google-ads-automation
```

**3. Másold át a példa fájlt:**
```bash
cp .env.example .env
```

**4. Ha sikerült, nem látsz semmit (ez jó jel!)**

Ellenőrizd, hogy létrejött:
```bash
ls -la .env
```

---

## 2. LÉPÉS: .env Fájl Megnyitása és Szerkesztése

Most meg kell nyitnod a `.env` fájlt egy szövegszerkesztőben.

### Windows-on:

**Opció 1: Notepad (legegyszerűbb)**

1. Nyisd meg a Fájlkezelőt (File Explorer)
2. Menj a projekt mappába: `Dokumentumok\google-ads-automation`
3. Keresd meg a `.env` fájlt
   - **FONTOS:** Lehet, hogy nem látod, mert a pont (`.`) előtagú fájlok rejtettek!
   - **Megoldás:** Fájlkezelő → Nézet → Jelöld be a "Rejtett elemek" opciót
4. Jobb klikk a `.env` fájlra → "Megnyitás ezzel" → "Jegyzettömb" (Notepad)

**Vagy parancssorból:**
```cmd
notepad .env
```

**Opció 2: Notepad++ (ajánlott, ha telepítve van)**

```cmd
notepad++ .env
```

**Opció 3: Visual Studio Code (ha telepítve van)**

```cmd
code .env
```

### Mac-en:

**Opció 1: TextEdit**

```bash
open -a TextEdit .env
```

**Opció 2: Visual Studio Code (ha telepítve van)**

```bash
code .env
```

**Opció 3: Nano (terminálban)**

```bash
nano .env
```

### Linux-en:

**Opció 1: Nano**

```bash
nano .env
```

**Opció 2: Gedit**

```bash
gedit .env
```

**Opció 3: Visual Studio Code**

```bash
code .env
```

---

## 3. LÉPÉS: .env Fájl Kitöltése

Most látni fogsz egy fájlt, ami így néz ki:

```env
# API Configuration
API_TITLE="Google Ads Automation API"
API_VERSION="1.0.0"
API_HOST="0.0.0.0"
API_PORT=8000
DEBUG=True

# Google Ads API Configuration
GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token_here
GOOGLE_ADS_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=your_client_secret_here
GOOGLE_ADS_REFRESH_TOKEN=your_refresh_token_here
GOOGLE_ADS_LOGIN_CUSTOMER_ID=your_login_customer_id_here

# Database Configuration
DATABASE_URL=sqlite:///./google_ads_automation.db

# Security
SECRET_KEY=your_secret_key_here_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Automation Settings
AUTO_BID_OPTIMIZATION_ENABLED=False
AUTO_BUDGET_OPTIMIZATION_ENABLED=False
AUTOMATION_CHECK_INTERVAL_MINUTES=60

# Performance Thresholds
MIN_ROAS_THRESHOLD=2.0
MAX_CPA_THRESHOLD=50.0
MIN_CTR_THRESHOLD=0.01
```

### Mit kell módosítanod?

Csak ezeket a sorokat kell kitöltened:

```env
GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token_here
GOOGLE_ADS_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=your_client_secret_here
GOOGLE_ADS_REFRESH_TOKEN=your_refresh_token_here
GOOGLE_ADS_LOGIN_CUSTOMER_ID=your_login_customer_id_here
```

---

## 4. LÉPÉS: Hitelesítési Adatok Megszerzése

### 4.1. Developer Token

**Honnan szerezd meg:**

1. Menj a Google Ads felületére: https://ads.google.com/
2. Jelentkezz be
3. Kattints a **"Tools"** ikonra (csavarkulcs) a jobb felső sarokban
4. **"Setup"** → **"API Center"**
5. Látni fogsz egy **"Developer token"** mezőt
6. Másold ki ezt az értéket

**Példa:**
```
AbCdEf1234567890
```

**Írd be a .env fájlba:**
```env
GOOGLE_ADS_DEVELOPER_TOKEN=AbCdEf1234567890
```

**FONTOS:** Ha még nincs Developer Token-ed:
- Kattints a **"Request Token"** gombra
- Töltsd ki az űrlapot
- Várj 1-2 napot, amíg a Google jóváhagyja
- **Addig is használhatsz tesztelési módot!**

### 4.2. Client ID és Client Secret

Ezeket a Google Cloud Console-ból szerezted meg (amikor létrehoztad az OAuth2 credentials-t).

**Honnan szerezd meg:**

**Opció 1: A letöltött credentials.json fájlból**

1. Nyisd meg a `credentials.json` fájlt (amit letöltöttél a Google Cloud Console-ról)
2. Keresd meg ezeket a sorokat:

```json
{
  "installed": {
    "client_id": "123456789-abcdefgh.apps.googleusercontent.com",
    "client_secret": "GOCSPX-AbCdEfGhIjKlMnOpQrStUv"
  }
}
```

3. Másold ki a `client_id` és `client_secret` értékeket

**Opció 2: Google Cloud Console-ból**

1. Menj a Google Cloud Console-ra: https://console.cloud.google.com/
2. Válaszd ki a projektedet
3. Menj a **"APIs & Services"** → **"Credentials"**
4. Keresd meg az OAuth 2.0 Client ID-t (amit létrehoztál)
5. Kattints rá
6. Látni fogod a **Client ID**-t és **Client secret**-et

**Írd be a .env fájlba:**
```env
GOOGLE_ADS_CLIENT_ID=123456789-abcdefgh.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=GOCSPX-AbCdEfGhIjKlMnOpQrStUv
```

### 4.3. Refresh Token

Ez a legbonyolultabb rész, de van egy egyszerű módszer!

**Módszer 1: Python script használata (AJÁNLOTT)**

1. Nyisd meg a terminált/parancssort
2. Lépj be a projekt mappába
3. Aktiváld a virtuális környezetet (lásd TELEPITESI_UTMUTATO.md)
4. Futtasd ezt a parancsot:

**Windows:**
```cmd
python -c "from google.ads.googleads.oauth2 import get_refresh_token; get_refresh_token()"
```

**Mac/Linux:**
```bash
python3 -c "from google.ads.googleads.oauth2 import get_refresh_token; get_refresh_token()"
```

5. Megnyílik egy böngésző ablak
6. Jelentkezz be a Google fiókodba
7. Kattints az **"Engedélyezés"** gombra
8. A terminálban megjelenik a refresh token
9. Másold ki

**Példa kimenet:**
```
Your refresh token is: 1//0abc123def456ghi789jkl
```

**Írd be a .env fájlba:**
```env
GOOGLE_ADS_REFRESH_TOKEN=1//0abc123def456ghi789jkl
```

**Módszer 2: OAuth2 Playground használata**

Ha a Python script nem működik:

1. Menj ide: https://developers.google.com/oauthplayground/
2. Kattints a fogaskerék ikonra (jobb felül)
3. Jelöld be: **"Use your own OAuth credentials"**
4. Írd be a Client ID-t és Client Secret-et
5. Bal oldalt keresd meg: **"Google Ads API v15"**
6. Válaszd ki: **"https://www.googleapis.com/auth/adwords"**
7. Kattints: **"Authorize APIs"**
8. Jelentkezz be és engedélyezd
9. Kattints: **"Exchange authorization code for tokens"**
10. Másold ki a **"Refresh token"** értéket

### 4.4. Login Customer ID

Ez a Google Ads ügyfél azonosítód.

**Honnan szerezd meg:**

1. Menj a Google Ads felületére: https://ads.google.com/
2. Jelentkezz be
3. A jobb felső sarokban látni fogsz egy **10 számjegyű azonosítót**
   - Például: `123-456-7890`
4. **FONTOS:** Vedd ki a kötőjeleket!
   - Helyes: `1234567890`
   - Helytelen: `123-456-7890`

**Írd be a .env fájlba:**
```env
GOOGLE_ADS_LOGIN_CUSTOMER_ID=1234567890
```

---

## 5. LÉPÉS: Fájl Mentése

### Windows Notepad:
1. **File** → **Save** (vagy CTRL + S)
2. Zárd be a Jegyzettömböt

### Mac TextEdit:
1. **File** → **Save** (vagy Command + S)
2. Zárd be a TextEdit-et

### Nano (Linux/Mac):
1. Nyomd meg: **CTRL + O** (mentés)
2. Nyomd meg: **Enter** (megerősítés)
3. Nyomd meg: **CTRL + X** (kilépés)

### Visual Studio Code:
1. **File** → **Save** (vagy CTRL/Command + S)
2. Zárd be a fájlt

---

## 6. LÉPÉS: Ellenőrzés

Most ellenőrizzük, hogy minden rendben van-e!

**1. Indítsd el az API-t:**

```bash
uvicorn app.main:app --reload
```

**2. Nyisd meg a böngészőt:**

```
http://localhost:8000/health
```

**3. Ha minden jó, látnod kell:**

```json
{
  "status": "healthy",
  "google_ads_configured": true
}
```

✅ **Ha `"google_ads_configured": true`** → SIKER! Minden rendben van!

❌ **Ha `"google_ads_configured": false`** → Valami hiba van a konfigurációban.

---

## 🔧 Hibaelhárítás

### "google_ads_configured": false

**Lehetséges okok:**

1. **A .env fájl nem létezik**
   - Ellenőrizd: `ls -la .env` (Mac/Linux) vagy `dir .env` (Windows)
   - Ha nincs, hozd létre újra (1. lépés)

2. **Hibás formátum**
   - Ne használj idézőjeleket: ❌ `GOOGLE_ADS_DEVELOPER_TOKEN="token"`
   - Helyes: ✅ `GOOGLE_ADS_DEVELOPER_TOKEN=token`
   - Ne legyen szóköz az `=` jel körül

3. **Hiányzó adatok**
   - Ellenőrizd, hogy minden mező ki van-e töltve
   - Ne maradjon benne `your_developer_token_here`

4. **Rossz refresh token**
   - Szerezz új refresh token-t (4.3. lépés)

### "Invalid refresh token" hiba

**Megoldás:**
1. Szerezz új refresh token-t (4.3. lépés)
2. Írd be a .env fájlba
3. Mentsd el
4. Indítsd újra az API-t

### "Developer token not approved"

**Megoldás:**
- A Developer Token jóváhagyása 1-2 napot vesz igénybe
- **Addig is használhatsz tesztelési módot:**
  - A .env fájlban hagyd üresen: `GOOGLE_ADS_DEVELOPER_TOKEN=`
  - Az API korlátozott módban fog működni

---

## 📋 Teljes Példa

Így néz ki egy kitöltött .env fájl:

```env
# API Configuration
API_TITLE="Google Ads Automation API"
API_VERSION="1.0.0"
API_HOST="0.0.0.0"
API_PORT=8000
DEBUG=True

# Google Ads API Configuration
GOOGLE_ADS_DEVELOPER_TOKEN=AbCdEf1234567890
GOOGLE_ADS_CLIENT_ID=123456789-abcdefgh.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=GOCSPX-AbCdEfGhIjKlMnOpQrStUv
GOOGLE_ADS_REFRESH_TOKEN=1//0abc123def456ghi789jkl
GOOGLE_ADS_LOGIN_CUSTOMER_ID=1234567890

# Database Configuration
DATABASE_URL=sqlite:///./google_ads_automation.db

# Security
SECRET_KEY=valami_nagyon_titkos_kulcs_123456
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Automation Settings
AUTO_BID_OPTIMIZATION_ENABLED=False
AUTO_BUDGET_OPTIMIZATION_ENABLED=False
AUTOMATION_CHECK_INTERVAL_MINUTES=60

# Performance Thresholds
MIN_ROAS_THRESHOLD=2.0
MAX_CPA_THRESHOLD=50.0
MIN_CTR_THRESHOLD=0.01
```

---

## ⚠️ FONTOS BIZTONSÁGI MEGJEGYZÉSEK

1. **SOHA ne oszd meg a .env fájlt senkivel!**
   - Tartalmazza a titkos hitelesítési adataidat

2. **SOHA ne töltsd fel a .env fájlt GitHub-ra!**
   - A `.gitignore` fájl már tartalmazza, de légy óvatos

3. **Ha véletlenül megosztottad:**
   - Azonnal generálj új Client Secret-et a Google Cloud Console-on
   - Szerezz új Refresh Token-t

---

## 🎉 Gratulálok!

Ha idáig eljutottál és a `/health` endpoint `"google_ads_configured": true`-t mutat, akkor sikeresen beállítottad a .env fájlt! 🎊

Most már használhatod az API-t a Google Ads kampányaid kezeléséhez!

---

## 📞 Segítség

Ha továbbra sem működik:
1. Ellenőrizd újra az összes lépést
2. Nézd meg a hibaüzenetet pontosan
3. Kérdezz bátran! 😊

---

**Készítette:** Manus AI  
**Utolsó frissítés:** 2025. október 20.

