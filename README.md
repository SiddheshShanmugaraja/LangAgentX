---
title: LangAgentsX Demo
sdk: docker
app_port: 7860
---

# LangAgentsX: Exploring Chains of Intelligence

LangAgentsX is a multi-agent chatbot system built using LangChain and LangGraph. It intelligently routes user queries through a network of specialized agents — each designed to fetch or reason from distinct knowledge sources like Wikipedia, arXiv, and Hugging Face models.

### 🔍 Key Features:
- 🌐 **Multi-agent collaboration** using LangGraph.
- 🧠 **Context-aware reasoning** powered by LangChain agents.
- 📚 **Dynamic knowledge retrieval** from Wikipedia and arXiv.
- 🤖 **LLM integration** with Hugging Face models.
- 🔄 **Modular and scalable** design for complex query routing.

## Run Locally
1. Clone the repo
2. Make sure Docker is installed
3. Deploy via Hugging Face or locally using:
```bash
docker build -t langagentsx .
docker run -p 7860:7860 langagentsx
```

> Designed for intelligent exploration across domains — one agent at a time.

---