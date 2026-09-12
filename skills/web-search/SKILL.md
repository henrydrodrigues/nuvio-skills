# Skill: Web Search & Image Sourcing

Guidelines for searching the web for real-world photography and imagery, filtering by license, and resolving ambiguous entity references. Covers query construction, candidate selection, license filtering, and fallback to AI generation.

## When to use web search vs. AI generation

| Entity type | Route | Reason |
|-------------|-------|--------|
| Real person (public figure) | Web search first | Authentic likeness; AI generation may produce inaccurate representation |
| Named place or landmark | Web search first | Actual photography preferred; AI often distorts architecture |
| Named organization / logo | Web search first | Brand guidelines require authentic assets |
| Abstract concept | AI generation | No real-world photograph exists or is appropriate |
| Niche entity with no licensable results | AI generation fallback | Web search returned no candidates passing license filter |

## Query construction

1. Start with the entity's canonical name: `"SpaceX Starship"`
2. Add a disambiguator when the name is ambiguous: `"SpaceX Starship rocket launch"`
3. Add license qualifier: append `site:commons.wikimedia.org` for CC-licensed results, or use the search API's license filter parameter.
4. Add resolution qualifier: `high resolution` or `4k` when the search API supports it.

Example queries:
- `"Artemis Program NASA Moon" site:commons.wikimedia.org`
- `"Elon Musk portrait" license:cc`
- `"Mars surface" high resolution`

## Candidate selection

From a result set, select the image that:
1. Passes the license filter (Creative Commons Attribution or CC0; reject All Rights Reserved).
2. Has the highest resolution (minimum 1080 × 1080 px for social assets).
3. Most directly depicts the target entity (prefer close shots over crowd shots for persons; prefer the landmark over a skyline for places).
4. Has the most recent publication date when recency matters (e.g., current CEO headshots).

If two candidates are equal, prefer the one from a more authoritative source (e.g., organization's own press kit, Wikipedia Commons).

## License filtering

Accepted licenses:
- `CC0` (public domain)
- `CC BY` (attribution)
- `CC BY-SA` (attribution, share-alike)
- `CC BY-ND` (attribution, no derivatives) — acceptable for unmodified use
- Operator-configured allowlist in workspace config

Rejected licenses:
- `All Rights Reserved`
- `CC BY-NC` (non-commercial restriction)
- `CC BY-NC-SA`
- `CC BY-NC-ND`
- Any license requiring payment

## Caching

After sourcing an image:
- Cache to `cache/web-photos/[entity-slug]_[license-code].[ext]`
- Record in `cache/web-photos/index.json`: `{"entity": "...", "license": "...", "source_url": "...", "cached_at": "...", "path": "..."}`
- On subsequent runs, check the cache index before making a new API call.

## Fallback to AI generation

If web search returns no candidates passing the license filter:
1. Log the miss: `"No licensable result for [entity]"` in the pack's asset sourcing log.
2. Construct an AI generation prompt: `[concept description] in the style of [workspace image_style], [mood], [palette anchors from _config/image-style.md]`.
3. Generate via the Image Generation connector.
4. Cache to `cache/ai-images/[prompt-hash].[ext]`.

Never silently fall back without logging the web search miss — the operator needs to know which assets are AI-generated vs. photographically sourced.

## Tool use declaration

```json
{
  "name": "web_search",
  "description": "Search the web for images of real-world entities, filtered by license and resolution. Use for: public figures, named places, organizations. Fall back to AI generation for abstract concepts or when no licensable result is found.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" },
      "license": { "type": "string", "enum": ["cc", "cc0", "any"] },
      "min_resolution": { "type": "string", "description": "e.g. '1080x1080'" }
    },
    "required": ["query"]
  }
}
```
