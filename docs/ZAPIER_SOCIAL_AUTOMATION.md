# Zapier-alapú közösségi média poszt automatizálás (Google Sheets alappal)

Ez a dokumentum összefoglalja, hogyan érdemes felépíteni egy Zapierre épülő folyamatot a közösségi média posztok kutatására, ötletelésére, generálására és jóváhagyott posztok előállítására. A megközelítés Google Sheets-et használ adattárolásra, és többnyelvű tartalmat (magyar, szlovák, román, angol, német) is támogat igény szerint.

## 1) Google Sheets struktúra (fülek és fő mezők)

1. **Kliens profil**: ügyfél neve, weboldal/blog link, hivatalos csatornák (FB/IG/LinkedIn/TikTok/YouTube), célközönség, hangnem/márkahang (ha van), kötelező/tiltott kifejezések, preferált nyelvek.
2. **Versenytársak**: ügyfél hivatkozás, 4–6 versenytárs neve, URL-ek csatornánként, megjegyzés a megfigyelt poszttípusokról/hosszokról.
3. **Jeles napok és események**: dátum, név, ország/régió, csatorna-relevancia, javasolt poszttípus (edukáció/értékesítés/story), forrás.
4. **Trend források (opcionális)**: RSS/YouTube/Blog link, témakör, frissítési gyakoriság.
5. **Csatornaspecifikus paraméterek**: csatorna, poszttípus, optimális hossz (karakter/perc), ajánlott emojiszám/stílus, hashtag szabály, CTA minta. Ezt a Zapok promptjai dinamikusan használják.
6. **Hashtag & CTA bank**: nyelv, téma, javasolt hashtagek, CTA-k; hivatkozás a kapcsolódó poszttípusra.
7. **Posztötletek**: ügyfél, csatorna, téma, jeles nap hivatkozás (ha van), poszttípus, javasolt hossz és emoji-szám, nyelv, státusz (Függő/Jóváhagyva/Elutasítva), megjegyzés a jóváhagyáshoz.
8. **Kész posztok**: ügyfél, csatorna, nyelv, jóváhagyott szöveg, emojik, hashtagek, CTA, tervezett dátum/időzítési javaslat, publikáció státusz (Nem/Elküldve), közzétett link (ha van).

## 2) Folyamat áttekintése

1. **Kutatási input** (félautomata, emberi felülvizsgálattal):
   - Kliens profil és csatornák megerősítése a Sheetben.
   - 4–6 versenytárs rögzítése csatornánként.
   - Jeles napok összegyűjtése (hazai és releváns nemzetközi), igény szerint trend források felvétele.
2. **Zap: kutatás → posztötlet**:
   - Trigger: új/frissített sor a *Kliens profil* vagy *Jeles napok* füleken, illetve manuális „Kutatás kész” jelölés.
   - Action: Formatter (adatok tisztítása) → OpenAI (promptba kerül: kliensprofil + versenytárs kivonat + jeles napok + csatorna-paraméterek + nyelvek). Kimenet: 5–15 ötlet, poszttípusok és nyelv megjelölésével, hosszal, emojiszámmal, hashtag/CTA javaslattal.
   - Output: írás a *Posztötletek* fülre, státusz „Függő”.
3. **Jóváhagyás** (Sheet): státusz „Jóváhagyva” vagy „Elutasítva”; megjegyzés opcionális.
4. **Zap: jóváhagyás → kész poszt**:
   - Trigger: *Posztötletek* sor státusza „Jóváhagyva”.
   - Action: OpenAI végleges szöveg (anti-sablon, természetes hang, csatorna- és nyelvspecifikus hossz + emojik + hashtag/CTA bank). Kimenet írása a *Kész posztok* fülre.
5. **(Opcionális) Publikáció**:
   - Trigger: *Kész posztok* sor „Publikáció dátum” kitöltve.
   - Action: Buffer/Hootsuite (vagy más scheduler) API; logolja a „Publikáció státusz” és link mezőket.

## 3) Prompt irányelvek (OpenAI lépésekhez)

- **Anti-sablon**: kerülje a generikus fordulatokat; kérj változatos mondatszerkezetet, természetes szóhasználatot.
- **Csatorna-hossz és emoji**: húzd be a *Csatornaspecifikus paraméterek* mezőit; ha nincs érték, használj konzervatív, emberi hosszt.
- **Nyelv**: mindig a *Posztötletek* sorában megadott nyelven dolgozz; ha hiányzik, kérj defaultként magyart, de jelezd, hogy választható szlovák/román/angol/német.
- **Hashtag/CTA**: válassz a bankból a téma és nyelv alapján; hiány esetén generálj, de maximum 3–5 hashtag csatornafüggően.
- **Ellenőrzés**: utasítsd a modellt, hogy azonos, egymás után ismétlődő emojikat kerülje; CTA legyen cselekvésorientált.

## 4) Biztonság és jogosultság

- A Google Sheetet csak az érintett csapattagokkal oszd meg (szerepkör: szerkesztő/megtekintő a feladatkörnek megfelelően).
- Ha Buffer/Hootsuite integrációt használsz, a hozzáférési tokeneket a Zapier beépített titkos tárában kezeld.
- Dokumentáld, ki felel a „Jóváhagyás” státusz módosításáért (pl. account manager).

## 5) Következő lépések (megvalósítási sorrend)

1. Google Sheet létrehozása a fenti fülekkel és mezőkkel; jogosultságok beállítása.
2. Minimum 1 kliensprofil kitöltése és 4–6 versenytárs felvitele csatornánként.
3. Csatornaspecifikus paramétertábla és Hashtag & CTA bank feltöltése (legalább magyar nyelvre).
4. Első Zap összeállítása: „Kutatás kész” → posztötlet generálás → írás a *Posztötletek* fülre.
5. Második Zap összeállítása: státusz „Jóváhagyva” → végleges poszt generálása → írás a *Kész posztok* fülre.
6. (Opcionális) Harmadik Zap: publikációs integráció Buffer/Hootsuite-tal.

Ez a folyamat iterálható: a kutatási inputokat rendszeresen frissítheted, az ötlet- és posztgenerálás pedig a jóváhagyási státuszok alapján automatizáltan működik.
