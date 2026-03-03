import pandas as pd
import numpy as np
import random
from datetime import datetime
import os
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_DIR = os.path.join(BASE_DIR, 'dados')
os.makedirs(DADOS_DIR, exist_ok=True)

np.random.seed(42)
random.seed(42)

produtos = {
    'Celular (Roubo/Furto)': {'categoria': 'Dispositivos', 'tipo_preco': 'variavel', 'qtd_fixa': 1},
    'Proteção Pix': {'categoria': 'Financeiro', 'tipo_preco': 'fixo', 'preco': 15.00, 'qtd_fixa': None},
    'Viagem Nacional': {'categoria': 'Viagem', 'tipo_preco': 'fixo', 'preco': 40.00, 'qtd_fixa': None},
    'Residencial (Básico)': {'categoria': 'Imóveis', 'tipo_preco': 'variavel', 'qtd_fixa': 1}
}

dados_simulados = []

# CONTROLE DE VOLUME: Definição do volume de vendas da empresa por mês.
# Totaliza 350 registros, bem distribuídos.
distribuicao_meses = {
    1: 65,  # Jan: Alto volume
    2: 25,  # Fev: Queda natural pós compra pré-carnaval
    3: 22,  # Março a Setembro: Estabilidade
    4: 22,  
    5: 22,
    6: 22,  
    7: 22,  
    8: 22,  
    9: 22,  
    10: 32, # Outubro: Aumenta volume levemente (Lançamentos), mas menor que Nov
    11: 48, # Novembro: Pico de volume (Black Friday) 
    12: 26  # Dezembro: Estabilidade com foco em viagem
}

for mes, qtd_vendas in distribuicao_meses.items():
    for _ in range(qtd_vendas):
        # Sorteia apenas o dia dentro do mês específico
        if mes in [1, 3, 5, 7, 8, 10, 12]: dia = random.randint(1, 31)
        elif mes == 2: dia = random.randint(1, 28)
        else: dia = random.randint(1, 30)
        
        data_venda = datetime(2023, mes, dia)
        
        # PESOS (PROBABILIDADE DE CADA PRODUTO SAIR)
        if mes == 1:
            pesos = [12, 1, 2, 1]  # Força no Celular
        elif mes == 2:
            pesos = [2, 1, 5, 1]   # Força em Viagem
        elif mes == 6:
            pesos = [2, 1, 1, 0.2] # Queda Residencial
        elif mes == 10:
            pesos = [5, 1, 1, 1]   # Aumento médio do Celular
        elif mes == 11:
            pesos = [10, 1, 1, 1]  # Pico explosivo do Celular na BF
        elif mes == 12:
            pesos = [2, 1, 5, 1]   # Força em Viagem
        else:
            pesos = [2, 1, 1, 1]   # Março a Set: Estável e linear

        nome_produto = random.choices(list(produtos.keys()), weights=pesos, k=1)[0]
        info = produtos[nome_produto]
        
        if info['tipo_preco'] == 'fixo':
            preco = info['preco']
            quantidade = random.randint(1, 2)
        else:
            # BOXPLOT
            if nome_produto == 'Celular (Roubo/Furto)':
                if mes in [1, 2]:
                    preco = round(random.uniform(40.0, 55.0), 2)
                elif mes in [10, 11]:
                    preco = round(random.uniform(110.0, 150.0), 2)
                else:
                    preco = round(random.uniform(75.0, 85.0), 2)
            else:
                preco = round(random.uniform(30.0, 80.0), 2)
            
            quantidade = info['qtd_fixa']

        registro = {
            'ID': str(uuid.uuid4())[:8],
            'Data': data_venda.strftime('%Y-%m-%d'),
            'Produto': nome_produto,
            'Categoria': info['categoria'],
            'Quantidade': quantidade,
            'Preço': preco
        }
        dados_simulados.append(registro)

df_raw = pd.DataFrame(dados_simulados)

# Inserindo os erros para a etapa de limpeza
idx_pix = df_raw[df_raw['Produto'] == 'Proteção Pix'].sample(4).index
df_raw.loc[idx_pix, 'Preço'] = np.nan
idx_datas = df_raw.sample(3).index
df_raw.loc[idx_datas, 'Data'] = pd.to_datetime(df_raw.loc[idx_datas, 'Data']).dt.strftime('%d/%m/%Y')
df_raw = pd.concat([df_raw, df_raw.tail(2)], ignore_index=True)

arquivo_raw = os.path.join(DADOS_DIR, 'vendas_raw.csv')
df_raw.to_csv(arquivo_raw, index=False)

# Limpeza
df_clean = df_raw.copy()
df_clean = df_clean.drop_duplicates()
df_clean.loc[(df_clean['Produto'] == 'Proteção Pix') & (df_clean['Preço'].isna()), 'Preço'] = 15.00
df_clean['Data'] = pd.to_datetime(df_clean['Data'], format='mixed', dayfirst=True).dt.strftime('%Y-%m-%d')

arquivo_clean = os.path.join(DADOS_DIR, 'vendas_clean.csv')
df_clean.to_csv(arquivo_clean, index=False)

df_clean['Valor_Total_Venda'] = df_clean['Quantidade'] * df_clean['Preço']
vendas_por_produto = df_clean.groupby('Produto')['Valor_Total_Venda'].sum().reset_index()
vendas_por_produto.columns = ['Produto', 'Total Vendas (R$)']
vendas_por_produto = vendas_por_produto.sort_values(by='Total Vendas (R$)', ascending=False)

print("\n" + "="*50)
print("ANALISE DE VENDAS")
print("="*50)
print(vendas_por_produto.to_string(index=False))
print("-" * 50)
produto_top = vendas_por_produto.iloc[0]['Produto']
valor_top = vendas_por_produto.iloc[0]['Total Vendas (R$)']
print(f"PRODUTO MAIS VENDIDO: {produto_top} (R$ {valor_top:.2f})")
print("="*50 + "\n")