# 🌐 Cliente Web OpenAI API

Un cliente web moderno y completo para interactuar con la API de OpenAI a través de tu servidor FastAPI.

## ✨ Características

- **🎨 Interfaz Moderna**: Diseño moderno con glassmorphism y animaciones suaves
- **📱 Responsive**: Funciona perfectamente en desktop, tablet y móvil
- **🔥 Todas las Funcionalidades**: Soporte completo para todos los endpoints de la API
- **⚡ Tiempo Real**: Indicador de estado en tiempo real del servicio
- **🎯 Fácil de Usar**: Interfaz intuitiva con tooltips y ejemplos
- **⌨️ Atajos de Teclado**: Ctrl+Enter para enviar desde cualquier campo
- **📊 Visualización Rica**: Resultados formateados con sintaxis highlighting

## 🚀 Funcionalidades Disponibles

### 1. **Health Check** 🏥
- Verificar el estado del servicio
- Información en tiempo real de la conectividad
- Estado del cliente OpenAI

### 2. **Listado de Modelos** 📋
- Obtener todos los modelos disponibles
- Visualización en grid organizada
- Información detallada de cada modelo

### 3. **Chat Completions** 💬
- Conversaciones con modelos GPT
- Control de temperatura (creatividad)
- Respuestas formateadas
- Historial de conversaciones

### 4. **Text Completions** ✍️
- Completado de texto clásico
- Control de temperatura y tokens máximos
- Ideal para generación de contenido
- Vista previa de respuestas

### 5. **Generación de Imágenes** 🎨
- Crear imágenes con DALL-E
- Múltiples tamaños disponibles
- Calidad estándar y HD
- Vista previa inmediata

### 6. **Text Embeddings** 🔢
- Crear embeddings de texto
- Múltiples modelos disponibles
- Vista previa de vectores
- Información dimensional

## 🎯 Cómo Usar

### 1. **Iniciar el Servidor**
Primero asegúrate de que tu servidor FastAPI esté corriendo:

```bash
cd ../
python server.py
```

### 2. **Abrir el Cliente Web**
Simplemente abre `index.html` en tu navegador:

```bash
# Opción 1: Doble click en index.html
# Opción 2: Abrir con navegador
start index.html

# Opción 3: Servidor local (recomendado)
python -m http.server 3000
# Luego ir a: http://localhost:3000
```

### 3. **Usar la Interfaz**
1. **Verificar Estado**: La página automáticamente verificará el estado del servicio
2. **Probar Endpoints**: Usa cada sección para probar diferentes funcionalidades
3. **Ver Resultados**: Los resultados se muestran con formato rico y datos completos

## ⌨️ Atajos de Teclado

- **Ctrl + Enter**: Enviar desde cualquier campo de texto
- **F5**: Actualizar estado del servicio

## 🎨 Personalización

### Cambiar URL del Servidor
Edita `script.js` línea 2:
```javascript
const API_BASE_URL = 'http://localhost:8000'; // Cambia esta URL
```

### Modificar Estilos
Edita `style.css` para personalizar:
- Colores y gradientes
- Espaciado y tamaños
- Animaciones y transiciones

## 🔧 Resolución de Problemas

### ❌ "Service Offline"
- Verifica que el servidor FastAPI esté corriendo
- Confirma que la URL en `script.js` sea correcta
- Revisa la consola del navegador para más detalles

### ❌ Errores CORS
El servidor ya tiene CORS habilitado, pero si tienes problemas:
- Usa `python -m http.server` en lugar de abrir el archivo directamente
- Verifica que el servidor tenga la configuración CORS correcta

### ❌ Errores 503 "Service Unavailable"
- Asegúrate de tener configurada tu clave API de OpenAI
- Crea un archivo `.env` con `OPENAI_API_KEY=tu_clave`
- Reinicia el servidor después de agregar la clave

## 📱 Compatibilidad

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Móviles modernos

## 🔄 Actualizaciones Automáticas

El cliente web se conecta automáticamente al servidor y muestra:
- Estado del servicio en tiempo real
- Errores y mensajes informativos
- Resultados formateados y organizados

## 💡 Consejos de Uso

1. **Temperatura**: 
   - 0.0-0.3: Respuestas focalizadas y deterministas
   - 0.4-0.7: Balance entre creatividad y coherencia
   - 0.8-2.0: Respuestas muy creativas y variadas

2. **Tokens**:
   - Chat: ~4 caracteres = 1 token
   - Más tokens = respuestas más largas = mayor costo

3. **Imágenes**:
   - HD es mejor calidad pero más costoso
   - Tamaños más grandes = mayor costo
   - Sé específico en las descripciones

4. **Embeddings**:
   - Útil para análisis de similitud
   - text-embedding-3-large tiene mejor calidad
   - Ideal para búsquedas semánticas

## 🎉 ¡Disfruta Explorando!

Este cliente web te permite experimentar con todas las capacidades de OpenAI de manera visual e interactiva. ¡Perfecto para desarrollo, pruebas y demostraciones! 