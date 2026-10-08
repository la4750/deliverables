# K-SOFTWARE-SHOPIFY — Storefront API (public read-only)

- **Domain**: Software / General | **Type**: API / Specification
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-007（Agent Skill: shopify）| **Extracted**: 2026-10-08

## 知识正文

Different endpoint, different token, used for customer-facing apps/hydrogen-style headless setups. Headers differ:

- **Endpoint:** `https://$SHOPIFY_STORE_DOMAIN/api/$SHOPIFY_API_VERSION/graphql.json`
- **Auth header (public):** `X-Shopify-Storefront-Access-Token: <public token>` — embeddable in browser
- **Auth header (private):** `Shopify-Storefront-Private-Token: <private token>` — server-only

```bash
curl -sS -X POST \
  "https://${SHOPIFY_STORE_DOMAIN}/api/${SHOPIFY_API_VERSION:-2026-01}/graphql.json" \
  -H "Content-Type: application/json" \
  -H "X-Shopify-Storefront-Access-Token: ${SHOPIFY_STOREFRONT_TOKEN}" \
  -d '{"query":"{ shop { name } products(first: 5) { edges { node { id title handle } } } }"}' | jq
```

## Provenance

- source_skill_id: `SKILL-GEN-SHOPIFY`
- source_skill_path: `/home/ubuntu/.hermes/hermes-agent/optional-skills/productivity/shopify/SKILL.md`
- source_name: `shopify`
- original_section: `Storefront API (public read-only)`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
