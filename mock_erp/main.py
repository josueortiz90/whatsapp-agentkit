# mock_erp/main.py — Servidor que simula un ERP REST del negocio
# Útil para desarrollar la integración API → AgentKit sin depender de un ERP real.
#
# Arranca con: uvicorn mock_erp.main:app --reload --port 9001
# Auth: Bearer token (MOCK_ERP_TOKEN en .env del mock; default "mock-erp-secret")
#
# Endpoints expuestos:
#   GET /productos?q=&limit=        → búsqueda (lista)
#   GET /productos/{codigo}/stock   → stock actual de un SKU
#   GET /precios/{codigo}           → precio actual de un SKU
#   GET /pedidos?telefono=          → pedidos del cliente (mock fijo)

import csv
import logging
import os
import random
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse

logger = logging.getLogger("mock_erp")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

TOKEN_ESPERADO = os.getenv("MOCK_ERP_TOKEN", "mock-erp-secret")
CSV_PATH = Path("knowledge/productos.csv")

app = FastAPI(title="Mock ERP - Ferretería Ortiz", version="0.1.0")


# ──────────────────────────────────────────────────────────────────────
# Datos: cargamos productos.csv una vez en memoria
# ──────────────────────────────────────────────────────────────────────

def _cargar_productos() -> list[dict]:
    if not CSV_PATH.exists():
        logger.warning(f"{CSV_PATH} no encontrado. El mock devolverá listas vacías.")
        return []
    productos = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["precio_mxn"] = float(row.get("precio_mxn") or 0)
            row["stock"] = int(row.get("stock") or 0)
            productos.append(row)
    return productos


PRODUCTOS = _cargar_productos()
logger.info(f"Mock ERP cargado con {len(PRODUCTOS)} productos")


# ──────────────────────────────────────────────────────────────────────
# Auth: Bearer token simple
# ──────────────────────────────────────────────────────────────────────

def requerir_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Falta header Authorization: Bearer <token>")
    token = authorization.removeprefix("Bearer ").strip()
    if token != TOKEN_ESPERADO:
        raise HTTPException(status_code=403, detail="Token inválido")


# ──────────────────────────────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────────────────────────────

@app.get("/")
async def health():
    return {"status": "ok", "service": "mock-erp", "productos_cargados": len(PRODUCTOS)}


@app.get("/productos", dependencies=[Depends(requerir_token)])
async def listar_productos(q: Optional[str] = None, limit: int = 10):
    """Busca productos por código, nombre, marca o categoría."""
    resultados = PRODUCTOS
    if q:
        q_lower = q.strip().lower()
        resultados = [
            p for p in PRODUCTOS
            if q_lower in " ".join(str(p.get(k, "")) for k in ("codigo", "nombre", "marca", "categoria")).lower()
        ]
    resultados = resultados[:limit]
    # Simulamos que el stock cambia ligeramente respecto al CSV (ERP en vivo)
    return {
        "productos": [
            {**p, "stock": _stock_simulado(p)}
            for p in resultados
        ],
        "total": len(resultados),
    }


@app.get("/productos/{codigo}/stock", dependencies=[Depends(requerir_token)])
async def stock_producto(codigo: str):
    """Stock actual de un SKU específico."""
    p = next((x for x in PRODUCTOS if x.get("codigo", "").lower() == codigo.lower()), None)
    if not p:
        raise HTTPException(status_code=404, detail=f"Producto {codigo} no existe")
    return {
        "codigo": p["codigo"],
        "nombre": p["nombre"],
        "stock_actual": _stock_simulado(p),
        "unidad": p.get("unidad", "pieza"),
    }


@app.get("/precios/{codigo}", dependencies=[Depends(requerir_token)])
async def precio_producto(codigo: str):
    """Precio actual de un SKU. El mock le suma una variación pequeña al CSV para simular cambios."""
    p = next((x for x in PRODUCTOS if x.get("codigo", "").lower() == codigo.lower()), None)
    if not p:
        raise HTTPException(status_code=404, detail=f"Producto {codigo} no existe")
    precio_base = float(p.get("precio_mxn", 0))
    # Simulamos una pequeña variación (-2% a +5%) según hash del código (estable por sesión)
    seed = sum(ord(c) for c in codigo) % 100
    variacion = (seed / 100.0 - 0.2) * 0.05  # rango -1% a +4%
    precio_actual = round(precio_base * (1 + variacion), 2)
    return {
        "codigo": p["codigo"],
        "nombre": p["nombre"],
        "precio_lista_mxn": precio_base,
        "precio_actual_mxn": precio_actual,
        "moneda": "MXN",
    }


@app.get("/pedidos", dependencies=[Depends(requerir_token)])
async def pedidos_cliente(telefono: str):
    """Pedidos previos del cliente. Mock fijo basado en el teléfono."""
    # Mock simple: si el teléfono termina en dígito par, devolvemos 2 pedidos. Si no, lista vacía.
    if not telefono or not telefono[-1].isdigit() or int(telefono[-1]) % 2 != 0:
        return {"telefono": telefono, "pedidos": []}
    return {
        "telefono": telefono,
        "pedidos": [
            {
                "pedido_id": 1001,
                "fecha": "2026-04-15",
                "total_mxn": 567.0,
                "estado": "entregado",
                "items": [
                    {"codigo": "FER-001", "nombre": "Martillo Truper 16oz", "cantidad": 3, "precio": 189.0},
                ],
            },
            {
                "pedido_id": 1042,
                "fecha": "2026-05-02",
                "total_mxn": 945.0,
                "estado": "entregado",
                "items": [
                    {"codigo": "FER-202", "nombre": "Codo PVC 90° 1/2 pulgada", "cantidad": 100, "precio": 8.50},
                    {"codigo": "FER-201", "nombre": "Tubo PVC 1/2 pulgada x 6m", "cantidad": 1, "precio": 89.0},
                ],
            },
        ],
    }


# ──────────────────────────────────────────────────────────────────────
# Utilidades
# ──────────────────────────────────────────────────────────────────────

def _stock_simulado(p: dict) -> int:
    """El stock del ERP varía respecto al CSV para simular movimientos del inventario."""
    base = int(p.get("stock", 0))
    # Variación ±20% según código (estable por sesión, pero distinta del CSV)
    seed = sum(ord(c) for c in p.get("codigo", "")) % 100
    variacion = (seed - 50) / 50.0 * 0.2  # -20% a +20%
    return max(0, int(base * (1 + variacion)))


@app.get("/_diag/productos")
async def diag_productos():
    """Diagnóstico interno: ver todos los productos cargados. Sin auth."""
    return {"total": len(PRODUCTOS), "primer_codigo": PRODUCTOS[0].get("codigo") if PRODUCTOS else None}
