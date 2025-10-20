# Google Ads Automation API - Telepítési Útmutató Kezdőknek

Ez az útmutató lépésről-lépésre végigvezet a teljes telepítési folyamaton, még akkor is, ha még soha nem dolgoztál programozással vagy API-kkal.

## 📋 Mire lesz szükséged?

1. Egy számítógép (Windows, Mac vagy Linux)
2. Internet kapcsolat
3. Google Ads fiók (vagy hozzáférés egy Google Ads fiókhoz)
4. Körülbelül 1-2 óra idő

---

## 1. LÉPÉS: Python Telepítése

A Python egy programozási nyelv, amit az alkalmazásunk használ.

### Windows-on:

1. **Menj a Python weboldalára:**
   - Nyisd meg a böngésződet
   - Írd be: https://www.python.org/downloads/
   
2. **Töltsd le a Python-t:**
   - Kattints a nagy sárga "Download Python 3.11.x" gombra
   - Egy fájl letöltődik (kb. 25 MB)

3. **Telepítsd a Python-t:**
   - Dupla kattintás a letöltött fájlon
   - **FONTOS:** Pipáld be a "Add Python to PATH" opciót!
   - Kattints az "Install Now" gombra
   - Várj, amíg a telepítés befejeződik
   - Kattints a "Close" gombra

4. **Ellenőrizd, hogy sikerült:**
   - Nyisd meg a "Command Prompt"-ot (Keresőbe írd: cmd)
   - Írd be: `python --version`
   - Nyomj Enter-t
   - Látnod kell valami ilyesmit: `Python 3.11.x`

### Mac-en:

1. **Nyisd meg a Terminal-t:**
   - Nyomd meg: Command + Space
   - Írd be: Terminal
   - Nyomj Enter-t

2. **Telepítsd a Homebrew-t** (ez egy segédprogram):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   - Nyomj Enter-t
   - Írd be a jelszavad, ha kéri
   - Várj, amíg befejeződik

3. **Telepítsd a Python-t:**
   ```bash
   brew install python@3.11
   ```

4. **Ellenőrizd:**
   ```bash
   python3 --version
   ```

---

## 2. LÉPÉS: Git Telepítése

A Git egy program, amivel le tudod tölteni a projektet a GitHub-ról.

### Windows-on:

1. **Menj a Git weboldalára:**
   - https://git-scm.com/download/win
   
2. **Töltsd le és telepítsd:**
   - Kattints a "Click here to download" linkre
   - Dupla kattintás a letöltött fájlon
   - Kattintgass végig a "Next" gombokon (az alapértelmezett beállítások jók)
   - Kattints a "Finish" gombra

3. **Ellenőrizd:**
   - Nyisd meg a Command Prompt-ot (cmd)
   - Írd be: `git --version`
   - Látnod kell valami ilyesmit: `git version 2.x.x`

### Mac-en:

A Git általában már telepítve van Mac-en. Ellenőrizd:

```bash
git --version
```

Ha nincs telepítve, a rendszer felajánlja, hogy telepítse.

---

## 3. LÉPÉS: Projekt Letöltése

Most letöltjük a projektet a számítógépedre.

### Windows-on:

1. **Nyisd meg a Command Prompt-ot** (cmd)

2. **Menj a Dokumentumok mappába:**
   ```
   cd %USERPROFILE%\Documents
   ```

3. **Töltsd le a projektet:**
   ```
   git clone https://github.com/laczkobalazs-alt/google-ads-automation.git
   ```
   - Ez létrehoz egy "google-ads-automation" nevű mappát

4. **Lépj be a projekt mappába:**
   ```
   cd google-ads-automation
   ```

### Mac/Linux-on:

1. **Nyisd meg a Terminal-t**

2. **Menj a Dokumentumok mappába:**
   ```bash
   cd ~/Documents
   ```

3. **Töltsd le a projektet:**
   ```bash
   git clone https://github.com/laczkobalazs-alt/google-ads-automation.git
   ```

4. **Lépj be a projekt mappába:**
   ```bash
   cd google-ads-automation
   ```

---

## 4. LÉPÉS: Virtuális Környezet Létrehozása

A virtuális környezet egy elkülönített hely, ahol a projekt függőségei lesznek.

### Windows-on:

1. **Hozd létre a virtuális környezetet:**
   ```
   python -m venv venv
   ```
   - Ez létrehoz egy "venv" nevű mappát
   - Várj 1-2 percet

2. **Aktiváld a virtuális környezetet:**
   ```
   venv\Scripts\activate
   ```
   - Ha sikerült, a parancssor elején látni fogsz egy `(venv)` feliratot

### Mac/Linux-on:

1. **Hozd létre a virtuális környezetet:**
   ```bash
   python3 -m venv venv
   ```

2. **Aktiváld a virtuális környezetet:**
   ```bash
   source venv/bin/activate
   ```
   - Ha sikerült, a parancssor elején látni fogsz egy `(venv)` feliratot

---

## 5. LÉPÉS: Függőségek Telepítése

Most telepítjük az összes szükséges programkönyvtárat.

**Mindkét operációs rendszeren ugyanaz:**

```bash
pip install -r requirements.txt
```

- Ez eltarthat 2-5 percig
- Sok szöveg fog megjelenni - ez normális!
- Várj, amíg visszakapod a parancssor vezérlést

---

## 6. LÉPÉS: Google Ads API Beállítása

Ez a legbonyolultabb rész, de végigvezetlek rajta!

### 6.1. Google Cloud Projekt Létrehozása

1. **Menj a Google Cloud Console-ra:**
   - https://console.cloud.google.com/
   - Jelentkezz be a Google fiókodba

2. **Hozz létre egy új projektet:**
   - Kattints a felső menüsorban a projekt nevére
   - Kattints a "NEW PROJECT" gombra
   - Adj neki egy nevet: pl. "Google Ads Automation"
   - Kattints a "CREATE" gombra
   - Várj 10-20 másodpercet

3. **Válaszd ki az új projektet:**
   - Kattints megint a projekt nevére
   - Válaszd ki az imént létrehozott projektet

### 6.2. Google Ads API Engedélyezése

1. **Menj az API Library-ba:**
   - Bal oldali menü → "APIs & Services" → "Library"
   - Vagy: https://console.cloud.google.com/apis/library

2. **Keresd meg a Google Ads API-t:**
   - A keresőbe írd be: "Google Ads API"
   - Kattints a "Google Ads API" találatra

3. **Engedélyezd az API-t:**
   - Kattints az "ENABLE" gombra
   - Várj 10-20 másodpercet

### 6.3. OAuth2 Credentials Létrehozása

1. **Menj a Credentials oldalra:**
   - Bal oldali menü → "APIs & Services" → "Credentials"
   - Vagy: https://console.cloud.google.com/apis/credentials

2. **Állítsd be az OAuth consent screen-t:**
   - Kattints az "OAuth consent screen" fülre
   - Válaszd az "External" opciót
   - Kattints a "CREATE" gombra
   
3. **Töltsd ki az űrlapot:**
   - App name: "Google Ads Automation"
   - User support email: a saját email címed
   - Developer contact: a saját email címed
   - Kattints a "SAVE AND CONTINUE" gombra
   - A "Scopes" résznél kattints a "SAVE AND CONTINUE" gombra
   - A "Test users" résznél add hozzá a saját email címed
   - Kattints az "ADD USERS" gombra
   - Kattints a "SAVE AND CONTINUE" gombra

4. **Hozz létre OAuth2 Client ID-t:**
   - Menj vissza a "Credentials" fülre
   - Kattints a "+ CREATE CREDENTIALS" gombra
   - Válaszd az "OAuth client ID" opciót
   - Application type: "Desktop app"
   - Name: "Google Ads Automation Desktop"
   - Kattints a "CREATE" gombra

5. **Töltsd le a credentials fájlt:**
   - Megjelenik egy ablak a Client ID-val és Client Secret-tel
   - Kattints a "DOWNLOAD JSON" gombra
   - Mentsd el a fájlt a projekt mappába `credentials.json` néven

### 6.4. Developer Token Megszerzése

1. **Menj a Google Ads felületére:**
   - https://ads.google.com/
   - Jelentkezz be

2. **Menj az API Center-be:**
   - Kattints a "Tools" ikonra (csavarkulcs)
   - "Setup" → "API Center"

3. **Kérj Developer Token-t:**
   - Ha még nincs, kattints a "Request Token" gombra
   - Töltsd ki az űrlapot
   - **FIGYELEM:** Ez eltarthat 1-2 napig, amíg a Google jóváhagyja!
   - Addig is használhatsz "test" módot

4. **Másold ki a Developer Token-t:**
   - Ha megkaptad, másold ki és mentsd el valahova

---

## 7. LÉPÉS: Konfigurációs Fájlok Beállítása

### 7.1. .env Fájl Létrehozása

1. **Másold át a példa fájlt:**

**Windows-on:**
```
copy .env.example .env
```

**Mac/Linux-on:**
```bash
cp .env.example .env
```

2. **Nyisd meg a .env fájlt egy szövegszerkesztőben:**
   - Windows: Notepad vagy Notepad++
   - Mac: TextEdit
   - Vagy bármilyen kódszerkesztő (pl. VS Code)

3. **Töltsd ki az adatokat:**
   ```
   GOOGLE_ADS_DEVELOPER_TOKEN=ide_jön_a_developer_token
   GOOGLE_ADS_CLIENT_ID=ide_jön_a_client_id
   GOOGLE_ADS_CLIENT_SECRET=ide_jön_a_client_secret
   GOOGLE_ADS_LOGIN_CUSTOMER_ID=ide_jön_az_ügyfél_azonosító
   ```

   - A Client ID és Client Secret a `credentials.json` fájlban van
   - Az ügyfél azonosító (Customer ID) a Google Ads felületén található (10 számjegy, kötőjelek nélkül)

4. **Mentsd el a fájlt**

### 7.2. google-ads.yaml Fájl Létrehozása

1. **Másold át a példa fájlt:**

**Windows-on:**
```
copy google-ads.yaml.example google-ads.yaml
```

**Mac/Linux-on:**
```bash
cp google-ads.yaml.example google-ads.yaml
```

2. **Nyisd meg a google-ads.yaml fájlt**

3. **Töltsd ki az adatokat:**
   ```yaml
   developer_token: "IDE_JÖN_A_DEVELOPER_TOKEN"
   client_id: "IDE_JÖN_A_CLIENT_ID"
   client_secret: "IDE_JÖN_A_CLIENT_SECRET"
   refresh_token: "IDE_JÖN_A_REFRESH_TOKEN"
   login_customer_id: "IDE_JÖN_AZ_ÜGYFÉL_AZONOSÍTÓ"
   ```

4. **Refresh Token megszerzése:**
   - Ez egy kicsit bonyolult, de van egy egyszerű módszer
   - Futtasd ezt a Python scriptet (a projekt mappában):

**Windows-on:**
```
python -c "from google.ads.googleads.oauth2 import get_refresh_token; get_refresh_token()"
```

**Mac/Linux-on:**
```bash
python3 -c "from google.ads.googleads.oauth2 import get_refresh_token; get_refresh_token()"
```

   - Megnyílik egy böngésző ablak
   - Jelentkezz be a Google fiókodba
   - Engedélyezd a hozzáférést
   - Másold ki a megjelenő refresh token-t
   - Illeszd be a `google-ads.yaml` fájlba

5. **Mentsd el a fájlt**

---

## 8. LÉPÉS: API Indítása

Most már készen állsz az API indítására!

### Mindkét operációs rendszeren:

1. **Győződj meg róla, hogy a virtuális környezet aktív:**
   - Látnod kell a `(venv)` feliratot a parancssor elején
   - Ha nem látod, aktiváld újra (lásd 4. lépés)

2. **Indítsd el az API-t:**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Ha minden jól megy, látnod kell valami ilyesmit:**
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

4. **Nyisd meg a böngésződet és menj ide:**
   - http://localhost:8000
   - Látnod kell egy JSON választ az API állapotáról

5. **Nézd meg az interaktív dokumentációt:**
   - http://localhost:8000/docs
   - Itt ki tudod próbálni az összes API végpontot!

---

## 9. LÉPÉS: Első API Hívás Kipróbálása

1. **Menj a dokumentációs felületre:**
   - http://localhost:8000/docs

2. **Próbáld ki a health check-et:**
   - Keresd meg a `GET /health` végpontot
   - Kattints rá
   - Kattints a "Try it out" gombra
   - Kattints az "Execute" gombra
   - Látnod kell a választ, hogy az API működik-e

3. **Próbáld ki a kampányok lekérdezését:**
   - Keresd meg a `GET /api/v1/campaigns/list` végpontot
   - Kattints rá
   - Kattints a "Try it out" gombra
   - Írd be a `customer_id`-t (a Google Ads ügyfél azonosítód)
   - Kattints az "Execute" gombra
   - Látnod kell a kampányaid listáját!

---

## ❓ Gyakori Problémák és Megoldások

### "Python nem található" hiba

**Megoldás:**
- Győződj meg róla, hogy a Python telepítve van
- Windows-on: Ellenőrizd, hogy a "Add Python to PATH" be volt-e pipálva
- Próbáld újraindítani a Command Prompt-ot vagy a számítógépet

### "pip nem található" hiba

**Megoldás:**
- Próbáld ezt: `python -m pip install -r requirements.txt`
- Vagy Mac-en: `python3 -m pip install -r requirements.txt`

### "Permission denied" hiba

**Megoldás:**
- Windows-on: Futtasd a Command Prompt-ot adminisztrátorként
- Mac/Linux-on: Használd a `sudo` parancsot

### "Google Ads API nincs konfigurálva" hiba

**Megoldás:**
- Ellenőrizd, hogy a `google-ads.yaml` fájl létezik
- Ellenőrizd, hogy az összes adat ki van töltve
- Ellenőrizd, hogy nincs extra szóköz vagy idézőjel

### "Invalid refresh token" hiba

**Megoldás:**
- Szerezz új refresh token-t (lásd 7.2. lépés)
- Győződj meg róla, hogy a credentials.json fájl helyes

---

## 🎉 Gratulálok!

Ha idáig eljutottál, sikeresen telepítetted és elindítottad a Google Ads Automation API-t!

### Mit tudsz most csinálni?

1. **Lekérdezni a kampányaid teljesítményét**
2. **Elemezni a kulcsszavakat**
3. **Automatizálási szabályokat létrehozni**
4. **Riasztásokat beállítani**

### Következő lépések:

- Olvasd el a `PROJEKT_OSSZEFOGLALO.md` fájlt
- Nézd meg a `docs/API_DOCUMENTATION.md` fájlt
- Próbálj ki különböző API végpontokat a `/docs` felületen

---

## 📞 Segítségre van szükséged?

Ha elakadtál vagy bármi nem működik:

1. Ellenőrizd újra az összes lépést
2. Nézd meg a hibaüzenetet pontosan
3. Keresd meg a hibát Google-on
4. Nyiss egy issue-t a GitHub-on: https://github.com/laczkobalazs-alt/google-ads-automation/issues

---

**Készítette:** Manus AI  
**Utolsó frissítés:** 2025. október 20.

