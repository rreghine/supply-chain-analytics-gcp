🇺🇸 **English** | [🇧🇷 Português](README.pt-BR.md)

# Supply Chain Analytics

![dbt](https://img.shields.io/badge/dbt-Core-orange?style=flat-square)
![BigQuery](https://img.shields.io/badge/BigQuery-GCP-blue?style=flat-square)
![Looker](https://img.shields.io/badge/Looker_Studio-Dashboard-brightgreen?style=flat-square)
![Vertex AI](https://img.shields.io/badge/Vertex_AI-Gemini_2.5_Flash-4285F4?style=flat-square)
![Cloud Run](https://img.shields.io/badge/Cloud_Run-Deployed-success?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

End-to-end Supply Chain analytics pipeline with Medallion architecture (Staging → Intermediate → Marts) on BigQuery, dimensional modeling with dbt Core — including data quality tests, full lineage, and documentation — a 3-page executive dashboard in Looker Studio, and a conversational AI agent deployed on Cloud Run via Vertex AI (Gemini 2.5 Flash + Claude Opus 4.8). Built on Google Cloud's public TheLook Ecommerce dataset.

---

## AI Agent — Cloud Run

Conversational agent deployed on Google Cloud Run with support for multiple AI models:

![Supply Chain AI Agent](docs/streamlit_agent.png)

### Models available in the agent

| Model | Provider | Use case |
|---|---|---|
| **Gemini 2.5 Flash** | Google Vertex AI | Fast KPI analysis |
| **Claude Opus 4.8** | Anthropic via Vertex AI | In-depth analysis |

---

## Dashboard — Looker Studio

### Operational Performance
![Operational Performance](docs/page1_operational.png)

### Geographic Performance
![Geographic Performance](docs/page2_geographic.png)

### Product Analysis
![Product Analysis](docs/page3_product.png)

---

## Architecture

```
TheLook Ecommerce
        ↓
Staging Layer — source cleaning and standardization
  stg_orders · stg_order_items · stg_products
  stg_users · stg_inventory · stg_distribution_centers
        ↓
Intermediate Layer — joins and business rules
  int_orders_enriched · int_order_logistics
        ↓
Marts Layer — final analytical models
  fct_orders · fct_order_items · kpis_supply_chain
        ↓
┌─────────────────────┬──────────────────────────┐
│  Looker Studio      │  AI Agent (Cloud Run)    │
│  3 pages            │  Streamlit + Vertex AI   │
│  Executive dashboard│  Gemini 2.5 Flash        │
│                     │  Claude Opus 4.8         │
└─────────────────────┴──────────────────────────┘
```

### Lineage Graph
![Lineage Graph](docs/lineage_graph.png)

---

## Project Structure

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

## Technologies Used

| Category | Tools |
|---|---|
| Cloud | Google Cloud Platform (GCP) |
| Data Warehouse | BigQuery |
| Transformation | dbt Core 1.11 |
| Visualization | Looker Studio |
| AI Agent | Vertex AI · Gemini 2.5 Flash · Claude Opus 4.8 |
| App Framework | Streamlit · Plotly |
| Deployment | Cloud Run (serverless) |
| Language | SQL · Python |
| Versioning | Git · GitHub |
| Dataset | TheLook Ecommerce (BigQuery Public Data) |

---

## Author

**Rafael Reghine Munhoz**
Analytics Engineer | Data Science & Analytics | MBA at USP (University of São Paulo)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-rafaelreghine-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/rafaelreghine)
[![GitHub](https://img.shields.io/badge/GitHub-rreghine-black?style=flat-square&logo=github)](https://github.com/rreghine)
