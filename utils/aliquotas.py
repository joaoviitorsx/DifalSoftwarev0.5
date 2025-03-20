ALIQUOTAS_INTERESTADUAIS = {
    "11": 7,  # Rondônia
    "12": 12,  # Acre
    "13": 7,  # Amazonas
    "14": 12,  # Roraima
    "15": 7,  # Pará
    "16": 12,  # Amapá
    "17": 7,  # Tocantins
    "21": 12,  # Maranhão
    "22": 7,  # Piauí
    "23": 12,  # Ceará
    "24": 12,  # Rio Grande do Norte
    "25": 12,  # Paraíba
    "26": 12,  # Pernambuco
    "27": 12,  # Alagoas
    "28": 12,  # Sergipe
    "29": 12,  # Bahia
    "31": 7,  # Minas Gerais
    "32": 12,  # Espírito Santo
    "33": 7,  # Rio de Janeiro
    "35": 7,  # São Paulo
    "41": 7,  # Paraná
    "42": 7,  # Santa Catarina
    "43": 7,  # Rio Grande do Sul
    "50": 7,  # Mato Grosso do Sul
    "51": 12,  # Mato Grosso
    "52": 12,  # Goiás
    "53": 12  # Distrito Federal
}

CODIGO_UF = {
    "12": "AC",  "27": "AL",  "13": "AM",  "16": "AP",  "29": "BA",
    "23": "CE",  "53": "DF",  "32": "ES",  "52": "GO",  "21": "MA",
    "51": "MT",  "50": "MS",  "31": "MG",  "15": "PA",  "25": "PB",
    "26": "PE",  "22": "PI",  "41": "PR",  "33": "RJ",  "24": "RN",
    "43": "RS",  "11": "RO",  "14": "RR",  "42": "SC",  "35": "SP",
    "28": "SE",  "17": "TO"
}

def obter_aliquota_interestadual(codigo_uf_origem):
    """Retorna a alíquota interestadual com base no código da UF de origem."""
    return ALIQUOTAS_INTERESTADUAIS.get(codigo_uf_origem, 12) / 100

def obter_codigo_uf(sigla_uf):
    """Retorna o código da UF com base na sigla do estado."""
    for codigo, sigla in CODIGO_UF.items():
        if sigla == sigla_uf:
            return codigo
    return None