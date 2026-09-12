---
name: remotion
description: >
  Remotion programmatic video rendering: composition catalog, prop schemas,
  render CLI invocation, and output verification for short-form video assets.
---

# Skill: Remotion Programmatic Rendering

Guidelines for rendering short-form video assets using Remotion's programmatic API. Covers composition catalog, prop schemas, render CLI invocation, and output verification.

## Composition catalog

Each social template ships as a named Remotion composition. Compositions live in `src/compositions/` of the workspace's Remotion project. At render time, the agent selects the composition ID and passes typed props.

| Template ID | Composition ID | Description | Typical duration |
|-------------|---------------|-------------|-----------------|
| `documentary` | `Documentary` | Slow Ken Burns pans over photography + voiceover | 45–90 s |
| `explainer` | `Explainer` | Kinetic typography over background, claim by claim | 30–60 s |
| `list` | `List` | Numbered card stack with fast cuts | 15–30 s |
| `story` | `Story` | Single-narrative arc with music bed + b-roll | 30–60 s |

## Prop schema

Each composition accepts a typed prop object. Validate props against the schema before calling the render CLI.

### Common props (all compositions)
```typescript
{
  "recordId": string,          // knowledge record ID
  "lang": string,              // BCP-47 language tag
  "voiceover": string,         // path to .mp3 file
  "script": ScriptLine[],      // [{start: number, end: number, text: string}]
  "brand": {
    "primaryColor": string,    // hex
    "backgroundColor": string, // hex
    "headingFont": string,
    "bodyFont": string
  }
}
```

### Documentary-specific props
```typescript
{
  "photos": PhotoAsset[],  // [{path: string, alt: string, duration: number}]
  "panDirection": "left-right" | "right-left" | "zoom-in" | "zoom-out"
}
```

### Explainer-specific props
```typescript
{
  "claims": string[],          // one claim per scene
  "backgroundImage": string,   // path to background asset
  "accentColor": string        // hex for animated underline
}
```

### List-specific props
```typescript
{
  "items": string[],           // list items (max 7)
  "numbering": boolean
}
```

### Story-specific props
```typescript
{
  "broll": VideoClip[],        // [{path: string, startSec: number, durationSec: number}]
  "musicTrack": string         // path to background music .mp3
}
```

## Render CLI invocation

```bash
npx remotion render \
  src/index.ts \
  [CompositionId] \
  [output-path].mp4 \
  --props='[props-json]' \
  --codec=h264 \
  --quality=85 \
  --scale=1
```

For batches: build props JSON to a temp file and pass via `--props-file` to avoid shell escaping issues:
```bash
echo '[props-json]' > /tmp/props-[record-slug].json
npx remotion render src/index.ts [CompositionId] output.mp4 --props-file=/tmp/props-[record-slug].json
```

## Thumbnail extraction

Extract a representative frame at 3 seconds:
```bash
ffmpeg -i output.mp4 -ss 3 -frames:v 1 thumbnail.png
```

## Output verification

After render:
```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,duration,bit_rate \
  -of json output.mp4
```

Expected: `width` = 1080, `height` = 1920 (vertical/Reels), duration within ±2 s of planned duration.

If render fails:
1. Check `stderr` for missing asset paths — resolve and retry.
2. Check for prop schema validation errors — fix the props object.
3. Log the error to `pack-batch-summary.md` and continue with remaining packs; queue failed pack for retry.

## Environment setup

```bash
cd [workspace]/remotion-project
npm install
# Verify compositions are registered:
npx remotion compositions src/index.ts
```
