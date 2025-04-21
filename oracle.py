from typing import Optional, List, Dict, Any
import oracledb
import os
from dotenv import load_dotenv
import logging

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SID = os.getenv("DB_SID")
# Verifica se todas as variáveis foram carregadas antes de montar o DSN
DSN = f"{DB_HOST}:{DB_PORT}/{DB_SID}" if all([DB_HOST, DB_PORT, DB_SID]) else None

def get_connection() -> Optional[oracledb.Connection]:
    """Tenta estabelecer uma conexão com o banco de dados Oracle."""
    if not DSN:
        logging.error("Credenciais do banco de dados não configuradas corretamente no .env (HOST, PORT ou SID faltando).")
        print("❌ Credenciais do banco de dados não configuradas corretamente no .env")
        return None
    try:
        # Tenta conectar usando as credenciais carregadas
        conexao = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DSN)
        logging.info("Conexão com Oracle estabelecida.")
        # Não imprime sucesso aqui para não poluir a saída das funções principais
        return conexao
    except oracledb.Error as erro: # Captura erros específicos do oracledb
        # Loga o erro detalhado
        logging.error("Falha ao conectar ao Oracle. DSN: %s, User: %s. Erro: %s", DSN, DB_USER, erro, exc_info=True)
        # Imprime mensagem mais amigável para o usuário
        print(f"❌ Falha ao conectar ao Oracle (Host: {DB_HOST}, Porta: {DB_PORT}, SID: {DB_SID}).")
        print("   Verifique se o banco está em execução, se as credenciais no .env estão corretas e se a rede está ok.")
        print(f"   Detalhe do erro Oracle: {erro}") # Mostra o detalhe do erro Oracle
        return None
    except Exception as e: # Captura outros erros inesperados
        logging.error("Erro inesperado ao tentar conectar ao Oracle: %s", e, exc_info=True)
        print(f"❌ Ocorreu um erro inesperado durante a conexão: {e}")
        return None


def listar_colheitas_oracle() -> List[Dict[str, Any]]:
    """Busca todos os registros de colheita do banco de dados Oracle."""
    sql = "SELECT ID, TALHAO, AREA, TIPO_COLHEITA, PRODUCAO, PERDA, PRODUTIVIDADE, PREJUIZO, DATA_COLETA FROM COLHEITA_CANA ORDER BY DATA_COLETA DESC, TALHAO ASC"
    conexao = None # Inicializa como None
    cursor = None # Inicializa como None
    resultados = []
    try:
        conexao = get_connection()
        if not conexao:
            # Mensagem de erro já foi impressa por get_connection
            return []  # Retorna lista vazia se não conectar

        cursor = conexao.cursor()
        cursor.execute(sql)
        # Pega os nomes das colunas do cursor para usar como chaves do dicionário
        colunas = [col[0].lower() for col in cursor.description]
        # Cria uma lista de dicionários, mapeando colunas para valores de cada linha
        resultados = [dict(zip(colunas, row)) for row in cursor]
        logging.info("Consulta ao Oracle retornou %d registros.", len(resultados))

    except oracledb.Error as erro_db:
        logging.error("Erro ao consultar Oracle: %s", erro_db, exc_info=True)
        print(f"❌ Erro ao consultar dados no Oracle: {erro_db}")
    except Exception as erro_geral:
        logging.error("Erro inesperado durante a consulta ao Oracle: %s", erro_geral, exc_info=True)
        print(f"❌ Erro inesperado ao processar consulta: {erro_geral}")
    finally:
        # Garante que cursor e conexão sejam fechados mesmo se ocorrer erro
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
            logging.info("Conexão com Oracle fechada após consulta.")
    return resultados


def salvar_colheita_oracle(colheita: Dict[str, Any]) -> None:
    """Salva um registro de colheita no banco de dados Oracle."""
    conexao = None # Inicializa como None
    cursor = None # Inicializa como None
    try:
        conexao = get_connection()
        if not conexao:
            # Mensagem de erro já foi impressa por get_connection
            # Não imprime novamente para evitar duplicidade
            return # Sai da função se não conectar

        # --- CORREÇÃO APLICADA AQUI ---
        # Ajustado para usar a coluna AREA e remover PRECO_TONELADA
        sql = """
            INSERT INTO COLHEITA_CANA (
                TALHAO, AREA, TIPO_COLHEITA, PRODUCAO, PERDA,
                PRODUTIVIDADE, PREJUIZO, DATA_COLETA
            ) VALUES (
                :talhao, :area_plantada, :tipo_colheita, :producao, :perda,
                :produtividade, :prejuizo, SYSDATE
            )
        """
        # --- FIM DA CORREÇÃO ---

        cursor = conexao.cursor()
        # Passa o dicionário 'colheita' diretamente, o driver mapeia as chaves
        cursor.execute(sql, colheita)
        conexao.commit() # Confirma a transação
        print("✅ Colheita salva com sucesso no Oracle.")
        logging.info("Registro de colheita para talhão %s salvo no Oracle.", colheita.get('talhao'))

    except oracledb.DatabaseError as erro_db:
        # Erros específicos do banco (constraint violation, tipo de dado, etc.)
        logging.error("Erro de banco de dados ao salvar no Oracle: %s", erro_db, exc_info=True)
        print(f"❌ Erro ao salvar no Oracle: {erro_db}")
        # Adiciona link de ajuda para erros ORA comuns
        if hasattr(erro_db, 'args') and erro_db.args:
             ora_error = erro_db.args[0]
             if hasattr(ora_error, 'code') and hasattr(ora_error, 'message'):
                 print(f"   Código Oracle: ORA-{ora_error.code:05d}")
                 # Link genérico para a documentação de erros Oracle
                 print(f"   Ajuda: https://docs.oracle.com/error-help/db/ora-{ora_error.code:05d}/")
        try:
            conexao.rollback() # Tenta reverter a transação em caso de erro
            logging.warning("Transação revertida (rollback) devido a erro ao salvar.")
        except Exception as rollback_error:
            logging.error("Erro ao tentar reverter transação: %s", rollback_error)

    except Exception as erro_geral:
        # Outros erros inesperados
        logging.error("Erro inesperado ao salvar no Oracle: %s", erro_geral, exc_info=True)
        print(f"❌ Ocorreu um erro inesperado ao tentar salvar: {erro_geral}")

    finally:
        # Garante que cursor e conexão sejam fechados
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
            logging.info("Conexão com Oracle fechada após tentativa de salvar.")
