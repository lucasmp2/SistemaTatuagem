# ============================================================
# criar_admin.py — Criação inicial de administrador
# Descrição: Cria a primeira conta administrativa com senha hash.
# Como rodar: python criar_admin.py
# ============================================================

from getpass import getpass
from pathlib import Path
import os

import bcrypt
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv(Path(__file__).with_name(".env"))


def criar_admin():
    # Solicita credenciais no terminal e grava somente o hash da senha.
    nome = input("Nome do administrador: ").strip()
    email = input("E-mail do administrador: ").strip().lower()
    senha = getpass("Senha (mínimo 8 caracteres): ")
    confirmacao = getpass("Confirme a senha: ")
    if not nome or not email or len(senha) < 8 or len(senha.encode("utf-8")) > 72 or senha != confirmacao:
        raise ValueError("Confira nome, e-mail e senha. As senhas devem coincidir e ter de 8 a 72 bytes.")

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "estudio_tatuagem"),
        charset="utf8mb4",
    )
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE tipo='admin'")
        if cursor.fetchone()[0]:
            raise ValueError("Já existe um administrador. Use o painel para criar funcionários.")
        senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cursor.execute(
            "INSERT INTO usuario (nome, email, senha, tipo) VALUES (%s, %s, %s, 'admin')",
            (nome, email, senha_hash),
        )
        conn.commit()
        print(f"Administrador {email} criado com sucesso.")
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    try:
        criar_admin()
    except (Error, ValueError) as erro:
        raise SystemExit(f"Não foi possível criar o administrador: {erro}") from erro