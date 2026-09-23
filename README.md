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
