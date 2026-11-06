# Triaje de las 37 pruebas que ya fallaban en `main` (6-nov-2026)

Las 37 fallan igual en `main` y en la rama `fix/remove-clarvix-gtm-container`; ninguna la introduce el PR de Analytics.
Entorno: `pytest` no venía instalado (se instaló con `pip`); no hay otros problemas de entorno.

| Grupo | Pruebas | Causa raíz | Tipo | Acción |
|---|---|---|---|---|
| Guardas previas a la migración de dominio | `test_domain_migration_goal11` (3), `test_final_launch_readiness_goal13` (3), `test_goal11_quality_gates::does_not_cutover_domain_or_enable_live_ads` | Exigen "no hay CNAME", "no hay anuncios", URLs `titus9123.github.io`. El sitio ya está en `freeutilitylab.com` con CNAME y AdSense (90 páginas con `adsbygoogle`) | **Obsoletas** | Retirar o invertir tras decidir el estado final del dominio |
| Prefijo de URL del sitio de proyecto (15 comprobadas por el texto del fallo; 2 por nombre de prueba) | `goal3` (3), `goal4` (3), `goal5` (3), `goal6` (3), `shared_modules_goal2`, `organic_sprint`, `goal11::support_pages`, `modern::budgetreset_loads_shared_budget_calc`, `modern::asset_lab_modern_css` | Esperan rutas `/free-utility-lab/…` y canónicos `github.io/free-utility-lab`; el sitio sirve desde la raíz del dominio propio | **Obsoletas** | Parametrizar el prefijo (`""`) y actualizar canónicos |
| Inventario del sitemap | `test_sitemap_validation::matches_local_html_inventory` | Cuenta 15 redirecciones `noindex` (refresh) como páginas que faltan en el sitemap; correctamente no están | **Obsoleta** (lógica del validador) | Excluir páginas `noindex`/`refresh` del inventario |
| Medición en aistackcost | `aistackcost_goal7::pages_load_ga4_before_relying_on_it` | Recorre también 7 redirecciones sin GA4 (innecesario). Las páginas indexables de aistackcost sí cargan `G-54GQ1ZT341` | **Obsoleta** | Saltar redirecciones |
| Funciones de aistackcost | `modern_improvements` (8: stack builder, overlap alert, ROI, budget max, namespace localStorage, URLs oficiales, precios con aviso, presets) + `goal7` (3: estructura de comparación, artefactos, schema) | Buscan elementos/ids (`aiToolGrid`, `aiOverlapAlert`, …) que **no existen** en ningún archivo actual | **Decisión de producto**: o las funciones se retiraron en la reescritura de contenido (pruebas obsoletas) o se perdieron (regresión) | Revisar con el propietario; no se tocó |

## Defecto real encontrado (relacionado con medición) y corregido aparte
4 páginas indexables de `movebudget/` no tenían ninguna etiqueta GA4: `moving-cost-checklist`, `moving-box-calculator`,
`free-printable-first-apartment-budget-worksheet`, `moving-cost-calculator-no-email`. Corregido en un PR independiente.

## Sin hallazgos de seguridad ni de publicación
No hay secretos ni referencias a `G-P4R22F19B8`/`GTM-KQ8MQBNQ` en el repositorio tras este PR.
