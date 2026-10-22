# ============================================================
# rotas/tatuadores.py — CRUD de Tatuadores
# Descrição: Endpoints de tatuadores e seus estilos de trabalho.
# ============================================================

from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from database import consultar, executar, executar_transacao

router = APIRouter()


class Tatuador(BaseModel):
    # Define os dados aceitos para criar ou atualizar um tatuador.
    nometatuador: str = Field(min_length=1, max_length=100)
    cpf: str = Field(pattern=r"^\d{11}$")
    email: str | None = Field(default=None, max_length=100)
    telefone: str | None = Field(default=None, max_length=20)
    datacontratacao: str | None = None
    idsenioridade: int = Field(gt=0)


class EstilosDoTatuador(BaseModel):
    # Define os IDs dos estilos associados ao tatuador.
    idestilos: List[int]


@router.get("")
def listar_tatuadores():
    # Retorna tatuadores com senioridade e estilos em formato legível.
    return consultar("""
        SELECT t.*, s.nome AS senioridade,
               GROUP_CONCAT(e.descricao ORDER BY e.descricao SEPARATOR ', ') AS estilos
        FROM tatuador t
        JOIN senioridade s ON t.idsenioridade = s.idsenioridade
        LEFT JOIN tatuador_estilo te ON t.idtatuador = te.idtatuador
        LEFT JOIN estilo e ON te.idestilo = e.idestilo
        GROUP BY t.idtatuador, s.nome
        ORDER BY t.nometatuador
    """)


@router.get("/{id}")
def buscar_tatuador(id: int):
    # Busca um tatuador pelo identificador.
    tatuador = consultar("SELECT * FROM tatuador WHERE idtatuador=%s", (id,), muitos=False)
    if not tatuador:
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    return tatuador


@router.post("", status_code=201)
def criar_tatuador(tatuador: Tatuador):
    # Cadastra um tatuador e devolve seu identificador.
    resultado = executar(
        "INSERT INTO tatuador (nometatuador, cpf, email, telefone, datacontratacao, idsenioridade) VALUES (%s, %s, %s, %s, %s, %s)",
        (tatuador.nometatuador, tatuador.cpf, tatuador.email, tatuador.telefone, tatuador.datacontratacao, tatuador.idsenioridade),
    )
    return {"mensagem": "Tatuador cadastrado com sucesso", "idtatuador": resultado["id"]}


@router.put("/{id}")
def atualizar_tatuador(id: int, tatuador: Tatuador):
    # Atualiza os dados de um tatuador existente.
    if not consultar("SELECT idtatuador FROM tatuador WHERE idtatuador=%s", (id,), muitos=False):
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    executar(
        "UPDATE tatuador SET nometatuador=%s, cpf=%s, email=%s, telefone=%s, datacontratacao=%s, idsenioridade=%s WHERE idtatuador=%s",
        (tatuador.nometatuador, tatuador.cpf, tatuador.email, tatuador.telefone, tatuador.datacontratacao, tatuador.idsenioridade, id),
    )
    return {"mensagem": "Tatuador atualizado com sucesso"}


@router.delete("/{id}")
def deletar_tatuador(id: int):
    # Exclui um tatuador que não tenha vínculos ativos.
    resultado = executar("DELETE FROM tatuador WHERE idtatuador=%s", (id,))
    if not resultado["linhas"]:
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    return {"mensagem": "Tatuador deletado com sucesso"}


@router.get("/{id}/estilos")
def listar_estilos_do_tatuador(id: int):
    # Retorna os estilos associados ao tatuador.
    if not consultar("SELECT idtatuador FROM tatuador WHERE idtatuador=%s", (id,), muitos=False):
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    return consultar("""
        SELECT e.idestilo, e.descricao
        FROM tatuador_estilo te JOIN estilo e ON te.idestilo=e.idestilo
        WHERE te.idtatuador=%s ORDER BY e.descricao
    """, (id,))


@router.put("/{id}/estilos")
def atualizar_estilos_do_tatuador(id: int, dados: EstilosDoTatuador):
    # Substitui de forma atômica a lista de estilos do tatuador.
    if not consultar("SELECT idtatuador FROM tatuador WHERE idtatuador=%s", (id,), muitos=False):
        raise HTTPException(status_code=404, detail="Tatuador não encontrado")
    comandos = [("DELETE FROM tatuador_estilo WHERE idtatuador=%s", (id,))]
    comandos.extend(
        ("INSERT INTO tatuador_estilo (idtatuador, idestilo, dataestilo) VALUES (%s, %s, CURDATE())", (id, idestilo))
        for idestilo in dados.idestilos
    )
    executar_transacao(comandos)
    return {"mensagem": "Estilos atualizados com sucesso"}