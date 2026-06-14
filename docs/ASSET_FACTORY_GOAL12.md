# Goal 12 ongoing asset factory

Goal 12 turns new asset creation into a repeatable workflow, not a round of manual page cloning. Use this checklist before creating or publishing any new Free Utility Lab asset.

## Repeatable workflow

1. **Plan the asset manifest first**
   - Copy `templates/new_asset_manifest.template.json` to a working manifest outside tracked production data or to a reviewed feature file.
   - Fill every required field before writing HTML: id, slug, category, page type, outputs, schema, tracking and related tools.
   - do not clone existing pages manually; use the manifest and existing shared modules as the contract.

2. **Add the catalog entry**
   - Update `data/marketplace.json` with a complete catalog entry.
   - Keep `public_url` on the current canonical base until an approved domain cutover.
   - Use the same id/slug/tracking_asset_id values from the manifest.

3. **Create the main product page**
   - Create the main product page at the catalog `local_path`.
   - Include canonical metadata, shared styles/scripts, accessible headings and a practical no-signup user flow.

4. **Confirm category hub inclusion**
   - Re-render or update the relevant marketplace/category hub so the new asset appears in its category.
   - Keep `/free-utility-lab/` base-path links intact.

5. **Ship a real tool/template/checklist/calculator**
   - Every new asset must include at least one real tool/template/checklist/calculator, worksheet, planner, guide or comparison page.
   - Avoid placeholder-only pages.

6. **Add copy/print/export outputs**
   - Include useful copy, print, download, CSV, PDF or checklist output actions as appropriate.
   - Prefer existing shared action helpers instead of bespoke one-off JavaScript.

7. **Add schema**
   - Include JSON-LD schema appropriate to the page, usually BreadcrumbList plus SoftwareApplication, FAQPage, HowTo or ItemList.
   - Keep schema URLs aligned with canonical URLs.

8. **Add tracking**
   - Use the standardized measurement events from Goal 10.
   - Do not forward private user inputs or secret-like fields.

9. **Add internal links**
   - Link to the category hub, all-tools hub and relevant related tools.
   - Avoid orphan pages and thin support pages.

10. **Run validation pass**
    - Validate the proposed manifest:
      ```bash
      python3 scripts/validate_new_asset.py path/to/new_asset.json
      ```
    - Run the full bundle:
      ```bash
      python3 scripts/run_all_validations.py
      ```

11. **Verify no secrets**
    - Keep manifests, docs, scripts and generated pages credential-free.
    - Use placeholders only for public labels, never credentials.

12. **Reject thin support pages**
    - Do not publish support pages that are only SEO text.
    - Each supporting page needs real utility content, schema where relevant, and internal links.

## Machine-checkable contract

The Goal 12 checklist lives in `data/asset_factory_checklist.json` and is validated by `scripts/validate_asset_factory.py`.

A proposed new asset manifest is validated by `scripts/validate_new_asset.py`. The manifest must cover:

- catalog entry;
- main product page;
- category hub inclusion;
- at least one real tool/template/checklist/calculator;
- copy/print/export outputs;
- schema;
- tracking;
- internal links;
- validation pass;
- no secrets;
- no thin support pages.
