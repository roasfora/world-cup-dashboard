# World Cup Dashboard

Dashboard local da FIFA World Cup 2026 feito com Streamlit, SQLite e Python.

## Visão geral

Este projeto é um aplicativo local para visualizar partidas da Copa do Mundo 2026.
Os dados são carregados de um banco SQLite local (`worldcup.db`) e exibidos em uma interface Streamlit.
Os usuários podem filtrar partidas por grupo, time e status, além de editar resultados manualmente.

## Funcionalidades principais

- Visualizar partidas da Copa do Mundo 2026
- Métricas de partidas totais, agendadas, ao vivo e encerradas
- Filtrar por grupo, time e status
- Edição manual de placares e status na seção de administração
- Suporte a override manual para proteger edições durante a sincronização com a API
- Sincronização opcional com API externa (`football-data.org`)

## Estrutura do projeto

- `app.py` - interface Streamlit
- `database.py` - conexão SQLite e consultas de dados
- `seed.py` - popula o banco de dados local com partidas de exemplo
- `api_client.py` - cliente para buscar partidas na API `football-data.org`
- `sync_matches.py` - sincroniza partidas da API com o banco local
- `requirements.txt` - dependências do projeto

## Requisitos

- Python 3.9+ (recomendado)
- `pip`
- dependências do arquivo `requirements.txt`

## Instalação

1. Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

> A API é opcional. Se você não usar chave de API, o app continuará funcionando com os dados seed locais.

## Inicializar o banco de dados

Execute o seed para popular o banco local com partidas de exemplo:

```bash
python seed.py
```

Se o banco já tiver dados e você quiser repovoá-lo, use:

```bash
python seed.py --force
```

## Executar o aplicativo

```bash
streamlit run app.py
```

Em seguida, abra o link mostrado no terminal.

## Sincronização de partidas com API

A sincronização é opcional e depende da variável de ambiente `FOOTBALL_DATA_API_KEY`.

1. Adicione sua chave ao `.env`:

```env
FOOTBALL_DATA_API_KEY=your_api_key_here
```

2. Execute a sincronização:

```bash
python sync_matches.py
```

O script irá:

- buscar partidas da Copa do Mundo 2026
- inserir novas partidas
- atualizar partidas existentes
- preservar resultados com override manual

## Edição manual

Dentro do Streamlit, use a seção **Administração de Partidas** para:

- selecionar uma partida
- atualizar placar
- atualizar status (`scheduled`, `live`, `finished`)
- salvar mudanças com `manual_override`
- resetar override quando desejar permitir nova sincronização da API

## Observações importantes

- `worldcup.db` é o banco de dados local e a fonte de verdade do app
- `.env` deve conter variáveis sensíveis e não deve ser enviado ao Git
- `.venv` e arquivos temporários estão ignorados pelo `.gitignore`

## Licença

Uso livre para fins educacionais e de aprendizado.
