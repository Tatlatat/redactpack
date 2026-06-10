# RedactPack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the RedactPack MVP as a local-first support-bundle sanitizer.

**Architecture:** Pure detector/redactor modules feed scanner/report modules; CLI remains a thin wrapper.

**Tech Stack:** Python 3.9+, setuptools, pytest, GitHub Actions.

---

- [ ] Create package metadata and model tests.
- [ ] Implement detector registry using TDD.
- [ ] Implement deterministic redactor using TDD.
- [ ] Implement policy loading using TDD.
- [ ] Implement scanner and reports using TDD.
- [ ] Implement CLI and benchmark using TDD.
- [ ] Add docs, examples, CI, and Checkpoint 2 internal review.
- [ ] Invoke Claude Fable 5 Checkpoint 2 review through tmux.
