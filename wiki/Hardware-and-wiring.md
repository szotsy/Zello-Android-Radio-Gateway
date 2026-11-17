# Hardver és bekötés / Hardware and wiring

> **A fejezet később további fotókkal és feliratozott ábrákkal bővül. / More photos and annotated illustrations will be added later.**

## Magyar

### USB–UART adapter
A támogatott, tesztelés alatt álló és még nem igazolt adapterek aktuális státuszát a [nyilvános USB–UART kompatibilitási lista](https://szotsy.github.io/Zello-Android-Radio-Gateway/usb-uart-compatibility.html) tartalmazza. Vásárlás előtt mindig ezt ellenőrizd. A konkrét adapterpanelen a CTS, GND és RTS jeleknek ténylegesen elérhetőknek kell lenniük; a chip neve önmagában nem garantálja a kompatibilitást.

### Kapcsolási rajz

![Orfeusz Gateway – hivatalos kapcsolási rajz](../docs/assets/OG-kapcsolasi-rajz.png)

[A kapcsolási rajz megnyitása teljes méretben / Open the wiring diagram at full size](../docs/assets/OG-kapcsolasi-rajz.png)

### Csatlakozók

**Con1 – rádió csatlakozó**
| Érintkező | Funkció |
|---|---|
| 1 | Squelch |
| 2 | GND |
| 3 | PTT |
| 4 | Speaker |
| 5 | MIC |

**Con2 – USB–UART adapter felőli csatlakozó**
| Érintkező | Funkció |
|---|---|
| A | CTS |
| B | GND |
| C | RTS |

**Figyelem:** a bekötés módosítása előtt ellenőrizd a rádió és az adapter pontos típusát, valamint a csatlakozó nézetét. A hibás bekötés károsíthatja az eszközöket. Ne végezz bekötési módosítást feszültség alatt.

### Később hozzáadandó képek
- A Con1 és Con2 csatlakozók fényképe, nézeti iránnyal.
- A projekt ellenőrzött kapcsolási rajza.
- USB–UART adapter fényképe (szemléltető; vásárlás előtt ellenőrizd a kompatibilitási listát).
- Rádióoldali csatlakozás részletei.

## English

### USB–UART adapter
The current status of verified, under-test and not-yet-verified adapters is published in the [public USB–UART compatibility list](https://szotsy.github.io/Zello-Android-Radio-Gateway/usb-uart-compatibility-en.html). Always check it before purchasing. The exact breakout board must physically expose CTS, GND and RTS; the chip name alone does not guarantee compatibility.

### Connectors

**Con1 – radio connector**
| Pin | Function |
|---|---|
| 1 | Squelch |
| 2 | GND |
| 3 | PTT |
| 4 | Speaker |
| 5 | MIC |

**Con2 – USB–UART adapter-side connector**
| Pin | Function |
|---|---|
| A | CTS |
| B | GND |
| C | RTS |

**Warning:** before changing any wiring, verify the exact radio and adapter models and the connector viewing orientation. Incorrect wiring may damage equipment. Never modify wiring while powered.

### Images to add later
- Photos of Con1 and Con2 with viewing orientation.
- The project's verified wiring diagram.
- USB–UART adapter photo (illustrative only; check the compatibility list before purchasing).
- Radio-side connector details.
