# Brand — AI Video Motion

> Style contract for every video this repo produces. Every step-2+ skill (TSX overlays,
> full-screen animations, diagrams, SFX) reads this file so all videos feel like one channel.
> **Keep it in sync with `remotion/src/brand.ts` + `remotion/src/fonts.ts`** (the same tokens, as
> code). `/brand-setup` owns all three.
> A calm, premium, practical **dark-base** look: navy background, white text, one red accent.

## 1. Identity & voice

- **Channel:** **AI Video Motion** — AI video and motion that looks finished, for creators, editors
  and one-person businesses.
- **Positioning:** calm, premium, practical. Finished-looking work, shown plainly. Dark navy canvas,
  generous space, one confident red accent.
- **Voice:** practical, direct, **no hype**. Show the result and how it was made; no superlatives,
  no "game-changer" filler. On-screen text deliberately **avoids em-dashes** — keep that in overlays too.
- **Energy for video:** quiet and finished, never loud. Motion is subtle: no big zooms, no bouncy
  movement. (No hard offset shadows, thick black borders, or sticker-pop looks.)
- **Not this channel:** The Content Revenue Lab (a separate free community) and its
  "content marketing for creators over 40" line. Never put either on an AI Video Motion video.

## 2. Logo / wordmark

- **Wordmark:** **AI · Video · Motion** — three parts, **"Video" in the red accent**, the rest in
  white, Arimo bold, tight tracking, **with word spaces** (reads "AI Video Motion", never
  "AIVideoMotion"). Set in `BRAND.wordmark` as `['AI ', 'Video', ' Motion']` — the spaces sit in
  the outer parts because shots join the three parts with no gap.
- **End-card sign-off:** "See you in the next one" — **no emoji**. Set in `BRAND.signoff`.
- No standalone logo mark is required (a favicon is enough). Use the wordmark as the lockup.
- Drop any portrait / brand-bumper assets you want to reuse under `media/library/` (e.g. a `logos/`
  or `faces/` entry) and reference them from shots via `staticFile('library/...')`.

## 3. Color palette (exact hex)

**Dark base.** The kit's role names are kept (`ink` = primary text, `paper` = full-screen bg); the
values are flipped for a dark brand.

| Role | Token | Hex | Use in video |
|---|---|---|---|
| **Primary accent** | `accent` (red) | `#E63946` | key words, the wordmark's "Video", active state, CTAs, fills |
| Secondary accent | `accent2` (soft steel blue) | `#8FA3D1` | quiet secondary emphasis; never competes with the red |
| Success / positive | `signal` (teal) | `#4DB8A8` | "done", "free", checkmarks |
| Success alt | `signalAlt` | `#5CC9B5` | teal companion |
| Warn / attention | `warn` (soft yellow) | `#F5D76E` | attention, "watch this" |
| Danger / contrast | `danger` (amber) | `#F4A261` | errors, "the hard way" (amber, not pink, so it never clashes with the red) |
| Primary text | `ink` (white) | `#FFFFFF` | headlines and body text on navy |
| Secondary text | `muted` (light blue-grey) | `#AEB6C6` | captions, labels, small text on navy |
| Background | `paper` (navy) | `#141F3D` | every full-screen graphic |
| Cards / panels | `cream` (lighter navy) | `#1D2A4D` | panels sitting on the navy bg |
| Borders | `line` | `#2C3A63` | 1px borders on navy |

**Measured contrast (chroma-js):** white on navy **16.2:1** · `muted` on navy **8.0:1** · red on navy
**3.9:1** · white on red **4.2:1** · white on card navy 12.8:1+.

- **Red text is for LARGE words only (34px+) and fills.** At 3.9:1 it passes for big key words but is
  too tight for small text. Small text on navy is white or `muted`. Pills/chips may be red with
  white text (4.2:1). If small red text is ever needed, the lighter red `#EF5A65` (4.9:1) is the
  sanctioned fallback.
- **Off-brand-sheet greys:** the channel's print grey `#5B6475` is only 2.7:1 on navy, so it is **not**
  used on the navy bg. The light grey `#F3F4F6` is an **optional light panel** (navy text on it,
  14.8:1; `#5B6475` for small text on it, 5.4:1) for the odd shot that needs one. It is not the
  standard card colour, because the default text colour is white.

**Dark UI / terminal scale** (GitHub-ink — for terminal & code mockups):
`#0d1117` (bg) · `#161b22` (panel) · `#30363d` (border) · `#8b949e` (dim text) · `#c9d1d9` (text).

**Signature gradient:** red → soft rose → navy (`#E63946 → #F28B95 → #141F3D`). Used sparingly, for
thin dividers and slow background glows.

## 4. Typography (3-font system)

| Role | Font | Weights | Use |
|---|---|---|---|
| **Display / headlines** | **Arimo** | 500 / 600 / 700 | titles, big statements, section cards, the wordmark |
| **Body / UI** | **Arimo** | 400 / 500 / 600 | subtitles, labels, body text, lower-third detail |
| **Code / mono** | **JetBrains Mono** | 400 / 500 / 700 | terminal mockups, code, prompts, file paths |
| **Claude wordmark serif** | **Source Serif 4** (`FONT_EDITORIAL`) | 600 | "Claude …" wordmark clones only — not a brand font |

Arimo is metric-compatible with **Liberation Sans**, the channel's PDF font, so videos match the
PDFs. **Arimo ships 400–700 only — never request 800/900.** All load from `@remotion/google-fonts`
(see `remotion/src/fonts.ts`). Headlines tight tracking; body normal; mono only for literal code.

## 5. Shape & depth

- **Radius:** ~14px (cards/panels), pills fully rounded. Terminal/code windows: ~10px with a title bar.
- **Depth:** cards are a lighter navy (`cream`) with a 1px `line` border and a deeper soft shadow
  (`0 8px 32px rgba(0,0,0,.30)`) — light-base shadows vanish on navy.
- **Never:** hard offset shadows, thick borders, sticker/pop looks, **white cards with white text**.
- **Window chrome** (browser/terminal mockups): rounded panel, top bar with 3 traffic-light dots
  + a mono label; content on the dark ink scale.

## 6. Motion language  ← *calm, premium, practical*

Translated to video (Remotion, **30fps**):

- **Entrances:** fade + rise. `opacity 0→1` and `translateY ~16px→0` over ~8 frames (~0.27s),
  ease-out. **No overshoot, no bounce, no spring wobble.** `EASINGS.overshoot` is deliberately the
  same curve as `easeOut` in this brand.
- **Exits:** fade + fall ~6 frames.
- **Emphasis:** red underline/highlight wipe behind a key word over ~5 frames; scale pop **max 1.02**.
- **Stagger:** 2 frames between list items / lines.
- **Backgrounds:** navy with a very slow, faint red/rose glow + faint dotted grid, 10–20s loops.
- **Never:** big zooms, punch-ins, crash zooms, spins, elastic, flashes, stamps.
- **Hook beats are NOT hotter.** The opening ~10s follows the same calm rules as the body (the kit's
  default "hook-beat exception" with overshoot pops, punch-in + flash and a climax stamp is OFF).
  One readable event at a time, each synced to its narration word.
- **Step markers & punchlines:** a "step N" line may get the full-screen StepTitle card
  (`remotion/src/lib/step-title.tsx`). When a line turns personal, cut back to the presenter full
  screen — graphics never cover a punchline — with **no punch-in and no face gags**.

## 7. Video delivery specs

- **Main canvas:** **1920×1080, 30 fps (constant).** This is the kit's default composition size, so
  new shots get it automatically.
- **Vertical (Instagram Reels):** **1080×1920, 30 fps (constant).** Each shot declares its own size,
  so a vertical graphic is authored as its own shot (`width: 1080, height: 1920` in its
  `compositionConfig`); landscape shots are not auto-converted. Reels safe area: keep text out of the
  **top 250px** and **bottom 420px** (Reels UI + caption), and ≥ 60px from the sides.
- **Constant frame rate is mandatory.** Screen recorders (e.g. Panda) write **variable** frame rate
  (measured: ~29.2 fps average, frame gaps 28–139ms). Before any cut, convert the raw recording to a
  constant 30 fps master so graphics stay in sync with the voice:
  `ffmpeg -i raw.mp4 -vf fps=30 -fps_mode cfr -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k master_30fps.mp4`
  A mismatch doesn't error — it just drifts every shot off the narration.
- **Safe margins (landscape):** keep text ≥ 5% from edges (title-safe ~7.5%). Lower-thirds in the
  bottom ~12–18% band, left-aligned to the margin.
- **Overlays never cover the presenter.** Overlays live in the top/bottom bands, or become
  **full-screen cutaways** (a full-screen TSX beat on navy).
- **Overlay types:** lower-third (name/term), keyword callout, full-screen statement/section card,
  animated diagram, UI/terminal mockup (TSX-first).
- **Visual editing rules** (honored by `/make-tsx`): concept beats = full-screen cutaways; overlays only
  for small persistent CTAs/badges; visuals sync to narration and never pre-empt it; real UI / real pages
  for config and service facts.
- **Captions:** overlays only (not word-level captions) for long-form; vertical reels may carry
  word-level captions inside the safe area.

## 8. Asset & source locations

- Master (example): `videos/video-1/reference/<cut>.mp4` · edited transcript:
  `videos/video-1/work/edited-transcript.json` (word times in the master timeline).
- Reusable brand assets: `media/library/` (typed folders — `logos/ sfx/ music/ faces/` each with an
  index/catalog). Per-video generated assets: `media/projects/<video>/`, referenced from shots as
  `staticFile('projects/<video>/x')`.
- Brand tokens as code: `remotion/src/brand.ts` (keep it in sync with this file).


## 9. Locked decisions & still-open

- **Brand = AI Video Motion, dark base** — navy `#141F3D`, white text, red `#E63946` accent, Arimo. ✓
- **Red = large words and fills only** (3.9:1 on navy). ✓
- **Motion = calm & practical** — subtle fade-and-rise, no bounce, no big zooms, no hotter hook (§6). ✓
- **Delivery = 1920×1080 @ 30fps CFR**, plus **1080×1920 @ 30fps** vertical reels; VFR recordings are
  converted to constant 30fps before cutting (§7). ✓
- **SFX taste:** quiet accents under the voice, no loud or punchy effects. See §10. ✓
- **Still open:** the kit's 37 example shots were designed for a light base and some hard-code white
  panels; on this navy brand a few may render white-on-white. They are reference only — new shots
  are authored for navy.

## 10. Sound design — SFX

Same energy as the motion: **quiet accents under the voice, felt-not-heard.** No loud or punchy
effects. Reference feel is Linear / Anthropic / Vercel product sound, NOT MrBeast-loud. SFX are
seasoning on the edit, never the show. When in doubt, leave the moment silent.

**Choose every cue by its FUNCTION** (the pro-editor model — 3+1 foundational sounds do the heavy
lifting; thousands of files are a trap). Ask what the beat needs:

| Function | Sound | Its job | Our (calm) sub-types |
|---|---|---|---|
| **Motion** | whoosh | direction/speed; carry one shot into the next | `whoosh-soft` (quick cut), `whoosh-wind` (soft, gliding) |
| **Tension** | riser | "something is coming"; hold on the edge before a reveal | `riser-soft` (gentle; NO cymbal-urgency riser) |
| **Emphasis** | impact / pop | "this moment matters"; lands as the new shot appears | `impact-soft`, `impact-deep-soft` (reveal, long tail), `pop-reveal` (UI reveal) |
| **Snap** | click | small, satisfying, alive; a sequence of related shots each on a click | `ui-click-soft`, `ui-toggle-on`, `ui-send` |

Plus two brand-specific extras: `page-flip` (storybook) and `chime-reward` (the "free"/gift moment).

- **Taste — subtle premium accents.** Quiet, tasteful, always UNDER the voice. Silence is part of
  the mix; never wall-to-wall. Nothing ever pops louder than the voice.
- **Layer for the big moments (build-and-drop).** The magic is in stacking: **riser → impact** on a
  scripted reveal (e.g. "wait a few minutes … *boom*"), **whoosh → pop/impact** so a cut stands out.
  In the plan a layer is just two events at the same/adjacent `at_s` that sum. Reserve layering for at most
  one moment per video; keep everything else single and sparse.
- **Density — propose only what really matters.** Score the signature moment of a beat, not every
  sub-frame. A click-sequence (3–4 related shots each on a click) counts as ONE gesture. **There is no
  optional tier**: cues flagged `optional` tend to get cut wholesale at first listen. A cue you would
  flag as deniable is a cue you don't propose.
- **What does NOT earn a cue** (each of these tends to get proposed and then cut):
  · **clicks on decorative animation** — card cascades, chip runs, hover pops. A click-sequence earns
  its clicks only when the narration ENUMERATES the items and each click lands on the word (the kept
  tile/row runs); a purely visual run gets silence.
  · **whooshes on secondary cutaways** — whoosh the cuts that change the argument (step titles, a
  scene the narration pivots into), never every mid-beat panel, scrub, or B-roll arrival.
  · **ambient texture under speech** — soft typing, pencil scribbles, shimmers, draw-along winds. The
  static/glitch rule generalizes: ALL decorative texture, not just noisy texture.
  · **a second sound inside one gesture** — the extra pop after a whoosh, a riser on a minor reveal.
  Layering stays reserved for the one hero moment.
- **Sync — to the VISUAL beat, and often the exact word.** A click on the toggle flip; a pop on the
  reveal; a whoosh on the cutaway; the impact on the drop word. Time off the shot's animation frames
  AND `edited-transcript.json` word times.
- **Levels.** Library clips are loudness-normalized to **~−20 LUFS** with a −1.5 dBFS peak ceiling, so a
  plan's per-cue `gain_db` is perceptually meaningful. The voice is ~−17 LUFS, so gain sets how far
  under it a cue sits: **payoffs ~−5/−6 · transitions ~−6/−8 · bed/texture ~−9/−11.** The SFX bus is
  **lightly ducked under the voice** (gentle sidechain, ~4 dB) in the audition mix; final
  polish/ducking/loudness is the final-mix step's job.
- **Signature motif.** Pick a recurring UI sound (the example uses a "Free Image Generator" toggle click
  — intro enable → later callback), the same `ui-toggle-on`, as a small sonic through-line.
- **Meme gags — OFF for this channel.** The kit's meme effects (fisheye snap + `meme-boom`, mime
  bump, crash zoom, SFX category `meme`) are not used: they are loud and punchy by design, and this
  brand has no loud cues. No cue ever has a positive `gain_db`.
- **Gentler levels than the kit default.** Sit cues further under the voice: payoffs ~−8 ·
  transitions ~−9/−10 · bed/texture ~−12. Layered build-and-drop moments: at most one per video.
- **What we deliberately do NOT do** (take the pro's *structure*, not the drama): cymbal-urgency risers,
  trailer-slam impacts, a whoosh on every movement, "funny" click+whoosh gags. **No static/glitch
  textures under narration** — glitch reads as NOISE over the voice at any gain; error/delete moments
  during speech get silence or one clean mechanical snap, never sustained static (save glitch textures
  for gaps where the voice is silent).
- **Source.** ElevenLabs **Sound Effects API** is primary (owned, consistent, reusable); curated
  royalty-free is the fallback. Every clip's `source` + `license` is recorded in the catalog.
- **Music.** No music bed in the SFX pass. Music (track selection + auto-ducking) is the final-mix step
  (`tools/gen_music.py` + `tools/mix_music.py`, drawing from `media/library/music/`).
- **Library is the durable asset.** Shared, cross-project at **`media/library/sfx/`** (`catalog.json` +
  `clips/`), seeded from `palette.json`, organized by function. It GROWS every video — reuse before
  generating (library-first). SFX that must live *inside* a Remotion shot go in `media/library/sfx/` via
  `staticFile()`.
