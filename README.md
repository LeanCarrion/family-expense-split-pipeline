# Family Expense Split Pipeline

## Descripción del Proyecto
Este proyecto resuelve una problemática común en la gestión de finanzas familiares: la centralización de resúmenes de tarjetas de crédito con extensiones adicionales y gastos cruzados. El objetivo principal es automatizar la ingesta de resúmenes bancarios mensuales, realizar el cálculo preciso de los saldos correspondientes a cada miembro de la familia (adicionales y consumos especiales) y optimizar el proceso de notificación final.

El sistema procesa los extractos financieros crudos, extrae los consolidados netos de manera segura y genera reportes individuales listos para ser despachados a cada destinatario, asegurando transparencia, orden y velocidad en la rendición de cuentas del mes.

## Características Principales
* **Ingesta Inteligente de Datos:** Lectura automática de resúmenes bancarios mensuales en formatos estándar desestructurados.
* **Procesamiento y Limpieza de Saldos:** Aislamiento de consumos directos por tarjeta, ignorando de forma segura cargos transitorios o impositivos no correspondientes según la estrategia mensual.
* **Reportes Consolidados:** Generación de resúmenes de deuda individuales detallando el concepto exacto y las monedas correspondientes (Pesos/Dólares).
* **Módulo de Notificación:** Preparación de estructuras de mensajes legibles y directos para canales de mensajería instantánea.

## Estructura del Repositorio
* `pipeline.py`: Script principal encargado del análisis, procesamiento y cálculo del resumen.
* `template_resumen.csv`: Archivo de muestra con datos ficticios para probar el funcionamiento del flujo sin exponer información privada.
* `.gitignore`: Configuración de seguridad para garantizar el aislamiento absoluto de los datos reales del usuario.

## Requisitos de Entrada
Para utilizar este pipeline de manera local, el archivo de entrada debe conservar la estructura por filas emitida en el extracto del home banking, incluyendo las secciones de identificación de tarjetas adicionales y sus montos netos asociados.
