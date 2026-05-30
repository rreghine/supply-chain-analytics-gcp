from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel
import pandas as pd

PROJECT_ID = "project-25116255-0ff6-4dc2-8df"
LOCATION = "us-central1"

def query_bigquery(sql: str) -> pd.DataFrame:
    client = bigquery.Client(project=PROJECT_ID)
    return client.query(sql).to_dataframe()

def get_kpis() -> pd.DataFrame:
    return query_bigquery("""
        SELECT * FROM `project-25116255-0ff6-4dc2-8df.dbt_supply_chain.kpis_supply_chain`
    """)

def get_orders_by_month() -> pd.DataFrame:
    return query_bigquery("""
        SELECT FORMAT_DATE('%Y-%m', created_at) as mes, COUNT(*) as total_pedidos
        FROM `project-25116255-0ff6-4dc2-8df.dbt_supply_chain.fct_orders`
        WHERE created_at IS NOT NULL
        GROUP BY mes ORDER BY mes
    """)

def get_revenue_by_country() -> pd.DataFrame:
    return query_bigquery("""
        SELECT country as pais, ROUND(SUM(order_revenue),2) as receita,
               COUNT(*) as pedidos, ROUND(AVG(lead_time_days),2) as lead_time_medio
        FROM `project-25116255-0ff6-4dc2-8df.dbt_supply_chain.fct_orders`
        GROUP BY country ORDER BY receita DESC LIMIT 10
    """)

def get_revenue_by_category() -> pd.DataFrame:
    return query_bigquery("""
        SELECT category as categoria, ROUND(SUM(sale_price),2) as receita
        FROM `project-25116255-0ff6-4dc2-8df.dbt_supply_chain.fct_order_items`
        WHERE category IS NOT NULL GROUP BY categoria ORDER BY receita DESC LIMIT 10
    """)

def get_revenue_by_brand() -> pd.DataFrame:
    return query_bigquery("""
        SELECT brand as marca, ROUND(SUM(sale_price),2) as receita
        FROM `project-25116255-0ff6-4dc2-8df.dbt_supply_chain.fct_order_items`
        WHERE brand IS NOT NULL GROUP BY marca ORDER BY receita DESC LIMIT 10
    """)

def get_scatter_data() -> pd.DataFrame:
    return query_bigquery("""
        SELECT country as pais, ROUND(AVG(lead_time_days),2) as lead_time,
               ROUND(SUM(order_revenue),2) as receita, COUNT(*) as pedidos
        FROM `project-25116255-0ff6-4dc2-8df.dbt_supply_chain.fct_orders`
        GROUP BY country ORDER BY receita DESC
    """)

def ask_gemini(question: str, context: str) -> str:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel("gemini-2.5-flash")
    prompt = f"""Voce e um analista especialista em Supply Chain com foco em varejo.
    Contexto dos dados atuais da operacao: {context}
    Responda em portugues de forma clara, objetiva e com insights acionaveis: {question}"""
    return model.generate_content(prompt).text

def ask_claude(question: str, context: str) -> str:
    import anthropic
    client = anthropic.AnthropicVertex(region="us-east5", project_id=PROJECT_ID)
    message = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"""Voce e um analista especialista em Supply Chain.
            Contexto: {context}. Responda em portugues: {question}"""}]
    )
    return message.content[0].text

def ask_agent(question: str, context: str, model: str = "gemini") -> str:
    if model == "claude":
        return ask_claude(question, context)
    return ask_gemini(question, context)
