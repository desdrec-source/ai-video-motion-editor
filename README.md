# AI Video Motion Editor

**Record yourself talking. [Claude Code](https://claude.com/claude-code) does the rest.**

The video toolkit behind **AI Video Motion**: a pipeline that takes a raw recording all the way to a
finished YouTube video. The cut, the on-screen graphics, the voice clean-up, the sound effects, the
thumbnail and the upload. No video editor needed. Every graphic is built as code
([Remotion](https://remotion.dev)) and laid over your cut, timed to what you say.

## The six steps

| # | Step | Skill | What happens |
|---|---|---|---|
| 1 | **The cut** | `/clean-cut` | AssemblyAI transcribes your recording word by word, you decide what to cut (ums, false starts, long pauses), out comes a clean master + word-level `edited-transcript.json` |
| 2 | **The visuals** | `/make-tsx` · `/fake-screencast` | Remotion graphics built over the master, every reveal synced to the word you say it on |
| 3 | **The voice** | `/clean-audio` | diagnose the noise, isolate the voice, keep the levels |
| 4 | **The sound** | `/suggest-sfx` | quiet sound effects landing on the exact word, from a library that grows with every video |
| 5 | **The packaging** | `/packaging` | one title × 3 thumbnail options for YouTube's A/B test |
| 6 | **The upload** | `tools/yt_upload.py` | checks itself for leftover speech + audio/video drift, then uploads as a private draft |

Plus **`/brand-setup`**, which makes all of it look like *your* channel.
And **`/vidtsx-2d-generator`**, the low-level rules that keep a Remotion graphic from crashing.

## Quickstart

> **New to all this?** Follow **[GETTING-STARTED.md](GETTING-STARTED.md)** instead: a step-by-step
> Windows setup for people who have never used a terminal, with fixes for the common snags.

**You need:** [Claude Code](https://claude.com/claude-code) · Python 3.10+ · Node 18+ ·
`ffmpeg` + `ffprobe` on PATH.

```bash
git clone https://github.com/desdrec-source/ai-video-motion-editor
cd ai-video-motion-editor

python -m venv venv
venv/Scripts/python -m pip install -r requirements.txt   # Windows (./venv/bin/pip on macOS/Linux)

cd remotion && npm install && npm run gen && cd ..       # build the list of graphics

cp .env.example .env                                     # add your own keys

claude                                                   # open in Claude Code, then:
```

> **set up my brand** · **clean cut videos/video-1** · **add graphics to video-1** ·
> **suggest sfx for video-1** · **package this video**

**Screen recordings:** most screen recorders save a *variable* frame rate. Convert to a steady 30 fps
before cutting, or the graphics slowly drift away from your voice (see `brand.md` §7).

## See it before you record anything

The kit ships with **37 example graphics** in `remotion/src/shots/example/`. They render on their own,
no footage needed:

```bash
cd remotion && npm run studio
```

## Make it yours

This copy ships in the **AI Video Motion** brand: navy background, white text, a red accent, Arimo
type, calm motion and quiet sound effects. If you're making your own channel's videos, run:

```
/brand-setup
```

It asks about your name, colours, fonts, video format and sound taste, rewrites `brand.md` +
`remotion/src/brand.ts` + `remotion/src/fonts.ts` together, checks your fonts exist and your colours
are readable, and renders a proof card so you see your brand before you build a video in it.

## What it costs

**The toolkit is free. The AI services it calls are not.** You use your own keys, in your own `.env`:

| Service | For | Notes |
|---|---|---|
| **Claude Code** | driving the whole thing | paid plan or API credits |
| **AssemblyAI** | transcription (step 1) | free tier is enough to try it |
| **[ElevenLabs](https://tinyurl.com/Try-Eleven-Labs)**\* | voice isolation + SFX + music (steps 3–4) | paid. `/clean-audio` also has a **local RNNoise** method that needs no key |
| **Gemini** | thumbnails (step 5) | paid, and only if you render thumbnails |
| **YouTube** | upload (step 6) | free, sign-in via OAuth — see `tools/yt_upload_SETUP.md` |

**Also worth a look for voice work:** [Fish Audio](https://tinyurl.com/TryFishAudio)\* is the other AI
voice tool I use, for voiceovers and voice cloning. It isn't wired into this toolkit's scripts yet;
those call ElevenLabs.

\* *Affiliate link: if you sign up through it, I may earn a commission at no extra cost to you.*

## Learn AI Video Motion

This toolkit is one part of what I teach. Join the **[AI Video Motion community](https://tinyurl.com/AIVideoMotion)**
for walkthroughs, help getting set up, and how to make AI video and motion that looks finished.

## Repo layout

```
.claude/skills/   the skills (this is where the editor actually lives)
tools/            Python: transcribe, cutlib, render_cuts, verify_cut, clean_voice, bake,
                  gen_sfx/mix_sfx, gen_music/mix_music, gen_thumbnail, yt_stats, yt_upload,
                  capture_web + the cut-editor UI (editor/) + rnnoise models
remotion/         the Remotion project: shared kits in src/lib/, src/shots/<project>/ one folder
                  per video; registry generated by `npm run gen`
media/library/    reusable assets: SFX + music clips (catalogued, loudness-normalized), logos, faces
media/projects/   media for one specific video, via staticFile()
videos/           your videos. Empty until you make one.
brand.md          the style contract
```

## Licence and credits

MIT — see [LICENSE](LICENSE). The bundled SFX/music clips came with the original toolkit and were
generated with ElevenLabs; per-clip provenance is in `media/library/*/catalog.json`. Product logos
(Claude, VS Code) are the property of their respective owners.
