CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin INTEGER
);

CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE,
    user_id INTEGER REFERENCES users
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title TEXT,
    subject_id INTEGER REFERENCES subjects,
    user_id INTEGER REFERENCES users,
    visible BOOLEAN
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads,
    sent_at TIMESTAMP,
    visible BOOLEAN
);
