
DROP TABLE restaurants;
DROP TABLE votes;
DROP TABLE employees;

CREATE TABLE IF NOT EXISTS restaurants (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title VARCHAR NOT NULL UNIQUE,
  description TEXT,
  street TEXT,
  count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS employees (
  email VARCHAR PRIMARY KEY,
  name VARCHAR
);

CREATE TABLE IF NOT EXISTS votes (
  date DATE,
  restaurant_id INTEGER,
  email VARCHAR,
  PRIMARY KEY (date, email)
);

CREATE TABLE IF NOT EXISTS counts (
  restaurant_id INTEGER PRIMARY KEY,
  counts INTEGER
);

INSERT INTO restaurants (title) VALUES ('B5');
INSERT INTO restaurants (title) VALUES ('Piazetta');
INSERT INTO restaurants (title) VALUES ('Bernerhof');
INSERT INTO restaurants (title) VALUES ('Chrigus Beck');

INSERT INTO employees(email, name) VALUES ('sw@studer-raimann.ch', 'Stefan Wanzenried');
INSERT INTO employees(email, name) VALUES ('fs@studer-raimann.ch', 'Fabian Schmid');
INSERT INTO employees(email, name) VALUES ('rb@studer-raimann.ch', 'Robin Baumgartner');
INSERT INTO employees(email, name) VALUES ('ot@studer-raimann.ch', 'Oskar Truffer');
INSERT INTO employees(email, name) VALUES ('tt@studer-raimann.ch', 'Theodor Truffer');
INSERT INTO employees(email, name) VALUES ('pz@studer-raimann.ch', 'Patricia Zuber');
INSERT INTO employees(email, name) VALUES ('gc@studer-raimann.ch', 'Gabriel Comte');
INSERT INTO employees(email, name) VALUES ('mr@studer-raimann.ch', 'Marcel Raimann');
INSERT INTO employees(email, name) VALUES ('ns@studer-raimann.ch', 'Nicolas Schäfli');
INSERT INTO employees(email, name) VALUES ('ss@studer-raimann.ch', 'Silas Stulz');
INSERT INTO employees(email, name) VALUES ('nm@studer-raimann.ch', 'Nicolas Märchy');
INSERT INTO employees(email, name) VALUES ('ms@studer-raimann.ch', 'Martin Studer');
INSERT INTO employees(email, name) VALUES ('jg@studer-raimann.ch', 'Johnny Gerber');