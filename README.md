# Ohjelmistotekniikka, harjoitustyö

Deep Learning Anti-Cheat (DLAC) on projekti joka analysoi pelaajia CSGO pelissä ja ennustaa käyttääkö pelaaja jotain avustusta jota ei saisi. 

## Asennus
```bash
poetry install
```


## Voit kokeilla sovellusta ajamalla
```bash
poetry run invoke start
```
Tämän pitäisi antaa terminaaliin ennustuksia. Mikäli kaikki sujuu kuten pitäisi, tulisi näkyä seuraavanlaisia rivejä:

```python
Confidence               Name                 STEAMID              Tick                       Demo
0.99811625       公雞Im💕Ur💕Crush公雞   76561199056381450       47400   match730_003418900824254841096_1146197551_182.dem
...
```
Voimme käydä tarkistamassa pelaajan profiilin Steamin kautta:
https://steamcommunity.com/profiles/76561199056381450/

Kappas vaan, pelaajalla on pelikielto sopivasti pelin aikoihin...

## Testit
```
poetry run invoke test
```

## Testikattavuusraportti
```
poetry run invoke coverage-report
```

## Dokumentaatio
- [Vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)
- [Tuntikirjanpito](./dokumentaatio/tuntikirjanpito.md)
