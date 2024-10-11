CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    role INTEGER
);

CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    area TEXT,
    role INTEGER,
    creator_name TEXT
);

CREATE TABLE private_areas (
    id SERIAL PRIMARY KEY,
    area_name TEXT,
    user_name TEXT,
    area_id INTEGER REFERENCES areas
);

CREATE TABLE chains (
    id SERIAL PRIMARY KEY,
    chain TEXT,
    area_id INTEGER REFERENCES areas,
    creator_name TEXT
);

CREATE TABLE chain_messages (
    id SERIAL PRIMARY KEY,
    message TEXT,
	sent_at TIMESTAMP,
    chain_id INTEGER REFERENCES chains,
    creator_name TEXT
);

