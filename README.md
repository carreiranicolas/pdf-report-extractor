# pdf-report-extractor

Automação em Python que extrai as tabelas de uma fatura em `.pdf`, gera um relatório `.xlsx` e o envia por e-mail.

## Como funciona

```
input/*.pdf ──► extração das tabelas ──► tratamento dos dados ──► output/relatorio_pedido_DDMMAAAA.xlsx ──► envio por e-mail
```

1. Cria os diretórios `input/` e `output/`, caso não existam.
2. Localiza o **único** `.pdf` presente em `input/` (a execução é interrompida se houver nenhum ou mais de um).
3. Extrai as tabelas de cada página com o `pdfplumber`:
   - a **última** tabela é tratada como a de valores finais;
   - as demais são unidas e têm as colunas numéricas convertidas (`1.234,56` → `1234.56`).
4. Gera o arquivo `.xlsx` com duas abas: **Tabela de Itens** e **Valores Finais**.
5. Envia o arquivo como anexo via Gmail (SMTP com SSL).

## Estrutura do projeto

```
pdf-report-extractor/
├── main.py                     # Orquestra o fluxo e é o único ponto que captura erros
├── pyproject.toml              # Metadados e dependências do projeto
├── uv.lock                     # Versões exatas instaladas (gerado pelo uv, não editar)
├── .env.example                # Modelo das variáveis de ambiente
├── resources/
│   └── configs/
│       └── geral.yaml          # Configurações que não são segredo
├── src/
│   ├── configs/                # Carregam o geral.yaml e o .env para os models
│   ├── models/                 # Modelos tipados (pydantic) dos parâmetros
│   ├── files/                  # Leitura de arquivos (YAML e pdf)
│   ├── tasks/                  # Etapas do fluxo (diretórios, tratamento, e-mail)
│   └── utils/                  # Funções auxiliares (logger, formatação)
├── input/                      # Onde o .pdf deve ser colocado
├── output/                     # Onde o .xlsx é gerado
└── logs/                       # Logs diários de execução (ignorados pelo git)
```

## Pré-requisitos

- Python **3.12** ou superior
- [uv](https://docs.astral.sh/uv/) — gerenciador de projetos e dependências

Para instalar o uv (Linux/macOS):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

No Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Instalação

```bash
git clone <url-do-repositorio>
cd pdf-report-extractor
uv sync
```

O `uv sync` cria o ambiente virtual `.venv` e instala exatamente as versões registradas no `uv.lock`.

## Configuração

### Variáveis de ambiente (`.env`)

Copie o modelo e preencha os valores:

```bash
cp .env.example .env
```

| Variável             | Descrição                                   |
|----------------------|---------------------------------------------|
| `FROM_EMAIL`         | Conta Gmail que envia o e-mail              |
| `TO_EMAIL`           | Destinatário do relatório                   |
| `APP_EMAIL_PASSWORD` | Senha de app do Gmail (não é a senha normal) |

A senha de app é gerada em **Conta Google → Segurança → Verificação em duas etapas → Senhas de app** (a verificação em duas etapas precisa estar ativa).

> O `.env` contém credenciais e **nunca** deve ser enviado ao repositório.

### Parâmetros gerais (`resources/configs/geral.yaml`)

| Chave               | Descrição                                                    |
|---------------------|--------------------------------------------------------------|
| `COLUNAS_NUMERICAS` | Colunas da tabela convertidas de texto para número           |
| `ARQUIVO_FINAL`     | Prefixo do nome do `.xlsx` (a data do dia é adicionada ao final) |
| `SHEETS`            | Nomes das abas do `.xlsx`                                    |
| `DIRETORIOS`        | Nomes dos diretórios de entrada e saída                      |

## Execução

Coloque o `.pdf` em `input/` e, **a partir da raiz do projeto**, execute:

```bash
uv run main.py
```

Também é possível executar pelo botão ▶ do VS Code, desde que o interpretador selecionado seja o do `.venv` (veja abaixo) e o arquivo aberto no editor seja o `main.py`.

## Logs

Cada execução é registrada no terminal e em `logs/execucao_AAAA-MM-DD.log` (um arquivo por dia; execuções do mesmo dia são acrescentadas ao mesmo arquivo).

```
18/10/2026 10:30:12 | INFO     | src.files.extrair_dados_pdf | Extração finalizada: 3 tabela(s) encontrada(s)
```

Em caso de erro, o traceback completo é gravado no log e o programa termina com código de saída `1`, permitindo que agendadores identifiquem a falha.

## Gerenciando dependências

| Ação                                  | Comando                  |
|---------------------------------------|--------------------------|
| Instalar as dependências do projeto   | `uv sync`                |
| Adicionar uma dependência             | `uv add <pacote>`        |
| Adicionar uma dependência de desenvolvimento | `uv add --dev <pacote>` |
| Remover uma dependência               | `uv remove <pacote>`     |
| Atualizar as versões no `uv.lock`     | `uv lock --upgrade`      |

Os comandos `add` e `remove` atualizam o `pyproject.toml`, o `uv.lock` e o `.venv` de uma só vez. Sempre faça commit dos dois arquivos juntos.

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).
