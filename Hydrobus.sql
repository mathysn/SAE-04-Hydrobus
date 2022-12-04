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
    PRIMARY KEY (code_modele)
);

CREATE TABLE reservoir(
    id_reservoir INT(25) AUTO_INCREMENT,
    volume_reservoir DECIMAL(5,2),
    code_modele INT(25),
    PRIMARY KEY (id_reservoir),
    FOREIGN KEY (code_modele) REFERENCES modele(code_modele) ON DELETE CASCADE
);

CREATE TABLE bus(
    id_bus INT(25) AUTO_INCREMENT,
    date_achat DATE NOT NULL,
    conso_annuelle DECIMAL(7,2),
    id_reservoir INT(25),
    PRIMARY KEY (id_bus),
    FOREIGN KEY (id_reservoir) REFERENCES reservoir(id_reservoir) ON DELETE CASCADE
);

CREATE TABLE changement_reservoir(
    id_changement INT(25) AUTO_INCREMENT,
    date_changement DATE NOT NULL,
    id_bus INT(25) NOT NULL,
    PRIMARY KEY (id_changement),
    FOREIGN KEY (id_bus) REFERENCES bus(id_bus) ON DELETE CASCADE
);

CREATE TABLE revision(
    id_revision INT(25) AUTO_INCREMENT,
    descriptif_revision VARCHAR(255),
    date_revision DATE NOT NULL,
    id_reservoir INT(25),
    PRIMARY KEY (id_revision),
    FOREIGN KEY (id_reservoir) REFERENCES reservoir(id_reservoir) ON DELETE CASCADE
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
    FOREIGN KEY (id_bus) REFERENCES bus(id_bus) ON DELETE CASCADE,
    FOREIGN KEY (id_type_incident) REFERENCES type_incident(id_type_incident) ON DELETE CASCADE
);

CREATE TABLE kilometrage(
    id_kilometrage INT(25) AUTO_INCREMENT,
    date_periode DATE NOT NULL,
    nombre_km DECIMAL(7,2),
    id_bus INT(25),
    PRIMARY KEY (id_kilometrage),
    FOREIGN KEY (id_bus) REFERENCES bus(id_bus) ON DELETE CASCADE
);

INSERT INTO modele (code_modele, libelle_modele, infos_modele)
VALUES (NULL, 'M-23L', "Pour un bus double"),
       (NULL, 'XL-17L', "Pour un bus triple"),
       (NULL, 'XS-41M', "Pour un bus simple");

INSERT INTO reservoir (id_reservoir, volume_reservoir, code_modele)
VALUES (NULL, 200.00, 2),
       (NULL, 350.00, 2),
       (NULL, 140.00, 1);

INSERT INTO bus (id_bus, date_achat, conso_annuelle, id_reservoir)
VALUES (NULL, '2011-12-02', 1677.25, 2),
       (NULL, '2012-03-14', 4300, 1),
       (NULL, '2022-04-27', 0, 3);

INSERT INTO changement_reservoir (id_changement, date_changement, id_bus)
VALUES (NULL, '2050-03-14', 2),
       (NULL, '2002-11-22', 1),
       (NULL, '2020-09-10', 3),
       (NULL, '2020-09-10', 2),
       (NULL, '2020-09-10', 2),
       (NULL, '2020-09-10', 1),
       (NULL, '2020-09-10', 3),
       (NULL, '2020-09-10', 3);

INSERT INTO revision (id_revision, descriptif_revision, date_revision, id_reservoir)
VALUES (NULL, 'RAS', '2020-09-10', 2),
       (NULL, 'Rien ne va', '2222-02-22', 1),
       (NULL, 'RAS', '2222-02-22', 3),
       (NULL, "Moteur à changer", '2222-02-22', 2);

INSERT INTO type_incident (id_type_incident, infos_type_incident)
VALUES (NULL, "Carambolage");

INSERT INTO incident (id_incident, date_incident, id_bus, id_type_incident)
VALUES (NULL, '2020-12-20', 2, 1),
       (NULL, '2021-12-20', 3, 1);

INSERT INTO kilometrage (id_kilometrage, date_periode, nombre_km, id_bus)
VALUES (NULL, '2020-12-12', 1200.5, 1),
       (NULL, '2021-01-12', 3000, 1),
       (NULL, '2021-02-12', 231, 1),
       (NULL, '2021-03-12', 5425, 1),
       (NULL, '2021-04-12', 3020, 2),
       (NULL, '2021-05-12', 545, 2),
       (NULL, '2021-06-12', 1535, 2),
       (NULL, '2021-07-12', 10526, 3),
       (NULL, '2021-08-12', 3020, 3);