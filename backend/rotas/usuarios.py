# ============================================================
# rotas/usuarios.py — Cadastro de funcionários
# Descrição: Permite que administradores criem contas de equipe.
# ============================================================

import bcrypt
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, field_validator

from database import executar

router = APIRouter()


class Usuario(BaseModel):
    # Define os dados de uma nova conta de funcionário.
    nome: str = Field(min_length=1, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=72)

    @field_validator("senha")
    @classmethod
    def validar_tamanho_senha(cls, senha: str):
        # Impede exceder o limite em bytes do bcrypt com caracteres multibyte.
        if len(senha.encode("utf-8")) > 72:
            raise ValueError("A senha deve ter no máximo 72 bytes")
        return senha


@router.post("", status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: Usuario):
    # Salva uma conta sem armazenar a senha em texto puro.
    senha_hash = bcrypt.hashpw(usuario.senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    try:
        executar("INSERT INTO usuario (nome, email, senha, tipo) VALUES (%s, %s, %s, 'funcionario')", (usuario.nome, usuario.email, senha_hash))
    except HTTPException as erro:
        if erro.status_code == 409:
            raise HTTPException(status_code=409, detail="Esse e-mail já está em uso") from erro
        raise
    return {"mensagem": "Funcionário cadastrado com sucesso"}