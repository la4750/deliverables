# K-SOFTWARE-ONE-THREE-ONE-RULE — one-three-one-rule: Example

- **Domain**: Software / General | **Type**: Pattern
- **Version scope**: 未标注（通识） | **Technology**: ROS
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-035（Agent Skill: one-three-one-rule）| **Extracted**: 2026-10-08

## 知识正文

User: "Give me a 1-3-1 for adding retry logic to our API client."

Agent:

**Problem:** API calls to external services fail intermittently under load and need graceful retry handling.

**Options:**

- **Option A: Exponential backoff with jitter in a shared utility.**
  Pros: Simple, well-understood pattern; single implementation shared across all callers.
  Cons: No circuit-breaking; callers still block during retries.

- **Option B: Retry library (tenacity) as a decorator on each endpoint call.**
  Pros: Configurable per-endpoint; built-in support for circuit breakers and rate limits.
  Cons: Adds a dependency; decorator pattern can obscure control flow.

- **Option C: Queue-based async retry with dead letter handling.**
  Pros: Non-blocking; failed calls are tracked and replayable; scales well.
  Cons: Significant complexity increase; requires a queue backend; overkill for low-volume services.

**Recommendation:** Option A. The call volume doesn't justify queue infrastructure, and a shared utility with exponential backoff + jitter covers the failure mode cleanly without new dependencies.

**Definition of Done:**
- `api_retry()` utility handles transient HTTP errors (429, 502, 503, 504).
- Retries up to 3 times with exponential backoff and jitter.
- All external API calls route through the retry utility.
- Logs each retry attempt with endpoint and attempt number.
- Tests cover retry exhaustion, immediate success, and transient-then-success scenarios.

**Implementation Plan:**
1. Create `utils/api_retry.py` with configurable max retries, base delay, and retryable status codes.
2. Add jitter using `random.uniform(0, base_delay)` to prevent thundering herd.
3. Wrap existing API calls in `api_client.py` with the retry utility.
4. Add unit tests mocking HTTP responses for each retry scenario.
5. Verify under load with a simple stress test against a flaky endpoint mock.

## Provenance

- source_skill_id: `SKILL-GEN-ONE-THREE-ONE-RULE`
- source_skill_path: `/home/ubuntu/.hermes/hermes-agent/optional-skills/communication/one-three-one-rule/SKILL.md`
- source_name: `one-three-one-rule`
- original_section: `Example`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
