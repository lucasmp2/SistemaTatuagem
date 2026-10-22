# ============================================================
# rotas/estilos.py — CRUD de Estilos
# Descrição: Endpoints para manter os estilos de tatuagem.
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from database import consultar, executar

router = APIRouter()


class Estilo(BaseModel):
    # Define os dados aceitos para um estilo.
    descricao: str = Field(min_length=1, max_length=50)


@router.get("")
def listar_estilos():
    # Retorna os estilos cadastrados.
    return consultar("SELECT * FROM estilo ORDER BY descricao")


@router.get("/{id}")
def buscar_estilo(id: int):
    # Busca um estilo pelo identificador.
    estilo = consultar("SELECT * FROM estilo WHERE idestilo=%s", (id,), muitos=False)
    if not estilo:
        raise HTTPException(status_code=404, detail="Estilo não encontrado")
    return estilo


@router.post("", status_code=201)
def criar_estilo(estilo: Estilo):
    # Cadastra um novo estilo.
    resultado = executar("INSERT INTO estilo (descricao) VALUES (%s)", (estilo.descricao,))
    return {"mensagem": "Estilo cadastrado com sucesso", "idestilo": resultado["id"]}


@router.put("/{id}")
def atualizar_estilo(id: int, estilo: Estilo):
    # Atualiza a descrição de um estilo existente.
    if not consultar("SELECT idestilo FROM estilo WHERE idestilo=%s", (id,), muitos=False):
        raise HTTPException(status_code=404, detail="Estilo não encontrado")
    executar("UPDATE estilo SET descricao=%s WHERE idestilo=%s", (estilo.descricao, id))
    return {"mensagem": "Estilo atualizado com sucesso"}


@router.delete("/{id}")
def deletar_estilo(id: int):
    # Exclui um estilo que não esteja associado a tatuadores.
    resultado = executar("DELETE FROM estilo WHERE idestilo=%s", (id,))
    if not resultado["linhas"]:
        raise HTTPException(status_code=404, detail="Estilo não encontrado")
    return {"mensagem": "Estilo deletado com sucesso"}