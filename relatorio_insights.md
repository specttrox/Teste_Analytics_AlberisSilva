# Relatório de Insights e Recomendações

Neste relatório, apresento os resultados da análise exploratória dos dados de vendas de seguros do ano de 2023. O objetivo foi identificar padrões financeiros e comportamentais para auxiliar a tomada de decisão.

Durante a análise, dois comportamentos distintos chamaram a atenção no produto "Seguro Celular (Roubo/Furto)":

1. Possível Risco Moral (Pré-Carnaval): Em janeiro e fevereiro, observamos um grande pico no faturamento do seguro de celular. No entanto, ao analisar a distribuição de preços via Boxplot, notamos que a mediana do valor das apólices caiu drasticamente nesses meses (R$ 40 a R$ 55). Isso indica que os usuários buscaram proteger aparelhos de baixo custo logo antes das festividades, levantando uma forte suspeita de autofraude e risco moral (segurar "celulares descartáveis" para forjar sinistros).
2. Sazonalidade Legítima (Black Friday): Em outubro e novembro, houve um novo pico de faturamento do seguro celular. Diferente do Carnaval, a mediana de preços subiu consideravelmente (R$ 110 a R$ 150). Isso reflete um comportamento genuíno de proteção de aparelhos recém-comprados de alto valor.

Paralelamente, identifiquei via SQL e gráficos que produtos como o "Seguro Residencial" possuem a menor saída em meses centrais (como junho), mas garantem uma receita de base estável.

Ações Sugeridas:

- Equipe Antifraude: Aplicar regras de validação mais rígidas e monitorar de perto os sinistros acionados para apólices de celular contratadas entre janeiro e fevereiro.
- Equipe de Negócios: Criar campanhas de incentivo para o Seguro Residencial e Proteção Pix entre março e setembro, visando compensar a estabilização das vendas do Seguro Celular nesse período.
