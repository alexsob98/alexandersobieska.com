# alexandersobieska.com

Static personal website. No framework, no database, no tracking.

## Update the site
1. Edit text in `build.py` (pages, talks, projects, bios) or add a paper to `src/publications.bib`
   (give it a `theme` field: feed, neuroethics, radicalization or llm-medethics).
2. Run `python3 build.py` — it rewrites everything in `docs/`.
3. Preview: `python3 -m http.server 8000 --directory docs`, open http://localhost:8000
4. Commit and push; GitHub Pages serves `docs/`.

Talks with a date in the future appear under "Upcoming" automatically; rebuild after the date passes.

## Notes
- Font: Schibsted Grotesk (SIL Open Font License, `docs/fonts/OFL.txt`), served from this site, not from Google.
- `docs/CNAME` holds the domain for GitHub Pages.
- `/legal/` is a DRAFT: fill in the postal address and check it before launch.
