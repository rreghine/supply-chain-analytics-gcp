# Supply Chain Analytics

![dbt](https://img.shields.io/badge/dbt-Core-orange?style=flat-square)
![BigQuery](https://img.shields.io/badge/BigQuery-GCP-blue?style=flat-square)
![Looker](https://img.shields.io/badge/Looker_Studio-Dashboard-brightgreen?style=flat-square)
![Vertex AI](https://img.shields.io/badge/Vertex_AI-Gemini_2.5_Flash-4285F4?style=flat-square)
![Cloud Run](https://img.shields.io/badge/Cloud_Run-Deployed-success?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

Pipeline analítico end-to-end de Supply Chain com arquitetura Medallion (Staging → Intermediate → Marts) no BigQuery, modelagem dimensional com dbt Core — incluindo testes de qualidade, lineage completo e documentação — dashboard executivo em 3 camadas no Looker Studio e agente conversacional com IA deployado no Cloud Run via Vertex AI (Gemini 2.5 Flash + Claude Opus 4.8). Construído sobre o dataset público TheLook Ecommerce do Google Cloud.

---

## AI Agent — Cloud Run

Agente conversacional deployado no Google Cloud Run com suporte a múltiplos modelos de IA:

![Supply Chain AI Agent](docs/streamlit_agent.png)

### Modelos disponíveis no agente

| Modelo | Provider | Uso |
|---|---|---|
| **Gemini 2.5 Flash** | Google Vertex AI | Análise rápida de KPIs |
| **Claude Opus 4.8** | Anthropic via Vertex AI | Análise aprofundada |

---

## Dashboard — Looker Studio

### Operational Performance
![Operational Performance](docs/page1_operational.png)

### Geographic Performance
![Geographic Performance](docs/page2_geographic.png)

### Product Analysis
![Product Analysis](docs/page3_product.png)

---

## Arquitetura

```
TheLook Ecommerce
        ↓
Staging Layer — limpeza e padronização das fontes
  stg_orders · stg_order_items · stg_products
  stg_users · stg_inventory · stg_distribution_centers
        ↓
Intermediate Layer — joins e regras de negócio
  int_orders_enriched · int_order_logistics
        ↓
Marts Layer — modelos analíticos finais
  fct_orders · fct_order_items · kpis_supply_chain
        ↓
┌─────────────────────┬──────────────────────────┐
│  Looker Studio      │  AI Agent (Cloud Run)    │
│  3 páginas          │  Streamlit + Vertex AI   │
│  Dashboard executivo│  Gemini 2.5 Flash        │
│                     │  Claude Opus 4.8         │
└─────────────────────┴──────────────────────────┘
```

### Lineage Graph
![Lineage Graph](docs/lineage_graph.png)

---

## Estrutura do Projeto

```
supply-chain-analytics-gcp/
│
├── supply_chain_analytics/          ← dbt project
│   ├── models/
│   │   ├── staging/                 ← Bronze/Silver
│   │   │   ├── _sources.yml
│   │   │   ├── _schema.yml
│   │   │   ├── stg_orders.sql
│   │   │   ├── stg_order_items.sql
│   │   │   ├── stg_products.sql
│   │   │   ├── stg_users.sql
│   │   │   ├── stg_inventory_items.sql
│   │   │   └── stg_distribution_centers.sql
│   │   ├── intermediate/            ← Business logic
│   │   │   ├── int_orders_enriched.sql
│   │   │   └── int_order_logistics.sql
│   │   └── marts/                   ← Gold
│   │       ├── fct_orders.sql
│   │       ├── fct_order_items.sql
│   │       └── kpis_supply_chain.sql
│   └── dbt_project.yml
│
├── agent/                           ← AI Agent
│   ├── streamlit_app.py             ← Interface
│   ├── gemini_agent.py              ← BigQuery + Vertex AI
│   ├── Dockerfile                   ← Cloud Run
│   └── requirements.txt
│
├── docs/                            ← Screenshots
│   ├── page1_operational.png
│   ├── page2_geographic.png
│   ├── page3_product.png
│   ├── streamlit_agent.png
│   └── lineage_graph.png
│
└── README.md
```
---

## Tecnologias Utilizadas

| Categoria | Ferramentas |
|---|---|
| Cloud | Google Cloud Platform (GCP) |
| Data Warehouse | BigQuery |
| Transformação | dbt Core 1.11 |
| Visualização | Looker Studio |
| AI Agent | Vertex AI · Gemini 2.5 Flash · Claude Opus 4.8 |
| App Framework | Streamlit · Plotly |
| Deploy | Cloud Run (serverless) |
| Linguagem | SQL · Python |
| Versionamento | Git · GitHub |
| Dataset | TheLook Ecommerce (BigQuery Public Data) |

---

## Autor

**Rafael Reghine Munhoz**
Analytics Engineer | Data Science & Analytics | MBA USP

[![LinkedIn](https://img.shields.io/badge/LinkedIn-rafaelreghine-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/rafaelreghine)
[![GitHub](https://img.shields.io/badge/GitHub-rreghine-black?style=flat-square&logo=github)](https://github.com/rreghine)
