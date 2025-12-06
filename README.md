# 🤖 Assistant de gouvernance — Microsoft Agent Framework

Application multi-agents pour l'analyse des politiques de télétravail, construite avec **Microsoft Agent Framework** et déployée sur **Azure AI Foundry**.

## 📋 Table des matières

- [Présentation](#-présentation)
- [Architecture](#-architecture)
- [Microsoft Agent Framework vs Semantic Kernel](#-microsoft-agent-framework-vs-semantic-kernel)
- [Installation](#-installation)
- [Configuration Azure AI Foundry](#-configuration-azure-ai-foundry)
- [Création des Agents](#-création-des-agents)
- [Configuration des Connecteurs MCP](#-configuration-des-connecteurs-mcp)
- [Migration depuis Semantic Kernel](#-migration-depuis-semantic-kernel)
- [Exécution](#-exécution)

---

## 🎯 Présentation

Cette application démontre l'utilisation de **Microsoft Agent Framework** pour orchestrer plusieurs agents IA spécialisés dans l'analyse des politiques de gouvernance. Chaque agent possède un rôle distinct et accède à des sources de données spécifiques via des connecteurs MCP (Model Context Protocol).

### Agents déployés

| Agent | Rôle | Connecteur MCP |
|-------|------|----------------|
| 📄 **Agent Document** | Analyse les politiques et guides internes | Azure AI Search (Vector Store) |
| 🌐 **Agent Web** | Recherche les tendances et bonnes pratiques | Bing Search Grounding |
| 🧠 **Agent Synthèse** | Consolide les informations et formule des recommandations | — |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Streamlit UI                               │
│                    (Interface utilisateur)                        │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                  Microsoft Agent Framework                        │
│                     (Orchestration Python)                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│   │   Agent     │    │   Agent     │    │   Agent     │         │
│   │  Document   │    │    Web      │    │  Synthèse   │         │
│   │     📄      │    │     🌐      │    │     🧠      │         │
│   └──────┬──────┘    └──────┬──────┘    └─────────────┘         │
│          │                  │                                    │
│          │                  │                                    │
│   ┌──────▼──────┐    ┌──────▼──────┐                            │
│   │  Connecteur │    │  Connecteur │                            │
│   │     MCP     │    │     MCP     │                            │
│   │ Vector Store│    │ Bing Search │                            │
│   └──────┬──────┘    └──────┬──────┘                            │
│          │                  │                                    │
└──────────┼──────────────────┼────────────────────────────────────┘
           │                  │
           ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│  Azure AI Search │  │   Bing Search   │
│  (Index vectoriel│  │   Grounding     │
│   des documents) │  │                 │
└─────────────────┘  └─────────────────┘
           │                  │
           └────────┬─────────┘
                    ▼
          ┌─────────────────┐
          │ Azure AI Foundry │
          │    (Projet)      │
          │   GPT-4o-mini    │
          └─────────────────┘
```

---

## 🔄 Microsoft Agent Framework vs Semantic Kernel

Microsoft Agent Framework représente une évolution architecturale significative par rapport à Semantic Kernel. Le tableau suivant présente les différences fondamentales entre les deux approches.

### Comparaison architecturale

| Aspect | Semantic Kernel | Microsoft Agent Framework |
|--------|-----------------|---------------------------|
| **Philosophie** | Orchestration de plugins et fonctions | Agents autonomes avec outils intégrés |
| **Gestion d'état** | Kernel centralisé | État géré par agent |
| **Persistance** | Threads via AIProjectClient | Threads natifs via Agent |
| **Connecteurs** | Plugins personnalisés | Protocole MCP standardisé |
| **Déploiement** | Code-first | Agents persistants dans Azure |
| **Configuration** | Programmatique | Déclarative + Azure Portal |

### Avantages de Microsoft Agent Framework

**Agents persistants** : Les agents sont créés et configurés dans Azure AI Foundry, puis référencés par leur ID dans le code. Cette approche permet de modifier la configuration des agents sans redéployer l'application.

**Protocole MCP** : Le Model Context Protocol standardise la communication entre les agents et leurs sources de données. Les connecteurs MCP pour Bing Search et Azure AI Search sont configurables directement dans Azure AI Foundry.

**Simplification du code** : L'absence de Kernel réduit la complexité du code. L'invocation des agents se fait via une API unifiée et les threads de conversation sont gérés automatiquement.

**Intégration native Azure** : L'authentification via Azure CLI et l'intégration avec Azure AI Foundry sont natives, sans configuration additionnelle.

---

## 📥 Installation

### Cloner le repository

```bash
git clone https://github.com/AmineGhazali9/MSAgentFramework.git
cd MSAgentFramework
```

### Créer l'environnement virtuel

```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate

# Linux / macOS
python -m venv .venv
source .venv/bin/activate
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

### Installer et configurer Azure CLI

Azure CLI est requis pour l'authentification auprès d'Azure AI Foundry.

```bash
# Windows (PowerShell)
winget install Microsoft.AzureCLI

# macOS
brew install azure-cli

# Linux (Ubuntu/Debian)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Après l'installation, authentifiez-vous :

```bash
az login
```

---

## ⚙️ Configuration Azure AI Foundry

### Étape 1 : Créer un projet Azure AI Foundry

1. Accédez à [Azure AI Foundry Studio](https://ai.azure.com)
2. Cliquez sur **Create project**
3. Sélectionnez ou créez un **Hub** Azure AI
4. Nommez votre projet (ex: `assistant-agents`)
5. Cliquez sur **Create**

### Étape 2 : Récupérer le Project Endpoint

Le Project Endpoint est l'URL unique de votre projet Azure AI Foundry.

1. Dans Azure AI Foundry Studio, ouvrez votre projet
2. Accédez à **Settings** → **Project properties**
3. Copiez la valeur de **Project endpoint**

Le format attendu est le suivant :
```
https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
```

### Étape 3 : Déployer un modèle LLM

1. Dans votre projet, accédez à **Models + endpoints**
2. Cliquez sur **Deploy model** → **Deploy base model**
3. Sélectionnez **gpt-4o-mini** (ou gpt-4o selon vos besoins)
4. Configurez le déploiement :
   - **Deployment name** : `gpt-4o-mini`
   - **Deployment type** : Standard
5. Cliquez sur **Deploy**
6. Notez le nom du déploiement pour la configuration

### Étape 4 : Configurer le fichier .env

Créez un fichier `.env` à la racine du projet :

```ini
# Azure AI Foundry - Project Configuration
AZURE_AI_PROJECT_ENDPOINT=https://<votre-resource>.services.ai.azure.com/api/projects/<votre-projet>
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o-mini

# Agent IDs (à compléter après création des agents)
#AGENT_DOCUMENT_ID=asst_xxxxxxxxxxxxxxxxxxxxxxxxx
AGENT1_ID="asst_xxxxxxxxxxxxxxxxxxxxxxxxx"
#AGENT_WEB_ID=asst_xxxxxxxxxxxxxxxxxxxxxxxxx
AGENT2_ID="asst_xxxxxxxxxxxxxxxxxxxxxxxxx"
#AGENT_SUMMARY_ID=asst_xxxxxxxxxxxxxxxxxxxxxxxxx
AGENT3_ID="asst_xxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

## 🤖 Création des Agents

Les agents sont créés dans Azure AI Foundry et persistent indépendamment du code. Chaque agent possède un ID unique utilisé pour l'invocation.

### Agent 1 : Agent Document (avec Vector Store)

Cet agent analyse les documents internes via Azure AI Search.

1. Dans Azure AI Foundry, accédez à **Agents**
2. Cliquez sur **New agent**
3. Configurez l'agent :

| Paramètre | Valeur |
|-----------|--------|
| **Name** | Agent Document |
| **Model** | gpt-5 |
| **Instructions** | Voir ci-dessous |

**Instructions de l'agent :**
```
Tu es un expert en analyse documentaire. Tu analyses les politiques internes, 
les guides et les procédures de l'entreprise concernant le télétravail.

Tes responsabilités :
- Extraire les informations pertinentes des documents internes
- Identifier les règles et conditions de télétravail
- Citer les sources documentaires précisément
- Signaler les ambiguïtés ou zones grises dans les politiques

Réponds toujours en français de manière structurée et professionnelle.
```

4. Ajoutez le connecteur **Azure AI Search** (voir section MCP)
5. Cliquez sur **Create**
6. Copiez l'**Agent ID** (format: `asst_xxxxxxxxx`)

### Agent 2 : Agent Web (avec Bing Search)

Cet agent recherche les tendances et bonnes pratiques via Bing.

1. Créez un nouvel agent avec la configuration suivante :

| Paramètre | Valeur |
|-----------|--------|
| **Name** | Agent Web |
| **Model** | gpt-5|
| **Instructions** | Voir ci-dessous |

**Instructions de l'agent :**
```
Tu es un expert en veille et tendances du marché du travail. Tu recherches 
les meilleures pratiques de télétravail et les évolutions réglementaires.

Tes responsabilités :
- Rechercher les tendances actuelles en matière de télétravail
- Identifier les bonnes pratiques des entreprises leaders
- Suivre les évolutions légales et réglementaires
- Comparer les approches sectorielles

Cite toujours tes sources avec les URLs. Réponds en français.
```

2. Ajoutez le connecteur **Bing Search Grounding** (voir section MCP)
3. Créez l'agent et copiez l'**Agent ID**

### Agent 3 : Agent Synthèse

Cet agent consolide les informations et génère des recommandations.

| Paramètre | Valeur |
|-----------|--------|
| **Name** | Agent Synthèse |
| **Model** | gpt-4o-mini |
| **Instructions** | Voir ci-dessous |

**Instructions de l'agent :**
```
Tu es un conseiller stratégique senior. Tu synthétises les analyses documentaires 
et les recherches web pour formuler des recommandations actionables.

Tes responsabilités :
- Consolider les informations des différentes sources
- Identifier les écarts entre pratiques internes et tendances du marché
- Formuler des recommandations concrètes et priorisées
- Proposer un plan d'action réaliste

Structure tes réponses avec :
1. Synthèse des constats
2. Analyse des écarts
3. Recommandations prioritaires
4. Prochaines étapes suggérées
```

---

## 🔌 Configuration des Connecteurs MCP

Le Model Context Protocol (MCP) permet aux agents d'accéder à des sources de données externes. Azure AI Foundry supporte nativement plusieurs connecteurs MCP.

### Connecteur Bing Search Grounding

Ce connecteur permet à l'agent d'effectuer des recherches web en temps réel.

#### Prérequis

1. Créez une ressource **Bing Search** dans le portail Azure :
   - Accédez au [Portail Azure](https://portal.azure.com)
   - Recherchez **Bing Search**
   - Créez une ressource avec le tier **S1** ou supérieur
   - Copiez la **clé API**

2. Associez Bing Search à votre projet Azure AI Foundry :
   - Dans Azure AI Foundry, accédez à **Connected resources**
   - Cliquez sur **New connection**
   - Sélectionnez **Bing Search**
   - Entrez votre clé API
   - Nommez la connexion (ex: `bing-search-connection`)

#### Configuration dans l'agent

1. Ouvrez l'agent concerné (Agent Web)
2. Dans la section **Tools**, cliquez sur **Add tool**
3. Sélectionnez **Bing Search Grounding**
4. Configurez les paramètres :

| Paramètre | Valeur recommandée |
|-----------|-------------------|
| **Connection** | bing-search-connection |
| **Market** | fr-CA (ou fr-FR) |
| **Safe Search** | Moderate |

5. Enregistrez la configuration

### Connecteur Azure AI Search (Vector Store)

Ce connecteur permet à l'agent d'interroger un index vectoriel contenant vos documents.

#### Étape 1 : Créer la ressource Azure AI Search

1. Dans le portail Azure, créez une ressource **Azure AI Search**
2. Sélectionnez le tier **Basic** minimum (requis pour la recherche vectorielle)
3. Notez l'**endpoint** et la **clé admin**

#### Étape 2 : Créer et peupler l'index vectoriel

1. Dans Azure AI Foundry, accédez à **Data + indexes**
2. Cliquez sur **New index**
3. Configurez l'index :

| Paramètre | Valeur |
|-----------|--------|
| **Index name** | politiques-index |
| **Data source** | Azure Blob Storage |
| **Embedding model** | text-embedding-ada-002 |

4. Uploadez vos documents (PDF, DOCX, TXT) contenant :
   - Politique de télétravail
   - Guide de l'employé
   - Conventions collectives
   - Procédures 

5. Lancez l'indexation et attendez la complétion

#### Étape 3 : Connecter l'index à l'agent

1. Ouvrez l'agent Document
2. Dans **Tools**, ajoutez **Azure AI Search**
3. Configurez :

| Paramètre | Valeur |
|-----------|--------|
| **Connection** | Votre connexion AI Search |
| **Index** | politiques-index |
| **Search type** | Hybrid (vector + keyword) |
| **Top K** | 5 |

4. Enregistrez

---

## 🔄 Migration depuis Semantic Kernel

Cette section détaille les modifications apportées pour migrer l'application de Semantic Kernel vers Microsoft Agent Framework.

### Modifications des imports

**Avant (Semantic Kernel) :**
```python
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings
from semantic_kernel import Kernel
from azure.identity.aio import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
```

**Après (Agent Framework) :**
```python
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
```

### Modifications de l'authentification

**Avant :**
```python
credential = DefaultAzureCredential()
client = AIProjectClient(
    credential=credential,
    subscription_id=SUBSCRIPTION_ID,
    resource_group_name=RESOURCE_GROUP,
    project_name=PROJECT_NAME
)
```

**Après :**
```python
credential = AzureCliCredential()
# Le client est créé via AzureAIAgentClient avec le project_endpoint
```

### Modifications de la création d'agent

**Avant (Semantic Kernel) :**
```python
kernel = Kernel()
agent_definition = await client.agents.create_agent(
    model=MODEL_NAME,
    name="Agent Document",
    instructions="..."
)
agent = AzureAIAgent(
    client=client,
    definition=agent_definition,
    kernel=kernel
)
thread = await client.agents.create_thread()
```

**Après (Agent Framework) :**
```python
async with AzureAIAgentClient(
    async_credential=credential,
    project_endpoint=PROJECT_ENDPOINT,
    model_deployment_name=MODEL_DEPLOYMENT,
    agent_id=AGENT_ID  # Agent pré-créé dans Azure
) as client:
    async with client.create_agent() as agent:
        # L'agent est prêt à être utilisé
```

### Modifications de l'invocation

**Avant :**
```python
response = await agent.get_response(
    messages=query,
    thread_id=thread.id
)
result = response.message.content
```

**Après :**
```python
response = await agent.run(query)
result = response.text
```

### Gestion des threads

**Avant :**
```python
thread = await client.agents.create_thread()
# Utilisation manuelle du thread_id
```

**Après :**
```python
thread = agent.get_new_thread()
# Ou gestion automatique par l'agent
```

### Résumé des changements de packages

| Package Semantic Kernel | Package Agent Framework |
|------------------------|-------------------------|
| `semantic-kernel` | `agent-framework` |
| `azure-ai-projects` | (inclus dans agent-framework) |
| `azure-identity` | `azure-identity` (identique) |

---

## ▶️ Exécution

### Vérifier la configuration

Avant de lancer l'application, vérifiez que :

1. **Azure CLI** est connecté :
```bash
az account show
```

2. **Les variables d'environnement** sont configurées :
```bash
# Vérifier le fichier .env
cat .env
```

3. **Les Agent IDs** sont renseignés dans le code ou le fichier `.env`

### Lancer l'application

```bash
streamlit run Assistant.py
```

L'application sera accessible à l'adresse `http://localhost:8501`.

### Utilisation

1. Entrez une question relative aux documents internes (ex: "Quelles sont les conditions de télétravail ?")
2. Entrez une question pour la recherche web (ex: "Tendances télétravail 2024")
3. Cliquez sur **Analyser**
4. Consultez les résultats des trois agents
5. Exportez le rapport en Markdown si nécessaire

---

## 📁 Structure du projet

```
MSAgentFramework/
├── Assistant.py          # Application principale
├── requirements.txt        # Dépendances Python
├── .env                    # Configuration (non versionné)
├── .env.example            # Template de configuration
├── README.md               # Documentation
└── docs/
    ├── migration-guide.md  # Guide de migration détaillé
    └── architecture.md     # Documentation architecture
```

---

## 🔧 Dépannage

### Erreur "Azure credential is required"

Cette erreur indique un problème d'authentification.

**Solution :**
```bash
az login
az account set --subscription "<votre-subscription-id>"
```

### Erreur "404 Resource not found"

Le Project Endpoint est incorrect.

**Solution :**
1. Vérifiez le format de l'endpoint dans Azure AI Foundry → Settings → Project properties
2. Assurez-vous que le format est : `https://<resource>.services.ai.azure.com/api/projects/<project>`

### Erreur "Agent not found"

L'Agent ID est invalide ou l'agent a été supprimé.

**Solution :**
1. Vérifiez les Agent IDs dans Azure AI Foundry → Agents
2. Mettez à jour les IDs dans le fichier `.env` ou le code

---

## 📚 Ressources

- [Documentation Microsoft Agent Framework](https://learn.microsoft.com/en-us/azure/ai-services/agents/)
- [Azure AI Foundry Studio](https://ai.azure.com)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Guide de migration Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/migration/)

---

## 📄 Licence

MIT License

---

## 👤 Auteur

**Amine Ghazali**  
GitHub: [@AmineGhazali9](https://github.com/AmineGhazali9)
