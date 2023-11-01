CREATE TABLE IF NOT EXISTS administrators(
    administrator_id integer NOT NULL PRIMARY KEY, 
    account_name varchar(50));
CREATE TABLE IF NOT EXISTS moderators(
    moderator_id INTEGER NOT NULL PRIMARY KEY, 
    account_name varchar(50));

CREATE TABLE IF NOT EXISTS channels(
    channel_id varchar(100) NOT NULL PRIMARY KEY,
    telegram_id integer NOT NULL, 
    channel_name varchar(50) NOT NULL, 
    reply_id integer DEFAULT NONE);

CREATE TABLE IF NOT EXISTS sub_preferences(
    subscriber_id INTEGER NOT NULL PRIMARY KEY REFERENCES subscribers(subscriber_id));
CREATE TABLE IF NOT EXISTS subscribers(
    subscriber_id INTEGER NOT NULL PRIMARY KEY, 
    expired_date DATE NOT NULL);