# Instrucciones para agentes

Plantilla de Neural Codex para el repo de una empresa. Completá la sección
«Este repo». Las secciones «Fijo» se conservan en cada sincronización.

La regla de gates que acompaña a este archivo es
`.cursor/rules/nc-quality-gates.mdc`. El contrato largo sigue en el repo fuente:
https://github.com/brolag/neural-codex

Si un valor sigue entre `<COMPLETAR: …>`, preguntá. No lo inventes.

## Este repo

- Stack: `<COMPLETAR: lenguaje, framework, servicios>`
- Tests: `<COMPLETAR: comando>`
- Lint y tipos: `<COMPLETAR: comando, o "no hay">`
- Entornos: `<COMPLETAR: nombres de local, staging y prod, y cómo se distingue cada uno>`
- No tocar: `<COMPLETAR: rutas, módulos, integraciones o datos fuera de alcance>`

Esos comandos son los que sirven de evidencia. Si el hueco sigue vacío, no hay
suite que correr.

## Fijo — rama y pull request

- Trabajá siempre en una rama nueva y abrí el pull request en draft.
- Nunca hagas push a `main` ni a la rama por defecto si tiene otro nombre.
- Nunca mergees el pull request.
- El plan (decisiones cerradas, criterios de aceptación y cómo verificarlos) va commiteado en la rama o escrito en el cuerpo del pull request.
- No dejes el plan solo en una carpeta ignorada por git. En el repo fuente, `plans/` está en `.gitignore`; eso no alcanza como evidencia revisable.

## Fijo — hace falta un OK explícito del humano

Sin un OK explícito del humano para este cambio, no hagas:

- migraciones de schema;
- cambios de datos;
- nada con secretos: leerlos, escribirlos, commitearlos o pegarlos en el PR, en logs o en el chat (incluye `.env`);
- deploys a producción.

## Fijo — evidencia y aprobación

- Cada criterio de aceptación lleva su propia evidencia (comando, salida, o lo observado en el flujo).
- Lo que no se corrió cuenta como `FAIL`. No lo marques `PASS` ni lo dejes en blanco.
- Quien escribe el cambio no se aprueba a sí mismo. El veredicto lo da otra persona o una sesión de revisión que no arrastra la narrativa del autor.
- Antes de dar el cambio por hecho, aplicá `.cursor/rules/nc-quality-gates.mdc`: seguridad (CWE y, si aplica, ASVS 5.0.0), simplicidad (ISO/IEC 25010:2023 como referencia) y usabilidad (ISO 9241-11:2018; WCAG 2.2 A/AA en superficies web tocadas).
- Un gate que no aplica queda `N/A` con motivo. No bajes un criterio después de un fallo.
