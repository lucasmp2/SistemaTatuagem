# ============================================================
# main.py — API do Estúdio de Tatuagem
# Descrição: Registra rotas, autenticação e arquivos estáticos.
# Como rodar: uvicorn main:app --reload
# ============================================================

from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

load_dotenv(Path(__file__).with_name(".env"))

from rotas import agendamentos, clientes, estilos, login, senioridade, tatuadores, usuarios
from seguranca import verificar_admin, verificar_token

app = FastAPI(title="API do Estúdio de Tatuagem", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PASTA_UPLOADS = Path(__file__).with_name("uploads")
PASTA_UPLOADS.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=PASTA_UPLOADS), name="uploads")
PASTA_AULAS = Path(__file__).resolve().parents[1] / "aulas"
app.mount("/aulas", StaticFiles(directory=PASTA_AULAS), name="aulas")

app.include_router(login.router, tags=["Login"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"], dependencies=[Depends(verificar_admin)])
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"], dependencies=[Depends(verificar_token)])
app.include_router(senioridade.router, prefix="/senioridade", tags=["Senioridade"], dependencies=[Depends(verificar_token)])
app.include_router(estilos.router, prefix="/estilos", tags=["Estilos"], dependencies=[Depends(verificar_token)])
app.include_router(tatuadores.router, prefix="/tatuadores", tags=["Tatuadores"], dependencies=[Depends(verificar_token)])
app.include_router(agendamentos.router, prefix="/agendamentos", tags=["Agendamentos"], dependencies=[Depends(verificar_token)])

app.mount(
    "/app",
    StaticFiles(directory=Path(__file__).resolve().parents[1] / "frontend", html=True),
    name="frontend",
)


@app.get("/")
def inicio():
    # Confirma que a API está respondendo.
    return {"mensagem": "API do estúdio de tatuagem funcionando!", "interface": "/app/"}