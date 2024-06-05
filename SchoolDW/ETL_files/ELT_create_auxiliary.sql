USE master;
CREATE DATABASE auxiliary;
GO

USE auxiliary;

CREATE TABLE vacations(start DATETIME, koniec DATETIME, PRIMARY KEY(start,koniec));

USE master;
GO