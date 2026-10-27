-- Mantém agendamentos e contas de cliente, removendo apenas o vínculo
-- quando o cliente relacionado for excluído.

SET @fk_agendamento_cliente = (
    SELECT CONSTRAINT_NAME
    FROM information_schema.KEY_COLUMN_USAGE
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'agendamento'
      AND COLUMN_NAME = 'idcliente'
      AND REFERENCED_TABLE_NAME = 'cliente'
    LIMIT 1
);
SET @sql_fk_agendamento = IF(
    @fk_agendamento_cliente IS NULL,
    'SELECT 1',
    CONCAT('ALTER TABLE `agendamento` DROP FOREIGN KEY `', REPLACE(@fk_agendamento_cliente, '`', '``'), '`')
);
PREPARE stmt_fk_agendamento FROM @sql_fk_agendamento;
EXECUTE stmt_fk_agendamento;
DEALLOCATE PREPARE stmt_fk_agendamento;

ALTER TABLE agendamento
    MODIFY idcliente INT DEFAULT NULL,
    ADD CONSTRAINT fk_agendamento_cliente
        FOREIGN KEY (idcliente) REFERENCES cliente(idcliente) ON DELETE SET NULL;

SET @fk_usuario_cliente = (
    SELECT CONSTRAINT_NAME
    FROM information_schema.KEY_COLUMN_USAGE
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = 'usuario'
      AND COLUMN_NAME = 'idcliente'
      AND REFERENCED_TABLE_NAME = 'cliente'
    LIMIT 1
);
SET @sql_fk_usuario = IF(
    @fk_usuario_cliente IS NULL,
    'SELECT 1',
    CONCAT('ALTER TABLE `usuario` DROP FOREIGN KEY `', REPLACE(@fk_usuario_cliente, '`', '``'), '`')
);
PREPARE stmt_fk_usuario FROM @sql_fk_usuario;
EXECUTE stmt_fk_usuario;
DEALLOCATE PREPARE stmt_fk_usuario;

ALTER TABLE usuario
    MODIFY idcliente INT DEFAULT NULL,
    ADD CONSTRAINT fk_usuario_cliente
        FOREIGN KEY (idcliente) REFERENCES cliente(idcliente) ON DELETE SET NULL;
