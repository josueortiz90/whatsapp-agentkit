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

> 📚 **Modelo de dos repos:** este repositorio es el **template** que lee Claude Code. Cuando `/build-agent` genere el codigo de TU agente, ese codigo va a un repo **separado y privado** (lo creas tu). El template se mantiene publico y reutilizable; tu agente con datos del negocio queda privado. Lee la seccion ["Como organizar tus repos"](#como-organizar-tus-repos-template-vs-agente-generado) para el detalle.

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
2. **Creas un repo NUEVO (privado) para TU agente** — Claude Code te da los comandos. **Importante:** NO subes los archivos a este repo (`whatsapp-agentkit`). Tu agente vive en su propio repo, generalmente privado, porque incluye tu catalogo, prompts y datos del negocio. Lee la siguiente seccion ("Como organizar tus repos") para el detalle.
3. **Conectas Railway** — entras a [railway.app](https://railway.app), le das TU repo privado y Railway lo deployea automaticamente
4. **Configuras las variables** — Claude Code te dice exactamente cuales poner en Railway (las mismas API keys de tu .env)
5. **Configuras el webhook** — Claude Code te guia para conectar tu proveedor de WhatsApp con la URL de Railway

Despues de esto, cualquier persona que te escriba por WhatsApp sera atendida por tu agente.

**Nota:** No necesitas saber de servidores ni de deploy. Claude Code te dice cada paso, que escribir y donde hacer click.

---

## Como organizar tus repos: template vs agente generado

Este proyecto trabaja con **dos repositorios distintos**:

| | Template (este repo) | Tu agente |
|---|---|---|
| **URL** | `josueortiz90/whatsapp-agentkit` (publico) | `tu-usuario/mi-negocio-agent` (privado, lo creas tu) |
| **Que contiene** | `CLAUDE.md`, `.skill/build-agent`, `README.md`, `start.sh`, `.env.example` | `agent/`, `config/`, `knowledge/`, `tests/`, `Dockerfile`, `requirements.txt`, `.env.example` |
| **Para que sirve** | Instrucciones que lee Claude Code para CONSTRUIR agentes | El codigo YA GENERADO de tu agente especifico, listo para deploy |
| **Privacidad** | Publico — sirve a otros usuarios de AgentKit | Privado — tiene el catalogo, prompts y datos de tu negocio |
| **Conectado a Railway** | No | Si — Railway deploya desde aqui |

### Por que dos repos?

Cuando corres `/build-agent`, Claude Code genera codigo personalizado para TU negocio: tu catalogo, tu tono, tu knowledge base, tus tools. Ese codigo es **tuyo**, no de AgentKit. Por eso:

- Mantenerlo en un repo separado evita que tus prompts y datos del negocio terminen en un repo publico.
- El template puede actualizarse (mejoras, fixes) sin afectar agentes que ya estan en produccion.
- Si tienes varios agentes (uno por negocio), cada uno vive en su propio repo y se deploya independientemente.

### Como funciona en la practica

```
1. Clonas el TEMPLATE (este repo)
   git clone https://github.com/josueortiz90/whatsapp-agentkit.git
   cd whatsapp-agentkit

2. Corres /build-agent en Claude Code
   Esto GENERA archivos en agent/, config/, knowledge/, tests/, etc.
   El .gitignore de este repo IGNORA esos archivos para no contaminar el template.

3. Cuando estas listo para deploy, creas TU repo privado:
   gh repo create mi-usuario/mi-negocio-agent --private
   #  o crealo manualmente en github.com

4. Copias los archivos generados a una nueva carpeta y los subes a TU repo:
   cp -r agent config knowledge tests requirements.txt Dockerfile \
        docker-compose.yml .env.example ../mi-negocio-agent/
   cd ../mi-negocio-agent
   git init -b main
   git remote add origin https://github.com/mi-usuario/mi-negocio-agent.git
   git add . && git commit -m "initial: agente generado con AgentKit"
   git push -u origin main

5. Conectas TU repo privado a Railway
   railway.app → New Project → Deploy from GitHub repo → mi-negocio-agent
```

### Ejemplo real

Este patron lo usa el creador del proyecto: el agente **"Viki"** para **Ferreteria Ortiz** vive en su propio repo privado, separado del template publico. El template recibe mejoras (dashboard, tool-use, GPS, factura) que se propagan a futuros agentes generados, mientras que el agente Viki tiene su propia historia de commits con cambios especificos del negocio.

### `.gitignore` recomendado para TU repo del agente

```gitignore
# Secretos
.env
.env.local

# Bases de datos locales (en produccion uses Supabase/Railway)
*.db
*.sqlite

# Python
__pycache__/
*.py[cod]
.venv/
venv/

# Helpers temporales
_*.py

# OS / IDE
.DS_Store
Thumbs.db
.vscode/
.idea/
```

NO incluyas en `.gitignore` las carpetas `agent/`, `config/` ni `knowledge/`: esas SI tienen que viajar al repo del agente porque son el codigo y datos que Railway va a deployear.

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
- Si el numero del agente esta dentro de un grupo de WhatsApp, los mensajes del grupo se ignoran automaticamente (chat_id `@g.us`). El agente esta hecho para atencion 1:1, no para participar en grupos.

---

## Caracteristicas destacadas

- 🛠️ **Tool-use loop con Claude** — Claude no solo responde, sino que ejecuta acciones reales: consulta stock, agrega al carrito, cierra pedidos, registra leads, escala a humanos, captura datos de factura. Todo con tope de iteraciones para evitar loops infinitos.
- 📍 **Ubicacion GPS nativa de WhatsApp** — El cliente comparte su ubicacion con el boton 📎 → Ubicacion y la direccion del pedido queda con coordenadas exactas (mas un texto libre con referencias visibles). Cero colonia/codigo postal.
- 🧾 **Facturacion digital integrada** — Cuando el cliente pide factura, el agente recolecta NIT/RFC, nombre y email (con validacion de formato) y los guarda asociados al ultimo pedido del cliente.
- 📊 **Dashboard web de gestion** — `/dashboard` con HTTP Basic Auth. Inbox de conversaciones con filtros (pendientes/atendidas/escaladas), CRM de leads (nuevo/contactado/cliente/perdido), gestion de pedidos (pendiente/confirmado/enviado/entregado/cancelado) y KPIs agregados (ingresos confirmados, conversaciones pendientes, etc.).
- 💾 **Persistencia real** — SQLAlchemy async con SQLite (dev) o PostgreSQL/Supabase (prod). Cuatro tablas: `mensajes`, `conversaciones`, `leads`, `pedidos` (con columnas `factura_nit/nombre/email`).
- 🔌 **Patron adaptador para WhatsApp** — Tres proveedores intercambiables (Whapi.cloud, Meta Cloud API, Twilio). Cambiar de proveedor es cambiar una variable de entorno.
- 🛡️ **Ignora chats grupales por defecto** — Si el numero del agente termina dentro de un grupo de WhatsApp, los mensajes del grupo (sufijo `@g.us`) se descartan en el provider, sin gastar tokens ni ensuciar el dashboard. El agente esta pensado para atencion 1:1.
- 🚀 **Deploy a Railway con un clic** — Push a GitHub → Railway lo deploya. Variables de entorno desde el panel. Webhook publico HTTPS automatico.

---

## Servicios externos: que usa AgentKit y para que

AgentKit no reinventa la rueda. Conecta varios servicios especializados, cada uno con un rol claro. Aqui esta cada uno:

### 🧠 Anthropic Claude API — el cerebro

- **Que es:** El servicio de inteligencia artificial de Anthropic. Es el modelo de lenguaje (`claude-sonnet-4-5`) que entiende los mensajes del cliente, decide que responder y decide cuando ejecutar una accion (tool-use).
- **Para que se usa en AgentKit:** Cada vez que un cliente escribe por WhatsApp, el agente le manda el mensaje + historial + tools disponibles a la API de Claude. Claude responde con texto o pidiendo ejecutar una tool. El "loop" se repite hasta que Claude da una respuesta final.
- **Costo:** Pago por uso. ~$3 por millon de tokens de entrada (~750 mil palabras). Para un agente de WhatsApp normal son centavos por mes.
- **Como conseguir:** [platform.anthropic.com](https://platform.anthropic.com/settings/api-keys) → Settings → API Keys → Create Key
- **Variable de entorno:** `ANTHROPIC_API_KEY`

### 📱 Whapi.cloud / Meta Cloud API / Twilio — el puente con WhatsApp

- **Que son:** Servicios que conectan tu numero de WhatsApp con tu agente. WhatsApp no permite que conectes directamente — necesitas pasar por un proveedor que ya tiene los permisos.
- **Para que se usan en AgentKit:**
  - Reciben los mensajes que mandan tus clientes y los envian a tu webhook (URL publica de Railway).
  - Envian las respuestas de tu agente de vuelta al cliente.
  - Manejan medios: texto, imagenes, audios, ubicacion GPS, etc.
- **Cual elegir:**

| Proveedor | Dificultad | Costo | Cuando usarlo |
|-----------|-----------|-------|---------------|
| **[Whapi.cloud](https://whapi.cloud)** | ⭐ Facil | Sandbox gratis, planes desde ~$39/mes | Empezar rapido, probar, negocios pequenos |
| **[Meta Cloud API](https://developers.facebook.com)** | ⭐⭐ Media | Gratis por conversacion (Meta cobra desde la segunda) | Produccion seria, oficial de WhatsApp |
| **[Twilio](https://twilio.com)** | ⭐⭐ Media | Pago por mensaje (~$0.005/msg) | Empresas, alta confiabilidad |

- **Variables de entorno:** dependen del proveedor (ver `.env.example`). Whapi: `WHAPI_TOKEN`. Meta: `META_ACCESS_TOKEN` + `META_PHONE_NUMBER_ID` + `META_VERIFY_TOKEN`. Twilio: `TWILIO_ACCOUNT_SID` + `TWILIO_AUTH_TOKEN` + `TWILIO_PHONE_NUMBER`.

### 💾 Supabase (o cualquier PostgreSQL) — la base de datos en produccion

- **Que es:** Supabase es un servicio que te da una base de datos PostgreSQL en la nube con un panel web para verla, plan free generoso (500 MB), y sin necesidad de administrar servidor.
- **Para que se usa en AgentKit:** Guarda persistentemente los mensajes, conversaciones, leads, pedidos y datos de facturacion del agente. Tu dashboard lee de aqui. En desarrollo local puedes usar SQLite (un archivo `.db`), pero en produccion Railway necesita una BD externa porque los contenedores se reinician sin estado.
- **Por que Supabase:** El plan free incluye 500 MB de PostgreSQL, panel visual para inspeccionar datos, y un connection string listo para usar. Alternativas validas: PostgreSQL en Railway (mas integrado pero plan free mas chico), Neon, AWS RDS, etc. Si la conexion string es `postgresql://...`, el codigo la acepta.
- **Costo:** Free hasta 500 MB y 50,000 mensajes mensuales activos. Pro $25/mes si creces.
- **Como conseguir:** [supabase.com](https://supabase.com) → New project → Settings → Database → Connection string → **modo Session pooler** (importante: NO Transaction, es incompatible con `asyncpg` por prepared statements).
- **Variable de entorno:** `DATABASE_URL=postgresql://user:pass@host:5432/postgres`
- ⚠️ Si tu password tiene caracteres especiales como `+` o `@`, URL-encode esos caracteres (`+` → `%2B`, `@` → `%40`).

### 🚀 Railway — el hosting de tu agente

- **Que es:** Una plataforma para deployar codigo de GitHub a internet con un par de clics. Sin configurar servidores, sin Kubernetes, sin DevOps. Detecta tu `Dockerfile` o `requirements.txt` y arma el contenedor solo.
- **Para que se usa en AgentKit:** Aloja tu agente en una URL publica HTTPS (`https://tu-app.up.railway.app`) que es la que apunta el webhook de tu proveedor de WhatsApp. Cuando un cliente manda un mensaje, llega a Railway, se procesa y se responde.
- **Por que Railway:** El plan free incluye $5 de credito mensual, suficiente para un agente activo de bajo volumen. Conecta directo a GitHub: push a `main` → redeploy automatico. Variables de entorno desde el panel (no hay que tocar el `.env`). Alternativas: Render, Fly.io, AWS App Runner, Google Cloud Run.
- **Costo:** Plan Hobby $5/mes de credito incluido. Pago por uso (RAM + CPU + ancho de banda).
- **Como conseguir:** [railway.app](https://railway.app) → New Project → Deploy from GitHub repo → seleccionas TU repo privado del agente.
- **Variables a configurar en Railway:** `ANTHROPIC_API_KEY`, las del proveedor (Whapi/Meta/Twilio), `DATABASE_URL` (Supabase), `DASHBOARD_USER`, `DASHBOARD_PASSWORD`, `PORT=8000`, `ENVIRONMENT=production`.

### 🐙 GitHub — versionado + integracion con Railway

- **Que es:** Plataforma de Git mas usada. Aloja codigo y se integra con Railway, Vercel, Cloudflare, etc.
- **Para que se usa en AgentKit:**
  - Guardar el codigo del **template** (publico, este repo) para que otros usuarios lo clonen.
  - Guardar el codigo de **TU agente generado** (privado, repo separado) para que Railway lo deploye.
  - GitHub Actions opcionales para CI/CD.
- **Costo:** Free para repos publicos. Free para repos privados ilimitados con colaboradores limitados (suficiente para un solo dueno).
- **Como conseguir:** [github.com](https://github.com) → New repository.

### 🔌 cloudflared — tunel local para probar webhook (solo desarrollo)

- **Que es:** Una herramienta de Cloudflare que crea un tunel publico HTTPS hacia un servicio que corre en tu maquina (`localhost:8000`). No requiere cuenta ni signup.
- **Para que se usa en AgentKit:** Cuando estas desarrollando localmente y quieres probar el webhook con WhatsApp REAL antes de deployar a Railway. Sin un tunel, el proveedor (Whapi/Meta/Twilio) no puede mandarle mensajes a tu `localhost`.
- **Costo:** Gratis. Sin cuenta. La URL es efimera (cambia cada vez que reinicias).
- **Como instalar:**
  - **Mac/Linux:** `brew install cloudflared`
  - **Windows:** `winget install Cloudflare.cloudflared`
- **Como usarlo:** Levantas uvicorn en local en :8000, luego en otra terminal: `cloudflared tunnel --url http://localhost:8000`. Te da una URL `https://*.trycloudflare.com` que apuntas en el webhook del proveedor.
- **Alternativa:** [ngrok](https://ngrok.com) (funciona igual pero requiere cuenta gratuita).

### 🐳 Docker — contenedores para deploy alternativo (opcional)

- **Que es:** Sistema de contenedores. Cada agente se empaqueta en una imagen Docker reproducible.
- **Para que se usa en AgentKit:** Railway usa Docker por debajo automaticamente. Solo necesitas tocarlo si quieres deployar a otro sitio (tu propio servidor, AWS, GCP, etc.) o correr localmente con `docker compose up`.
- **Costo:** Free.
- **Cuando lo necesitas:** Si Railway no te conviene y prefieres self-hosting en tu propio servidor.

### Resumen visual

```
            ┌─────────────────────────────────────────────┐
            │  Cliente final manda mensaje por WhatsApp   │
            └───────────────────┬─────────────────────────┘
                                │
                                v
                ┌──────────────────────────────────────┐
                │  Whapi.cloud / Meta Cloud API /      │
                │  Twilio  (eliges UNO)                │
                │  Rol: puente con WhatsApp            │
                └──────────────┬───────────────────────┘
                               │ POST /webhook
                               v
            ┌──────────────────────────────────────────┐
            │  Tu agente corriendo en Railway          │
            │  Rol: hosting publico HTTPS              │
            └────┬──────────────┬────────────────┬─────┘
                 │              │                │
        consulta │       persiste│         renderiza
                 v              v                v
       ┌──────────────┐  ┌──────────────┐  ┌─────────────┐
       │ Anthropic    │  │ Supabase     │  │ Dashboard   │
       │ Claude API   │  │ PostgreSQL   │  │ /dashboard  │
       │ Rol: cerebro │  │ Rol: BD prod │  │ Rol: humano │
       └──────────────┘  └──────────────┘  └─────────────┘

   Para versionado:  GitHub (template publico + repo privado del agente)
   Para dev local:   cloudflared (tunel HTTPS hacia localhost:8000)
```

---

## Requisitos previos

Necesitas estas cuentas/herramientas antes de empezar. Las 4 primeras son obligatorias; las 3 ultimas solo si vas a deployar a produccion.

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

### 5. (Opcional para produccion) Cuenta de Supabase

Solo si vas a deployar el agente: necesitas una base de datos PostgreSQL en la nube.

1. Ve a [supabase.com](https://supabase.com) y crea cuenta
2. New project → guarda el password de BD que generes (no lo veras de nuevo)
3. Espera 1-2 minutos a que el proyecto este "Healthy" (verde)
4. Settings → Database → Connection string → **modo Session pooler**
5. Copia la cadena, reemplaza `[YOUR-PASSWORD]` por la real (URL-encoded si tiene `+` o `@`)

Si solo vas a probar el agente en local con `test_local.py`, **NO necesitas Supabase** — usa SQLite por defecto.

### 6. (Opcional para produccion) Cuenta de Railway

Para alojar el agente en internet con una URL publica.

1. Ve a [railway.app](https://railway.app)
2. Autoriza Railway en tu cuenta de GitHub (le da acceso a tus repos)
3. Plan Hobby trae $5/mes de credito gratis — suficiente para empezar

### 7. (Opcional, solo dev local con WhatsApp real) cloudflared

Si quieres probar el webhook con WhatsApp real sin deployar, instala cloudflared:

- **Mac/Linux:** `brew install cloudflared`
- **Windows:** `winget install Cloudflare.cloudflared`

Lo usaras asi: `cloudflared tunnel --url http://localhost:8000` para crear un tunel HTTPS publico.

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
