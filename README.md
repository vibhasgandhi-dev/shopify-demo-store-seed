# Shopify demo store seeder

Seeds a development store with a realistic catalogue (17 coffee-gear products, 43 variants, 4 smart collections, real photos) using the Admin GraphQL API, in one run. Used to build the demo store behind my Shopify Function and checkout-extension demos.

What it shows:
- `productSet` (synchronous) with options, variants, prices, compare-at, SKUs, tracked inventory at a location, and images pulled straight from URLs.
- Smart collections (`collectionCreate` with tag rules) created before products so products fall into place.
- `publishablePublish` to the Online Store and Shop channels.
- Idempotent collection creation; products keyed by handle.

## Run

Start `shopify app dev` for any app installed on the store with `write_products, write_publications, write_inventory, write_files` scopes. The CLI prints a local GraphiQL proxy URL with a key; the script POSTs to that proxy so no access token is handled by hand.

```bash
export GRAPHIQL_KEY=...            # from the shopify app dev output
export LOCATION_ID=gid://shopify/Location/...
export PUBLICATION_ONLINE=gid://shopify/Publication/...
python3 seed.py                    # all products
python3 seed.py ceramic-pour-over-dripper   # one product
```

Look up `LOCATION_ID` and `PUBLICATION_ONLINE` with:

```graphql
{ locations(first: 3) { nodes { id name } } publications(first: 5) { nodes { id name } } }
```

Photos are Unsplash images referenced by URL (`unsplash-candidates.json` holds the shortlist per category). Swap in your own catalogue by editing the `P` list in `seed.py`.

Vibhas Gandhi

## Making the grid look right

Two things matter more than the photos themselves:
- Every image is requested as a **4:5 centre crop** (`fit=crop&w=1600&h=2000`), so cards line up.
- The theme's product-card `image_ratio` is set to `portrait` instead of `adapt` (`shopify theme pull/push` on `templates/collection.json` and `templates/index.json`; the Admin API's `themeFilesUpsert` needs a Shopify exemption, the CLI does not).

## Theme overrides (Horizon)

`theme-overrides/` holds the three JSON files pushed to the live Horizon theme with `shopify theme push --only …`:
- `templates/index.json`: hero uses an uploaded Shopify Files image (`shopify://shop_images/…`), h1 heading, CTA to the Brewers collection, large height.
- `templates/collection.json`: product cards at `image_ratio: portrait`.
- `sections/header-group.json`: announcement bar advertising the spend-and-save tiers that the discount Function applies.

Upload the hero photo first with `fileCreate` (Admin GraphQL, `contentType: IMAGE`, no custom filename when the source URL has no extension), then reference it by its stored filename.
