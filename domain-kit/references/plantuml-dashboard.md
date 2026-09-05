# PlantUML no dashboard domain-kit

O preview do dashboard (`products/{produto}/dashboard.html`, aba **Preview**) renderiza blocos
`` `plantuml `` / `` `uml `` em diagramas SVG via **servidor PlantUML local**.

---

## Porta padrão: **8765**

Escolhida para evitar conflito com portas comuns de dev:

| Porta | Uso típico |
| --- | --- |
| 8080 | Spring Boot, APIs Java |
| 3000 | Node / React |
| 5173 | Vite |
| **8765** | **PlantUML domain-kit** |

Configurável em `.domain/config.yml` (`plantuml.server`) ou variável `PLANTUML_SERVER`.

---

## Subir o servidor

```bash
# No hub (após domain.install):
.domain/scripts/start_plantuml_server.sh

# Direto do pacote domain-kit:
bash domain-kit/scripts/start_plantuml_server.sh
```

Requisito: **Docker** com imagem `plantuml/plantuml-server:jetty`.

Override de porta:

```bash
PLANTUML_PORT=9000 .domain/scripts/start_plantuml_server.sh
```

Parar:

```bash
docker stop domain-kit-plantuml
```

---

## Regenerar o dashboard

Com o servidor ativo, a geração **embute SVG** nos artefatos (funciona offline depois):

```bash
.domain/scripts/regenerate_dashboard.sh products/meu-produto
```

Sem servidor na geração, o HTML ainda tenta renderizar via JavaScript ao abrir a aba Preview
(desde que o servidor esteja rodando no browser).

---

## Configuração do hub

`.domain/config.yml`:

```yaml
plantuml:
  server: http://127.0.0.1:8765
  port: 8765
```

Variável de ambiente (tem precedência):

```bash
export PLANTUML_SERVER=http://127.0.0.1:8765
```

---

## Validação de sintaxe (agente)

Para checagem durante authoring, use o MCP **`user-plantuml`** (`check_syntax`, `render_diagram`).
Não use o servidor público `plantuml.com` — alinhe com as skills DDD do pacote pessoais.

---

## Troubleshooting

| Sintoma | Ação |
| --- | --- |
| Bloco de código em vez de diagrama | Suba `start_plantuml_server.sh` e regenere o dashboard |
| `414 URI Too Long` | Servidor local com POST (script Docker) — não use GET/plantuml.com |
| CORS / fetch falhou | Abra o dashboard via servidor HTTP (`python3 -m http.server`) se `file://` bloquear |
| Porta em uso | `PLANTUML_PORT=8877 start_plantuml_server.sh` + atualize `config.yml` |

Teste rápido:

```bash
curl -sf -X POST -H 'Content-Type: text/plain' \
  --data $'@startuml\nAlice -> Bob: ok\n@enduml' \
  http://127.0.0.1:8765/svg | head -3
```
