/* =========================================================================================
   PARTE 2: CONSULTAS SQL
   Candidato: Alberis Silva
   Tabela base assumida: vendas (refletindo a estrutura do arquivo vendas_clean.csv)
   ========================================================================================= */

/* -----------------------------------------------------------------------------------------
   QUERY 1: Faturamento total por produto
   Objetivo: Listar o nome do produto, categoria e a soma total de vendas (Quantidade * Preço) 
   para cada produto, ordenado pelo valor total de vendas em ordem decrescente.
   
   Explicação da lógica:
   - Utilizando a função de agregação SUM() multiplicando a Quantidade pelo Preço unitário 
     diretamente dentro da consulta para obter o faturamento (Total_Vendas).
   - O GROUP BY agrupa os resultados pelo Produto e Categoria, garantindo que a soma 
     seja calculada para cada item específico do portfólio.
   - O ORDER BY ... DESC garante que o produto que mais gerou receita apareça no topo.
   ----------------------------------------------------------------------------------------- */

SELECT 
    Produto,
    Categoria,
    SUM(Quantidade * Preço) AS Total_Vendas
FROM 
    vendas
GROUP BY 
    Produto,
    Categoria
ORDER BY 
    Total_Vendas DESC;


/* -----------------------------------------------------------------------------------------
   QUERY 2A: Produto que menos vendeu em Junho de 2024 (Conforme Edital)
   Objetivo: Identificar os produtos que venderam menos no mês de junho de 2024.
   
   Explicação da lógica (NOTA CRÍTICA):
   - A query abaixo atende estritamente à solicitação do case para "junho de 2024". 
   - Contudo, conforme a premissa definida na Parte 1 do case, o dataset simulado compreende 
     apenas o período de 01/01/2023 a 31/12/2023.
   - Portanto, a execução desta query retornará um result set VAZIO (0 linhas).
   ----------------------------------------------------------------------------------------- */

SELECT 
    Produto,
    SUM(Quantidade * Preço) AS Faturamento_Mensal
FROM 
    vendas
WHERE 
    Data >= '2024-06-01' AND Data <= '2024-06-30'
GROUP BY 
    Produto
ORDER BY 
    Faturamento_Mensal ASC
LIMIT 1;


/* -----------------------------------------------------------------------------------------
   QUERY 2B: Produto que menos vendeu em Junho de 2023 (Ajuste Lógico)
   Objetivo: Identificar o produto com o menor faturamento no mês de junho do ano base (2023).
   
   Explicação da lógica:
   - Filtramos o mês de junho de 2023 usando a cláusula WHERE com range de datas.
   - Agrupamos por produto e somamos o faturamento.
   - Ordenamos de forma ascendente (ASC) para que o menor valor suba para a primeira linha.
   - O LIMIT 1 garante que apenas o produto com o menor desempenho seja retornado. 
     (Nota: caso a base de dados fosse SQL Server, usa-se SELECT TOP 1).
   ----------------------------------------------------------------------------------------- */

SELECT 
    Produto,
    SUM(Quantidade * Preço) AS Faturamento_Mensal
FROM 
    vendas
WHERE 
    Data >= '2023-06-01' AND Data <= '2023-06-30'
GROUP BY 
    Produto
ORDER BY 
    Faturamento_Mensal ASC
LIMIT 1;

/* FIM DO SCRIPT */