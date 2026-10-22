# ============================================================
# seguranca.py — Verificação de token e autorização
# Descrição: Valida JWTs e restringe operações administrativas.
# ============================================================

import os

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

esquema_token = HTTPBearer(auto_error=False)


def verificar_token(credenciais: HTTPAuthorizationCredentials | None = Depends(esquema_token)):
    # Confere a assinatura e validade do token recebido.
    if credenciais is None:
        raise HTTPException(status_code=401, detail="Token não informado", headers={"WWW-Authenticate": "Bearer"})
    chave = os.getenv("SECRET_KEY")
    if not chave:
        raise HTTPException(status_code=503, detail="Configure SECRET_KEY no backend/.env.")
    try:
        payload = jwt.decode(credenciais.credentials, chave, algorithms=["HS256"])
        if not payload.get("sub") or not payload.get("tipo"):
            raise HTTPException(status_code=401, detail="Token inválido")
        return payload
    except jwt.ExpiredSignatureError as erro:
        raise HTTPException(status_code=401, detail="Token expirado, faça login novamente", headers={"WWW-Authenticate": "Bearer"}) from erro
    except jwt.InvalidTokenError as erro:
        raise HTTPException(status_code=401, detail="Token inválido", headers={"WWW-Authenticate": "Bearer"}) from erro


def verificar_admin(payload: dict = Depends(verificar_token)):
    # Exige que o token válido pertença a um administrador.
    if payload.get("tipo") != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return payload