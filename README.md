# AgentKit — WhatsApp AI Agent Builder

Construye tu propio agente de WhatsApp con inteligencia artificial en menos de 30 minutos.
No necesitas saber programar. Claude Code construye todo por ti.

<!-- ![AgentKit Demo](demo.gif) -->

---

## Que es AgentKit?

AgentKit es un proyecto que usa **Claude Code** (la herramienta de programacion de Anthropic)
para generar un agente de WhatsApp completo y personalizado para tu negocio.

Tu solo respondes preguntas sobre tu negocio. Claude Code se encarga de:
- Escribir todo el codigo
- Configurar la conexion con WhatsApp (incluyendo soporte para **ubicacion GPS nativa**)
- Crear un "cerebro" con IA que usa **tool-use loop** (puede consultar stock, agregar al carrito, cerrar pedidos, registrar leads, escalar a un humano)
- Levantar un **dashboard web** donde puedes ver cada conversacion, marcar quien fue atendido, gestionar leads, pedidos y datos de facturacion
- Persistir todo en una **base de datos real** (SQLite local o PostgreSQL/Supabase en produccion): mensajes, conversaciones, leads, pedidos y facturas
- Dejarlo listo para que tus clientes le escriban

---

## Como funciona? (El flujo completo)

### Paso 1: Tu clonas el repo y corres un comando

**Mac / Linux:**
```bash
git clone https://github.com/josueortiz90/whatsapp-agentkit.git
cd whatsapp-agentkit
bash start.sh
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/josueortiz90/whatsapp-agentkit.git
cd whatsapp-agentkit
# start.sh requiere bash. Opciones en Windows:
#   - Git Bash (viene con Git for Windows): bash start.sh
#   - WSL: wsl bash start.sh
#   - O simplemente verifica manualmente:
#       python --version    # debe ser 3.11+
#       claude --version    # Claude Code instalado
```

`start.sh` solo verifica que tengas Python 3.11+ y Claude Code instalados.

### Paso 2: Abres Claude Code y escribes /build-agent

```bash
claude
# Dentro de Claude Code escribe:
/build-agent
```

Esto activa el sistema. Claude Code lee las instrucciones de `CLAUDE.md` y empieza
a guiarte paso a paso.

### Paso 3: Claude Code te entrevista (5 minutos)

Te hace 10 preguntas, una por una:

1. **Nombre de tu negocio** — ej: "Cafeteria El Buen Sabor"
2. **A que se dedica** — ej: "Vendemos cafe de especialidad y postres artesanales"
3. **Para que quieres el agente** — responder preguntas, agendar citas, tomar pedidos, etc.
4. **Nombre del agente** — ej: "Sofia" (el nombre que veran tus clientes)
5. **Tono de comunicacion** — profesional, amigable, vendedor, o empatico
6. **Horario de atencion** — ej: "Lunes a Viernes 9am a 6pm"
7. **Archivos de tu negocio** — menu, precios, FAQ (los pones en la carpeta /knowledge)
8. **API Key de Anthropic** — la llave para usar Claude AI (te guia a obtenerla)
9. **Proveedor de WhatsApp** — eliges entre Whapi.cloud, Meta, o Twilio
10. **Credenciales del proveedor** — el token o keys de tu servicio de WhatsApp

### Paso 4: Claude Code construye tu agente (2-5 minutos)

Con tus respuestas, genera automaticamente estos archivos:

```
tu-proyecto/
├── agent/                     ← EL AGENTE COMPLETO
│   ├── main.py                Servidor FastAPI: webhook + monta el dashboard
│   ├── brain.py               Cerebro con tool-use loop de Claude
│   ├── memory.py              SQLAlchemy: mensajes, conversaciones, leads, pedidos, KPIs
│   ├── tools.py               Tools que Claude puede invocar: consultar_stock,
│   │                          agregar_al_carrito, confirmar_pedido, registrar_lead,
│   │                          escalar_a_humano, registrar_datos_factura
│   ├── providers/             Conexion con tu servicio de WhatsApp
│   │   ├── base.py            Interfaz comun (parsear_webhook / enviar_mensaje)
│   │   ├── __init__.py        Selecciona el proveedor desde .env
│   │   └── whapi.py           Adaptador (o meta.py / twilio.py). Parsea
│   │                          mensajes de texto Y ubicacion GPS nativa.
│   └── dashboard/             ← DASHBOARD DE GESTION (HTTP Basic Auth)
│       ├── auth.py            Login con DASHBOARD_USER / DASHBOARD_PASSWORD
│       ├── routes.py          /dashboard, /dashboard/leads, /dashboard/pedidos
│       └── templates/         Jinja2: inbox, conversacion, leads, pedidos
│
├── config/                    ← CONFIGURACION
│   ├── business.yaml          Datos de tu negocio
│   └── prompts.yaml           El "prompt" que define la personalidad del agente
│                              (incluye flujos de envio GPS y facturacion)
│
├── knowledge/                 ← TUS ARCHIVOS
│   └── (menu.pdf, precios.txt, productos.csv, etc.)
│
├── tests/
│   └── test_local.py          Simulador de chat en tu terminal
│
├── requirements.txt           Dependencias de Python
├── Dockerfile                 Para produccion
├── docker-compose.yml         Orquestacion
└── .env                       Tus API keys + DASHBOARD_USER/PASSWORD (nunca se sube)
```

### Paso 5: Pruebas tu agente en la terminal (5 minutos)

Claude Code ejecuta un simulador de chat donde TU escribes como si fueras un cliente:

```
Tu: Hola, que horarios tienen?
Agente: Hola! Nuestro horario es de Lunes a Viernes de 9am a 6pm.
        Quieres que te ayude con algo mas?

Tu: Cuanto cuesta el cafe americano?
Agente: El cafe americano tiene un precio de $45 pesos.
        Te gustaria ordenar uno?
```

Si algo no te gusta, le dices a Claude Code y lo ajusta al momento.

### Paso 6: Deploy a produccion (opcional, 10 minutos)

Cuando estes satisfecho con tu agente, Claude Code te guia para ponerlo en linea:

1. **Claude Code prepara tu proyecto** para produccion (ajusta configuracion)
2. **Tu lo subes a GitHub** — Claude Code te da los comandos exactos para crear tu repo
3. **Conectas Railway** — entras a [railway.app](https://railway.app), le das tu repo de GitHub y Railway lo deployea automaticamente
4. **Configuras las variables** — Claude Code te dice exactamente cuales poner en Railway (las mismas API keys de tu .env)
5. **Configuras el webhook** — Claude Code te guia para conectar tu proveedor de WhatsApp con la URL de Railway

Despues de esto, cualquier persona que te escriba por WhatsApp sera atendida por tu agente.

**Nota:** No necesitas saber de servidores ni de deploy. Claude Code te dice cada paso, que escribir y donde hacer click.

---

## Como funciona el agente ya en produccion?

```
Un cliente escribe "Hola, quiero un martillo" por WhatsApp
         |
         v
Tu proveedor de WhatsApp (Whapi/Meta/Twilio) recibe el mensaje
         |
         v
Envia el mensaje a tu servidor en Railway via webhook
         |
         v
agent/providers/ → Normaliza el mensaje. Si el cliente comparte ubicacion
                   GPS (boton nativo de WhatsApp), se convierte en texto:
                   "[UBICACION COMPARTIDA] Lat: X, Lng: Y · maps link"
         |
         v
agent/memory.py → Busca el historial de ESE cliente y registra el mensaje
                  nuevo (tablas: mensajes + conversaciones)
         |
         v
agent/brain.py → Tool-use loop con Claude:
                 1. Envia system prompt + historial + tools disponibles
                 2. Si Claude pide una tool (ej. agregar_al_carrito), se ejecuta
                    y el resultado vuelve a Claude
                 3. Se repite hasta que Claude genera la respuesta final
                 4. Las acciones con efecto (pedidos, leads, factura)
                    se persisten en la BD via agent/tools.py + agent/memory.py
         |
         v
agent/providers/ → Envia la respuesta de vuelta por WhatsApp
         |
         v
El cliente recibe la respuesta en segundos

         ╔══════════════════════════════════════════════════════════╗
         ║  Mientras tanto, en /dashboard (HTTP Basic Auth):        ║
         ║    - Veo todas las conversaciones (atendidas/pendientes) ║
         ║    - Reviso los leads capturados                         ║
         ║    - Marco pedidos como enviados/entregados              ║
         ║    - Reviso datos de facturacion por pedido              ║
         ╚══════════════════════════════════════════════════════════╝
```

**Cosas importantes:**
- Cada cliente tiene su propio historial. Si alguien vuelve al dia siguiente, el agente recuerda la conversacion.
- El agente NUNCA inventa informacion. Solo responde con lo que tu le diste y con lo que las tools le devuelven.
- Si no sabe algo, responde: "No tengo esa informacion, dejame conectarte con alguien del equipo." y escala via la tool `escalar_a_humano`.
- Cuando toma un pedido, NO te pide colonia/codigo postal — te pide una **descripcion libre** del domicilio + tu **ubicacion GPS** usando el boton nativo de WhatsApp. La direccion final queda con coordenadas exactas para el repartidor.
- Cuando pides factura, recolecta **NIT/RFC + nombre + email** (valida el formato del email) y lo asocia al ultimo pedido.

---

## Caracteristicas destacadas

- 🛠️ **Tool-use loop con Claude** — Claude no solo responde, sino que ejecuta acciones reales: consulta stock, agrega al carrito, cierra pedidos, registra leads, escala a humanos, captura datos de factura. Todo con tope de iteraciones para evitar loops infinitos.
- 📍 **Ubicacion GPS nativa de WhatsApp** — El cliente comparte su ubicacion con el boton 📎 → Ubicacion y la direccion del pedido queda con coordenadas exactas (mas un texto libre con referencias visibles). Cero colonia/codigo postal.
- 🧾 **Facturacion digital integrada** — Cuando el cliente pide factura, el agente recolecta NIT/RFC, nombre y email (con validacion de formato) y los guarda asociados al ultimo pedido del cliente.
- 📊 **Dashboard web de gestion** — `/dashboard` con HTTP Basic Auth. Inbox de conversaciones con filtros (pendientes/atendidas/escaladas), CRM de leads (nuevo/contactado/cliente/perdido), gestion de pedidos (pendiente/confirmado/enviado/entregado/cancelado) y KPIs agregados (ingresos confirmados, conversaciones pendientes, etc.).
- 💾 **Persistencia real** — SQLAlchemy async con SQLite (dev) o PostgreSQL/Supabase (prod). Cuatro tablas: `mensajes`, `conversaciones`, `leads`, `pedidos` (con columnas `factura_nit/nombre/email`).
- 🔌 **Patron adaptador para WhatsApp** — Tres proveedores intercambiables (Whapi.cloud, Meta Cloud API, Twilio). Cambiar de proveedor es cambiar una variable de entorno.
- 🚀 **Deploy a Railway con un clic** — Push a GitHub → Railway lo deploya. Variables de entorno desde el panel. Webhook publico HTTPS automatico.

---

## Requisitos previos

Necesitas 4 cosas antes de empezar:

### 1. Python 3.11 o superior
- **Mac**: `brew install python` o descarga de [python.org](https://www.python.org/downloads/)
- **Windows**: Descarga de [python.org](https://www.python.org/downloads/windows/) (marca "Add to PATH")
- **Linux**: `sudo apt install python3.11`
- Verifica: `python3 --version` (en Windows: `python --version`)

### 2. Claude Code
```bash
# Primero necesitas Node.js: https://nodejs.org
npm install -g @anthropic-ai/claude-code

# Autenticate (solo la primera vez)
claude
```

### 3. API Key de Anthropic
1. Ve a [platform.anthropic.com](https://platform.anthropic.com/settings/api-keys)
2. Crea una cuenta o inicia sesion
3. Ve a Settings → API Keys → Create Key
4. Copia la key (empieza con `sk-ant-...`)

### 4. Cuenta de WhatsApp API (elige una)

| Proveedor | Dificultad | Costo | Mejor para |
|-----------|-----------|-------|------------|
| [Whapi.cloud](https://whapi.cloud) | Facil | Sandbox gratis | Empezar rapido, probar |
| [Meta Cloud API](https://developers.facebook.com) | Media | Gratis por conversacion | Produccion seria |
| [Twilio](https://twilio.com) | Media | Pago por mensaje | Empresas, alta confiabilidad |

**Si no estas seguro, empieza con Whapi.cloud.** Es la opcion mas rapida — te registras, copias un token, y listo.

---

## Inicio rapido (3 comandos)

```bash
# 1. Clona el repositorio
git clone https://github.com/josueortiz90/whatsapp-agentkit.git
cd whatsapp-agentkit

# 2. Verifica tu entorno
bash start.sh        # Mac/Linux/Git Bash
#  En PowerShell sin Git Bash: verifica manual con `python --version` y `claude --version`

# 3. Abre Claude Code y construye tu agente
claude
# Escribe: /build-agent
```

Claude Code te guia desde ahi. Solo responde las preguntas.

---

## Proveedores de WhatsApp

AgentKit soporta 3 proveedores. Tu eliges cual usar durante el setup.

### Whapi.cloud (recomendado para empezar)
- Registrate en [whapi.cloud](https://whapi.cloud)
- Tienen un sandbox gratuito (no necesitas verificar nada)
- Solo necesitas: **1 token**
- Ideal para probar y para negocios pequenos

### Meta Cloud API (oficial)
- Configura en [developers.facebook.com](https://developers.facebook.com)
- Es la API oficial de WhatsApp (de Meta/Facebook)
- Necesitas: **Access Token** + **Phone Number ID** + **Verify Token**
- Requiere cuenta de Facebook Business verificada
- Gratis por conversacion (pagas solo por conversaciones iniciadas por ti)

### Twilio
- Registrate en [twilio.com](https://twilio.com)
- Muy confiable, excelente documentacion
- Necesitas: **Account SID** + **Auth Token** + **Phone Number**
- Tiene sandbox para probar gratis
- Pago por mensaje en produccion

---

## Casos de uso

| Tipo de negocio | Que hace el agente | Ejemplo |
|-----------------|-------------------|---------|
| **Restaurante** | Responde sobre menu, horarios, ubicacion | "El platillo del dia es..." |
| **Clinica/Salon** | Agenda citas y reservaciones | "Tu cita quedo para el martes a las 3pm" |
| **Inmobiliaria** | Califica leads y envia info de propiedades | "Tenemos 3 departamentos en tu rango..." |
| **Tienda online** | Toma pedidos por WhatsApp | "Tu pedido de 2 pasteles quedo confirmado" |
| **SaaS/Software** | Soporte tecnico post-venta | "Para resetear tu contrasena, sigue estos pasos..." |
| **Cualquier negocio** | Responde preguntas frecuentes 24/7 | "Nuestro horario es..." |

---

## Comandos utiles (despues del setup)

```bash
# Probar el agente sin WhatsApp (chat en terminal)
python tests/test_local.py

# Arrancar el servidor localmente (webhook + dashboard)
uvicorn agent.main:app --reload --port 8000

# Abrir el dashboard
# → http://localhost:8000/dashboard
#   Usuario / contrasena: DASHBOARD_USER / DASHBOARD_PASSWORD (tu .env)

# Probar el webhook con WhatsApp real desde tu maquina (tunel publico):
#   Mac/Linux:    cloudflared tunnel --url http://localhost:8000
#   Windows:      winget install Cloudflare.cloudflared
#                 cloudflared tunnel --url http://localhost:8000
# Apunta el webhook de tu proveedor a la URL https://...trycloudflare.com/webhook

# Build Docker para produccion
docker compose up --build

# Ver logs del agente
docker compose logs -f agent
```

---

## Personalizar tu agente despues

No necesitas tocar codigo. Abre Claude Code y pidele cambios en lenguaje natural:

```bash
# Cambiar como responde el agente
claude "El agente esta siendo muy formal. Hazlo mas amigable y casual."

# Agregar informacion nueva
claude "Agregamos un nuevo servicio de delivery. Actualiza el agente."

# Agregar una herramienta
claude "Quiero que el agente pueda consultar disponibilidad de citas."

# Cambiar de proveedor de WhatsApp
claude "Quiero migrar de Whapi a Meta Cloud API."
```

---

## Stack tecnico

Para los curiosos, esto es lo que se usa por debajo:

| Componente | Tecnologia | Para que sirve |
|-----------|-----------|----------------|
| IA | Claude (claude-sonnet-4-5) con **tool-use loop** | Cerebro: razona, ejecuta acciones, persiste resultados |
| Servidor | FastAPI + Uvicorn | Recibe webhooks de WhatsApp y sirve el dashboard |
| WhatsApp | Whapi.cloud / Meta / Twilio | Conecta con WhatsApp (tu eliges). Whapi parsea ubicacion GPS nativa. |
| Base de datos | SQLite (local) o PostgreSQL/Supabase (prod) con SQLAlchemy async | Mensajes, conversaciones, leads, pedidos, datos de factura |
| Dashboard | Jinja2 server-side + HTTP Basic Auth | Inbox, gestion de leads y pedidos, KPIs |
| Deploy | Docker + Railway | Pone tu agente en internet con un click |
| Config | python-dotenv + YAML | API keys + personalidad del agente |

---

## Arquitectura (para desarrolladores)

```
                      WhatsApp (cliente)
                            |
                            v
Proveedor (Whapi/Meta/Twilio) ←→ agent/providers/ (normaliza texto + GPS)
                            |
                            v
        FastAPI (agent/main.py) ←→ agent/memory.py (SQLAlchemy async)
              |                          |
              |                          ├── tabla mensajes
              |                          ├── tabla conversaciones
              |                          ├── tabla leads
              |                          └── tabla pedidos (+ factura_*)
              v
Claude API (agent/brain.py)  ←→ agent/tools.py  (6 tools registradas)
   |                                  ├── consultar_stock
   |   loop while                     ├── agregar_al_carrito
   |   stop_reason == tool_use:       ├── confirmar_pedido
   |     ejecutar tool                ├── registrar_lead
   |     pasarle el resultado         ├── escalar_a_humano
   |     a Claude                     └── registrar_datos_factura
   v
Respuesta enviada de vuelta por WhatsApp

  ┌──────────────────────────────────────────────────────────┐
  │  agent/dashboard/  (mismo FastAPI, /dashboard/*)         │
  │    HTTP Basic Auth → routes.py → templates Jinja2        │
  │    Lee de la misma BD para mostrar inbox/leads/pedidos   │
  └──────────────────────────────────────────────────────────┘
```

**Patrones clave:**

- **Adaptador de proveedor** — Cada proveedor de WhatsApp (Whapi/Meta/Twilio) implementa la misma interfaz `ProveedorWhatsApp` con `parsear_webhook()` y `enviar_mensaje()`. `main.py` no sabe ni le importa cual estas usando.
- **Tool-use loop** — `brain.py` itera mientras Claude pida tools (tope `MAX_TOOL_ITERATIONS=6`). Cada tool ejecuta logica de negocio y devuelve un JSON que Claude lee en la siguiente vuelta.
- **Persistencia separada** — El carrito vive en memoria efimera (RAM), pero al confirmar el pedido se persiste a BD. Asi los reinicios no pierden ventas cerradas.
- **Provider parsea ubicacion GPS** — Cuando el cliente comparte ubicacion con el boton nativo de WhatsApp, el provider la convierte a `"[UBICACION COMPARTIDA] Lat: X, Lng: Y · maps link"` para que Claude la lea como texto sin necesidad de campos estructurados extra.

---

## Preguntas frecuentes

**Necesito saber programar?**
No. Claude Code escribe todo el codigo por ti. Tu solo respondes preguntas.

**Cuanto cuesta?**
- AgentKit es gratis y open source
- Claude API: pagas por uso (~$3/millon de tokens, muy barato para un bot)
- WhatsApp: depende del proveedor (Whapi tiene sandbox gratis)
- Railway: plan gratis disponible para proyectos pequenos

**Puedo usar esto con mi negocio real?**
Si. Despues de las pruebas locales, lo subes a Railway y cualquier cliente
que te escriba por WhatsApp sera atendido por tu agente.

**Y si el agente no sabe algo?**
Responde algo como: "No tengo esa informacion, dejame conectarte con alguien
de nuestro equipo." Nunca inventa datos.

**Puedo tener multiples agentes?**
Si. Clona el repo varias veces, uno por negocio. Cada agente es independiente.

**Puedo cambiar de proveedor de WhatsApp despues?**
Si. Abre Claude Code y dile: "Quiero cambiar de Whapi a Meta Cloud API."
El regenerara los archivos necesarios.

---

## Creditos

Creado por **Todo de IA** — [@soyenriquerocha](https://instagram.com/soyenriquerocha)

Construido con [Claude Code](https://claude.ai/claude-code) para builders de LATAM.

---

## Licencia

MIT — Usa este proyecto como quieras, para lo que quieras.
