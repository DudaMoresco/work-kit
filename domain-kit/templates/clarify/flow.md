> Roteiro **interno** — inline em `/domain.flow`. Não invocar `/domain.clarify`.

# Fluxo operacional {NN} — perguntas (camada negócio)

1. **Ator** principal deste cenário?
2. **Pré-condições** de negócio (estado do domínio antes)?
3. **Passos** em linguagem ubíqua (sem nomes de serviço/fila)?
4. **Resultado** esperado e **métrica de sucesso**?
5. **Exceções** de negócio (caminhos alternativos)?
6. Conflito com algum **D-n** existente?

Template: [fluxo-operacional.md](../../templates/fluxo-operacional.md)

**Path canônico (negócio):** `01-product/04-operacional/fluxos/{NN}-{slug}.md`

**Detalhe técnico (fora do escopo):** opcional — próxima etapa técnica (fora deste kit).

Confirmar deps satisfeitas no `flows-registry.yml` antes de gravar.
