# Quoridor - Jogo de Tabuleiro Multiplayer para 4 Jogadores (XML-RPC)

Este é um projeto que implementa o clássico jogo de tabuleiro **Quoridor** para até **4 jogadores** utilizando uma arquitetura **Cliente/Servidor** via protocolo **XML-RPC** em Python. O projeto conta com validações de regras de negócio (posicionamento de barreiras e peões) e uma estrutura de testes unitários com o framework **pytest**.

## 🚀 Como Executar o Jogo

Para iniciar uma partida com 4 jogadores, você precisará abrir **5 terminais** no seu sistema (1 para o Servidor e 4 para os Clientes).

### 1. Iniciar o Servidor (Terminal 1)
O servidor exige que você informe o **host (IP)** e a **porta** como argumentos ao executar o comando. Para rodar localmente na sua máquina, use `localhost` (ou `127.0.0.1`) e uma porta livre (ex: `8000`):

```bash
python3 run_server.py localhost 8000
```

### 2. Iniciar os Clientes (Terminais 2, 3, 4 e 5)
Com o servidor rodando, abra mais 4 terminais independentes. Cada terminal representará um jogador diferente na partida. 

Execute o comando abaixo em **cada um dos 4 terminais**:

```bash
python3 run_client.py localhost 8000
```
*(Nota: Certifique-se de usar o mesmo host e porta que você definiu ao ligar o servidor).*

---

## 🧪 Como Rodar os Testes Automatizados

O projeto utiliza o **pytest** para garantir a estabilidade das regras de movimentação, conversão de coordenadas e validações de barreiras.

### Passo 1: Ativar seu ambiente virtual e instalar as dependências
```bash
# Crie e ative a venv (caso ainda não tenha feito)
python3 -m venv venv
source venv/bin/activate

# Instale as dependências do projeto
pip install -r requirements.txt
```

### Passo 2: Executar os testes
Na raiz do projeto, execute o comando:
```bash
pytest -v
```

### Passo 3: Verificar a Cobertura de Testes (Coverage)
Para ver a porcentagem de linhas de código que estão cobertas pelos testes, execute:
```bash
pytest --cov=core --cov-report=html tests/
```
Para abrir o relatório visual gerado diretamente no seu navegador (se estiver usando WSL):
```bash
explorer.exe htmlcov/index.html
```

---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **XML-RPC** (Biblioteca nativa `xmlrpc.server` e `xmlrpc.client`)
* **pytest** (Framework de testes)
* **pytest-cov** (Métricas de cobertura de código)
