CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    area TEXT,
    role INTEGER,
    creator_name TEXT
);

CREATE TABLE chains (
    id SERIAL PRIMARY KEY,
    chain TEXT,
    area_id INTEGER,
    area_name TEXT,
    creator_id INTEGER,
    creator_name TEXT
);

CREATE TABLE chain_messages (
    id SERIAL PRIMARY KEY,
    message TEXT,
	sent_at TIMESTAMP,
    chain_id INTEGER,
    chain_name TEXT,
    creator_id INTEGER,
    creator_name TEXT
);

CREATE TABLE private_areas (
    id SERIAL PRIMARY KEY,
    area_name TEXT,
    user_name TEXT,
    area_id INTEGER,
    user_id INTEGER
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    role INTEGER
);
