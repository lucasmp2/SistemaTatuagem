# Estúdio de Tatuagem

Sistema de gestão de estúdio com MySQL, API FastAPI e páginas HTML/CSS/JavaScript sem etapa de build. O material guiado das 16 aulas está em [aulas/](aulas/) e as convenções do projeto em [REGRAS.md](REGRAS.md).

## Requisitos

- Python 3.10 ou mais recente
- MySQL/MariaDB local (por exemplo, o MySQL do XAMPP)
- Navegador moderno

## Configuração inicial

1. Inicie o MySQL no XAMPP e importe [banco/estudio_tatuagem.sql](banco/estudio_tatuagem.sql) pelo phpMyAdmin.
2. No PowerShell, crie e ative o ambiente virtual e instale as dependências:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Crie `backend/.env` diretamente com as configurações do seu MySQL:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=estudio_tatuagem
SECRET_KEY=cole_a_chave_aleatoria_gerada_no_proximo_passo
```

Gere a chave aleatória com:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Mantenha essa chave e as credenciais reais do banco fora do Git. O `.env` já é ignorado.

4. O SQL já cadastra o administrador e as contas da equipe. Acesse com um destes e-mails:

| Conta | Perfil |
|---|---|
| `admin@estudio.com` | Administrador |
| `lucas@estudio.com` | Funcionário |
| `carla@estudio.com` | Funcionário |
| `pedro@estudio.com` | Funcionário |
| `ricardo@gmail.com` | Funcionário |
| `felipe@gmail.com` | Funcionário |
| `gui@gmail.com` | Funcionário |

Senha de demonstração para as sete contas: `12345`. Ela foi solicitada para este ambiente local; troque-a antes de expor o sistema à internet. Os hashes bcrypt estão no banco, nunca a senha em texto puro.

Se estiver usando um banco sem essas contas e ainda não houver administrador, crie-o pelo terminal:

```powershell
python criar_admin.py
```

O script solicita nome, e-mail e senha sem exibir a senha digitada. O endpoint de cadastro de funcionários exige um administrador; não existe cadastro público de contas da equipe. O cadastro pelo painel exige senha de pelo menos oito caracteres.

## Executar

Na pasta `backend`, com o ambiente virtual ativo:

```powershell
uvicorn main:app --reload
```

- Interface pelo servidor: `http://127.0.0.1:8000/app/`
- Documentação da API: `http://127.0.0.1:8000/docs`
- Verificação da API: `http://127.0.0.1:8000/`

Também é possível abrir `frontend/index.html` diretamente pelo Gerenciador de Arquivos. Nesse caso, mantenha a API ligada no terminal: as páginas usam `http://127.0.0.1:8000` para acessar o backend e o banco. Abrir o HTML sozinho não inicia a API. Faça login com o administrador inicial; o painel permite cadastrar funcionários e gerenciar clientes, tatuadores, especialidades e agendamentos.

## API

Os CRUDs de `/clientes`, `/senioridade`, `/estilos`, `/tatuadores` e `/agendamentos` exigem JWT. `POST /login` é público. `POST /usuarios` exige token válido de administrador. Imagens aprovadas são enviadas em `POST /agendamentos/{id}/desenho` e servidas em `/uploads/`.

O arquivo SQL contém estrutura e dados de demonstração; importá-lo novamente em um banco existente não apaga dados nem redefine tabelas existentes.
