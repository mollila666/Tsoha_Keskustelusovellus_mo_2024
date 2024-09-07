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

Sovellus perustuu 4 taulukkoon, areas hallitsee keskustelu-alueita, chains hallitsee ketjuja, chain_messages hallitsee viestejä ja users käyttäjiä.

CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    area TEXT,
    role INTEGER,
    user_id INTEGER
);

CREATE TABLE chains (
    id SERIAL PRIMARY KEY,
    chain TEXT,
    area_id INTEGER REFERENCES areas,
    creator_id INTEGER
);

CREATE TABLE chain_messages (
    id SERIAL PRIMARY KEY,
    message TEXT,
	sent_at TIMESTAMP,
    chain_id INTEGER REFERENCES chains,
    creator_id INTEGER
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    role INTEGER
);
Sovellukseni vaatii; from sqlalchemy.sql import text. Ja execute-funktion kutsuissa SQL-komennon ympärille funktio text.

Sovellus ei ole testattavissa Fly.iossa.
