---
name: explain-current-flow
description: Explain how an existing feature, behavior, integration, event flow, data flow, or user workflow works right now by checking OpenSpec specs first when present, then verifying the implementation. Use when the user asks questions like "how does X work?", "what happens when X occurs?", "where is X handled?", "what decides this outcome?", or asks follow-up questions about specific conditions, resources, inputs, outputs, edge cases, or code paths.
---

# Explain Current Flow

## Overview

Answer questions about current behavior by reconstructing how the system works now. In OpenSpec-based repositories, read OpenSpec first to understand intended behavior, then verify against implementation. Prefer a clear business-logic explanation over a code tour. Use implementation details only to support the explanation or when the user asks for them.

## Workflow

1. Identify the behavior from the user's words.
   - Extract likely feature names, business terms, events, routes, commands, resources, and synonyms.
   - Use these terms for targeted searches instead of reading broad directories first.
   - Adapt to the repository's structure. Do not assume OpenSpec or any specific framework, service, or language exists in every repository.

2. Read OpenSpec intent before implementation when available.
   - If the repository has `openspec/`, search `openspec/specs` and `openspec/changes` for the behavior.
   - Read matching canonical `openspec/specs/**/spec.md` files first.
   - If an active OpenSpec change is relevant, read its `proposal.md`, `design.md`, `tasks.md`, and spec deltas.
   - Treat active changes as pending intent unless the implementation confirms they are already live.
   - If OpenSpec is absent or has no relevant match, check nearby product docs, ADRs, README files, tickets, tests, or design notes when they exist.
   - Treat OpenSpec and other docs as intent, not proof of current behavior.
   - If specs/docs are absent, stale, or unrelated, continue from the code.

3. Disambiguate only when needed.
   - If one likely behavior exists after checking intent sources, proceed.
   - If several plausible behaviors exist, ask one concise question with the concrete candidates.
   - If the user asks a follow-up that clearly refers to previous context, continue from that context and inspect only what is needed.

4. Verify current behavior in implementation.
   - Follow the runtime path far enough to explain the user-visible behavior.
   - Inspect entry points, branching conditions, state reads/writes, downstream calls, outputs, and implemented error handling.
   - Use `rg -i "<term>|<synonym>"`, `rg --files`, and targeted file reads before broad file reads.
   - If OpenSpec or documentation disagrees with code, say so briefly and answer based on the code for "right now".

5. Answer at the right level of detail.
   - Default to business logic: actors, trigger, important decisions, data movement, outcome, and notable failure/skip behavior.
   - Avoid listing every file, function, class, variable, resource, or line by default.
   - Include specific files, functions, resource names, schemas, environment variables, API payloads, table keys, schedules, or line-level citations only when the user asks for that detail or the detail is necessary to make the explanation accurate.
   - Do not propose changes unless the user asks.

## Answer Shape

Start with one sentence naming the behavior and whether the answer is based on OpenSpec, code, or both.

For a default answer, use a short flow:

1. What starts the behavior.
2. What the system checks or decides.
3. What data it reads or writes.
4. What other components or external systems it calls.
5. What result the user or downstream system sees.
6. What happens on failure, retry, skip, or fallback when implemented.

Close with a short `Checked:` line naming the main OpenSpec specs/changes, other docs, and code areas used. Keep this list compact.

## Specific Follow-Ups

For narrow questions, answer only the narrower question after inspecting the exact code or config needed. Examples:

- Which component owns a step.
- Which condition makes the behavior apply or skip.
- Which state record, table key, queue, topic, route, or endpoint is used.
- Which external API endpoint or payload is sent.
- Which error path or retry behavior is implemented.
- Where a specific value is derived.

Use clickable local file links with line numbers when exact code references are useful. If the answer cannot be verified in current implementation, say what was found and what was not found.

## Example Output

For a question like "How does checkout cancellation work right now?", answer in this style after inspecting the actual repository:

1. The flow starts when the user cancels from the checkout screen or when the payment provider sends a cancellation callback.
2. The system validates that the checkout session still belongs to the current order and has not already reached a terminal state.
3. It updates the order/payment state, releases any temporary reservation when that logic is implemented, and records the cancellation reason when available.
4. It notifies downstream systems only for the implemented cases.
5. The user sees the order return to the configured non-paid state, or an error if the session cannot be matched.

Replace the generic phrases with the repository's actual behavior. Add file-level or line-level detail only if the user asks for it or the detail changes the business meaning.
