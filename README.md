# Teste Analytics - Quod

Este repositório contém a resolução do Teste para Estagiário de Analytics da Quod. O projeto simula a base de dados de uma InsurTech (startup de seguros digitais), realiza a limpeza técnica dos dados, conduz uma análise exploratória focada na prevenção de fraudes e extrai consultas SQL relevantes para o negócio.

## Estrutura do Repositório

A organização dos arquivos foi pensada para separar claramente os dados brutos, os dados processados, os scripts de execução e os resultados visuais:

```text
Teste_Analytics_AlberisSilva/
├── README.md
├── relatorio_insights.md
├── dados/
│   ├── vendas_raw.csv                     <- Dataset bruto contendo erros propositais.
│   └── vendas_clean.csv                   <- Dataset limpo após o tratamento.
├── scripts_python/
│   ├── 01_geracao_e_limpeza.py            <- Script para criação dos dados, injeção de erros e limpeza.
│   └── 02_analise_exploratoria.py         <- Script para geração dos gráficos e análises estatísticas.
├── sql/
│   └── consultas_sql.sql                  <- Consultas SQL com base nas tabelas geradas.
└── graficos/
    ├── 01_tendencia_faturamento_total.png <- Gráfico de tendência (Total).
    ├── 02_tendencia_faturamento_produtos.png <- Gráfico de tendência (Por Produto).
    └── 03_boxplot_precos_celular.png      <- Gráfico estatístico de ticket médio.

## Dependências Necessárias

Para executar os scripts em Python, é necessário ter o Python 3 instalado, além das seguintes bibliotecas:

- pandas
- numpy
- matplotlib
- seaborn

Você pode instalá-las via terminal utilizando o comando:
pip install pandas numpy matplotlib seaborn

## Como Executar os Scripts

A execução deve seguir uma ordem estrita para garantir o fluxo correto do pipeline de dados:

1. Abra o terminal na pasta raiz do projeto.
2. Execute o primeiro script para gerar a base de dados e limpá-la:
   python scripts_python/01_geracao_e_limpeza.py
3. Com os dados limpos gerados na pasta `dados/`, execute o segundo script para gerar os gráficos na pasta `graficos/`:
   python scripts_python/02_analise_exploratoria.py

## Suposições e Premissas da Simulação

Para a construção deste case, as seguintes premissas de negócio foram assumidas:

1. Modelo de Negócio: A base simula uma empresa de micro-seguros digitais. Foram definidos quatro produtos: Seguro Celular (Roubo/Furto), Proteção Pix, Seguro Viagem Nacional e Seguro Residencial Básico.
2. Precificação e Quantidades: Produtos como Proteção Pix possuem valor fixo (R$ 15,00). O Seguro Celular possui valor variável de acordo com o aparelho protegido, sendo registrado sempre com Quantidade = 1 por apólice para permitir a análise correta do ticket médio (mediana).
3. Injeção de Erros: Para a etapa de limpeza, o script `01` insere propositalmente valores nulos no produto Proteção Pix, formatações de data incorretas e linhas duplicadas. A correção utiliza regras de negócio (ex: preencher nulos do Pix com seu valor fixo padrão).
4. Nota sobre o SQL (Parte 2): A Tarefa 2 solicita uma consulta para identificar o menor volume de vendas em "junho de 2024". Como o período simulado estipulado na Tarefa 1 é exclusivamente o ano de 2023, a query original foi documentada com a explicação do retorno vazio, e uma query adicional ajustada para junho de 2023 foi fornecida para demonstrar a lógica solicitada.
```
