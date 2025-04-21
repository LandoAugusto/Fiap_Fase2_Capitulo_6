# Arquivo: funcoes.py
# Funções auxiliares para cadastro, cálculo e geração de arquivos/relatórios

import json
import logging
import os
from typing import List, Dict, Any, Tuple, Optional

# Configuração do logging (caso este arquivo seja executado separadamente)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carrega limites do .env com valores padrão caso não definidos
LIMITE_PRODUTIVIDADE = float(os.getenv("LIM_PROD", 85.0))
LIMITE_PREJUIZO = float(os.getenv("LIM_PREJU", 2000.0))

def cadastrar_colheita() -> Optional[Dict[str, Any]]:
    """Coleta os dados de uma nova colheita do usuário e calcula campos derivados."""
    print("\n--- Cadastro de nova colheita ---")
    try:
        talhao = input("Informe o talhão (ex: A1): ").strip().upper()
        if not talhao:
            print("❌ Talhão não pode ser vazio.")
            return None

        area = float(input("Área plantada em hectares (ex: 1.5): "))
        if area <= 0:
            print("❌ Área deve ser maior que zero.")
            return None

        tipo_colheita = ""
        while tipo_colheita not in ["manual", "mecanica"]:
            tipo_colheita = input("Tipo de colheita (manual/mecanica): ").strip().lower()
            if tipo_colheita not in ["manual", "mecanica"]:
                print("❌ Tipo inválido. Digite 'manual' ou 'mecanica'.")

        producao = float(input("Produção em toneladas (ex: 100.0): "))
        if producao < 0:
            print("❌ Produção não pode ser negativa.")
            return None

        perda = float(input("Perda estimada em toneladas (ex: 5.0): "))
        if perda < 0:
            print("❌ Perda não pode ser negativa.")
            return None
        if perda > producao:
             print("⚠️ Alerta: Perda maior que a produção registrada.")


        preco_tonelada = float(input("Preço da tonelada (R$) (ex: 250.0): "))
        if preco_tonelada < 0:
             print("❌ Preço não pode ser negativo.")
             return None

        # Cálculos
        prejuizo = perda * preco_tonelada
        produtividade = producao / area if area > 0 else 0 # Evita divisão por zero

        colheita = {
            "talhao": talhao,
            "area": area,
            "tipo_colheita": tipo_colheita,
            "producao": producao,
            "perda": perda,
            "produtividade": round(produtividade, 2),
            "prejuizo": round(prejuizo, 2)
        }
        return colheita

    except ValueError:
        print("❌ Erro: Entrada inválida. Certifique-se de digitar números onde esperado.")
        return None
    except Exception as e:
         logging.error("Erro inesperado no cadastro: %s", e, exc_info=True)
         print("❌ Ocorreu um erro inesperado durante o cadastro.")
         return None


def formatar_exibicao_colheitas(colheitas: List[Dict[str, Any]]):
    """Formata e exibe os dados de uma lista de colheitas no console."""
    if not colheitas:
        print("\nNenhum registro para exibir.")
        return

    print("\n--- Registros de Colheita ---")
    # Cabeçalho (ajuste as larguras conforme necessário)
    print(f"{'ID':<5} {'Talhão':<8} {'Área(ha)':<10} {'Tipo':<10} {'Produção(t)':<12} {'Perda(t)':<10} {'Produt.(t/ha)':<15} {'Prejuízo(R$)':<12} {'Data':<12}")
    print("-" * 104)

    for c in colheitas:
        # Formata a data se existir e for do tipo datetime, senão usa string vazia
        data_colheita_str = c.get('data_coleta').strftime('%Y-%m-%d') if c.get('data_coleta') else 'N/A'

        print(f"{str(c.get('id', 'N/A')):<5} "
              f"{c.get('talhao', ''):<8} "
              f"{c.get('area', 0):<10.2f} "
              f"{c.get('tipo_colheita', ''):<10} "
              f"{c.get('producao', 0):<12.2f} "
              f"{c.get('perda', 0):<10.2f} "
              f"{c.get('produtividade', 0):<15.2f} "
              f"{c.get('prejuizo', 0):<12.2f} "
              f"{data_colheita_str:<12}")
    print("-" * 104)


def gerar_relatorio_txt(colheitas: List[Dict[str, Any]], nome_arquivo: str = "relatorio_colheita.txt") -> bool:
    """Gera um arquivo de texto (.txt) com os dados das colheitas."""
    if not colheitas:
        logging.warning("Nenhuma colheita fornecida para gerar relatório TXT.")
        return False
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write("=== Relatório de Colheitas ===\n\n")
            for c in colheitas:
                 data_str = c.get('data_coleta').strftime('%Y-%m-%d') if c.get('data_coleta') else 'N/A'
                 f.write(f"TALHÃO {c.get('talhao', 'N/A')} (ID: {c.get('id', 'N/A')}) - Data: {data_str}\n")
                 f.write(f"  Área: {c.get('area', 0):.2f} ha | Tipo: {c.get('tipo_colheita', 'N/A')}\n")
                 f.write(f"  Produção: {c.get('producao', 0):.2f} t | Perda: {c.get('perda', 0):.2f} t\n")
                 f.write(f"  Produtividade: {c.get('produtividade', 0):.2f} t/ha\n")
                 f.write(f"  Prejuízo Estimado: R$ {c.get('prejuizo', 0):.2f}\n")
                 f.write("-" * 40 + "\n")
            logging.info("Relatório TXT salvo com sucesso em %s", nome_arquivo)
            return True
    except IOError as e:
        logging.error("Erro ao escrever relatório TXT '%s': %s", nome_arquivo, e, exc_info=True)
        return False

def salvar_json(colheitas: List[Dict[str, Any]], nome_arquivo: str = "dados_colheita.json") -> bool:
    """Salva os dados das colheitas em um arquivo JSON."""
    if not colheitas:
        logging.warning("Nenhuma colheita fornecida para salvar em JSON.")
        return False

    # Converter objetos datetime para string ISO format para serialização JSON
    def converter_datas(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        raise TypeError(f"Objeto do tipo {type(obj)} não é serializável em JSON")

    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(colheitas, f, indent=4, ensure_ascii=False, default=converter_datas)
        logging.info("Dados JSON salvos com sucesso em %s", nome_arquivo)
        return True
    except (IOError, TypeError) as e:
        logging.error("Erro ao salvar arquivo JSON '%s': %s", nome_arquivo, e, exc_info=True)
        return False


def gerar_relatorio_estatistico(colheitas: List[Dict[str, Any]]) -> Optional[Dict[str, Dict[str, float]]]:
    """Calcula estatísticas de produtividade (média) por tipo de colheita."""
    if not colheitas:
        logging.warning("Nenhuma colheita para gerar estatísticas.")
        return None

    estatisticas_por_tipo: Dict[str, List[float]] = {"manual": [], "mecanica": []}
    for c in colheitas:
        tipo = c.get("tipo_colheita")
        produtividade = c.get("produtividade")
        if tipo in estatisticas_por_tipo and produtividade is not None:
            estatisticas_por_tipo[tipo].append(produtividade)

    resultado: Dict[str, Dict[str, float]] = {}
    for tipo, lista_produtividades in estatisticas_por_tipo.items():
        if lista_produtividades:
            media = sum(lista_produtividades) / len(lista_produtividades)
            resultado[tipo] = {"media_produtividade": round(media, 2), "registros": len(lista_produtividades)}
        else:
            resultado[tipo] = {"media_produtividade": 0.0, "registros": 0}

    return resultado


def alertar_colheitas_ineficientes(colheitas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Identifica colheitas com baixa produtividade e alto prejuízo."""
    alertas: List[Dict[str, Any]] = []
    if not colheitas:
        logging.warning("Nenhuma colheita para verificar alertas.")
        return alertas

    logging.info("Verificando alertas com Limite Produtividade < %.2f t/ha e Limite Prejuízo > R$ %.2f",
                 LIMITE_PRODUTIVIDADE, LIMITE_PREJUIZO)

    for c in colheitas:
        produtividade = c.get("produtividade", 0)
        prejuizo = c.get("prejuizo", 0)
        if produtividade < LIMITE_PRODUTIVIDADE and prejuizo > LIMITE_PREJUIZO:
            alertas.append(c)

    return alertas