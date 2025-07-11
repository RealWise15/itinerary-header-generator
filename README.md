# 🛫 Travel Itinerary Header Generator

Aplicación web que permite generar itinerarios de vuelo en formato PDF de manera profesional y personalizada.  
Ideal para agencias de viaje que necesiten emitir documentos con membretes, logos y textos legales ajustados a cada plataforma.

---

## 🎯 Funcionalidades principales

- 📤 Carga de un archivo PDF base con información del itinerario
- 🖼️ Selección de aerolínea y plataforma (Agencia, Despegar, Almundo, etc.)
- 🧾 Inserción automática de:
  - Membrete (imagen superior)
  - Logo de aerolínea
  - Texto legal personalizado
  - Imagen de pie de página
- 💻 Interfaz web intuitiva y responsiva
- 📥 Descarga del PDF final generado con la nueva estética

---

## ⚙️ Tecnologías utilizadas

| Capa         | Herramienta / Lenguaje |
|--------------|-------------------------|
| Backend      | Python + Flask          |
| PDF Engine   | ReportLab + PyPDF2      |
| Frontend     | HTML5 + CSS3 + JavaScript |
| Renderizado  | Jinja2 Templates        |

---

## 🧪 Cómo ejecutarlo localmente

1. Clonar este repositorio:

```bash
git clone https://github.com/RealWise15/itinerary-header-generator.git
cd itinerary-header-generator
