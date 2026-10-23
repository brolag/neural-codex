# Export para Cursor

Este directorio es la versión para Cursor del material genérico de Neural Codex.
El plugin de Codex (`plugins/neural-codex/`, marketplace en
`.agents/plugins/marketplace.json`) sigue siendo la fuente de verdad. Acá no hay
otro skill root, otro `hooks.json`, ni un instalador que copie archivos al home.

Los archivos que viajan a cada empresa llevan prefijo `nc-`, salvo `AGENTS.md`,
que en destino ocupa el nombre que Cursor ya lee.

## Qué se copia en este lote

| En este repo | En el repo de la empresa |
|---|---|
| `cursor/rules/nc-quality-gates.mdc` | `.cursor/rules/nc-quality-gates.mdc` |
| `cursor/AGENTS.template.md` | `AGENTS.md` |

`nc-quality-gates.mdc` es una regla de proyecto de Cursor: Markdown con
frontmatter `description` y `alwaysApply: true`. Con `alwaysApply: true` la
regla entra en cada chat; `globs` no decide y por eso este archivo no lo trae.
La `description` queda para quien lee el archivo. Formato vigente:
https://cursor.com/docs/rules

La regla resume qué revisar (seguridad, simplicidad, usabilidad) y apunta al
contrato largo en este repo. Esos enlaces siguen válidos después de la copia,
porque el repo de la empresa no contiene las skills.

## Cómo sincronizar

Hacelo con un pull request. No hay script de copia.

1. En el repo de la empresa, creá una rama y un pull request en draft. Sin push a `main` y sin merge.
2. Copiá cada `cursor/rules/nc-*.mdc` a `.cursor/rules/`, conservando el nombre `nc-`.
3. Si la empresa no tiene `AGENTS.md`, copiá `cursor/AGENTS.template.md` a `AGENTS.md` y completá stack, tests, lint, entornos y qué no tocar.
4. Si ya existe `AGENTS.md`, integrá a mano las secciones marcadas «Fijo». No pises el stack ni los comandos locales, y no reescribas desde la empresa los archivos `nc-`: el cambio nace en este repo.
5. Dejá el diff en el PR para que una persona lo revise y lo mergee.

Actualizaciones posteriores repiten el mismo PR. Los archivos `nc-*` de la
empresa se reemplazan por la versión de este repo; lo específico de la empresa
vive en `AGENTS.md`, fuera de ese prefijo.

## Pendiente para lotes siguientes

Skills de Cursor, todavía sin exportar:

- `nc-spec`
- `nc-craft`
- `nc-exercise`
- `nc-discover`

Hooks: los handlers Python del plugin siguen en `plugins/neural-codex/hooks/`
(bloqueo de comandos destructivos, archivos sensibles, inyección obvia en
inputs ejecutables, aviso de credenciales en la salida, nota previa al
compactado). Instalar el plugin no los confía. Este lote no los traduce a
Cursor ni agrega un segundo manifiesto de hooks.

`$vet` tampoco entra en esta lista. Quien escribe no se aprueba a sí mismo; la
revisión independiente sigue definida en la skill de Codex y en la regla de
gates. Si más adelante hace falta un `nc-vet` para otra sesión, se decide en
ese lote.

Hoy `tests/test_plugin_structure.py` exige que los únicos `SKILL.md` del repo
sean los cinco de `plugins/neural-codex/skills/`. Un lote de skills que agregue
otro `SKILL.md` acá tiene que actualizar ese contrato a propósito, o guardar el
material de Cursor en un formato que no sea un segundo skill root de Codex.
