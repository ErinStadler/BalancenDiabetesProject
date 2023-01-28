CREATE TABLE users_profile (
    user_id serial PRIMARY KEY,
    email VARCHAR unique NOT NULL,
    password VARCHAR NOT NULL,
    min_range INTEGER DEFAULT 70,
    max_range INTEGER DEFAULT 200,
    name VARCHAR NOT NULL
);

CREATE TABLE bloodsugars (
    bs_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users_profile(user_id) NOT NULL,
    bloodsugar INTEGER NOT NULL,
    input_date TIMESTAMP NOT NULL DEFAULT current_TIMESTAMP
);

CREATE TABLE insulin (
    insulin_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users_profile(user_id) NOT NULL,
    insulin_use INTEGER NOT NULL,
    input_date TIMESTAMP NOT NULL DEFAULT current_TIMESTAMP
)