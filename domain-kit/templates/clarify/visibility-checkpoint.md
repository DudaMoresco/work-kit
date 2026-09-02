> Roteiro **interno** — checkpoint de visibilidade após criar rascunhos ou promover. Usado por `/domain.init`, `/domain.scan`, `/domain.discover`, etc.

O usuário precisa **ver** dashboard, rascunhos e changelog **durante** a sessão — não só no final.

## Quando exibir

- Após criar índices do produto (início do init)
- **Após cada lote de rascunhos** gravado em `.draft/`
- Após cada promote material
- No encerramento da sessão (handoff)

## Comando (obrigatório)

Rodar após scaffold, rascunhos ou promote:

```bash
.domain/scripts/sync_product_workspace.py --hub {hub} --product {p}
```

Para registrar rascunho no manifest (recomendado):

```bash
.domain/scripts/sync_product_workspace.py --hub {hub} --product {p} \
  --register ".draft/sources.yml:sources.yml:domain.init" \
  --register ".draft/01-product/00-scan/scan-manifest.json:01-product/00-scan/scan-manifest.json:domain.init"
```

(um `--register` por par draft → target; repetir após cada artefato novo)

## Bloco no chat (copiar saída do script ou montar)

```markdown
## Visibilidade do workspace

- **Dashboard:** `products/{p}/dashboard.html` → aba **Rascunhos**
- **Changelog:** `products/{p}/CHANGELOG.md` (após promotes)
- **Rascunhos:** `products/{p}/.draft/` — listar arquivos criados neste turno

Abra o dashboard no browser ou no explorador de arquivos do IDE.
```

## Regras

1. **Não** esperar o fim do init para o primeiro dashboard — regenerar assim que `.draft/` ou índices existirem
2. Gravar rascunhos **em disco** (não só no chat) antes de pedir OK
3. Atualizar `.draft/manifest.json` via `sync_product_workspace.py --register` ou manualmente
4. CHANGELOG só após promote — mas **linkar** o path mesmo vazio para o usuário saber onde ficará o log
