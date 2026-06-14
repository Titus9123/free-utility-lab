# Goal 11 domain migration readiness

This runbook prepares Free Utility Lab for a future custom-domain cutover without changing the live GitHub Pages domain yet.

## Selected domain

- selected_custom_domain: `freeutilitylab.com`
- current_canonical_base: `https://titus9123.github.io/free-utility-lab/`
- target_canonical_base: `https://freeutilitylab.com/`
- current base path: `/free-utility-lab/`

Do not create CNAME in this readiness slice. The site must keep the current GitHub Pages canonicals, sitemap URLs, and `/free-utility-lab/` asset paths until the final cutover is explicitly approved.

## canonical rewrite plan

1. Rewrite every absolute canonical URL from `https://titus9123.github.io/free-utility-lab/` to `https://freeutilitylab.com/` while preserving the same slug.
2. Rewrite matching `og:url`, JSON-LD `url`, `mainEntityOfPage`, breadcrumb `item`, and WebSite `url` values in the same pass.
3. Keep relative/internal links valid; after cutover, root-relative asset paths may need a separate base-path review if GitHub Pages serves the custom domain at `/`.
4. Run the full local validation bundle before publishing the rewritten URLs.

## sitemap URL rewrite plan

1. Rewrite every `sitemap.xml` `<loc>` from the current GitHub Pages base to `https://freeutilitylab.com/`.
2. Keep the sitemap URL count equal to the local static HTML inventory.
3. Validate XML parsing, duplicate checks, and local HTML mapping before submitting the sitemap.
4. Submit `https://freeutilitylab.com/sitemap.xml` in Google Search Console only after DNS and hosting verification pass.

## redirect strategy

GitHub Pages does not provide repository-level custom 301 redirect rules for this static project. The safe strategy is:

- use GitHub Pages custom-domain cutover as the primary migration path;
- keep old GitHub Pages URLs available during transition as much as GitHub Pages allows;
- use custom-domain canonicals after cutover;
- add proxy/CDN redirects later only if hosting changes and explicit redirect support is available.

## GSC new property checklist

- Create and verify a new Search Console property for `freeutilitylab.com`.
- Submit the custom-domain sitemap after DNS, TLS, and GitHub Pages custom-domain verification are stable.
- Monitor indexed pages, duplicate/canonical decisions, crawl errors, and priority cluster impressions.
- Compare old GitHub Pages property signals with the new property during the transition window.

## GA4 continuity check

- Keep the current measurement bridge and event names unchanged during migration.
- Confirm `page_view`, `asset_view`, `cta_click`, `copy_result`, and `print_result` fire on the custom domain.
- Annotate the cutover date in analytics reporting so source/referral changes are understood.

## post-migration crawl validation

1. Run `python3 scripts/run_all_validations.py` after the rewrite.
2. Fetch the home page plus representative pages from budget, meal, moving, and AI tools clusters.
3. Confirm canonical, `og:url`, and JSON-LD URLs use `https://freeutilitylab.com/` and no longer mix GitHub Pages absolute URLs.
4. Confirm `sitemap.xml` contains the custom domain and the same URL count as the local HTML inventory.
5. Submit the sitemap in the new GSC property and monitor crawl/indexing results.

## Current readiness validator

Run this before final cutover:

```bash
python3 scripts/validate_domain_migration.py
```

It verifies the selected custom domain, current and target canonical bases, sitemap/HTML inventory parity, required migration checklist sections, and that this readiness slice has not accidentally performed the cutover.
