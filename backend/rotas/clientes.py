# ============================================================
# rotas/clientes.py — CRUD de Clientes
# Descrição: Endpoints para consultar e manter clientes.
# ============================================================

from datetime import date

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from database import consultar, executar

router = APIRouter()


class Cliente(BaseModel):
    # Define os dados aceitos para criar ou atualizar um cliente.
    nome: str = Field(min_length=1, max_length=100)
    cpf: str = Field(pattern=r"^\d{11}$")
    telefone: str | None = Field(default=None, max_length=20)
    datacadastro: date | None = None
    cidade: str | None = Field(default=None, max_length=100)
    uf: str | None = Field(default=None, pattern=r"^[A-Za-z]{2}$")


@router.get("")
def listar_clientes():
    # Retorna os clientes em ordem alfabética.
    return consultar("SELECT * FROM cliente ORDER BY nome")


@router.get("/{id}")
def buscar_cliente(id: int):
    # Busca um cliente pelo identificador.
    cliente = consultar("SELECT * FROM cliente WHERE idcliente = %s", (id,), muitos=False)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.post("", status_code=status.HTTP_201_CREATED)
def criar_cliente(cliente: Cliente):
    # Cadastra um cliente e devolve seu identificador.
    resultado = executar(
        "INSERT INTO cliente (nome, cpf, telefone, datacadastro, cidade, uf) VALUES (%s, %s, %s, %s, %s, %s)",
        (cliente.nome, cliente.cpf, cliente.telefone, cliente.datacadastro, cliente.cidade, cliente.uf),
    )
    return {"mensagem": "Cliente cadastrado com sucesso", "idcliente": resultado["id"]}


@router.put("/{id}")
def atualizar_cliente(id: int, cliente: Cliente):
    # Atualiza os dados de um cliente existente.
    if not consultar("SELECT idcliente FROM cliente WHERE idcliente = %s", (id,), muitos=False):
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    executar(
        "UPDATE cliente SET nome=%s, cpf=%s, telefone=%s, datacadastro=%s, cidade=%s, uf=%s WHERE idcliente=%s",
        (cliente.nome, cliente.cpf, cliente.telefone, cliente.datacadastro, cliente.cidade, cliente.uf, id),
    )
    return {"mensagem": "Cliente atualizado com sucesso"}


@router.delete("/{id}")
def deletar_cliente(id: int):
    # Exclui um cliente que não possua agendamentos associados.
    resultado = executar("DELETE FROM cliente WHERE idcliente = %s", (id,))
    if not resultado["linhas"]:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"mensagem": "Cliente deletado com sucesso"}