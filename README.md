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
Tämän pitäisi avata file explorer jolla pysyt navigoimaan src/csvs kansioon 
ja valita csv tiedosto. Parin sekunnin jälkeen pitäisi avautua seuraavanlainen ikkuna:
![](./dokumentaatio/kuvat/example_output.png)



Voimme myös käydä tarkistamassa pelaajan profiilin Steamin kautta:
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
- [Changelog](./dokumentaatio/changelog.md)
- [Arkkitehtuuri](./dokumentaatio/arkkitehtuuri.md)