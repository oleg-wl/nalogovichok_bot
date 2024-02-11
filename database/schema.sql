CREATE TABLE IF EXISTS bot_users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(256),
    chat_id INTEGER
);