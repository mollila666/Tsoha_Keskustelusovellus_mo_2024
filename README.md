Sovelluksen nykyinen tilanne:

Sovelluksella on toimiva pohja ja alla listatut toiminnot toimivat:

	Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
	Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
	Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
	Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
	Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
	Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
	Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
	Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

Sovelluksen ulkoasu on vaiheessa ja hyvin pelkistetty. Tämä on tarkoitus tehdä seuraavaksi, kun palaute palautteesta II on saatu.

Testaus ohjeet:

Sovellus ei ole testattavissa Fly.iossa.

Kloonaa tämä repositorio omalle koneellesi ja siirry sen juurikansioon. Luo kansioon .env-tiedosto ja määritä sen sisältö seuraavanlaiseksi:

DATABASE_URL=<tietokannan-paikallinen-osoite>
SECRET_KEY=<salainen-avain>

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla:

$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt

Määritä vielä tietokannan skeema komennolla

$ psql < schema.sql

Nyt voit käynnistää sovelluksen komennolla

$ flask run

################################################################################################################
# palautus I alla
#################################################################################################################

Keskustelusovellus

Sovellus seuraa pääsääntöisesti kurssimateriaalissa listattuja esimerkki aiheen toiminnallisuuksia:

Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.
Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

Sovellus perustuu 5 taulukkoon, areas hallitsee keskustelu-alueita, chains hallitsee ketjuja, chain_messages hallitsee viestejä, users käyttäjiä ja private_areas salaiset alueet.

CREATE TABLE areas ( id SERIAL PRIMARY KEY, area TEXT, role INTEGER, user_id INTEGER );

CREATE TABLE chains ( id SERIAL PRIMARY KEY, chain TEXT, area_id INTEGER, creator_id INTEGER );

CREATE TABLE chain_messages ( id SERIAL PRIMARY KEY, message TEXT, sent_at TIMESTAMP, chain_id INTEGER, creator_id INTEGER );

CREATE TABLE users ( id SERIAL PRIMARY KEY, name TEXT, password TEXT, role INTEGER );

CREATE TABLE private_areas (id SERIAL PRIMARY KEY, area TEXT, user TEXT, area_id INTEGER, user_id INTEGER);

Sovellukseni vaatii; from sqlalchemy.sql import text. Ja execute-funktion kutsuissa SQL-komennon ympärille funktio text.

Sovellus ei ole testattavissa Fly.iossa.
