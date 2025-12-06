"""
Assistant – Cadre de gouvernance
Migré de Semantic Kernel vers Microsoft Agent Framework
"""
import asyncio
import os
import streamlit as st
from dotenv import load_dotenv

from azure.identity.aio import AzureCliCredential
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient

# Load configuration from .env file
load_dotenv()

# ----- Agent IDs Configuration -----
# Document Search Agent (Agent 1)
AGENT1_ID = os.environ.get("AGENT1_ID")
# Web Search Agent (Agent 2)
AGENT2_ID = os.environ.get("AGENT2_ID")
# Summary Agent (Agent 3)
AGENT3_ID = os.environ.get("AGENT3_ID")

# ----- Azure Project Configuration -----
PROJECT_ENDPOINT = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
MODEL_DEPLOYMENT = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")

# Agent icons
agent_icons = {
    "document": "📄",
    "web": "🌐",
    "summary": "🧠"
}

st.set_page_config(page_title="Assistant ", layout="wide")
st.title("🤖 Assistant — cadre de gouvernance ")

# Sidebar
with st.sidebar:
    st.header("⚙️ Paramètres")
    st.markdown(f"{agent_icons['document']} **Agent Document ID**: `{AGENT1_ID}`")
    st.markdown(f"{agent_icons['web']} **Agent Web ID**: `{AGENT2_ID}`")
    st.markdown(f"{agent_icons['summary']} **Agent Résumé ID**: `{AGENT3_ID}`")
    
    st.divider()
    st.info("🔐 Authentification: Azure CLI\n\nExécutez `az login` avant de lancer l'application.")
    
    st.divider()
    st.caption(f"**Endpoint**: `{PROJECT_ENDPOINT}`")
    st.caption(f"**Model**: `{MODEL_DEPLOYMENT}`")

    # Inputs utilisateur 
    web_input = st.text_area("🌐 Question Agent Web", value="", placeholder="Demandez quelque chose")
    doc_input = st.text_area("📄 Question Agent Document", value="", placeholder="Demandez quelque chose")
    
    # Bouton pour lancer les agents
    run_button = st.button("🚀 Lancer les agents")


async def run_single_agent(credential, agent_id: str, query: str) -> str:
    """
    Run a single agent using Microsoft Agent Framework.
    
    L'agent est récupéré par son ID existant en passant agent_id au constructeur
    de AzureAIAgentClient, puis en créant un ChatAgent wrapper.
    """
    # Créer le client avec l'agent_id existant
    async with AzureAIAgentClient(
        async_credential=credential,
        project_endpoint=PROJECT_ENDPOINT,
        model_deployment_name=MODEL_DEPLOYMENT,
        agent_id=agent_id  # Récupère l'agent existant par son ID
    ) as client:
        # Créer un ChatAgent qui utilise ce client
        async with client.create_agent() as agent:
            response = await agent.run(query)
            return response.text


async def run_agents(doc_query: str, web_query: str) -> None:
    """Run all three agents with the given queries using Azure CLI authentication."""
    
    async with AzureCliCredential() as credential:
        try:
            # ----- Agent 1: Document Search Agent -----
            with st.spinner(f"{agent_icons['document']} Agent Document en cours..."):
                response_doc_text = await run_single_agent(credential, AGENT1_ID, doc_query)
            
            with st.expander(f"{agent_icons['document']} Réponse de l'agent Document", expanded=True):
                st.chat_message("assistant").markdown(response_doc_text)

            # ----- Agent 2: Web Search Agent -----
            with st.spinner(f"{agent_icons['web']} Agent Web en cours..."):
                response_web_text = await run_single_agent(credential, AGENT2_ID, web_query)
            
            with st.expander(f"{agent_icons['web']} Résultat de la recherche Web", expanded=True):
                st.chat_message("assistant").markdown(response_web_text)

            # ----- Agent 3: Summary Agent -----
            combined_input = f"Extrait 1 : {response_doc_text}\n\nExtrait 2 : {response_web_text}"
            
            with st.spinner(f"{agent_icons['summary']} Agent Résumé en cours..."):
                response_summary_text = await run_single_agent(credential, AGENT3_ID, combined_input)
            
            with st.expander(f"{agent_icons['summary']} Synthèse et recommandations", expanded=True):
                st.chat_message("assistant").markdown(response_summary_text)

            st.success("✅ Tous les agents ont terminé leur exécution.")

        except Exception as e:
            error_msg = str(e)
            st.error(f"❌ Erreur: {error_msg}")
            
            # Messages d'aide spécifiques selon l'erreur
            if "404" in error_msg:
                st.warning("""
                💡 **Erreur 404 - Resource not found**
                
                **Causes possibles:**
                1. L'endpoint du projet n'est pas au bon format
                2. Les agents n'existent pas dans ce projet
                
                **Format d'endpoint attendu:**
                `https://<resource>.services.ai.azure.com/api/projects/<project-name>`
                
                **Comment trouver le bon endpoint:**
                1. Allez sur https://ai.azure.com
                2. Ouvrez votre projet
                3. Settings → Project properties → "Project endpoint"
                """)
            elif "credential" in error_msg.lower() or "authentication" in error_msg.lower():
                st.warning("""
                💡 **Erreur d'authentification**
                
                Exécutez `az login` dans PowerShell avant de relancer l'application.
                """)
            
            import traceback
            with st.expander("🔍 Détails de l'erreur"):
                st.code(traceback.format_exc())


# Main execution
if run_button:
    if not doc_input and not web_input:
        st.warning("⚠️ Veuillez entrer au moins une question.")
    else:
        # Définir des valeurs par défaut si une question est vide
        doc_query = doc_input if doc_input else "Résume la politique de télétravail"
        web_query = web_input if web_input else "Quelles sont les meilleures pratiques de télétravail?"
        
        asyncio.run(run_agents(doc_query, web_query))
