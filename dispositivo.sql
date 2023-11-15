-- Exclua a tabela tv se ela existir
DROP TABLE IF EXISTS tv;

-- Crie a tabela tv
CREATE TABLE tv (
    IP VARCHAR(15) PRIMARY KEY,
    porta INT NOT NULL,
    valor INT NOT NULL,
    `status` INT NOT NULL DEFAULT 1,
    apelido VARCHAR(255) NOT NULL
);

-- Exclua a tabela lampada se ela existir
DROP TABLE IF EXISTS lampada;

-- Crie a tabela lampada
CREATE TABLE lampada (
    IP VARCHAR(15) PRIMARY KEY,
    porta INT NOT NULL,
    valor VARCHAR(255) NOT NULL,
    `status` INT NOT NULL DEFAULT 1,
    apelido VARCHAR(255) NOT NULL
);

-- Exclua a tabela ar_condicionado se ela existir
DROP TABLE IF EXISTS ar_condicionado;

-- Crie a tabela ar_condicionado
CREATE TABLE ar_condicionado (
    IP VARCHAR(15) PRIMARY KEY,
    porta INT NOT NULL,
    valor INT NOT NULL,
    `status` INT NOT NULL DEFAULT 1,
    apelido VARCHAR(255) NOT NULL
);
