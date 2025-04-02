# Ruokareseptit
Sovelluksen idea on, että käyttäjät pystyvät jakamaan ruokareseptejä.

## Sovelluksen tämänhetkinen tilanne:

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään sovellukseen reseptejä sekä muokkaamaan ja poistamaan omia reseptejään.
- Käyttäjä pystyy lisäämään kuvia reseptiin.
- Käyttäjä näkee kaikkien käyttäjien sovellukseen lisäämät reseptit.
- Käyttäjä pystyy etsimään hakusanalla sekä omia että muiden käyttäjien lisäämiä reseptejä.
- Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.
- Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun, kuten ruokalajin (esim. keitot, salaatit, pastat) tai erityisruokavalion (esim. gluteeniton, vegaaninen).
- Käyttäjä pystyy antamaan reseptille arvostelun sisältäen kommentin ja arvosanan. Reseptistä näytetään eri käyttäjien antamat arvostelut.

## Sovellukseen suunnitteilla olevat ominaisuudet:

- Reseptistä näytetään arvosanojen keskiarvo.

## Sovelluksen asennus:

Asenna `flask`-kirjasto:
```
$ pip install flask
```


Luo tietokannan taulut ja lisää alkutiedot:
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```
Käynnistä sovellus:
```
$ flask run
```
