import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =============================================================================
# 1. CONFIGURAÇÃO DE DIRETÓRIOS E CARREGAMENTO
# =============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_DIR = os.path.join(BASE_DIR, 'dados')
GRAFICOS_DIR = os.path.join(BASE_DIR, 'graficos')
os.makedirs(GRAFICOS_DIR, exist_ok=True)

arquivo_clean = os.path.join(DADOS_DIR, 'vendas_clean.csv')
df = pd.read_csv(arquivo_clean)

df['Data'] = pd.to_datetime(df['Data'])
df['Mes'] = df['Data'].dt.month
df['Faturamento_Total'] = df['Quantidade'] * df['Preço']

# =============================================================================
# 2. FUNÇÕES AUXILIARES E PREPARAÇÃO DOS DADOS
# =============================================================================
# Função para formatar os números do eixo Y para o padrão brasileiro (R$)
def formatar_moeda(valor, posicao):
    return f'R$ {valor:,.0f}'.replace(',', '.')

faturamento_total = df.groupby('Mes')['Faturamento_Total'].sum()
faturamento_produto = df.pivot_table(index='Mes', columns='Produto', values='Faturamento_Total', aggfunc='sum', fill_value=0)
meses_labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# =============================================================================
# 3. GRÁFICO 1: TENDÊNCIA TOTAL DE VENDAS
# =============================================================================
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

plt.plot(faturamento_total.index, faturamento_total.values, 
         color='#1d3557', linewidth=3, linestyle='-', marker='o', markersize=8)

plt.title('Tendência Mensal de Vendas (2023) - Faturamento Total', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Mês', fontsize=12, labelpad=10)
plt.ylabel('Faturamento (R$)', fontsize=12, labelpad=10)
plt.xticks(range(1, 13), meses_labels, fontsize=11)
plt.yticks(fontsize=11)

# Usando função para formatar o eixo Y
ax = plt.gca()
ax.yaxis.set_major_formatter(plt.FuncFormatter(formatar_moeda))

plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, '01_tendencia_faturamento_total.png'), dpi=300)
plt.close()
print("-> Gráfico 1 (Total) salvo em 'graficos/01_tendencia_faturamento_total.png'")

# =============================================================================
# 4. GRÁFICO 2: TENDÊNCIA DE FATURAMENTO POR PRODUTO
# =============================================================================
plt.figure(figsize=(14, 7))
sns.set_theme(style="whitegrid")

cores = {
    'Celular (Roubo/Furto)': '#e63946', 
    'Viagem Nacional': '#457b9d',       
    'Residencial (Básico)': '#2a9d8f',  
    'Proteção Pix': '#f4a261'           
}

for produto in faturamento_produto.columns:
    plt.plot(faturamento_produto.index, faturamento_produto[produto], 
             label=produto, color=cores.get(produto, 'gray'), linewidth=2.5, marker='o')

plt.title('Tendência Mensal por Produto (2023) - Composição do Faturamento', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Mês', fontsize=12, labelpad=10)
plt.ylabel('Faturamento (R$)', fontsize=12, labelpad=10)
plt.xticks(range(1, 13), meses_labels, fontsize=11)

# Usando função para formatar o eixo Y
ax = plt.gca()
ax.yaxis.set_major_formatter(plt.FuncFormatter(formatar_moeda))

plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0., frameon=False, fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, '02_tendencia_faturamento_produtos.png'), dpi=300)
plt.close()
print("-> Gráfico 2 (Por Produto) salvo em 'graficos/02_tendencia_faturamento_produtos.png'")

# =============================================================================
# 5. GRÁFICO 3: BOXPLOT DO TICKET MÉDIO (CELULAR)
# =============================================================================
plt.figure(figsize=(12, 6))
sns.set_theme(style="whitegrid")

df_celular = df[df['Produto'] == 'Celular (Roubo/Furto)']

sns.boxplot(data=df_celular, x='Mes', y='Preço', color='#e63946', width=0.5, linewidth=1.5)

plt.title('Variação do Ticket Médio - Seguro Celular (2023)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Mês', fontsize=12)
plt.ylabel('Preço da Apólice (R$)', fontsize=12)
plt.xticks(range(0, 12), meses_labels, fontsize=11)

# Usando função para formatar o eixo Y
ax = plt.gca()
ax.yaxis.set_major_formatter(plt.FuncFormatter(formatar_moeda))

plt.tight_layout()
plt.savefig(os.path.join(GRAFICOS_DIR, '03_boxplot_precos_celular.png'), dpi=300)
plt.close()
print("-> Gráfico 3 (Boxplot) salvo em 'graficos/03_boxplot_precos_celular.png'")

# =============================================================================
# 6. INSIGHTS OBSERVADOS
# =============================================================================
"""
DOCUMENTAÇÃO DE INSIGHTS E PADRÕES:

Insight 1: Anomalia de Comportamento Pré-Carnaval (Risco de Fraude)
A análise combinada da 'Tendência por Produto' e do 'Boxplot de Ticket Médio' revela 
uma assimetria suspeita nos meses de Janeiro e Fevereiro. Há um salto no volume de 
faturamento do Seguro Celular. Contudo, o Boxplot evidencia que a mediana do preço 
pago pelas apólices nesse período cai drasticamente (R$ 40 - R$ 55), indicando a 
contratação de seguros para aparelhos de baixo valor agregado. Essa divergência aponta 
para uma forte hipótese de Risco Moral: usuários garantindo cobertura para "celulares 
do ladrão" (aparelhos secundários) antes das festividades, o que exige atenção da 
equipe de Antifraude quanto à sinistralidade dessa safra específica.

Insight 2: Sazonalidade Legítima vs. Linearidade da Base
A tendência financeira evidencia um comportamento genuíno de mercado nos meses finais 
do ano. O Seguro Celular volta a apresentar pico de faturamento em Outubro e Novembro, 
mas o Boxplot mostra que, diferentemente do Carnaval, a mediana de preços sobe consideravelmente 
(R$ 110 - R$ 150). Isso reflete a proteção real de aparelhos recém-lançados (efeito Apple/Samsung) 
e aquisições de Black Friday. Paralelamente, o 'Seguro Residencial' e a 'Proteção Pix' mantêm 
faturamento majoritariamente linear ao longo de todo o ano, confirmando a estabilidade e a menor 
suscetibilidade desses produtos a fraudes sazonais repentinas.
"""