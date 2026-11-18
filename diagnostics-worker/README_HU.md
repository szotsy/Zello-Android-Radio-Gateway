# Orfeusz Gateway – anonim diagnosztikai napló fogadó

Ez a Cloudflare Worker a diagnosztikai ZIP-eket GitHub-fiók nélkül fogadja, és privát Cloudflare R2 bucketbe menti.

## Fontos állapot

A forráskód a GitHub repóban van, de a szolgáltatás még nem él, amíg a Cloudflare-fiókban az R2 bucket és a Worker nincs létrehozva/telepítve. A mobilalkalmazásba csak a ténylegesen telepített Worker URL-je kerülhet.

## Védelmi korlátok

- maximum 10 MB/feltöltés;
- ZIP aláírás ellenőrzése;
- IP-címenként legfeljebb 5 feltöltés/óra a Cloudflare Rate Limiting bindinggal;
- a feltöltött fájlok privát R2 tárhelyre kerülnek;
- nincs nyilvános lista vagy letöltési végpont;
- a feltöltéshez nem kell GitHub-fiók;
- a Worker nem küld automatikus e-mailt és nem teszi közzé a naplókat.

## Telepítés

1. Cloudflare-ben hozz létre egy R2 bucketet orfeusz-diagnostic-logs néven.
2. Telepítsd a Wrangler CLI-t, majd jelentkezz be: npx wrangler login.
3. A diagnostics-worker mappában futtasd: npx wrangler deploy.
4. Ellenőrizd, hogy az R2 binding és a rate-limit binding aktív. A rate limit namespace azonosítóját szükség esetén állítsd a Cloudflare-fiókban kiosztott értékre.
5. A telepítés után kapott workers.dev URL lesz az alkalmazás feltöltési végpontja, útvonala /api/diagnostics.

## Teszt

A végpont POST /api/diagnostics kérést vár application/zip vagy application/octet-stream tartalommal. Siker esetén HTTP 201 és egy uploadId érkezik.

## Adatvédelem és üzemeltetés

A napló ZIP-ek hibakeresési adatokat tartalmazhatnak. A bucketet privátan kell tartani, a hozzáférést csak az üzemeltető kapja meg. Állíts be R2 lifecycle szabályt az incoming/ objektumokra 14 napos automatikus törléssel. A feltöltési URL nyilvános, ezért a korlátozásokat és a tárhelyhasználatot rendszeresen ellenőrizni kell.

A Worker jelenleg csak fogad és tárol; a naplókat nem továbbítja e-mailre vagy GitHubra.
