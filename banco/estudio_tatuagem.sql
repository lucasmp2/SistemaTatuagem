CREATE DATABASE IF NOT EXISTS estudio_tatuagem
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE estudio_tatuagem;

CREATE TABLE IF NOT EXISTS senioridade (
    idsenioridade INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS estilo (
    idestilo INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tatuador (
    idtatuador INT AUTO_INCREMENT PRIMARY KEY,
    nometatuador VARCHAR(100) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    email VARCHAR(100),
    telefone VARCHAR(20),
    datacontratacao DATE,
    idsenioridade INT NOT NULL,
    CONSTRAINT fk_tatuador_senioridade FOREIGN KEY (idsenioridade)
        REFERENCES senioridade(idsenioridade)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tatuador_estilo (
    idtatuador INT NOT NULL,
    idestilo INT NOT NULL,
    dataestilo DATE,
    PRIMARY KEY (idtatuador, idestilo),
    CONSTRAINT fk_tatuador_estilo_tatuador FOREIGN KEY (idtatuador)
        REFERENCES tatuador(idtatuador),
    CONSTRAINT fk_tatuador_estilo_estilo FOREIGN KEY (idestilo)
        REFERENCES estilo(idestilo)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS cliente (
    idcliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    datacadastro DATE,
    cidade VARCHAR(100),
    uf CHAR(2)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS agendamento (
    idagendamento INT AUTO_INCREMENT PRIMARY KEY,
    idcliente INT DEFAULT NULL,
    idtatuador INT NOT NULL,
    dataagendamento DATE NOT NULL,
    horaagendamento TIME NOT NULL,
    descricaotatuagem TEXT,
    desenhoaprovado VARCHAR(255),
    valortatuagem DECIMAL(10, 2),
    status ENUM('pendente', 'confirmado', 'concluido', 'cancelado')
        NOT NULL DEFAULT 'pendente',
    CONSTRAINT fk_agendamento_cliente FOREIGN KEY (idcliente)
        REFERENCES cliente(idcliente) ON DELETE SET NULL,
    CONSTRAINT fk_agendamento_tatuador FOREIGN KEY (idtatuador)
        REFERENCES tatuador(idtatuador)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS usuario (
    idusuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('admin', 'funcionario', 'cliente') NOT NULL DEFAULT 'funcionario',
    idcliente INT DEFAULT NULL,
    CONSTRAINT fk_usuario_cliente FOREIGN KEY (idcliente)
        REFERENCES cliente(idcliente) ON DELETE SET NULL
) ENGINE=InnoDB;

INSERT IGNORE INTO senioridade (idsenioridade, nome) VALUES
    (1, 'Júnior'), (2, 'Pleno'), (3, 'Sênior');

INSERT IGNORE INTO estilo (idestilo, descricao) VALUES
    (1, 'Blackwork'), (2, 'Aquarela'), (3, 'Realismo'), (4, 'Old School');

INSERT IGNORE INTO tatuador
    (idtatuador, nometatuador, cpf, email, telefone, datacontratacao, idsenioridade)
VALUES
    (1, 'Lucas Mendes', '11111111111', 'lucas@estudio.com', '11999990001', '2020-03-01', 3),
    (2, 'Carla Souza', '22222222222', 'carla@estudio.com', '11999990002', '2022-06-15', 2),
    (3, 'Pedro Lima', '33333333333', 'pedro@estudio.com', '11999990003', '2024-01-10', 1);

INSERT IGNORE INTO tatuador_estilo (idtatuador, idestilo, dataestilo) VALUES
    (1, 1, '2020-03-01'), (1, 3, '2021-05-10'),
    (2, 2, '2022-06-15'), (3, 4, '2024-01-10');

INSERT IGNORE INTO cliente (idcliente, nome, cpf, telefone, datacadastro, cidade, uf) VALUES
    (1, 'Ana Silva', '44444444444', '11988880001', '2024-01-15', 'São Paulo', 'SP'),
    (2, 'Bruno Costa', '55555555555', '31988880002', '2024-03-22', 'Belo Horizonte', 'MG');

INSERT IGNORE INTO agendamento
    (idagendamento, idcliente, idtatuador, dataagendamento, horaagendamento,
     descricaotatuagem, valortatuagem, status)
VALUES
    (1, 1, 1, '2026-11-10', '14:00:00', 'Mandala no braço', 350.00, 'pendente'),
    (2, 2, 2, '2026-11-11', '10:00:00', 'Rosa aquarela no ombro', 200.00, 'pendente');

INSERT INTO usuario (nome, email, senha, tipo) VALUES
    ('Administrador', 'admin@estudio.com', '$2b$12$AOK/te1/GNc3XpQ5nrCzyuVUgAUyjusGTx2uTLSAYOD7EwxO6iGSO', 'admin'),
    ('Lucas Mendes', 'lucas@estudio.com', '$2b$12$tywQIO/zdomKCf9.EPSHTeNQDmkhWN0hiNA2.vdrZxoAAKRrqKhQi', 'funcionario'),
    ('Carla Souza', 'carla@estudio.com', '$2b$12$jfVUhEgtJ7atmjIxwt/VcuhG4UwdJwyHT9e9NdO1wCnrLXK8sRaq6', 'funcionario'),
    ('Pedro Lima', 'pedro@estudio.com', '$2b$12$XYd74oLTYjQkckqWL5r10.Om860KT8HR0LOV2E5nx3wDCl29Xiqa6', 'funcionario'),
    ('Ricardo', 'ricardo@gmail.com', '$2b$12$QWaMRconb0EdqNtIsIhl7.lBMBTIJCgsw7zkA0.bKx4AukyT9AA8K', 'funcionario'),
    ('Felipe', 'felipe@gmail.com', '$2b$12$s.jMo8mp4hbSuUrxmLmDUe73dunvxYU2tUNyi0nmWmQB4YNT35Cey', 'funcionario'),
    ('Guilherme', 'gui@gmail.com', '$2b$12$34prHsDyiLe8tE/cowboU.uX020A/e4SibD8NpQkdvTnlFH7SSIHO', 'funcionario')
ON DUPLICATE KEY UPDATE
    nome = VALUES(nome), senha = VALUES(senha), tipo = VALUES(tipo);