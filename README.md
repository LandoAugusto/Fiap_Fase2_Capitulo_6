# Projeto de Modelagem de Banco de Dados Relacional – Gestão Inteligente do Agro

## 🎯 Introdução e Objetivo

Este projeto foi desenvolvido como atividade prática disponibilizada para o **Capítulo 1 – “Um mapa do tesouro”**, integrante da Fase 2 do curso de Inteligência Artificial da FIAP. Para sua elaboração, foram aplicados os conceitos apresentados nos **Capítulos 10, 11 e 12**, relacionados à modelagem de banco de dados relacional.

O principal objetivo é estruturar um sistema de banco de dados normalizado por meio da criação de um **Modelo Entidade-Relacionamento (MER)** e de um **Diagrama Entidade-Relacionamento (DER)**, simulando um cenário voltado à agricultura de precisão.

A solução proposta utiliza sensores para monitoramento em tempo real de variáveis do solo, como umidade, pH e nutrientes. Os dados são processados e armazenados para subsidiar decisões técnicas, como a aplicação de insumos agrícolas, além de possibilitar análises históricas e preditivas, otimizando os recursos e promovendo maior eficiência no cultivo.

### Regras de Negócio
- Sensores registram leituras a cada hora, armazenadas em `TBL_MONITORAMENTO`.
- O sistema compara leituras com valores mínimo/máximo definidos em `TBL_CULTURA_PRODUTO_SENSOR_CONFIGURACAO` para sugerir ajustes.
- Aplicações de água ou nutrientes são registradas em `TBL_APLICACAO_MONITORAMENTO` apenas quando as leituras estão fora dos limites ideais.

O banco foi projetado em **3ª Forma Normal (3NF)**, garantindo ausência de redundâncias e dependências parciais ou transitivas.

---

## 📝 Informações Relevantes e Dados Necessários

O sistema deve responder a perguntas como:

1. **Qual foi a quantidade total de água aplicada em cada mês?**
   - Dados: Data/hora e quantidade de água aplicada (`TBL_APLICACAO_MONITORAMENTO`).
   - Exemplo de consulta:
     ```sql
     SELECT TO_CHAR(a.dt_inclusao, 'YYYY-MM') AS mes, SUM(a.vlr_aplicado) AS total_agua
     FROM TBL_APLICACAO_MONITORAMENTO a
     JOIN TBL_MONITORAMENTO m ON a.cd_monitoramento = m.cd_monitoramento
     JOIN TBL_CULTURA_PRODUTO_SENSOR cps ON m.cd_cultura_produto_sensor = cps.cd_cultura_produto_sensor
     JOIN TBL_PRODUTO_SENSOR ps ON cps.cd_produto_sensor = ps.cd_produto_sensor
     JOIN TBL_PRODUTO p ON ps.cd_produto = p.cd_produto
     WHERE p.nm_produto = 'Agua'
     GROUP BY TO_CHAR(a.dt_inclusao, 'YYYY-MM');
     ```

2. **Como variou o nível de pH do solo ao longo do ano?**
   - Dados: Data/hora e valores de pH (`TBL_MONITORAMENTO`).
   - Exemplo de consulta:
     ```sql
     SELECT TO_CHAR(m.dt_inclusao, 'YYYY-MM') AS mes, AVG(m.vlr_medido) AS media_ph
     FROM TBL_MONITORAMENTO m
     JOIN TBL_CULTURA_PRODUTO_SENSOR cps ON m.cd_cultura_produto_sensor = cps.cd_cultura_produto_sensor
     JOIN TBL_PRODUTO_SENSOR ps ON cps.cd_produto_sensor = ps.cd_produto_sensor
     JOIN TBL_SENSOR s ON ps.cd_sensor = s.cd_sensor
     WHERE s.nm_sensor = 'Sensor de PH'
     GROUP BY TO_CHAR(m.dt_inclusao, 'YYYY-MM');
     ```

3. **Quais são os valores ideais para cada cultura monitorada?**
   - Dados: Faixas mínimas/máximas por sensor e cultura (`TBL_CULTURA_PRODUTO_SENSOR_CONFIGURACAO`).
   - Exemplo de consulta:
     ```sql
     SELECT c.nm_cultura, s.nm_sensor, cfg.vlr_minimo, cfg.vlr_maximo
     FROM TBL_CULTURA c
     JOIN TBL_CULTURA_PRODUTO_SENSOR cps ON c.cd_cultura = cps.cd_cultura
     JOIN TBL_CULTURA_PRODUTO_SENSOR_CONFIGURACAO cfg ON cps.cd_cultura_produto_sensor = cfg.cd_cultura_produto_sensor
     JOIN TBL_PRODUTO_SENSOR ps ON cps.cd_produto_sensor = ps.cd_produto_sensor
     JOIN TBL_SENSOR s ON ps.cd_sensor = s.cd_sensor;
     ```

---

## 🧱 Modelo Entidade-Relacionamento (MER)

### Entidades e Atributos

1. **TBL_SENSOR**
   - `cd_sensor` – NUMBER – Chave primária
   - `nm_sensor` – VARCHAR(50) – Nome do sensor (e.g., 'pH', 'Umidade')
   - `cd_status` – NUMBER(1) – Status (0 = inativo, 1 = ativo)
   - `cd_usuario_inclusao` – NUMBER – Usuário que criou o registro
   - `dt_inclusao` – DATE – Data de criação
   - Constraints: `cd_status CHECK (cd_status IN (0, 1))`, `nm_sensor NOT NULL`

2. **TBL_PRODUTO**
   - `cd_produto` – NUMBER – Chave primária
   - `nm_produto` – VARCHAR(50) – Nome do produto (e.g., 'Água', 'Fertilizante NPK')
   - `cd_usuario_inclusao`, `dt_inclusao` – Dados administrativos
   - Constraints: `nm_produto NOT NULL`

3. **TBL_CULTURA**
   - `cd_cultura` – NUMBER – Chave primária
   - `nm_cultura` – VARCHAR(50) – Nome da cultura (e.g., 'Soja', 'Milho')
   - `cd_usuario_inclusao`, `dt_inclusao` – Dados administrativos
   - Constraints: `nm_cultura NOT NULL`

4. **TBL_PRODUTO_SENSOR**
   - `cd_produto_sensor` – NUMBER – Chave primária
   - `cd_sensor` – NUMBER – FK para `TBL_SENSOR`
   - `cd_produto` – NUMBER – FK para `TBL_PRODUTO`

5. **TBL_CULTURA_PRODUTO_SENSOR**
   - `cd_cultura_produto_sensor` – NUMBER – Chave primária
   - `cd_cultura` – NUMBER – FK para `TBL_CULTURA`
   - `cd_produto_sensor` – NUMBER – FK para `TBL_PRODUTO_SENSOR`

6. **TBL_CULTURA_PRODUTO_SENSOR_CONFIGURACAO**
   - `cd_cultura_produto_sensor_configuracao` – NUMBER – Chave primária
   - `cd_cultura_produto_sensor` – NUMBER – FK
   - `vlr_minimo`, `vlr_maximo` – NUMBER(10,6) – Limites para a cultura
   - Constraints: `vlr_minimo <= vlr_maximo`

7. **TBL_MONITORAMENTO**
   - `cd_monitoramento` – NUMBER – Chave primária
   - `cd_cultura_produto_sensor` – NUMBER – FK
   - `vlr_medido` – NUMBER(10,6) – Valor lido pelo sensor
   - `dt_inclusao` – DATE – Data/hora da leitura
   - Constraints: `vlr_medido NOT NULL`

8. **TBL_APLICACAO_MONITORAMENTO**
   - `cd_aplicacao` – NUMBER – Chave primária
   - `cd_monitoramento` – NUMBER – FK
   - `vlr_medido`, `vlr_minimo`, `vlr_maximo`, `vlr_aplicado` – NUMBER(10,6)
   - `dt_inclusao` – DATE – Data/hora da aplicação

### Índices
- Índice em `TBL_MONITORAMENTO(dt_inclusao)` para consultas temporais.
- Índice em `TBL_APLICACAO_MONITORAMENTO(dt_inclusao)` para relatórios mensais.

### Relacionamentos e Cardinalidade
- **1:N** entre `TBL_PRODUTO` e `TBL_PRODUTO_SENSOR`.
- **1:N** entre `TBL_SENSOR` e `TBL_PRODUTO_SENSOR`.
- **1:N** entre `TBL_CULTURA` e `TBL_CULTURA_PRODUTO_SENSOR`.
- **1:N** entre `TBL_PRODUTO_SENSOR` e `TBL_CULTURA_PRODUTO_SENSOR`.
- **1:N** entre `TBL_CULTURA_PRODUTO_SENSOR` e `TBL_MONITORAMENTO`.
- **1:N** entre `TBL_MONITORAMENTO` e `TBL_APLICACAO_MONITORAMENTO`.

### Diagrama Entidade-Relacionamento (DER)
![DER](Sql Data Modeler.png)

---

## 🔗 Estrutura do Repositório

- `Cap 1 - Um mapa do tesouro.dmd` – Modelo no SQL Developer Data Modeler.
- `Sql Data Modeler.png` – Imagem do DER.
- `script cap 1.sql` – Script SQL para criação e inserção de dados.
- `README.md` – Documentação do projeto.

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos
- **SQL Developer Data Modeler** (versão 21.2 ou superior).
- Conta no [Oracle Live SQL](https://livesql.oracle.com/) ou um ambiente Oracle local.
- Editor de texto para visualizar o script SQL (e.g., VS Code).

### Passos
1. **Visualizar o modelo**:
   - Abra o arquivo `.dmd` no SQL Developer Data Modeler para explorar o DER.
2. **Executar o script SQL**:
   - Acesse o Oracle Live SQL.
   - Faça upload do `script cap 1.sql` e execute para criar as tabelas e inserir dados de teste.
3. **Validar os dados**:
   - Execute a consulta abaixo para verificar as leituras:
     ```sql
     SELECT * FROM TBL_MONITORAMENTO WHERE ROWNUM <= 10;
     ```
   - Teste as consultas da seção "Informações Relevantes" para validar os resultados.

---

## 🌱 Possíveis Extensões

- **Modelos Preditivos Simples**: Com os dados históricos registrados em `TBL_MONITORAMENTO`, é possível aplicar regressões lineares ou modelos de séries temporais simples (como média móvel ou suavização exponencial) para estimar variações futuras de umidade ou pH, contribuindo, por conseguinte, uma irrigação mais eficiente.

- **Dashboards Operacionais**: Usando ferramentas como Power BI, Metabase ou até planilhas conectadas ao banco, é possível gerar painéis visuais com gráficos de tendência por cultura, tipo de sensor, faixas críticas de medição, entre outros indicadores operacionais.

- **Alertas com SQL + Scripts Externos**: É viável desenvolver um script externo (em Python, por exemplo) que execute periodicamente consultas SQL no banco de dados e envie e-mails ou mensagens via API (como Telegram) sempre que forem detectadas leituras fora dos limites definidos em `TBL_CULTURA_PRODUTO_SENSOR_CONFIGURACAO`.

- **Exportação Automatizada de Relatórios**: Criar processos automatizados que consolidem os dados de cada cultura/sensor em arquivos `.csv` ou `.xlsx` e os enviem semanalmente para os responsáveis técnicos ou para o produtor.

---

## ✅ Entregas Atendidas
- [x] Modelo Entidade-Relacionamento (MER) documentado.
- [x] Diagrama Entidade-Relacionamento (DER) gerado.
- [x] Script SQL para criação e inserção de dados.
- [x] Repositório organizado no GitHub.

---

## 👤 Informações do Grupo
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
- **Capítulo:** 1 - Um mapa do tesouro

---

## 🔗 Link para o Repositório
[] <!-- Incluir o link -->
