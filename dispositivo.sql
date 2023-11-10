-- Exclua a tabela tv se ela existir
DROP TABLE IF EXISTS tv;

-- Crie a tabela tv
CREATE TABLE tv (
    id INT AUTO_INCREMENT PRIMARY KEY,
    IP VARCHAR(15) NOT NULL,
    porta INT NOT NULL,
    valor INT NOT NULL,
    `status` INT NOT NULL DEFAULT 1
);

-- Exclua a tabela lampada se ela existir
DROP TABLE IF EXISTS lampada;

-- Crie a tabela lampada
CREATE TABLE lampada (
    id INT AUTO_INCREMENT PRIMARY KEY,
    IP VARCHAR(15) NOT NULL,
    porta INT NOT NULL,
    valor VARCHAR(255) NOT NULL,
    `status` INT NOT NULL DEFAULT 1
);

-- Exclua a tabela ar_condicionado se ela existir
DROP TABLE IF EXISTS ar_condicionado;

-- Crie a tabela ar_condicionado
CREATE TABLE ar_condicionado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    IP VARCHAR(15) NOT NULL,
    porta INT NOT NULL,
    valor INT NOT NULL,
    `status` INT NOT NULL DEFAULT 1
);
