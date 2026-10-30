// Video brand tokens (see /brand.md). Import these in every shot
// so all videos stay consistent; change a value here and every shot updates.
//
// AI Video Motion: a calm, premium, DARK-base look. Navy background, white text,
// red accent. Written by `/brand-setup`; keep this file, /brand.md and fonts.ts in sync.
import { Easing } from 'remotion';

// Channel identity. Any shot that puts your name on screen reads it from here,
// so one edit re-brands every video you have ever made in this repo.
export const BRAND = {
  // The wordmark, split in three so the MIDDLE part renders in the accent color.
  // "AI Video Motion" renders the word "Video" in red. The spaces live in the outer parts
  // because the shots join the three parts with no gap.
  wordmark: ['AI ', 'Video', ' Motion'] as readonly string[],
  signoff: 'See you in the next one',
} as const;

// NOTE on the dark base: the role NAMES are the kit's (ink = primary text, paper = full-screen bg),
// the VALUES are flipped for a dark brand. ink is white, paper is navy.
export const COLORS = {
  // roles
  accent: '#E63946', // red — primary. 3.9:1 on navy: LARGE words (34px+) and fills only, never small text
  accent2: '#8FA3D1', // soft steel blue — secondary
  signal: '#4DB8A8', // teal — success / "free"
  signalAlt: '#5CC9B5', // teal companion
  warn: '#F5D76E', // soft yellow — attention
  danger: '#F4A261', // amber — error / contrast (not pink: it would clash with the red)
  ink: '#FFFFFF', // primary text (on navy)
  muted: '#AEB6C6', // secondary text / captions (8.0:1 on navy)
  paper: '#141F3D', // navy — full-screen bg
  cream: '#1D2A4D', // lighter navy — cards / panels on the bg
  line: '#2C3A63', // 1px borders on navy
  // dark UI / terminal scale (GitHub-ink)
  d900: '#0d1117',
  d800: '#161b22',
  d600: '#30363d',
  d400: '#8b949e',
  d300: '#c9d1d9',
} as const;

// signature gradient: red -> soft rose -> navy
export const GRADIENT = `linear-gradient(120deg, ${COLORS.accent}, #F28B95, ${COLORS.paper})`;

export const RADIUS = { card: 16, panel: 14, window: 10, pill: 999 } as const;

// Deeper shadows: the soft light-base ones vanish on navy.
export const SHADOW = {
  soft: '0 8px 32px rgba(0,0,0,0.30)',
  card: '0 10px 40px rgba(0,0,0,0.28)',
} as const;

// Calm, practical easings. Use these — never Easing.out(...) wrappers.
export const EASINGS = {
  easeOut: Easing.bezier(0.33, 1, 0.68, 1),
  easeIn: Easing.bezier(0.32, 0, 0.67, 0),
  easeInOut: Easing.bezier(0.37, 0, 0.63, 1),
  overshoot: Easing.bezier(0.33, 1, 0.68, 1), // kept for compatibility; NO overshoot in this brand
} as const;
