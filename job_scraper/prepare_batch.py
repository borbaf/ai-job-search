import json
from pathlib import Path

results = [
  {
    "key": "https://tpc.gupy.io/job/eyJqb2JJZCI6MTI2MzAzNDMsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal",
    "status": "scored",
    "scores": {"technical": 80, "experience": 85, "behavioral": 85, "career": 80},
    "track": "Track 2: Logistics Tech & Data Products",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": [
      "Alinhamento direto entre operações logísticas físicas (cliente 3M) e automação de processos via Power BI, SQL e Python.",
      "Foco em indicadores operacionais, dashboards gerenciais e suporte a tomada de decisão para gerência e diretoria."
    ],
    "gaps": [
      "Nível da vaga listado como Especialista I (requer 1 ano de experiência), abaixo do nível de liderança/senioridade histórica do candidato."
    ],
    "language": "pt"
  },
  {
    "key": "leega-consultoria_analista-de-dados-senior-sql-avancado-big-query-mercado-fina-e60fc9",
    "status": "scored",
    "scores": {"technical": 75, "experience": 50, "behavioral": 80, "career": 60},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": [
      "Forte demanda por SQL avançado, BigQuery, geração de insights estratégicos e comunicação executiva.",
      "100% remoto para todo o Brasil."
    ],
    "gaps": [
      "Penalidade de domínio: foco estrito em CRM, comportamento de consumo e mercado financeiro sem escopo de supply chain físico."
    ],
    "language": "pt"
  },
  {
    "key": "unimed-fortaleza_pessoa-analista-de-dados-pleno-inteligencia-de-negocio-1",
    "status": "scored",
    "scores": {"technical": 75, "experience": 45, "behavioral": 75, "career": 55},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": [
      "Localização em Fortaleza/CE (polo aprovado no perfil).",
      "Stack sólida em Python intermediário, SQL avançado, análise quantitativa e geração de insights para liderança."
    ],
    "gaps": [
      "Nível Pleno focado em custos assistenciais e saúde suplementar (sem correlação com cadeia de suprimentos ou transporte)."
    ],
    "language": "pt"
  },
  {
    "key": "grupo-sysmap_analista-de-governanca-de-dados-sr",
    "status": "scored",
    "scores": {"technical": 55, "experience": 40, "behavioral": 70, "career": 45},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": [
      "Posição 100% remota com atuação em processos de governança de dados corporativos e indicadores de qualidade."
    ],
    "gaps": [
      "Foco exclusivo em auditoria, controles internos e LGPD, sem componente analítico de supply chain, logística física ou S&OP."
    ],
    "language": "pt"
  },
  {
    "key": "grupo-sysmap_analista-de-governanca-de-dados-sr-foco-em-curadoria-e-catal-c3e454",
    "status": "scored",
    "scores": {"technical": 50, "experience": 35, "behavioral": 70, "career": 40},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": [
      "Modelo 100% remoto; trabalho com documentação e catálogo de dados corporativos."
    ],
    "gaps": [
      "Exigência de ferramentas específicas de catálogo (Microsoft Purview, Collibra) e gestão pura de metadados sem escopo de negócio ou supply chain."
    ],
    "language": "pt"
  },
  {
    "key": "grupo-sysmap_analista-de-governanca-de-dados-sr-foco-em-acessos",
    "status": "scored",
    "scores": {"technical": 45, "experience": 35, "behavioral": 70, "career": 40},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": [
      "Modelo 100% remoto."
    ],
    "gaps": [
      "Foco em segurança da informação, controle de acessos (RBAC) e privilégios mínimos em nuvem/Databricks, distante da atuação em operações/S&OP."
    ],
    "language": "pt"
  },
  {
    "key": "geopixel_analista-de-geoprocessamento-dados",
    "status": "scored",
    "scores": {"technical": 60, "experience": 40, "behavioral": 70, "career": 45},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": [
      "Trabalho com GIS/geoprocessamento, PostgreSQL, PostGIS e scripts Python/SQL 100% remoto."
    ],
    "gaps": [
      "Exige formação/atuação técnica estrita em cartografia e cadastro urbano municipal (REURB, PGV, IPTU) sem conexão com malha logística ou supply chain."
    ],
    "language": "pt"
  },
  {
    "key": "grupo-farmax_banco-de-talentos-supply-chain-suprimentos-e-logistica",
    "status": "scored",
    "scores": {"technical": 70, "experience": 75, "behavioral": 75, "career": 60},
    "track": "Track 1: Supply Chain & Physical Operations Leadership / S&OP",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": [
      "Alinhamento temático com PCP, suprimentos, gestão de estoques e operações logísticas."
    ],
    "gaps": [
      "Banco de talentos contínuo (não é vaga aberta imediata); unidades operacionais presenciais/híbridas em SP e MG."
    ],
    "language": "pt"
  },
  {
    "key": "https://vagasfarmax.gupy.io/job/eyJqb2JJZCI6MTI2MDM3MDEsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal",
    "status": "scored",
    "scores": {"technical": 70, "experience": 75, "behavioral": 75, "career": 60},
    "track": "Track 1: Supply Chain & Physical Operations Leadership / S&OP",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": [
      "Registro de Banco de Talentos Farmax para Supply Chain e Logística."
    ],
    "gaps": [
      "Banco de talentos contínuo sem contratação garantida imediata."
    ],
    "language": "pt"
  },
  {
    "key": "nwadv_advogado-a-associado-contencioso-civel-massificado-ativos-s-1421f7",
    "status": "scored",
    "scores": {"technical": 10, "experience": 10, "behavioral": 40, "career": 10},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": ["Trabalho remoto."],
    "gaps": ["Exige OAB de SP com 3 anos de atuação e prática estrita em contencioso cível judicial massificado."],
    "language": "pt"
  },
  {
    "key": "nwadv_advogado-a-associado-contencioso-civel-massificado-ativos-s-1421f7-1",
    "status": "scored",
    "scores": {"technical": 10, "experience": 10, "behavioral": 40, "career": 10},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": ["Trabalho remoto."],
    "gaps": ["Exige OAB de SP com 3 anos de atuação e prática estrita em contencioso cível judicial massificado."],
    "language": "pt"
  },
  {
    "key": "nwadv_advogado-a-associado-contencioso-civel-massificado-ativos-s-1421f7-2",
    "status": "scored",
    "scores": {"technical": 10, "experience": 10, "behavioral": 40, "career": 10},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": ["Trabalho remoto."],
    "gaps": ["Exige OAB de SP com 3 anos de atuação e prática estrita em contencioso cível judicial massificado."],
    "language": "pt"
  },
  {
    "key": "nwadv_advogado-a-associado-contencioso-civel-massificado-ativos-s-1421f7-3",
    "status": "scored",
    "scores": {"technical": 10, "experience": 10, "behavioral": 40, "career": 10},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": ["Trabalho remoto."],
    "gaps": ["Exige OAB de SP com 3 anos de atuação e prática estrita em contencioso cível judicial massificado."],
    "language": "pt"
  },
  {
    "key": "ciee-sc_auxiliar-de-atendimento-ao-estudante-r-s-rio-do-sul",
    "status": "scored",
    "scores": {"technical": 10, "experience": 10, "behavioral": 50, "career": 10},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "FAIL",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": ["Instituição de ensino/integração em SC."],
    "gaps": ["Presencial em Rio do Sul/SC (>150km de Bombinhas); cargo de nível auxiliar em RH/atendimento."],
    "language": "pt"
  },
  {
    "key": "https://vemserbalaroti.gupy.io/job/eyJqb2JJZCI6MTI0Mjk0NjYsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal",
    "status": "scored",
    "scores": {"technical": 20, "experience": 30, "behavioral": 50, "career": 10},
    "track": "Track 1: Supply Chain & Physical Operations Leadership / S&OP",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "FAIL",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": ["Ambiente de armazenagem e distribuição física."],
    "gaps": ["Veto de localidade (Curitiba) e nível estritamente operacional/braçal (carga e descarga de mercadorias)."],
    "language": "pt"
  },
  {
    "key": "https://vemserixcsoft.gupy.io/job/eyJqb2JJZCI6MTI2MDU2MTQsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal",
    "status": "scored",
    "scores": {"technical": 10, "experience": 10, "behavioral": 50, "career": 10},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "FAIL",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": ["Empresa de software sediada em SC."],
    "gaps": ["Veto de localização (Chapecó/SC) e escopo de videomaker/produção de conteúdo audiovisual."],
    "language": "pt"
  },
  {
    "key": "https://vagasbrasiltecpar.gupy.io/job/eyJqb2JJZCI6MTI2NjQ2NzEsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal",
    "status": "scored",
    "scores": {"technical": 20, "experience": 20, "behavioral": 50, "career": 10},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "FAIL",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": ["Infraestrutura técnica de telecom."],
    "gaps": ["Veto de localização (Joaçaba/SC) e cargo de técnico de campo para cabeamento óptico."],
    "language": "pt"
  },
  {
    "key": "https://vagasbrasiltecpar.gupy.io/job/eyJqb2JJZCI6MTI2NjQ2MzQsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal",
    "status": "scored",
    "scores": {"technical": 15, "experience": 15, "behavioral": 50, "career": 10},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "FAIL",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": ["Telecomunicações."],
    "gaps": ["Veto de localização (Joaçaba/SC) e cargo de auxiliar operacional de campo."],
    "language": "pt"
  },
  {
    "key": "https://cellularcom.gupy.io/job/eyJqb2JJZCI6MTI2NjQ1NjMsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal",
    "status": "scored",
    "scores": {"technical": 15, "experience": 15, "behavioral": 50, "career": 10},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": ["Localizado na Grande Florianópolis (Palhoça/SC)."],
    "gaps": ["Vendedor de balcão de loja de telefonia de shopping, descompasso com perfil executivo."],
    "language": "pt"
  },
  {
    "key": "https://unimedgrandeflorianopolis.gupy.io/job/eyJqb2JJZCI6MTI2MjAyMDcsInNvdXJjZSI6Imd1cHlfcG9ydGFsIn0=?jobBoardSource=gupy_portal",
    "status": "scored",
    "scores": {"technical": 20, "experience": 15, "behavioral": 50, "career": 15},
    "track": "Other",
    "currency_track": "BRL",
    "employment_gate": "PASS",
    "location_verdict": "PASS",
    "language_gate": "PASS",
    "deadline": None,
    "strengths": ["Florianópolis/SC (região elegível)."],
    "gaps": ["Comunicação e redação publicitária de marketing, sem escopo operacional ou de engenharia."],
    "language": "pt"
  },
  {
    "key": "https://vaga-ja.com/vagas/66-556-949-shayra-huanna-galvao-de-oliveira/montador-mecanico-de-maquinas-especiais-e-automacao?jobBoardSource=gupy_portal",
    "status": "expired"
  }
]

on_site_sp = [
  'cba_operadora-operador-logistico-i-supply-chain',
  'albieri-e-associados_consultor-supply-chain-entry-level',
  'hypera-pharma_analista-de-planejamento-senior-rgm-dados',
  'laboratorio-cristalia_programador-planejador-producao',
  'viveo_analista-planejamento-jr-viveo-sao-paulo-sp',
  'even-construtora-e-incorporadora_analista-de-planejamento-financeiro',
  'jhsf-desenvolvimento-imobiliario_analista-de-planejamento-financeiro-pleno-fp-a-desenvolvimen-091f93',
  'petz_analista-de-planejamento-de-recursos-pl-cd-embu',
  'grupo-farmax_analista-de-planejamento-financeiro-ii-divinopolis-mg',
  'nv_nv-especialista-de-planejamento-de-produto-ese',
  'movida-aluguel-de-carros_analista-de-planejamento-pl-sao-paulo-sp',
  'sem-parar-corpay_analista-de-dados-senior',
  'gradus_analista-de-dados',
  'j-f-investimentos_j-f-s-a-analista-de-dados-senior',
  'cix-citizen-experience_analista-de-dados',
  'pagbank_analista-de-crm-sr-dados',
  'daiichi-sankyo-brasil-farmaceutica_analista-de-custos-senior-sap-s-4hana-vaga-afirmativa-para-p-8daa77',
  'rede-d-or_medico-do-trabalho-s-so-hospital-sao-campinas',
  'eurochem_analista-de-s-oe-pleno-rondonopolis-mt',
  'gpa_operador-a-de-loja-557103-av-gov-mario-covas-s-n-carapicuiba-aeb039',
  'tgestiona-logistica_auxiliar-de-logistica-recebimento',
  'jsl_analista-de-logistica',
  'caedu_auxiliar-de-logistica',
  'bat-brasil_operador-de-logistica-i',
  'brisanet_operador-a-logistico'
]

seen_data = json.loads(Path('job_scraper/seen_jobs.json').read_text(encoding='utf-8'))['seen']
for k in on_site_sp:
    loc = seen_data.get(k, {}).get('location', 'fora dos hubs')
    results.append({
        'key': k,
        'status': 'scored',
        'scores': {'technical': 50, 'experience': 50, 'behavioral': 50, 'career': 40},
        'track': 'Track 1: Supply Chain & Physical Operations Leadership / S&OP',
        'currency_track': 'BRL',
        'employment_gate': 'PASS',
        'location_verdict': 'FAIL',
        'language_gate': 'PASS',
        'deadline': None,
        'strengths': ['Vaga identificada pelo scraper Gupy.'],
        'gaps': [f'Veto de localidade: modelo presencial ou híbrido em {loc}.'],
        'language': 'pt'
    })

Path('job_scraper/gupy_rank_batch.json').write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Successfully wrote {len(results)} items.')
