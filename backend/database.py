# ============================================================
# database.py — Conexão e consultas ao banco MySQL
# Descrição: Carrega as configurações locais e centraliza as
#            operações usadas pelos endpoints da API.
# ============================================================

from pathlib import Path
import os

import mysql.connector
from dotenv import load_dotenv
from fastapi import HTTPException
from mysql.connector import Error, IntegrityError

load_dotenv(Path(__file__).with_name(".env"))


def conectar():
    # Abre uma conexão com o banco configurado no arquivo .env.
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "estudio_tatuagem"),
            charset="utf8mb4",
        )
    except Error as erro:
        raise HTTPException(status_code=503, detail="Não foi possível conectar ao MySQL. Confira o XAMPP e o arquivo backend/.env.") from erro


def consultar(sql: str, parametros: tuple = (), muitos: bool = True):
    # Executa uma consulta e devolve uma linha ou uma lista de linhas.
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, parametros)
        return cursor.fetchall() if muitos else cursor.fetchone()
    except Error as erro:
        raise HTTPException(status_code=500, detail="Erro ao consultar os dados do banco.") from erro
    finally:
        cursor.close()
        conn.close()


def executar(sql: str, parametros: tuple = ()):
    # Executa uma alteração e retorna o ID criado e a quantidade afetada.
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, parametros)
        conn.commit()
        return {"id": cursor.lastrowid, "linhas": cursor.rowcount}
    except IntegrityError as erro:
        conn.rollback()
        raise HTTPException(status_code=409, detail="Operação conflitante: verifique valores únicos e relacionamentos existentes.") from erro
    except Error as erro:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Erro ao salvar os dados no banco.") from erro
    finally:
        cursor.close()
        conn.close()


def executar_transacao(comandos: list[tuple[str, tuple]]):
    # Executa várias alterações de forma atômica.
    conn = conectar()
    cursor = conn.cursor()
    try:
        for sql, parametros in comandos:
            cursor.execute(sql, parametros)
        conn.commit()
    except IntegrityError as erro:
        conn.rollback()
        raise HTTPException(status_code=409, detail="Relacionamento inválido; confira os IDs informados.") from erro
    except Error as erro:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Erro ao salvar os dados no banco.") from erro
    finally:
        cursor.close()
        conn.close()