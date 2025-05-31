# 🤖 Servicio API de OpenAI

Un servicio FastAPI completo para integrar las capacidades de OpenAI en tus aplicaciones. Este proyecto proporciona una API REST robusta, un cliente Python y una interfaz web moderna para interactuar con los modelos de OpenAI.

## ✨ Características

- **💬 Chat Completions** - Conversaciones con modelos GPT
- **📝 Text Completions** - Completado de texto clásico
- **🎨 Generación de Imágenes** - Crear imágenes con DALL-E
- **🔢 Embeddings** - Vectores de texto para análisis semántico
- **📋 Listado de Modelos** - Obtener modelos disponibles
- **🏥 Health Checks** - Monitoreo del estado del servicio
- **📚 Documentación Automática** - Swagger UI integrado
- **🌐 Cliente Web** - Interfaz moderna y responsive
- **🐍 Cliente Python** - Librería fácil de usar
- **🔧 CORS Habilitado** - Listo para aplicaciones web

## 🚀 Inicio Rápido

### Prerequisitos

- Python 3.8+
- Clave API de OpenAI

### Instalación

1. **Clona el repositorio**
   ```bash
   git clone <tu-repositorio>
   cd openai/v1
   ```

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura tu clave API**
   ```bash
   # Crea un archivo .env
   echo "OPENAI_API_KEY=tu_clave_api_aqui" > .env
   ```

4. **Inicia el servidor**
   ```bash
   python server.py
   ```

5. **¡Listo! 🎉**
   - **🌐 Cliente Web**: http://localhost:8000
   - **📚 Documentación API**: http://localhost:8000/docs
   - **🏥 Health Check**: http://localhost:8000/health

## 🌐 Cliente Web

### Interfaz Moderna y Completa

El cliente web incluye una interfaz moderna con todas las funcionalidades:

- **🎨 Diseño Moderno**: Glassmorphism, gradientes y animaciones
- **📱 Responsive**: Funciona en desktop, tablet y móvil
- **⚡ Tiempo Real**: Estado del servicio en vivo
- **🎯 Fácil de Usar**: Interfaz intuitiva con ejemplos

### Funcionalidades Disponibles

1. **💬 Chat Completions**
   - Conversaciones con GPT-3.5 y GPT-4
   - Control de temperatura (creatividad)
   - Respuestas formateadas

2. **📝 Text Completions**
   - Completado de texto con GPT-3.5-turbo-instruct
   - Control de tokens y temperatura

3. **🎨 Generación de Imágenes**
   - DALL-E 3 con múltiples tamaños
   - Calidad estándar y HD
   - Vista previa inmediata

4. **🔢 Embeddings**
   - text-embedding-ada-002 y modelos más nuevos
   - Análisis de vectores
   - Información dimensional

5. **📋 Listado de Modelos**
   - Todos los modelos disponibles
   - Información detallada
   - Vista organizada

### Acceder al Cliente Web

```bash
# Opción 1: Navegador directo
start http://localhost:8000

# Opción 2: Servidor local
cd public
python -m http.server 3000
# Luego ir a: http://localhost:3000
```

## 🐍 Cliente Python

### Uso Básico

```python
from client import ApiClient

# Crear cliente
client = ApiClient("http://localhost:8000")

# Chat completion
response = client.chat_completion([
    {"role": "user", "content": "Hola, ¿cómo estás?"}
])
print(response['message'])

# Generación de imagen
image = client.generate_image("Un gato con sombrero")
print(f"Imagen: {image['url']}")
```

### Ejecutar Ejemplos

```bash
# Cliente básico
python client.py

# Ejemplos avanzados
python examples.py

# Pruebas de todos los endpoints
python test_web_client.py
```

## 📚 API Endpoints

### Endpoints Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Cliente web (interfaz) |
| `/health` | GET | Estado del servicio |
| `/chat` | POST | Chat completions |
| `/completion` | POST | Text completions |
| `/images/generate` | POST | Generación de imágenes |
| `/embeddings` | POST | Text embeddings |
| `/models` | GET | Listado de modelos |
| `/docs` | GET | Documentación Swagger |

### Ejemplos de Uso

#### Chat Completion
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "user", "content": "Hola"}
    ],
    "temperature": 0.7
  }'
```

#### Generación de Imagen
```bash
curl -X POST "http://localhost:8000/images/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Un paisaje futurista",
    "size": "1024x1024",
    "quality": "hd"
  }'
```

## 🔧 Configuración

### Variables de Entorno

Crea un archivo `.env` en el directorio raíz:

```env
# Obligatorio
OPENAI_API_KEY=sk-proj-tu_clave_api_de_openai_aqui

# Opcional
OPENAI_ORG_ID=tu_organization_id  # Si usas organizaciones
```

### Configuración del Servidor

```python
# server.py - Configuraciones principales
app = FastAPI(
    title="OpenAI API Service",
    description="Servicio completo de OpenAI",
    version="1.0.0"
)

# CORS habilitado para cliente web
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Archivos estáticos para cliente web
app.mount("/static", StaticFiles(directory="public"))
```

## 🧪 Testing

### Probar Todos los Endpoints

```bash
# Script de pruebas completo
python test_web_client.py
```

### Verificar Estado

```bash
# Health check
curl http://localhost:8000/health

# Modelos disponibles
curl http://localhost:8000/models
```

## 📱 Compatibilidad

### Cliente Web
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Móviles modernos

### Python
- ✅ Python 3.8+
- ✅ Windows, macOS, Linux

## 🔒 Seguridad

- **🔑 API Key**: Almacenada en variables de entorno
- **🚫 No logs**: Las claves no se registran en logs
- **🔐 HTTPS Ready**: Configurable para producción
- **🛡️ Rate Limiting**: Implementable con middleware

## 🚀 Desarrollo

### Estructura del Proyecto

```
openai/v1/
├── server.py           # Servidor FastAPI principal
├── client.py           # Cliente Python
├── examples.py         # Ejemplos avanzados
├── test_web_client.py  # Script de pruebas
├── requirements.txt    # Dependencias
├── README.md          # Esta documentación
├── SETUP.md           # Guía de configuración
└── public/            # Cliente web
    ├── index.html     # Interfaz principal
    ├── style.css      # Estilos modernos
    ├── script.js      # Funcionalidad JS
    └── README.md      # Documentación del cliente web
```

### Agregar Nuevos Endpoints

1. **Definir modelo Pydantic**
```python
class NuevoRequest(BaseModel):
    parametro: str = Field(..., description="Descripción")
```

2. **Crear endpoint**
```python
@app.post("/nuevo-endpoint")
async def nuevo_endpoint(request: NuevoRequest):
    check_openai_client()
    # Lógica aquí
    return {"resultado": "..."}
```

3. **Actualizar cliente web** (añadir en `script.js`)
4. **Actualizar cliente Python** (añadir método en `client.py`)

### Ejecutar en Desarrollo

```bash
# Con recarga automática
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

## 📊 Monitoreo

### Logs del Servidor

```bash
# Ejecutar con logs detallados
python server.py

# Logs de uvicorn
uvicorn server:app --log-level debug
```

### Métricas de Uso

El servidor proporciona información de uso en las respuestas:

```json
{
  "message": "Respuesta del modelo",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 15,
    "total_tokens": 25
  }
}
```

## 🤝 Contribuciones

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

### Problemas Comunes

**❌ Error 503 "Service Unavailable"**
- Verifica tu clave API en el archivo `.env`
- Asegúrate de que la clave sea válida y tenga créditos

**❌ Error CORS**
- El servidor ya tiene CORS habilitado
- Si usas un puerto diferente, actualiza `script.js`

**❌ "Module not found"**
- Ejecuta `pip install -r requirements.txt`
- Verifica que estés en el directorio correcto

### Obtener Ayuda

1. **Documentación**: http://localhost:8000/docs
2. **Issues**: Reporta problemas en el repositorio
3. **Logs**: Revisa la consola del servidor para errores detallados

## 🎉 ¡Listo para Usar!

Tu servicio OpenAI está ahora completamente configurado con:

- ✅ **API REST robusta** con FastAPI
- ✅ **Cliente web moderno** y responsive  
- ✅ **Cliente Python** fácil de usar
- ✅ **Documentación completa** y ejemplos
- ✅ **Scripts de testing** incluidos
- ✅ **Interfaz intuitiva** para todos los endpoints

**¡Disfruta explorando las capacidades de OpenAI! 🚀** 