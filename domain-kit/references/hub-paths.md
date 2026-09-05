# Mapa de paths do hub (domain-kit)

**Fonte canônica** de onde gravar artefatos. Em comando `domain-*`, o **wrapper vence** se houver conflito com a skill.

Idioma dos artefatos: **pt-BR**. Plan mode: rascunhos em `.draft/` até OK do usuário.

---

## Árvore canônica

```text
products/{produto}/
├── product-README.md          # cartão PM
├── sources.yml
├── flows-registry.yml
├── domain-status.json
├── CHANGELOG.md
├── .draft/                    # espelho dos paths abaixo até promote
├── 01-product/
│   ├── 00-scan/               # Evidências
│   ├── 01-vision/             # Estratégico (design-estrategico)
│   ├── 02-domain/             # UL, BCs, desafio, abertos, evolucoes, cenarios/
│   ├── 03-discovery/
│   │   ├── 00-as-is/          # fluxogramas / regras as-is (ÚNICO lugar)
│   │   ├── 01-event-storming/
│   │   └── 02-domain-storytelling/
│   └── 04-operacional/
│       ├── fluxos/{NN}-{slug}.md
│       └── requisitos.md      # NFRs de produto
└── 05-decisoes/produto.md     # registry D-n
```

`arch/` é **fora do escopo** do domain-kit: pasta opcional no produto, nunca requerida, nunca gated. Não criar nem validar `arch/` como entrega deste kit.

---

## Por fase

| Fase | Paths principais |
| --- | --- |
| Evidências | `01-product/00-scan/` (`scan-manifest.json`, `sintese-evidencias.md`), `sources.yml` |
| Estratégico | `01-product/01-vision/01-design-estrategico.md`, `02-domain/{desafio,linguagem-ubiqua,bounded-contexts}.md` |
| Descoberta | `03-discovery/01-event-storming/`, `03-discovery/02-domain-storytelling/`, opcional `03-discovery/00-as-is/` |
| Operacional | `04-operacional/fluxos/`, `04-operacional/requisitos.md`, `05-decisoes/produto.md`, `flows-registry.yml` |

---

## Glossário vs dicionário

| Artefato | Onde | Papel |
| --- | --- | --- |
| Glossário de sessão (story) | junto da story em `03-discovery/02-domain-storytelling/` | termos da narrativa da sessão |
| Linguagem ubíqua canônica | `02-domain/linguagem-ubiqua.md` | dicionário estável do produto |

---

## Skills bundled neste kit

Know-how em `.domain/skills/` após install. Design tático e integração técnica **não** fazem parte do domain-kit.
