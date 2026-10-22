# ============================================================
# rotas/agendamentos.py — CRUD e desenhos dos agendamentos
# Descrição: Endpoints para sessões, status e imagens aprovadas.
# ============================================================

from datetime import date, time
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pydantic import BaseModel, Field

from database import consultar, executar

router = APIRouter()
PASTA_UPLOADS = Path(__file__).resolve().parents[1] / "uploads"
TIPOS_IMAGEM = {"image/jpeg", "image/png", "image/gif", "image/webp"}
TAMANHO_MAXIMO = 5 * 1024 * 1024


class Agendamento(BaseModel):
    # Define os dados aceitos para criar ou atualizar um agendamento.
    idcliente: int = Field(gt=0)
    idtatuador: int = Field(gt=0)
    dataagendamento: date
    horaagendamento: time
    descricaotatuagem: str | None = None
    valortatuagem: float | None = Field(default=None, ge=0)
    status: str | None = None


def normalizar_agendamento(agendamento: dict):
    # Converte o horário retornado pelo conector MySQL para texto.
    if agendamento and agendamento.get("horaagendamento"):
        horario = agendamento["horaagendamento"]
        if hasattr(horario, "total_seconds"):
            total_segundos = int(horario.total_seconds())
            horas, resto = divmod(total_segundos, 3600)
            minutos, segundos = divmod(resto, 60)
            agendamento["horaagendamento"] = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        else:
            agendamento["horaagendamento"] = horario.strftime("%H:%M:%S")
    return agendamento


@router.get("")
def listar_agendamentos():
    # Lista sessões com os nomes do cliente e do tatuador.
    agendamentos = consultar("""
        SELECT a.*, c.nome AS cliente, t.nometatuador AS tatuador
        FROM agendamento a
        JOIN cliente c ON a.idcliente=c.idcliente
        JOIN tatuador t ON a.idtatuador=t.idtatuador
        ORDER BY a.dataagendamento, a.horaagendamento
    """)
    return [normalizar_agendamento(item) for item in agendamentos]


@router.get("/{id}")
def buscar_agendamento(id: int):
    # Busca os dados de um agendamento pelo identificador.
    agendamento = consultar("SELECT * FROM agendamento WHERE idagendamento=%s", (id,), muitos=False)
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return normalizar_agendamento(agendamento)


@router.post("", status_code=status.HTTP_201_CREATED)
def criar_agendamento(agendamento: Agendamento):
    # Cadastra uma sessão com status inicial pendente.
    resultado = executar(
        "INSERT INTO agendamento (idcliente, idtatuador, dataagendamento, horaagendamento, descricaotatuagem, valortatuagem) VALUES (%s, %s, %s, %s, %s, %s)",
        (agendamento.idcliente, agendamento.idtatuador, agendamento.dataagendamento, agendamento.horaagendamento, agendamento.descricaotatuagem, agendamento.valortatuagem),
    )
    return {"mensagem": "Agendamento cadastrado com sucesso", "idagendamento": resultado["id"]}


@router.put("/{id}")
def atualizar_agendamento(id: int, agendamento: Agendamento):
    # Atualiza os dados e o status de uma sessão existente.
    if not consultar("SELECT idagendamento FROM agendamento WHERE idagendamento=%s", (id,), muitos=False):
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    status_validos = {"pendente", "confirmado", "concluido", "cancelado"}
    novo_status = agendamento.status or "pendente"
    if novo_status not in status_validos:
        raise HTTPException(status_code=422, detail="Status de agendamento inválido")
    executar(
        "UPDATE agendamento SET idcliente=%s, idtatuador=%s, dataagendamento=%s, horaagendamento=%s, descricaotatuagem=%s, valortatuagem=%s, status=%s WHERE idagendamento=%s",
        (agendamento.idcliente, agendamento.idtatuador, agendamento.dataagendamento, agendamento.horaagendamento, agendamento.descricaotatuagem, agendamento.valortatuagem, novo_status, id),
    )
    return {"mensagem": "Agendamento atualizado com sucesso"}


@router.delete("/{id}")
def deletar_agendamento(id: int):
    # Exclui um agendamento existente.
    resultado = executar("DELETE FROM agendamento WHERE idagendamento=%s", (id,))
    if not resultado["linhas"]:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return {"mensagem": "Agendamento deletado com sucesso"}


@router.post("/{id}/desenho")
async def upload_desenho(id: int, arquivo: UploadFile = File(...)):
    # Valida e armazena a imagem aprovada do agendamento.
    if not consultar("SELECT idagendamento FROM agendamento WHERE idagendamento=%s", (id,), muitos=False):
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    if arquivo.content_type not in TIPOS_IMAGEM:
        raise HTTPException(status_code=415, detail="Envie uma imagem JPEG, PNG, GIF ou WebP")
    conteudo = await arquivo.read(TAMANHO_MAXIMO + 1)
    if not conteudo or len(conteudo) > TAMANHO_MAXIMO:
        raise HTTPException(status_code=413, detail="A imagem deve ter até 5 MB")
    extensao = {"image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif", "image/webp": ".webp"}[arquivo.content_type]
    nome_arquivo = f"{id}_{uuid4().hex}{extensao}"
    PASTA_UPLOADS.mkdir(parents=True, exist_ok=True)
    caminho = PASTA_UPLOADS / nome_arquivo
    caminho.write_bytes(conteudo)
    try:
        executar("UPDATE agendamento SET desenhoaprovado=%s WHERE idagendamento=%s", (nome_arquivo, id))
    except HTTPException:
        caminho.unlink(missing_ok=True)
        raise
    return {"mensagem": "Desenho enviado com sucesso", "arquivo": nome_arquivo}