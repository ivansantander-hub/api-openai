# 🤖 Servicio API de OpenAI

Un servicio FastAPI completo para integrar las capacidades de OpenAI en tus aplicaciones. Este proyecto proporciona una API REST robusta y un cliente Python para interactuar con los modelos de OpenAI.

## ✨ Características

- **Chat Completions** - Conversaciones con modelos GPT
- **Text Completions** - Completado de texto clásico
- **Generación de Imágenes** - Crear imágenes con DALL-E
- **Embeddings** - Vectores de texto para análisis semántico
- **Listado de Modelos** - Obtener modelos disponibles
- **Health Checks** - Monitoreo del estado del servicio
- **Documentación Automática** - Swagger UI integrado
- **CORS Habilitado** - Listo para aplicaciones web
- **Cliente Python** - Interfaz fácil de usar

## 🚀 Inicio Rápido

### Prerequisitos

- Python 3.8+
- Clave API de OpenAI

### Instalación

1. **Clona o descarga el proyecto**
   ```bash
   cd /tu/directorio/del/proyecto
   ```

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura las variables de entorno**
   
   Crea un archivo `.env` en el directorio raíz:
   ```env
   OPENAI_API_KEY=tu_clave_api_de_openai_aqui
   ```

4. **Ejecuta el servidor**
   ```bash
   python server.py
   ```

   El servidor estará disponible en: `http://localhost:8000`

### Verificar la Instalación

Una vez que el servidor esté ejecutándose, puedes:

- **Ver la documentación interactiva**: `http://localhost:8000/docs`
- **Verificar el estado**: `http://localhost:8000/health`
- **Ejecutar el cliente de prueba**: `python client.py`

## 📖 Uso de la API

### Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Página principal |
| GET | `/health` | Verificación de estado |
| POST | `/chat` | Completado de chat |
| POST | `/completion` | Completado de texto |
| POST | `/images/generate` | Generación de imágenes |
| POST | `/embeddings` | Creación de embeddings |
| GET | `/models` | Lista de modelos disponibles |

### Ejemplos de Uso

#### 1. Chat Completion

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hola, cuéntame un chiste"}
    ],
    "model": "gpt-3.5-turbo",
    "temperature": 0.7
  }'
```

#### 2. Generación de Imágenes

```bash
curl -X POST "http://localhost:8000/images/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Un gato usando lentes de sol",
    "size": "1024x1024",
    "quality": "standard"
  }'
```

#### 3. Embeddings

```bash
curl -X POST "http://localhost:8000/embeddings" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hola mundo",
    "model": "text-embedding-ada-002"
  }'
```

## 🐍 Uso del Cliente Python

```python
from client import ApiClient

# Inicializar cliente
client = ApiClient(base_url="http://localhost:8000")

# Chat completion
response = client.chat_completion([
    {"role": "user", "content": "Explícame la inteligencia artificial"}
])
print(response['message'])

# Generar imagen
image_response = client.generate_image("Un paisaje futurista")
print(f"URL de imagen: {image_response['urls'][0]}")

# Crear embeddings
embedding_response = client.create_embedding("Texto para analizar")
print(f"Vector de {len(embedding_response['embeddings'][0])} dimensiones")
```

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `OPENAI_API_KEY` | Tu clave API de OpenAI | ✅ |
| `OPENAI_ORG_ID` | ID de organización (opcional) | ❌ |

### Modelos Soportados

- **Chat**: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo-preview`
- **Completions**: `gpt-3.5-turbo-instruct`
- **Imágenes**: `dall-e-3`, `dall-e-2`
- **Embeddings**: `text-embedding-ada-002`, `text-embedding-3-small`, `text-embedding-3-large`

## 📁 Estructura del Proyecto

```
openai-api-service/
├── server.py              # Servidor FastAPI principal
├── client.py            # Cliente Python para testing
├── requirements.txt     # Dependencias de Python
├── README.md           # Este archivo
└── .env                # Variables de entorno (crear manualmente)
```

## 🛠 Desarrollo

### Ejecutar en Modo Desarrollo

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### Ejecutar Tests

```bash
python client.py
```

### Ver Documentación

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🚨 Consideraciones de Seguridad

1. **Nunca expongas tu clave API** - Usa variables de entorno
2. **Configura CORS apropiadamente** para producción
3. **Implementa autenticación** si es necesario
4. **Limita el rate limiting** para evitar costos excesivos
5. **Monitorea el uso** de tokens y costos

## 💰 Costos de OpenAI

Ten en cuenta que usar esta API generará costos en tu cuenta de OpenAI:

- **GPT-3.5-turbo**: ~$0.002 por 1K tokens
- **GPT-4**: ~$0.03 por 1K tokens
- **DALL-E 3**: ~$0.04 por imagen (1024x1024)
- **Embeddings**: ~$0.0001 por 1K tokens

Consulta la [página de precios de OpenAI](https://openai.com/pricing) para información actualizada.

## 🐛 Solución de Problemas

### Error: "OpenAI API key is not configured"
- Verifica que el archivo `.env` existe y contiene `OPENAI_API_KEY`
- Asegúrate de que la clave API es válida

### Error: "Connection refused"
- Verifica que el servidor está ejecutándose en `http://localhost:8000`
- Revisa que no hay conflictos de puertos

### Error: "Rate limit exceeded"
- Estás haciendo demasiadas solicitudes muy rápido
- Implementa delays entre solicitudes o reduce la frecuencia

### Error: "OpenAI client is not initialized"
- Reinstala las dependencias: `pip install -r requirements.txt`
- Verifica que tu clave API es válida
- Revisa que no hay problemas de conectividad

## 📞 Soporte

Para problemas o sugerencias:

1. Revisa la documentación de OpenAI
2. Verifica los logs del servidor
3. Consulta los ejemplos en `client.py`

## 📄 Licencia

Este proyecto es de código abierto. Úsalo libremente para tus proyectos personales o comerciales.

---

**¡Disfruta construyendo con IA! 🚀** 