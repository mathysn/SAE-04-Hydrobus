DROP TABLE IF EXISTS changement_reservoir;
DROP TABLE IF EXISTS incident;
DROP TABLE IF EXISTS kilometrage;
DROP TABLE IF EXISTS bus;
DROP TABLE IF EXISTS revision;
DROP TABLE IF EXISTS reservoir;
DROP TABLE IF EXISTS modele;
DROP TABLE IF EXISTS type_incident;

CREATE TABLE modele(
    code_modele INT(25) AUTO_INCREMENT,
    libelle_modele VARCHAR(255),
    infos_modele VARCHAR(255),
    volume_reservoir DECIMAL(5,2),
    PRIMARY KEY (code_modele)
);

CREATE TABLE reservoir(
    id_reservoir INT(25) AUTO_INCREMENT,
    code_modele INT(25),
    PRIMARY KEY (id_reservoir),
    FOREIGN KEY (code_modele) REFERENCES modele(code_modele)
);

CREATE TABLE bus(
    id_bus INT(25) AUTO_INCREMENT,
    date_achat DATE,
    conso_annuelle DECIMAL(7,2),
    id_reservoir INT(25),
    PRIMARY KEY (id_bus),
    CONSTRAINT bus_fk FOREIGN KEY (id_reservoir) REFERENCES reservoir(id_reservoir)
);

CREATE TABLE changement_reservoir(
    id_changement INT(25) AUTO_INCREMENT,
    date_changement DATE NOT NULL,
    id_bus INT(25),
    PRIMARY KEY (id_changement),
    CONSTRAINT FOREIGN KEY (id_bus) REFERENCES bus(id_bus)
);

CREATE TABLE revision(
    id_revision INT(25) AUTO_INCREMENT,
    descriptif_revision VARCHAR(255),
    date_revision DATE,
    id_reservoir INT(25),
    PRIMARY KEY (id_revision),
    FOREIGN KEY (id_reservoir) REFERENCES reservoir(id_reservoir)
);

CREATE TABLE type_incident(
    id_type_incident INT(25) AUTO_INCREMENT,
    infos_type_incident VARCHAR(255),
    PRIMARY KEY (id_type_incident)
);

CREATE TABLE incident(
    id_incident INT(25) AUTO_INCREMENT,
    date_incident DATE NOT NULL,
    id_bus INT(25),
    id_type_incident INT(25),
    PRIMARY KEY (id_incident),
    FOREIGN KEY (id_bus) REFERENCES bus(id_bus),
    FOREIGN KEY (id_type_incident) REFERENCES type_incident(id_type_incident)
);

CREATE TABLE kilometrage(
    date_periode DATE,
    nombre_km DECIMAL(7,2),
    id_bus INT(25),
    PRIMARY KEY (date_periode),
    FOREIGN KEY (id_bus) REFERENCES bus(id_bus)
);

INSERT INTO modele (code_modele, libelle_modele, infos_modele, volume_reservoir)
VALUES (NULL, 'Reservoir300', "Un réservoir de volume 300L", 300),
       (NULL, 'Reservoir200', "Un réservoir de volume 300L", 200.00),
       (NULL, 'Reservoir600', "Un réservoir de volume 300L", 600);

INSERT INTO reservoir (id_reservoir, code_modele)
VALUES (NULL, 2),
       (NULL, 2),
       (NULL, 1);

INSERT INTO bus (id_bus, date_achat, conso_annuelle, id_reservoir)
VALUES (NULL, '2011-12-02', 1677.25, 1),
       (NULL, '2012-03-14', 4300, 2),
       (NULL, '2022-04-27', 0, 3);

INSERT INTO changement_reservoir (id_changement, date_changement, id_bus)
VALUES (NULL, '2050-03-14', 2),
       (NULL, '2002-11-22', 1),
       (NULL, '2020-09-10', 3);

INSERT INTO revision (id_revision, descriptif_revision, date_revision, id_reservoir)
VALUES (NULL, 'RAS', '2020-09-10', 2),
       (NULL, 'rien ne va', '2222-02-22', 1);

INSERT INTO type_incident (id_type_incident, infos_type_incident)
VALUES (NULL, "carambolage");

INSERT INTO incident (id_incident, date_incident, id_bus, id_type_incident)
VALUES (NULL, '2020-12-20', 2, 1),
       (NULL, '2021-12-20', 3, 1);

INSERT INTO kilometrage (date_periode, nombre_km, id_bus)
VALUES ('2020-12-12', 1200.5, 1);

SELECT * FROM modele;
SELECT * FROM reservoir;
SELECT * FROM bus;
SELECT * FROM changement_reservoir;
SELECT * FROM revision;
SELECT * FROM type_incident;
SELECT * FROM incident;
SELECT * FROM kilometrage;