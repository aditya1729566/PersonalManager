# Frontend AGENTS.md

This file documents the current frontend code and components for contributors and agents.

Overview
- Next.js App Router project using `output: "export"` (static build).
- UI is a single-board Kanban app with drag & drop powered by `@dnd-kit`.
- Styling: TailwindCSS.

Key files
- `src/app/layout.tsx` — top-level layout and global fonts/styles. (AI sidebar removed temporarily.)
- `src/app/page.tsx` — main page that renders the Kanban board.
- `src/components/KanbanBoard.tsx` — main board component assembling columns and cards.
- `src/components/KanbanColumn.tsx` — column component, renders cards and add-card button.
- `src/components/KanbanCard.tsx` — individual card component.
- `src/components/KanbanCardPreview.tsx` — card preview used in drag/drop UI.
- `src/components/NewCardForm.tsx` — form to add a new card.
- `src/components/AiSidebar.tsx` — AI chat sidebar (present but not rendered by default).
- `src/lib/kanban.ts` — helper utilities for manipulating the kanban data structure.

Tests
- Unit tests: `src/lib/kanban.test.ts`, `components/KanbanBoard.test.tsx`.
- E2E: Playwright tests under `tests/`.

Notes for contributors
- To run dev: `cd frontend && npm run dev` (Next dev HMR).
- To build static export: `npm run build` then `npx next export`.
- The AI sidebar component exists at `src/components/AiSidebar.tsx` but is intentionally not rendered from `layout.tsx` for now.

Contact
- For plan and architecture decisions, see `docs/PLAN.md`.
