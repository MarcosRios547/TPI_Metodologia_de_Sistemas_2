# Diagnóstico: Calidad, Deuda Técnica y Code Smells

- **Proyecto:** Sistema de gestión de solicitudes académicas estudiantiles (versión base procedural `sistema.py` en Python 3.10+ con persistencia en `datos.json` y exportación a `reporte.txt`).

---

## 1. Calidad Externa vs. Calidad Interna

### Calidad externa (lo que percibe el usuario)
- **Funcionamiento operativo:** Cumple con el flujo principal en consola (menú interactivo, registro de estudiantes, responsables y solicitudes, cambio de estado, asignación de responsable, búsqueda y generación de reporte).
- **Persistencia básica:** Mantiene los datos entre ejecuciones mediante `datos.json` y permite exportar un reporte de texto.

### Calidad interna (lo que condiciona el mantenimiento y la evolución)
- **Alta fragilidad y bajo acoplamiento sano:** Todo gira alrededor de un diccionario global mutable `d` y funciones sueltas con nombres opacos (`d`, `F`, `n`, `e`, `t`, `p`, `r`, `f`, `reg`, `reg_est`).
- **Duplicación y responsabilidades mezcladas:** Se repite lógica en búsquedas y reglas de estado, y se mezclan reglas de negocio con `print`, `input` y escritura/lectura de archivos (`open` sin `with`, `except:` vacío).
- **Difícil de probar y escalar:** El estado global, los retornos genéricos `'ERROR'`, la falta de validación en entradas (`int(input())` sin manejo de `ValueError`) y la generación de IDs (`len(d["s"]) + 1`) encarecen cualquier cambio futuro.

---

## 2. Deuda Técnica y Code Smells Detectados

1. **Nombres deficientes / opacos:** Variables y funciones crípticas (`d`, `F`, `reg`, `reg_est`, `n`, `e`, `t`, `p`, `r`, `f`) en todo el script que dificultan leer qué representa cada dato.
2. **Estado global mutable:** Uso del diccionario global `d` y `global d` en `cargar()`, generando efectos colaterales difíciles de rastrear o aislar en pruebas.
3. **Long Parameter List:** La función `reg` recibe 8 parámetros posicionales, aumentando el riesgo de errores por orden o tipo de argumento.
4. **Obsesión por primitivos y números mágicos:** Uso de enteros/códigos sueltos para tipo de solicitud, prioridad y estado en lugar de tipos o enumeraciones explícitas del dominio.
5. **Código duplicado:** Repetición de lógica en `buscar` (traducciones/ramas repetidas tres veces), validaciones y controles de estados finales (*resuelta* o *rechazada*).
6. **Long Method:** Funciones extensas y cargadas de ramas/responsabilidades (como `buscar`, `reporte` y `main`), difíciles de entender y modificar sin romper algo.
7. **Mezcla de responsabilidades / violación de SRP:** Reglas de negocio mezcladas con entrada/salida por consola (`print`/`input`) y manejo de archivos dentro de las mismas funciones.
8. **Persistencia rudimentaria y acoplada:** Acceso directo a `datos.json` y `reporte.txt` con `open` sin `with` y bloques `except:` vacíos que ocultan fallos reales.
9. **Retornos poco informativos y entradas sin validar:** Mensajes/retornos `'ERROR'` genéricos y conversiones directas como `int(input())` sin capturar `ValueError` en `main`.
10. **Generación de ID frágil:** Cálculo de identificadores basado en `len(d["s"]) + 1`, propenso a colisiones o inconsistencias ante borrados o cambios.
11. **Código muerto:** Presencia de elementos sin uso o comentados (como `viejo_exportar`, `calcular_demora` comentada e imports/comentarios residuales) que agregan ruido.