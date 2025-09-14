# 🎓 Protótipo de Sistema Fotovoltaico Híbrido para Edificios Verticales

[![Universidad del Istmo](https://img.shields.io/badge/Universidad-del%20Istmo-blue)](https://unis.edu.gt)
[![Programa](https://img.shields.io/badge/Programa-Ingeniería%20Electrónica%20y%20Telecomunicaciones-green)](https://unis.edu.gt)
[![Estado](https://img.shields.io/badge/Estado-En%20Desarrollo-yellow)](https://github.com/JavierCel)

## 📋 Descripción del Proyecto

Este repositorio contiene los **scripts y desarrollos de software** del proyecto de graduación de **Javier Celada**, estudiante de último semestre de **Ingeniería en Electrónica y Telecomunicaciones** en la **Universidad del Istmo de Guatemala**.

### 🎯 Objetivo

Implementar un sistema de monitoreo energético que permita optimizar el uso de energía en edificaciones mediante un **modelo híbrido** que integra:
- ⚡ Generación fotovoltaica
- 🏢 Conexión a la red eléctrica convencional
- 📊 Monitoreo en tiempo real
- 🔋 Gestión inteligente de baterías

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Red Electrica │    │   Medidor       │    │   ThingsBoard   │
│   Domiciliar    │───▶│   Bidireccional │───▶│   Cloud IoT    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
┌─────────────────┐    ┌─────────────────┐
│   Sistema de    │    │   ESP32 +       │
│   Baterías      │───▶│   VE.Direct     │
└─────────────────┘    └─────────────────┘
```

## 💻 Componentes de Software

### 🔌 Medidor Bidireccional (Tuya IoT)

**Archivo:** `tuya_energy_monitor.py`

Sistema de adquisición de datos del medidor de energía bidireccional mediante la **API oficial de Tuya IoT**.

#### Características principales:
- ✅ Conexión segura con servidor Tuya IoT
- 🔐 Autenticación automática con credenciales del proyecto
- 🎫 Gestión inteligente de tokens de acceso
- 🔄 Regeneración automática de tokens antes de expiración
- 📡 Consulta de propiedades y estados del dispositivo
- ⏱️ Monitoreo en tiempo real (lectura cada 2 segundos)
- 📋 Procesamiento de datos en formato JSON
- ☁️ Integración directa con ThingsBoard Cloud IoT

#### Dependencias:
```bash
pip install requests json datetime threading
```

### 🔋 Monitor de Baterías (ESP32 - VE.Direct)

**Archivo:** `esp32_battery_monitor.ino`

Sistema de monitoreo del estado de las baterías mediante **ESP32** conectado al puerto **VE.Direct**.

#### Características principales:
- 🔧 Configuración automática del puerto VE.Direct
- 📡 Comunicación serial estable con dispositivos de monitoreo
- 📊 Lecturas periódicas de parámetros de batería
- ⏱️ Monitoreo en tiempo real (lectura cada 2 segundos)
- 📋 Procesamiento y estructuración de datos en JSON
- ☁️ Transmisión automática a ThingsBoard Cloud IoT

#### Dependencias:
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <SoftwareSerial.h>
```

## 📊 Dashboard y Visualización

Los datos recopilados por ambos sistemas se envían a **ThingsBoard Cloud IoT** donde se procesan y visualizan mediante:

- 📈 Gráficos en tiempo real de producción y consumo energético
- 🔋 Estado de carga y salud de las baterías
- ⚡ Balance energético del sistema híbrido
- 📱 Alertas y notificaciones automáticas
- 📊 Reportes de eficiencia y ahorro energético

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- Arduino IDE 1.8 o superior
- Cuenta en Tuya IoT Platform
- Cuenta en ThingsBoard Cloud

### Configuración del Medidor Tuya
1. Clona el repositorio
2. Instala las dependencias de Python
3. Configura las credenciales de Tuya IoT en `config.py`
4. Ejecuta el script principal

### Configuración del ESP32
1. Abre el archivo `.ino` en Arduino IDE
2. Configura las credenciales WiFi y ThingsBoard
3. Selecciona la placa ESP32 correcta
4. Sube el código al microcontrolador

## 📈 Resultados Esperados

- **Eficiencia Energética:** Optimización del 15-25% en el consumo
- **Monitoreo:** Datos en tiempo real con latencia < 3 segundos
- **Disponibilidad:** Sistema operativo 24/7
- **Escalabilidad:** Adaptable a diferentes tamaños de edificación

## 🔬 Metodología de Investigación

- **Tipo:** Investigación aplicada con enfoque cuantitativo
- **Diseño:** Experimental con prototipo funcional
- **Variables:** Producción solar, consumo energético, estado de baterías
- **Métricas:** Eficiencia, ahorro económico, reducción de CO₂

## 📚 Documentación Adicional

- [Manual de Usuario](docs/user_manual.md)
- [Guía de Instalación](docs/installation_guide.md)
- [Documentación Técnica](docs/technical_specs.md)
- [Esquemas Eléctricos](docs/electrical_diagrams/)

## 👨‍💻 Autor

**Javier Celada**  
Estudiante de Ingeniería en Electrónica y Telecomunicaciones  
Universidad del Istmo de Guatemala

## 📫 Contacto

- 📧 **Email:** [vcelada@unis.edu.gt](mailto:vcelada@unis.edu.gt)
- 🐙 **GitHub:** [@JavierCel](https://github.com/JavierCel)
- 💼 **LinkedIn:** [Javier Celada](https://linkedin.com/in/javier-celada)

## 🙏 Agradecimientos

- Universidad del Istmo de Guatemala
- Facultad de Ingeniería
- Asesores del proyecto de graduación

---

⭐ **Si este proyecto te resulta útil, no olvides darle una estrella en GitHub**

*Último update: Septiembre 2025*
