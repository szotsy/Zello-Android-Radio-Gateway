# Hardver és bekötés / Hardware and wiring

> **A fejezetet később fotókkal és feliratozott bekötési képekkel egészítjük ki. / Photos and annotated wiring illustrations will be added later.**

## Magyar

### Ellenőrzött adapter
Az alkalmazással ellenőrzött USB–soros adapter az **FTDI FT232R**:
- VID: `0403`
- PID: `6001`

Más USB–soros adapterek (például CH340-alapú típusok) működése nincs igazolva.

### Csatlakozók

**Con1 – rádió csatlakozó**
| Érintkező | Funkció |
|---|---|
| 1 | Squelch |
| 2 | GND |
| 3 | PTT |
| 4 | Speaker |
| 5 | MIC |

**Con2 – FTDI csatlakozó**
| Érintkező | Funkció |
|---|---|
| A | CTS |
| B | GND |
| C | RTS |

**Figyelem:** a bekötés módosítása előtt ellenőrizd a rádió és az adapter pontos típusát, valamint a csatlakozó nézetét. A hibás bekötés károsíthatja az eszközöket. Ne végezz bekötési módosítást feszültség alatt.

### Később hozzáadandó képek
- A Con1 és Con2 csatlakozók fényképe, nézeti iránnyal.
- A projekt ellenőrzött kapcsolási rajza.
- FTDI FT232R adapter fényképe.
- Rádióoldali csatlakozás részletei.

## English

### Verified adapter
The USB-to-serial adapter verified with the application is **FTDI FT232R**:
- VID: `0403`
- PID: `6001`

Operation with other USB-to-serial adapters (including CH340-based models) has not been verified.

### Connectors

**Con1 – radio connector**
| Pin | Function |
|---|---|
| 1 | Squelch |
| 2 | GND |
| 3 | PTT |
| 4 | Speaker |
| 5 | MIC |

**Con2 – FTDI connector**
| Pin | Function |
|---|---|
| A | CTS |
| B | GND |
| C | RTS |

**Warning:** before changing any wiring, verify the exact radio and adapter models and the connector viewing orientation. Incorrect wiring may damage equipment. Never modify wiring while powered.

### Images to add later
- Photos of Con1 and Con2 with viewing orientation.
- The project's verified wiring diagram.
- FTDI FT232R adapter photo.
- Radio-side connector details.
