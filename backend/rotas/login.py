# ============================================================
# rotas/login.py — Login com Token JWT
# Descrição: Confere credenciais e emite tokens temporários.
# ============================================================

from datetime import datetime, timedelta, timezone
import os

import bcrypt
import jwt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator

from database import consultar

router = APIRouter()


class CredenciaisLogin(BaseModel):
    # Define os dados enviados para autenticação.
    email: EmailStr
    senha: str = Field(min_length=1, max_length=72)

    @field_validator("senha")
    @classmethod
    def validar_tamanho_senha(cls, senha: str):
        # Impede que o bcrypt receba mais de 72 bytes.
        if len(senha.encode("utf-8")) > 72:
            raise ValueError("A senha deve ter no máximo 72 bytes")
        return senha


@router.post("/login")
def login(dados: CredenciaisLogin):
    # Valida a senha e devolve um JWT com validade de duas horas.
    usuario = consultar("SELECT idusuario, email, senha, tipo FROM usuario WHERE email=%s", (dados.email,), muitos=False)
    if not usuario or not bcrypt.checkpw(dados.senha.encode("utf-8"), usuario["senha"].encode("utf-8")):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")
    chave = os.getenv("SECRET_KEY")
    if not chave:
        raise HTTPException(status_code=503, detail="Configure SECRET_KEY no backend/.env.")
    expiracao = datetime.now(timezone.utc) + timedelta(hours=2)
    token = jwt.encode({"sub": usuario["email"], "tipo": usuario["tipo"], "exp": expiracao}, chave, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}