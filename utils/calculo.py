from utils.aliquotas import obter_aliquota_interestadual

def calcular_difal(valor_operacao, uf_origem, uf_empresa, aliquota_interna):
    """Calcula o DIFAL considerando as alíquotas internas e interestaduais."""
    if uf_origem == uf_empresa:
        return 0.0 
    
    # Obtém a alíquota interestadual
    aliquota_interestadual = obter_aliquota_interestadual(uf_origem)
    icms_origem = valor_operacao * aliquota_interestadual
    
    # Base de cálculo para o ICMS de destino
    base_calculo = (valor_operacao - icms_origem) / (1 - aliquota_interna)
    icms_destino = base_calculo * aliquota_interna
    
    return icms_destino - icms_origem

def formatar_numero(valor):
    """Converte strings numéricas para float, tratando valores inválidos."""
    if not valor or isinstance(valor, float) or isinstance(valor, int):
        return float(valor) if valor else 0.0
    if isinstance(valor, str):
        valor = valor.strip()
        if valor.lower() in ["não informado", "-", "", "null"]:
            return 0.0
        return float(valor.replace(".", "").replace(",", "."))
    return 0.0

def extrair_info_chave_nfe(chave_nfe):
    """Extrai UF e Ano/Mês da chave de acesso da NF-e."""
    if chave_nfe.startswith("NFe"):
        chave_nfe = chave_nfe[3:] 
    
    if len(chave_nfe) == 44:  
        uf_codigo = chave_nfe[:2] 
        aa_mm = chave_nfe[2:6] 
        ano = "20" + aa_mm[:2] 
        mes = aa_mm[2:] 
        return uf_codigo, ano, mes
    
    return "Desconhecido", "", ""