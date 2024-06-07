# README

## Generar un archivo de configuración para scrapeo

Este README explica cómo generar un archivo de configuración para el servicio de scrapeo descrito en el código. Este servicio utiliza Playwright para la automatización del navegador y anticaptcha para resolver reCAPTCHA.

### Requisitos previos

- Python 3.8 o superior
- Playwright
- anticaptchaofficial
- pdfplumber
- dotenv

### Importante!
Configurar las variables de entorno en un archivo `.env`:
    ```
    KEY_ANTICAPTCHA=tu_clave_de_anticaptcha
    ```

### Generar un archivo de configuración

El archivo de configuración es un JSON que define cómo debe ejecutarse el proceso de scrapeo. A continuación se describe un ejemplo de configuración y los parámetros que se utilizan.

#### Ejemplo de archivo de configuración (EDEMSA)

```json
{
  "company_name": "edemsa",
  "service_type": "luz",
  "scrapping_type": "pdf",
  "schedule": {
    "scheduling_type": "mensual",
    "day_of_month": "8",
    "start_time": "01:00",
    "end_time": "00:00"
  },
  "scrapping_config": {
    "url": "https://oficinavirtual.edemsa.com/login.php",
    "captcha": true,
    "captcha_sequence": [
      {
        "element_type": "input",
        "component_type": "id",
        "query": false,
        "content": "nic"
      },
      {
        "content": "//*[@id=\"consultaFacturas\"]/div[2]/div"
      },
      {
        "captcha_button_content": "//*[@id=\"consultaFacturas\"]/div[3]/button"
      }
    ],
    "sequence": [
      {
        "query": false,
        "content": "tfacturasImpagas",
        "element_type": "div",
        "component_type": "id",
        "debt": true,
        "no_debt_text": "No existen facturas adeudadas para el nic seleccionado."
      },
      {
        "query": false,
        "content": "pagas-tab",
        "element_type": "button",
        "component_type": "id"
      },
      {
        "query": false,
        "content": "tfactura",
        "element_type": "div",
        "component_type": "id"
      },
      {
        "query": false,
        "content": "fact_pagas_fuera_oficina",
        "element_type": "buttons",
        "component_type": "id"
      }
    ]
  }
}
```

### Parámetros del archivo de configuración

#### 1. Información general

- `company_name`: Nombre de la compañía (e.g., "edemsa").
- `service_type`: Tipo de servicio (e.g., "luz"). 
    - Existen 5 tipos de servicios:
        - "internet"
        - "agua"
        - "luz"
        - "gas"
        - "otro"

- `scrapping_type`: Tipo de contenido a scrapear (e.g., "pdf").
    - Existen 2 tipos de contenido:
        - "pdf": es para scrapeo de facturas en formato PDF.
        - "web": es para scrapeo de información en páginas web.

#### 2. Programación

- `schedule`: Define la programación del scrapeo.
  - `scheduling_type`: Tipo de programación (e.g., "mensual").
  - `day_of_month`: Día del mes para ejecutar el scrapeo (e.g., "8").
  - `start_time`: Hora de inicio (e.g., "01:00").
  - `end_time`: Hora de finalización (e.g., "00:00").

#### 3. Configuración de scrapeo

- `scrapping_config`: Configuración específica del proceso de scrapeo paso por paso. En esta debera replicar los pasos que se realizan manualmente para obtener la información deseada.

  - `url`: URL de la página a scrapear.
  - `captcha`: Indica si hay un CAPTCHA en la página (true/false).
  - `captcha_sequence`: Secuencia para resolver el CAPTCHA.
    - `element_type`: Tipo de elemento (e.g., "input").
    - `component_type`: Tipo de componente (e.g., "id").
    - `query`: Si es necesario hacer una consulta (true/false).
    - `content`: Selector del contenido del elemento.
    - `captcha_button_content`: Selector del botón para resolver el CAPTCHA.

  - `sequence`: Secuencia de acciones para navegar y extraer la información.
    - `element_type`: Tipo de elemento (e.g., "div", "button").
    - `component_type`: Tipo de componente (e.g., "id").
    - `query`: Si es necesario hacer una consulta (true/false).
    - `content`: Selector del contenido del elemento.
    - `debt`: Indica si se busca información de deuda (true/false).
    - `no_debt_text`: Texto que indica que no hay deuda.

### Notas adicionales

- Asegúrate de que los selectores en el archivo de configuración sean precisos y válidos para la página web objetivo.
- Si la página web cambia su estructura, es posible que necesites actualizar el archivo de configuración.
- Maneja con cuidado las credenciales y claves API, especialmente en archivos de configuración y entorno.

---