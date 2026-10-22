# ============================================================
# rotas/senioridade.py — CRUD de Senioridade
# Descrição: Endpoints para manter níveis de experiência.
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from database import consultar, executar

router = APIRouter()


class Senioridade(BaseModel):
    # Define os dados aceitos para uma senioridade.
    nome: str = Field(min_length=1, max_length=50)


@router.get("")
def listar_senioridades():
    # Retorna todos os níveis de senioridade.
    return consultar("SELECT * FROM senioridade ORDER BY idsenioridade")


@router.get("/{id}")
def buscar_senioridade(id: int):
    # Busca uma senioridade pelo identificador.
    senioridade = consultar("SELECT * FROM senioridade WHERE idsenioridade=%s", (id,), muitos=False)
    if not senioridade:
        raise HTTPException(status_code=404, detail="Senioridade não encontrada")
    return senioridade


@router.post("", status_code=201)
def criar_senioridade(senioridade: Senioridade):
    # Cadastra uma nova senioridade.
    resultado = executar("INSERT INTO senioridade (nome) VALUES (%s)", (senioridade.nome,))
    return {"mensagem": "Senioridade cadastrada com sucesso", "idsenioridade": resultado["id"]}


@router.put("/{id}")
def atualizar_senioridade(id: int, senioridade: Senioridade):
    # Atualiza uma senioridade existente.
    if not consultar("SELECT idsenioridade FROM senioridade WHERE idsenioridade=%s", (id,), muitos=False):
        raise HTTPException(status_code=404, detail="Senioridade não encontrada")
    executar("UPDATE senioridade SET nome=%s WHERE idsenioridade=%s", (senioridade.nome, id))
    return {"mensagem": "Senioridade atualizada com sucesso"}


@router.delete("/{id}")
def deletar_senioridade(id: int):
    # Exclui um nível que não esteja associado a tatuadores.
    resultado = executar("DELETE FROM senioridade WHERE idsenioridade=%s", (id,))
    if not resultado["linhas"]:
        raise HTTPException(status_code=404, detail="Senioridade não encontrada")
    return {"mensagem": "Senioridade deletada com sucesso"}