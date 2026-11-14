# Orfeusz Gateway

![Orfeusz Gateway – Android, Zello és rádió](images/Orfeuszbanner.png)

Androidos, kétirányú Zello–rádió kapuállomás.

![Android](https://img.shields.io/badge/ANDROID-3D3D3D?style=for-the-badge&logo=android&logoColor=white) ![Zello](https://img.shields.io/badge/ZELLO-F36C21?style=for-the-badge&logoColor=white) ![Radio Gateway](https://img.shields.io/badge/RADIO_GATEWAY-171717?style=for-the-badge&logoColor=white) ![Version](https://img.shields.io/badge/VERSION-1.10.54-F36C21?style=for-the-badge)

## Mire szolgál az Orfeusz Gateway?

Az **Orfeusz Gateway** egy Android-alapú rádiós átjáróalkalmazás, amely lehetővé teszi a hagyományos rádióforgalom és a Zello-hálózat kétirányú összekapcsolását.

A rendszer segítségével a hagyományos rádióval leadott adás eljuthat a Zello felhasználóihoz, a Zello felől érkező hang pedig továbbítható a csatlakoztatott rádióra. Így a két különböző kommunikációs rendszer használói közvetlenül kommunikálhatnak egymással.

Ennek köszönhetően azok is bekapcsolódhatnak a rádiós kommunikációba, akiknek nincs saját kézi rádiójuk: elegendő egy internetkapcsolattal rendelkező okostelefon és a Zello alkalmazás.

A lehetőségek azonban itt nem érnek véget! Ha egy másik földrajzi helyen is működik egy Zello-kapuállomás, a két kapuállomás segítségével a hagyományos rádióforgalom akár a világ másik felére is eljuthat.

**Minél több kapuállomás csatlakozik ugyanahhoz a Zello-csoporthoz, annál több földrajzi helyre juthat el az adásod.** Gondolj bele: akár otthon, a kanapén ülve, a kezedben tartott kis kézi rádióval is megszólíthatsz másik városban, országban vagy akár egy másik kontinensen lévő rádiósokat – feltéve, hogy ott is működik egy megfelelően beállított kapuállomás.

Az Orfeusz Gateway tehát **összekapcsolja a hagyományos rádiózás egyszerűségét az internet által biztosított földrajzi szabadsággal**, valódi, kétirányú kommunikációs lehetőséget teremtve a rádió és a Zello között.

> **Fontos – szükséges rádiós hardver:** az alkalmazás használatához nem elegendő egy gyári Baofeng rádió és egy egyszerű csatlakozókábel. **Átalakított Baofeng UV-5R vagy BF-888S rádió szükséges**, továbbá egy külön rádióinterfész és az interfészhez csatlakozó USB–UART adapter. Az igazolt USB–UART adapter típusa: **FTDI FT232R (VID: 0403, PID: 6001)**. A kapcsolási rajzokat és a megépített rendszer fényképeit hamarosan közzéteszem.

## A régi PC-s Zello-kapuállomások kiváltása

Az Orfeusz Gateway a korábbi, PC-n futó Zello-kliensre épülő rádiós kapuállomások Android-alapú alternatívája. A régi PC-s Zello-kliens kivezetése után sem kell feltétlenül lemondanod a már meglévő rádiós kapuállomásodról: az Orfeusz Gateway segítségével ismét használatba veheted, és a kapuállomás működését egy Android-eszközre helyezheted át.

Így a korábban kiépített rádiós rendszered – megfelelő, kompatibilis rádióval és interfésszel – tovább használható, PC-s Zello-kliens nélkül. **Fontos:** a meglévő hardver közvetlen újrahasználhatósága a kialakításától függ; az alkalmazás jelenleg az átalakított Baofeng UV-5R vagy BF-888S rádióval és az igazolt FTDI FT232R USB–UART adapterrel tesztelt.

## Szükséges hardver és dokumentáció

- Átalakított Baofeng UV-5R vagy BF-888S rádió.
- Külön rádióinterfész.
- Igazolt USB–UART adapter: FTDI FT232R (VID: 0403, PID: 6001).

**Hamarosan:** feltöltöm az átalakított rádió és a rádióinterfész kapcsolási rajzait, valamint a megépített hardverről készült fényképeket.

**Nem kell megijedni az építéstől!** Ha forrasztottál már korábban, a kapcsolási rajzok alapján minimális forrasztási és elektronikai ismerettel is meg tudod építeni. Nem szükséges hozzá komoly elektronikai szaktudás – egy kis türelem és alapvető kézügyesség elegendő.

- Csomagnév: `com.videotourzala.zellogateway`
- GitHub-repó: `szotsy/Zello-Android-Radio-Gateway`
- Alapértelmezett ág: `main`


## Hardvergaléria

A következő képek az Orfeusz Gateway rendszerének látványtervei. **AI-val készített illusztrációk, nem dokumentációs célú, hiteles fényképek a tényleges áramköri kialakításról.** A pontos bekötést és az alkatrészeket a kapcsolási rajzok, illetve az eredeti hardverfotók dokumentálják.

| A teljes rendszer | A rádióinterfész | Belső elektronikai részlet |
|---|---|---|
| ![A teljes Orfeusz Gateway rendszer látványterve](images/Gateway-system-illustration.png) | ![A rádióinterfész látványterve](images/Radio-interface-illustration.png) | ![A rádióinterfész belső részletének látványterve](images/Radio-interface-detail-illustration.png) |

## Képernyőképek

Az alábbi képek az Orfeusz Gateway felületét, valamint a rádió és az FTDI adapter állapotjelzéseit mutatják be.

| FTDI nincs csatlakoztatva | FTDI csatlakoztatva / készenlét |
|---|---|
| ![FTDI nincs csatlakoztatva](docs/screenshots/Screenshot_20261114_134559.jpg) | ![FTDI csatlakoztatva](docs/screenshots/Screenshot_20261114_134649.jpg) |

| Rádió vétel | Rádió adás |
|---|---|
| ![Rádió vétel](docs/screenshots/Screenshot_20261114_134721.jpg) | ![Rádió adás](docs/screenshots/Screenshot_20261114_134735.jpg) |

## Android-biztonsági figyelmeztetések és engedélyek

### Ha az Android figyelmeztet az alkalmazásra

Az Orfeusz Gateway-t a GitHub Releases oldalról, a Google Play Áruházon kívül lehet letölteni és telepíteni. Emiatt az Android vagy a Google Play Protect a telepítéskor biztonsági figyelmeztetést jeleníthet meg, illetve külön ellenőrzést kérhet. **Egy ilyen figyelmeztetés önmagában nem bizonyítja, hogy az alkalmazás kártékony.**

Az alkalmazást kifejezetten a Zello és a csatlakoztatott rádió közötti kétirányú hangkapcsolat, valamint az FTDI rádióinterfész vezérlésére fejlesztem. Nem célja a készülék károsítása vagy a felhasználó megtévesztése. A telepítés előtt mindig ellenőrizd, hogy az APK-t a projekt hivatalos [GitHub Releases oldaláról](https://github.com/szotsy/Zello-Android-Radio-Gateway/releases/latest) töltötted-e le. Ismeretlen forrásból származó, átnevezett vagy módosított APK telepítését nem javaslom. Ha a rendszer konkrét kártevőt azonosít, ne hagyd figyelmen kívül a jelzést; ellenőrizd a fájl eredetét és a kiadás hitelességét.

### Szükséges Android-engedélyek

A hibátlan működéshez az alkalmazás által ténylegesen kért Android-engedélyeket meg kell adni. Az engedélyek megtagadása vagy későbbi visszavonása egyes funkciókat – például a hangkezelést vagy a háttérben történő működést – korlátozhatja, ezért a Zello és a rádió közötti kapcsolat nem feltétlenül fog megfelelően működni.

- Első indításkor olvasd el az Android engedélykéréseit, és add meg az alkalmazás működéséhez kért engedélyeket.
- USB-s FTDI adapter csatlakoztatásakor engedélyezd az Android által megjelenített USB-eszköz-hozzáférést is.
- Ha korábban megtagadtál egy engedélyt, az Android **Beállítások → Alkalmazások → Orfeusz Gateway → Engedélyek** menüpontjában ellenőrizheted és módosíthatod. A menüpontok neve Android-verziónként és gyártónként eltérhet.
- Az engedélyeket csak a hivatalos alkalmazásnak add meg, és csak az Android által ténylegesen felkínált kéréseket hagyd jóvá.

## Kiadási állapot

- Legfrissebb publikált GitHub Release: **1.10.54**.
- Version Code: **91**.
- Az 1.10.54 APK letölthető a [GitHub Releases oldalról](https://github.com/szotsy/Zello-Android-Radio-Gateway/releases/latest).
- Új GitHub Release csak a ténylegesen lefordított és ellenőrzött APK-val készüljön.

## Frissítési rendszer

### Régi telepítések migrációja

A gyökérben lévő `update.json` szándékosan megmarad. A régi, JSON-alapú frissítést használó telepítéseket az **1.10.46** migrációs verzióra irányítja. Törölni vagy átírni csak külön migrációs döntés alapján szabad.

### Új frissítési rendszer

Az 1.10.46-tól az alkalmazás a GitHub Releases API-n keresztül keresi a legújabb stabil kiadást:

`https://api.github.com/repos/szotsy/Zello-Android-Radio-Gateway/releases/latest`

Az alkalmazás a GitHub Release tagjét a telepített Gradle-verzióval hasonlítja össze. APK-assetet csak akkor keres, ha valóban újabb kiadás érhető el.

## APK-elnevezés

A release tag és az APK neve egyezzen a kiadás verziójával. Például az 1.10.50 kiadás APK assetje:

`Orfeusz.Gateway_v1.10.50.apk`

## Hardverkompatibilitás

**Igazolt adapter: FTDI FT232R – VID: 0403, PID: 6001.**

Az alkalmazás jelenleg kizárólag az FTDI FT232R USB–UART adapterrel tesztelt és igazoltan működőképes. Más FTDI típusok, CH340G és egyéb USB–UART adapterek támogatása nem igazolt, működésük nem garantált.

## Üzembiztonság

- Az FTDI RTS/CTS és PTT vezérlés a kapuállomás kritikus működési része.
- Más funkciók vagy felületi elemek módosításakor a rádióvezérlési logikát nem szabad indokolatlanul megváltoztatni.
- A „Zello telepítve” jelzés nem bizonyítja az élő Zello-kapcsolatot.
- A frissítés kézzel indítható; automatikus háttér-ellenőrzés és automatikus telepítés nincs.

## Fejlesztési szabályok

- A Gradle `versionName` és `versionCode`, az alkalmazásban megjelenő verzió, a diagnosztikai napló és a kiadási leírás legyen összhangban.
- Az alkalmazás verzióját a kód a Gradle által generált BuildConfig adatokból olvassa.
- A forrásjelölt AndroidIDE-ben történő buildelése és tesztelése kötelező a publikálás előtt.
- A teljes AndroidIDE-forrásprojekt külön, verziószámmal elnevezett ZIP-csomagban készül.
