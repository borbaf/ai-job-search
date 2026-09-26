# AI Job Search

Framework de busca e candidatura a vagas, com triagem, ranqueamento e aplicação assistidos por IA. O projeto roda na sua máquina, orquestrado pelo agente Antigravity (agy), e combina coleta de postagens, scoring contra o perfil do candidato e um tracker de candidaturas.

## Objetivo

Reduzir o esforço manual de procurar e aplicar a vagas. O framework coleta postagens, ranqueia as mais aderentes ao perfil do candidato e orienta onde concentrar o esforço de aplicação, com controle de cota para uso em free tier.

## Visão geral do framework

O trabalho é dividido em três comandos complementares:

- /scrape: encontra e deduplica postagens de vagas.
- /rank: pontua as postagens coletadas contra o framework de fit e devolve um shortlist ranqueado (triage, não avaliação final).
- /apply: avalia uma vaga em profundidade, com pesquisa de empresa, e orienta a candidatura.

O /rank é a ponte entre os dois: ele ranqueia o que foi coletado para você decidir onde gastar o esforço de /apply. A avaliação do /apply permanece autoritativa e sempre roda de novo na hora de aplicar.

## Setup GCP (resolvido)

O projeto usa um projeto GCP dedicado, ai-job-search-borbaf, para as chamadas de modelo. O setup foi validado com 6 testes (gcloud autenticado, projeto correto, variáveis de ambiente, billing e API de IA habilitada).

O gargalo anterior de cota (erro 429) foi eliminado. A causa era o projeto antigo coherent-voice-420518 persistido em dois lugares:

- settings.json do CLI (C:\Users\borba\.gemini\antigravity-cli\settings.json), campo gcp.project.
- Keyring do Windows Credential Manager (alvo gemini:antigravity), campo project_id.

Ambos foram corrigidos para ai-job-search-borbaf, com backup do settings em settings.json.bak. O cabeçalho do agy agora mostra GCP Project: ai-job-search-borbaf e as chamadas vão para o endpoint do projeto dedicado, sem erro de cota.

Para execuções pontuais sem mexer no estado persistido, é possível usar agy --project ai-job-search-borbaf.

## Comandos principais

- /rank --limit 5: ranqueia até 5 vagas novas (uso recomendado em free tier para uma única chamada de scoring).
- /rank --all: re-ranqueia todas as vagas não aplicadas (útil após mudanças no perfil).
- /rank --top N: define o tamanho do shortlist (padrão 5).
- /scrape: coleta novas postagens.
- /apply: avalia uma vaga em profundidade.

## Testes

A suíte de testes fica em tests/:

- test-setup.ps1: checklist de ambiente GCP (gcloud, billing, API, variáveis). Útil se o 429 reaparecer ou ao trocar de máquina.
- test_vertex.py: teste de conectividade direta com a API Vertex.
- Demais test_*.py: suíte de testes do código do projeto (pytest).

Para validar o código:

```bash
python -m pytest tests -q
```

Para validar o ambiente GCP:

```powershell
.\tests\test-setup.ps1
```

## Stack

GCP (Vertex AI), Python, SQL e o agente Antigravity (agy) para orquestração dos comandos.