DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
  username TEXT NOT NULL ,
  password TEXT NOT NULL
)