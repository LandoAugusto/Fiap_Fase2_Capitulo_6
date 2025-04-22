# 🌾 Sistema de Gestão de Colheita de Cana-de-Açúcar

Projeto acadêmico da FIAP desenvolvido para o curso de Inteligência Artificial, com foco na resolução de uma dor real do agronegócio: **a gestão de produtividade, perdas e prejuízos nas colheitas de cana-de-açúcar**.

---

## 🎯 Objetivo

Criar uma solução em Python que permita o **controle eficiente da produção agrícola**, identificando colheitas com baixa produtividade e altos prejuízos. O sistema também fornece relatórios gerenciais e estatísticos para suporte à tomada de decisão, de forma acessível e automatizada.

---

## 📍 Dor no Agronegócio Endereçada

A falta de controle preciso sobre os indicadores das colheitas — como área, produtividade, perdas e prejuízos — gera decisões equivocadas e prejuízos financeiros. O projeto resolve essa dor com uma interface simples de uso, porém tecnicamente robusta.

---

## ✅ Requisitos Técnicos Atendidos

Este projeto contempla **todos os conteúdos exigidos** nos capítulos 3 a 6 da disciplina:

- **Capítulo 3 – Subalgoritmos:**
  - Funções com parâmetros e retorno (`cadastrar_colheita()`, `formatar_exibicao_colheitas()`, etc.)

- **Capítulo 4 – Estruturas de Dados:**
  - Uso de `listas`, `dicionários`, `tuplas`, `tipagem estática` com `typing`.

- **Capítulo 5 – Manipulação de Arquivos:**
  - Geração de relatórios em `.txt`.
  - Exportação de dados em `.json` com serialização de datas.

- **Capítulo 6 – Banco de Dados Oracle:**
  - Integração com Oracle via `oracledb`.
  - Criação de tabela com constraints.
  - Operações `INSERT` e `SELECT` com tratamento de erros e fechamento de conexões.

---

## 🧠 Funcionalidades

- Cadastro e validação de colheitas (com salvamento no Oracle)
- Cálculo de produtividade (t/ha) e prejuízo (R$)
- Identificação de colheitas ineficientes (baixa produtividade e alto prejuízo) com base nos dados do Oracle
- Relatórios em `.txt` e `.json` (gerados a partir dos dados do Oracle)
- Consulta de dados salvos no Oracle
- Estatísticas por tipo de colheita (manual x mecânica) com base nos dados do Oracle

---

## 🛠️ Estrutura do Projeto

projeto_colheita_final_ENTREGA_FINAL_v2/
│
├── main.py                                  # Interface principal em linha de comando
├── funcoes.py                               # Funções auxiliares e cálculos
├── oracle.py                                # Conexão e integração com Oracle
├── criar_banco_colheita_cana_de_acucar.sql  # Script de criação da tabela
├── dados_colheita.json                      # Exemplo de exportação dos dados em JSON
├── relatorio_colheita.txt                   # Exemplo de relatório em texto plano
├── gestao_colheita.log                      # Arquivo de log gerado pela aplicação
├── .env.example                             # Arquivo de exemplo para variáveis de ambiente 
├── requirements.txt                         # Dependências do projeto
├── README.md                                # Este arquivo
├── teste_conexao.py                         # Script para teste isolado da conexão Oracle

---

## 📦 Como Executar

1.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure as Variáveis de Ambiente**: 
    * Copie o arquivo `.env.example` que está neste repositório.
    * Renomeie a cópia para `.env`.
    * **Abra o arquivo `.env` e preencha-o com as credenciais e configurações do SEU ambiente Oracle.** Use os seguintes nomes de variáveis:

        ```dotenv
        # Configurações do banco de dados Oracle
        DB_USER=SEU_USUARIO_ORACLE     # Ex: SYSTEM ou um usuário dedicado que você criou
        DB_PASSWORD=SUA_SENHA_ORACLE    # A senha correspondente ao usuário acima
        DB_HOST=localhost              # Ou o endereço/IP do seu servidor Oracle
        DB_PORT=1522                   # A porta onde seu Listener Oracle está escutando (verifique com lsnrctl status)
        DB_SID=XE                      # Ou o SID/Service Name correto do seu banco

        # --- Limites opcionais para alertas ---
        # Remova o '#' da linha abaixo se quiser definir um limite diferente do padrão (85.0)
        # LIM_PROD=85.0

        # Remova o '#' da linha abaixo se quiser definir um limite diferente do padrão (2000.0)
        # LIM_PREJU=2000.0
        ```

3.  **Crie a tabela no Oracle**:
    * Conecte-se ao seu banco de dados Oracle usando uma ferramenta como SQL\*Plus ou SQL Developer (use o `DB_USER` e `DB_PASSWORD` que você configurou no `.env`).
    * Execute o conteúdo do script `criar_banco_colheita_cana_de_acucar.sql` para criar a tabela `COLHEITA_CANA`.

4.  **Execute o programa**:
    * Abra um terminal na pasta do projeto (`projeto_colheita_final_ENTREGA_FINAL_v2`).
    * (Opcional, mas recomendado: Ative seu ambiente virtual Python, se estiver usando um).
    * Digite o comando:
        ```bash
        python main.py
        ```

---

## 📌 Observações

- Os limites de produtividade (`LIM_PROD`) e prejuízo (`LIM_PREJU`) para os alertas podem ser configurados no arquivo `.env`. Se não forem definidos, o sistema usará valores padrão definidos em `funcoes.py` (85.0 t/ha e R$ 2000.00, respectivamente).
- O sistema gera logs no arquivo `gestao_colheita.log` e exibe mensagens de status/erro no console.
- A aplicação depende da correta configuração do arquivo `.env` e da disponibilidade do banco de dados Oracle para funcionar corretamente.

---

## ✍️ Autores

Grupo:
- **Nome:** Daniele Antonieta Garisto Dias
- **RM:** RM565106
- **Nome:** Leandro Augusto Jardim da Cunha
- **RM:** RM561395
- **Nome:** Luiz Eduardo da Silva
- **RM:** RM561701
- **Nome:** Vanessa Teles Paulino
- **RM:** RM565180
- **Nome:** João Victor Viana de Sousa
- **RM:** RM565136

- **Fase:** 2
- **Capítulo:** 6 - Python e além
- **Disciplina:** Inteligência Artificial – FIAP
- **Data:** Abril/2025
