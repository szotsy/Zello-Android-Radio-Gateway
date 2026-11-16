# Hibaelhárítás / Troubleshooting

> **A hibaelhárítási folyamat később képernyőképekkel és példákkal egészül ki. / Screenshots and examples will be added later.**

## Magyar

### Az USB–UART adapter nem jelenik meg
- Ellenőrizd az USB-kábelt és az OTG/USB-csatlakozást.
- A megbízható működés jelenleg az FTDI FT232R adapterrel igazolt (VID 0403, PID 6001); más adapterek kompatibilitása még nem igazolt.
- Csatlakoztatáskor fogadd el az Android USB-engedélykérését, ha megjelenik.

### Nincs rádióvétel (RX)
- Ellenőrizd a rádió és a Con1 csatlakozó közötti bekötést.
- Ellenőrizd a Squelch jel és a GND csatlakozását.
- Ne változtass találomra a lábkiosztáson.

### A PTT / adás nem működik
- Ellenőrizd a PTT-vezeték és az FTDI-illesztés dokumentált bekötését.
- Ellenőrizd a csatlakozó tájolását és a rádió kompatibilitását.
- Ne tesztelj adást olyan frekvencián vagy módon, amelyre nincs jogosultságod.

### Hangprobléma
- Ellenőrizd a rádió hangcsatlakozásait és a hangerőszinteket.
- Ellenőrizd az Android hangkimeneti beállításait.

### Hibabejelentés
Ha a hiba továbbra is fennáll, a [GitHub hibabejelentő sablonok](https://github.com/szotsy/Zello-Android-Radio-Gateway/issues/new/choose) segítségével küldd be. A verziószámot, készüléktípust, reprodukciós lépéseket és – személyes adatoktól megtisztított – naplókat is mellékeld.

## English

### USB–UART adapter is not detected
- Check the USB cable and OTG/USB connection.
- Reliable operation is currently verified with the FTDI FT232R adapter (VID 0403, PID 6001); other adapters are not yet verified.
- Accept Android's USB permission prompt when it appears.

### No radio receive (RX)
- Check the wiring between the radio and the Con1 connector.
- Verify the Squelch signal and GND connection.
- Do not guess or randomly change pin assignments.

### PTT / transmit does not work
- Check the documented PTT wiring and FTDI interface.
- Verify connector orientation and radio compatibility.
- Do not transmit on frequencies or in ways for which you are not authorized.

### Audio problem
- Check the radio audio connections and volume levels.
- Check Android audio output settings.

### Report an issue
If the problem persists, use the [GitHub issue templates](https://github.com/szotsy/Zello-Android-Radio-Gateway/issues/new/choose). Include the app version, device model, reproduction steps and logs with personal information removed.
