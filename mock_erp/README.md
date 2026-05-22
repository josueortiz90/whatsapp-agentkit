# Mock ERP — servidor de prueba para integración API → AgentKit

Servidor FastAPI que **simula un ERP REST** del negocio. Sirve para desarrollar y probar la integración con el agente sin depender de un ERP real.

## Arrancar

```powershell
# Desde D:\Proyectos\whatsapp-agentkit\ (o el dir del agente)
$env:MOCK_ERP_TOKEN = "mock-erp-secret"   # opcional, ese es el default
python -m uvicorn mock_erp.main:app --reload --port 9001
```

Health check: `http://localhost:9001/`

## Endpoints

Todos requieren `Authorization: Bearer mock-erp-secret` (excepto el `/`).

| Método | Path | Descripción |
|---|---|---|
| `GET` | `/productos?q=&limit=10` | Búsqueda. Devuelve lista con stock simulado (varía ±20% del CSV) |
| `GET` | `/productos/{codigo}/stock` | Stock actual de un SKU |
| `GET` | `/precios/{codigo}` | Precio actual con variación ±5% del CSV |
| `GET` | `/pedidos?telefono=X` | Historial mock. Devuelve 2 pedidos si el último dígito es par, vacío si impar |

## Datos

Los productos se cargan desde `knowledge/productos.csv` (al startup). El stock y precio se simulan ligeramente diferentes al CSV para que el agente realmente _aporte valor_ consultando el ERP en vez de leer del prompt.

## Cuándo reemplazar por el ERP real

En `config/api_negocio.yaml`:

```yaml
api:
  base_url: "http://localhost:9001"          # mock
  # base_url: "https://erp.tu-empresa.com"   # real
  auth:
    type: bearer
    token: "${API_NEGOCIO_TOKEN}"            # env var
```

Solo cambia `base_url` + el token; los nombres de los endpoints son los mismos.

## Test rápido con curl

```bash
TOKEN=mock-erp-secret

curl -s http://localhost:9001/                                                  | jq
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:9001/productos?q=martillo | jq
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:9001/productos/FER-001/stock | jq
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:9001/precios/FER-001 | jq
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:9001/pedidos?telefono=59175344248" | jq
```
