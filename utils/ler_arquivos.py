import pandas as pd
import xmltodict
from PySide6.QtWidgets import QMessageBox, QFileDialog
from utils.calculo import calcular_difal, formatar_numero, extrair_info_chave_nfe
from utils.aliquotas import CODIGO_UF
from openpyxl import load_workbook
from openpyxl.styles import Font

def carregar_ncms_validos(arquivo_ncms):
    """Carrega e padroniza os NCMs da planilha, garantindo otimização para grandes volumes."""
    try:
        df = pd.read_excel(arquivo_ncms, dtype=str)
        df.columns = df.columns.str.strip().str.upper()
        if "NCM" in df.columns:
            df["NCM"] = df["NCM"].str.replace(".", "", regex=True).fillna("DESCONHECIDO")
        elif "NCM 2" in df.columns:
            df["NCM"] = df["NCM 2"].str.replace(".", "", regex=True).fillna("DESCONHECIDO")
        else:
            QMessageBox.critical(None, "Erro", "Nenhuma coluna 'NCM' ou 'NCM 2' encontrada na planilha de NCMs.")
            return pd.DataFrame()
        return df
    except Exception as e:
        QMessageBox.critical(None, "Erro ao carregar planilha", f"Erro: {str(e)}")
        return pd.DataFrame()

def carregar_planilha_xmls(arquivo_xmls):
    """Carrega e valida a planilha de XMLs de forma eficiente."""
    try:
        df = pd.read_excel(arquivo_xmls, dtype=str)
        df.columns = df.columns.str.strip().str.upper()
        colunas_necessarias = {
            "CHAVE_NF", "NCM", "CFOP", "VALOR_PRODUTO", "ICMS_ORIGINAL", "ICMS_VALOR",
            "NOME_CLIENTE", "CNPJ_CLIENTE", "NUMERO_NOTA", "COD_PRODUTO", "NOME_PRODUTO"
        }
        colunas_faltando = colunas_necessarias - set(df.columns)
        if colunas_faltando:
            QMessageBox.critical(None, "Erro", f"Colunas ausentes na planilha XMLs: {', '.join(colunas_faltando)}")
            return pd.DataFrame()
        
        for coluna in colunas_necessarias:
            df[coluna] = df[coluna].fillna("DESCONHECIDO")
        
        return df
    except Exception as e:
        QMessageBox.critical(None, "Erro ao carregar planilha", f"Erro: {str(e)}")
        return pd.DataFrame()

def processar_nfes(arquivo_xmls, arquivo_ncms, progresso, janela):
    """Processa os arquivos XML e NCM para cálculo do DIFAL."""
    
    # Verifica se os arquivos foram selecionados
    if not arquivo_xmls or not arquivo_ncms:
        QMessageBox.warning(janela, "Erro", "Selecione os arquivos antes de processar!")
        return
    
    try:
        # Carrega os arquivos Excel
        df_ncms = pd.read_excel(arquivo_ncms, dtype=str)
        df_xmls = pd.read_excel(arquivo_xmls, dtype=str)

        # Normaliza os nomes das colunas
        df_ncms.columns = df_ncms.columns.str.strip().str.upper()
        df_xmls.columns = df_xmls.columns.str.strip().str.upper()

        # Verifica se as colunas essenciais estão presentes
        colunas_necessarias = {"CHAVE_NF", "NCM", "CFOP", "VALOR_PRODUTO", "ICMS_ORIGINAL", "ICMS_VALOR",
                               "NOME_CLIENTE", "CNPJ_CLIENTE", "NUMERO_NOTA", "COD_PRODUTO", "NOME_PRODUTO"}
        if not colunas_necessarias.issubset(df_xmls.columns):
            QMessageBox.critical(janela, "Erro", "A planilha XMLs está faltando colunas essenciais.")
            return

        resultados = []
        total = len(df_xmls)

        for i, row in df_xmls.iterrows():
            try:
                chave_nfe = row.get("CHAVE_NF", "").strip()
                uf_origem, ano, mes = extrair_info_chave_nfe(chave_nfe)
                valor_produto = formatar_numero(row.get("VALOR_PRODUTO", "0"))
                icms_origem = formatar_numero(row.get("ICMS_ORIGINAL", "0"))
                icms_destino = formatar_numero(row.get("ICMS_VALOR", "0"))

                # Obtém o estado da empresa
                uf_empresa = CODIGO_UF.get(janela.empresa["cnpj"][:2], "Desconhecido")
                aliquota_interna = janela.aliquota / 100

                difal = calcular_difal(valor_produto, uf_origem, uf_empresa, aliquota_interna)

                resultados.append({
                    "ANO": ano,
                    "MÊS": mes,
                    "PARTIC": row.get("NOME_CLIENTE", "").strip(),
                    "CNPJ": row.get("CNPJ_CLIENTE", "").strip(),
                    "CFOP": row.get("CFOP", "").strip(),
                    "NF": row.get("NUMERO_NOTA", "").strip(),
                    "UF": uf_origem,
                    "CHAVE NFE": chave_nfe,
                    "CODIGO": row.get("COD_PRODUTO", "").strip(),
                    "DESCRICAO": row.get("NOME_PRODUTO", "").strip(),
                    "NCM": row.get("NCM", "").strip(),
                    "DIFAL": "SIM" if difal > 0 else "NÃO",
                    "VR ITEM": valor_produto,
                    "ICMS ORIGEM": icms_origem,
                    "ICMS DESTINO": icms_destino,
                    "VR DIFAL": difal,
                })

            except Exception as e:
                print(f"Erro ao processar linha {i}: {e}")

            progresso.setValue(int((i + 1) / total * 100))

        df_resultado = pd.DataFrame(resultados)

        caminho_saida, _ = QFileDialog.getSaveFileName(janela, "Salvar Planilha de Cálculos", "", "Planilhas Excel (*.xlsx)")
        if caminho_saida:
            df_resultado.to_excel(caminho_saida, index=False)
            QMessageBox.information(janela, "Concluído", "Planilha gerada com sucesso!")

        abrir_arquivo = QMessageBox.question(janela, "Abrir Planilha", "Deseja abrir a planilha gerada?", QMessageBox.Yes | QMessageBox.No)
        if abrir_arquivo == QMessageBox.Yes:
            import os
            os.startfile(caminho_saida)
        
        self.progress_bar.setValue(0)

    except Exception as e:
        QMessageBox.critical(janela, "Erro ao processar arquivos", f"Ocorreu um erro: {str(e)}")