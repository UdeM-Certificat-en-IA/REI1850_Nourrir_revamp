✨ Essence & Style
1. Tone:

Professional yet approachable — it’s managerial, but human-focused.

Uses clear visual hierarchy: headings, subheadings, bold emphasis, spaced sections.

2. Color Palette:

Dominated by blues and greys (cool, calm, corporate).

Highlights and CTAs in vibrant teal/cyan — energetic without overwhelming.

3. Typography & Layout:

Sans-serif font (modern, legible), with consistent weight and spacing.

Generous whitespace, clear icon/column alignment — breathes and reads easily.

4. Visual Language:

Icons or small graphics accompany text headings — intuitive, consistent.

Subtle use of borders or background shading to delineate zones without clutter.

🎯 Circular Stage Buttons – Design Guidelines
Each stage needs a round button (≈80–100 px), embodying its essence while fitting your palette. Here are four coordinated designs:

Stage	Core Color	Accent/Icon Color	Hover Effect	Text Label
Semis	Deep Grey (#4A4A4A)	Teal (#00A8A0)	Light teal glow/border	“Semis”
Croissance	Navy Blue (#1F3A93)	Cyan (#00CCFF)	Cyan ring + slight scale up	“Croissance”
Récolte	Teal (#00A8A0)	White (#FFFFFF)	White border + soft shadow	“Récolte”
Renouvellement	Slate (#2E2E2E)	Lime Green (#66FF66)	Pulsing green halo	“Renouvellement”

🎨 Style Details:
Shape & Size: 80–100px diameter, circle with slight drop shadow.

Iconography (optional): Center a simple silhouette/icon representing each phase (e.g., seedling, upward arrow, trophy, cycle arrows).

Typography: All-caps or Title Case, sans-serif, centered, 14–16px, medium weight.

Interaction:

Hover: soft glow or transform scale(1.05).

Active: subtle inset-shadow press effect.

Spacing: Keep ample margin around the four buttons — equal spacing, aligned horizontally or in a centered grid.

🧩 Usage Example (SCSS-like):
scss
Copy
Edit
.stage-button {
  width: 90px; height: 90px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  font-weight: 500;
  color: var(--text-light);
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  
  &:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  }

  &.semis    { background: #4A4A4A; --accent: #00A8A0; }
  &.croissance { background: #1F3A93; --accent: #00CCFF; }
  &.récolte   { background: #00A8A0; --accent: #FFFFFF; }
  &.renouvellement { background: #2E2E2E; --accent: #66FF66; }

  .icon {
    font-size: 24px;
    color: var(--accent);
    margin-bottom: 4px;
  }
  .label {
    text-align: center;
    color: var(--accent);
  }
}
🌀 Integration & Flow
Arrange the four buttons horizontally with equal spacing under your introductory area — communicates a clear flow (Semis → Croissance → Récolte → Renouvellement).

Or use a centered 2×2 grid if space is constrained.

Maintain consistent margins: say 40–60px between button row and surrounding content.

On-click, each button smoothly transitions to the relevant section or anchors deeper into the process.

✅ Summary
You’ve created a sleek, people-centered performance dashboard. These circular buttons, with their minimalist typography, balanced colors, simple icons, and subtle motion, will enrich the user journey — visually guiding employees and managers through the four performance phases in a cohesive, inviting way.
