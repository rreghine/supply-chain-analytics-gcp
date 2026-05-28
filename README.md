# Supply Chain Analytics

![dbt](https://img.shields.io/badge/dbt-Core-orange?style=flat-square)
![BigQuery](https://img.shields.io/badge/BigQuery-GCP-blue?style=flat-square)
![Looker](https://img.shields.io/badge/Looker_Studio-Dashboard-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

Pipeline analítico end-to-end de Supply Chain com arquitetura Medallion (Bronze → Silver → Gold) no BigQuery, modelagem dimensional com dbt e dashboard executivo no Looker Studio — construído sobre o dataset público TheLook Ecommerce do Google.

---

## Preview

### Operational Performance
![Operational Performance](docs/page1_operational.png)

### Geographic Performance
![Geographic Performance](docs/page2_geographic.png)

### Product Analysis
![Product Analysis](docs/page3_product.png)

---

## Contexto de Negócio

Operações de Supply Chain geram grandes volumes de dados — pedidos, entregas, lead times, fornecedores. Sem modelagem analítica estruturada, esses dados ficam dispersos e inacessíveis para decisão.

**Perguntas centrais respondidas:**

- Qual o On-Time Delivery Rate da operação?
- Quais países têm o maior lead time — e maior receita?
- Quais categorias e marcas concentram o faturamento?
- Como o volume de pedidos evolui ao longo do tempo?

---

## Dataset

**TheLook Ecommerce — BigQuery Public Data**

- Dataset público do Google com dados simulados de e-commerce
- Tabelas: `orders`, `order_items`, `products`, `users`, `inventory_items`, `distribution_centers`
- Escala: ~30.000 pedidos, 13 países, receita total de R$ 2,67M

---

## Arquitetura

```
TheLook Ecommerce (BigQuery Public Data)
        ↓
Staging Layer — limpeza e padronização das fontes
  stg_orders · stg_order_items · stg_products
  stg_users · stg_inventory · stg_distribution_centers
        ↓
Intermediate Layer — joins e regras de negócio
  int_orders_enriched · int_order_items_enriched
        ↓
Marts Layer — modelos analíticos finais
  fct_orders · fct_order_items · kpis_supply_chain
        ↓
Looker Studio — Dashboard Executivo (3 páginas)
```

### Lineage Graph
![Lineage Graph](docs/lineage_graph.png)

---

## Estrutura do Projeto

```
supply-chain-analytics-gcp/
│
├── supply_chain_analytics/
│   ├── models/
│   │   ├── staging/
│   │   │   ├── _sources.yml
│   │   │   ├── _schema.yml
│   │   │   ├── stg_orders.sql
│   │   │   ├── stg_order_items.sql
│   │   │   ├── stg_products.sql
│   │   │   ├── stg_users.sql
│   │   │   ├── stg_inventory_items.sql
│   │   │   └── stg_distribution_centers.sql
│   │   ├── intermediate/
│   │   │   ├── int_orders_enriched.sql
│   │   │   └── int_order_items_enriched.sql
│   │   └── marts/
│   │       ├── fct_orders.sql
│   │       ├── fct_order_items.sql
│   │       └── kpis_supply_chain.sql
│   ├── dbt_project.yml
│   └── profiles.yml
├── docs/
│   ├── page1_operational.png
│   ├── page2_geographic.png
│   └── page3_product.png
└── README.md
```

---

## KPIs — Supply Chain

| Métrica | Valor | Descrição |
|---|---|---|
| **Total de Pedidos** | 30.960 | Volume total da operação |
| **Receita Total** | R$ 2.673.584,52 | Faturamento consolidado |
| **On-Time Delivery Rate** | 69,63% | % pedidos entregues no prazo |
| **Lead Time Médio** | 3,5 dias | Tempo médio entre pedido e entrega |

---

## Dashboard — 3 Páginas

### Pág 1 · Operational Performance
Visão temporal da operação — evolução de pedidos por mês, distribuição de Lead Time vs Receita por país, volume de pedidos por país e tabela consolidada de performance.

### Pág 2 · Geographic Performance
Mapa geográfico de receita por país, ranking de países por faturamento e tabela com pedidos, receita e lead time médio por região.

### Pág 3 · Product Analysis
Receita por categoria, receita por marca e treemap de distribuição geográfica — identificando os produtos e marcas que concentram o faturamento.

---

## Testes de Qualidade

```
dbt test — PASS=15 ERROR=0

✅ not_null — order_id, user_id, status, created_at
✅ unique — order_id
✅ accepted_values — status in ['Complete', 'Cancelled', 'Returned', ...]
✅ relationships — order_items → orders
✅ not_null — kpis (total_orders, total_revenue, on_time_delivery_rate)
```

---

## Tecnologias Utilizadas

| Categoria | Ferramentas |
|---|---|
| Cloud | Google Cloud Platform (GCP) |
| Data Warehouse | BigQuery |
| Transformação | dbt Core 1.11 |
| Visualização | Looker Studio |
| Linguagem | SQL · Python |
| Versionamento | Git · GitHub |
| Dataset | TheLook Ecommerce (BigQuery Public Data) |

---

## Autor

**Rafael Reghine Munhoz**  
Analytics Engineer | Data Science & Analytics | MBA USP

[![LinkedIn](https://img.shields.io/badge/LinkedIn-rafaelreghine-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/rafaelreghine)
[![GitHub](https://img.shields.io/badge/GitHub-rreghine-black?style=flat-square&logo=github)](https://github.com/rreghine)
