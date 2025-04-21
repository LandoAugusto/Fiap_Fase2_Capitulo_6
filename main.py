# Arquivo principal do sistema - main.py

import logging
from funcoes import (
    cadastrar_colheita,
    formatar_exibicao_colheitas,
    gerar_relatorio_txt,
    salvar_json,
    gerar_relatorio_estatistico,
    alertar_colheitas_ineficientes,
    LIMITE_PRODUTIVIDADE,
    LIMITE_PREJUIZO
)
from oracle import (
    salvar_colheita_oracle,
    listar_colheitas_oracle # Agora retorna dados
)

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("gestao_colheita.log"), logging.StreamHandler()])

logging.info("Iniciando o Sistema de Gestão de Colheita...")

# Loop principal
while True:
    print("\n=== SISTEMA DE GESTÃO DE COLHEITA DE CANA-DE-AÇÚCAR ===")
    # --- Textos do Menu Ajustados ---
    print("1. Cadastrar nova colheita (e salvar no Oracle)") # Ajustado
    print("2. Listar todas as colheitas (do Oracle)")      # Ajustado
    # --- Fim dos Ajustes no Menu ---
    print("3. Gerar relatório (.txt)")
    print("4. Salvar dados (.json)")
    print("5. Relatório estatístico por tipo de colheita")
    print("6. Alerta de colheitas ineficientes")
    print("0. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        try:
            nova_colheita = cadastrar_colheita()
            if nova_colheita:
                # Prepara o dicionário para o Oracle (precisa corresponder às colunas)
                # Assumindo que as chaves de `nova_colheita` já correspondem aos parâmetros esperados
                # por `salvar_colheita_oracle` (verificar `oracle.py` se necessário)
                colheita_para_db = {
                    "talhao": nova_colheita["talhao"],
                    "area_plantada": nova_colheita["area"], # Ajustar chave se nome da coluna for diferente
                    "tipo_colheita": nova_colheita["tipo_colheita"],
                    "producao": nova_colheita["producao"],
                    "perda": nova_colheita["perda"],
                    "produtividade": nova_colheita["produtividade"],
                    "prejuizo": nova_colheita["prejuizo"]
                    # DATA_COLETA é DEFAULT SYSDATE no Oracle
                }

                # Tenta salvar no Oracle
                salvar_colheita_oracle(colheita_para_db) # Não retorna status aqui, apenas imprime
                # A mensagem de sucesso/erro é impressa dentro de salvar_colheita_oracle

        except Exception as e:
            logging.error("Erro inesperado na opção 1: %s", e, exc_info=True)
            print("❌ Ocorreu um erro inesperado durante o cadastro.")

    elif opcao == "2": # Listar colheitas
        try:
            colheitas_db = listar_colheitas_oracle()
            formatar_exibicao_colheitas(colheitas_db)
        except Exception as e:
            logging.error("Erro inesperado na opção 2: %s", e, exc_info=True)
            print("❌ Ocorreu um erro inesperado ao listar colheitas.")

    elif opcao == "3": # Gerar TXT
        try:
            colheitas_db = listar_colheitas_oracle()
            if colheitas_db:
                if gerar_relatorio_txt(colheitas_db): # Passa os dados lidos do Oracle
                    print(f"✅ Relatório salvo em relatorio_colheita.txt")
                else:
                    print("❌ Falha ao gerar relatório TXT.")
            else:
                 print("ℹ️ Não há dados no Oracle para gerar o relatório.")
        except Exception as e:
            logging.error("Erro inesperado na opção 3: %s", e, exc_info=True)
            print("❌ Ocorreu um erro inesperado ao gerar relatório TXT.")

    elif opcao == "4": # Salvar JSON
        try:
            colheitas_db = listar_colheitas_oracle()
            if colheitas_db:
                if salvar_json(colheitas_db): # Passa os dados lidos do Oracle
                    print(f"✅ Dados salvos em dados_colheita.json")
                else:
                    print("❌ Falha ao salvar arquivo JSON.")
            else:
                 print("ℹ️ Não há dados no Oracle para salvar em JSON.")
        except Exception as e:
            logging.error("Erro inesperado na opção 4: %s", e, exc_info=True)
            print("❌ Ocorreu um erro inesperado ao salvar JSON.")

    elif opcao == "5": # Relatório Estatístico
        try:
            colheitas_db = listar_colheitas_oracle()
            estatisticas = gerar_relatorio_estatistico(colheitas_db) # Passa os dados lidos do Oracle
            if estatisticas:
                print("\n📊 Relatório Estatístico de Produtividade (t/ha):")
                for tipo, dados in estatisticas.items():
                    if dados['registros'] > 0:
                        print(f"  - {tipo.capitalize()}: Média {dados['media_produtividade']:.2f} (baseado em {dados['registros']} registros)")
                    else:
                        print(f"  - {tipo.capitalize()}: Sem registros.")
            else:
                print("ℹ️ Não há dados suficientes no Oracle para gerar estatísticas.")
        except Exception as e:
            logging.error("Erro inesperado na opção 5: %s", e, exc_info=True)
            print("❌ Ocorreu um erro inesperado ao gerar estatísticas.")

    elif opcao == "6": # Alerta de Ineficiência
        try:
            colheitas_db = listar_colheitas_oracle()
            colheitas_alerta = alertar_colheitas_ineficientes(colheitas_db) # Passa os dados lidos do Oracle
            if colheitas_alerta:
                print("\n🚨 Alerta de Colheitas Ineficientes:")
                print(f"   (Produtividade < {LIMITE_PRODUTIVIDADE:.2f} t/ha E Prejuízo > R$ {LIMITE_PREJUIZO:.2f})")
                for c in colheitas_alerta:
                     # Usa .get com default para evitar KeyError se a coluna não existir
                     data_str = c.get('data_coleta').strftime('%Y-%m-%d') if c.get('data_coleta') else 'N/A'
                     print(f"  - ID {c.get('id', 'N/A')} | Talhão {c.get('talhao', '')} ({data_str}) | Produt.: {c.get('produtividade', 0):.2f} t/ha | Prejuízo: R$ {c.get('prejuizo', 0):.2f}")
            elif colheitas_db: # Só diz que não há alerta se houve dados para analisar
                print("\n✅ Nenhuma colheita em situação crítica encontrada nos dados do Oracle.")
            else:
                print("ℹ️ Não há dados no Oracle para verificar alertas.")
        except Exception as e:
            logging.error("Erro inesperado na opção 6: %s", e, exc_info=True)
            print("❌ Ocorreu um erro inesperado ao verificar alertas.")

    elif opcao == "0":
        print("Encerrando o programa...")
        logging.info("Sistema de Gestão de Colheita encerrado.")
        break

    else:
        print("❌ Opção inválida. Tente novamente.")
