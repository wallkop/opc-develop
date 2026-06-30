#!/usr/bin/env python3
"""Lightweight tests for opc-develop helper scripts."""

from __future__ import annotations

import os
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NEXT = ROOT / "next_feature_slug.py"
PARSE = ROOT / "parse_review_status.py"
VALIDATE = ROOT / "validate_opc_artifacts.py"
PLUGIN_ROOT = ROOT.parents[1]


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode:
        raise AssertionError(f"command failed: {args}\nstdout={result.stdout}\nstderr={result.stderr}")
    return result


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_next_feature_slug() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        features = Path(tmp) / "docs/features"
        (features / "1-alpha").mkdir(parents=True)
        (features / "105-beta").mkdir()
        (features / "legacy").mkdir()
        result = run(str(NEXT), "007-New Feature!!", "--features-dir", str(features))
        assert result.stdout.strip() == "106-new-feature"

        (features / "new-feature").mkdir()
        result = run(str(NEXT), "new-feature", "--features-dir", str(features), check=False)
        assert result.returncode == 1
        assert "同名无编号旧 feature" in result.stderr


def test_parse_review_status() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        review = Path(tmp) / "review.md"
        write(review, "**Status:** Approved\n")
        assert run(str(PARSE), str(review)).stdout.strip() == "Approved"

        write(review, "**Status:** Approved\n\n**Status:** Issues Found\n")
        result = run(str(PARSE), str(review), check=False)
        assert result.returncode == 1
        assert "exactly one status" in result.stderr


def make_feature(root: Path) -> Path:
    feature = root / "docs/features/1-sample"
    write(feature / "requirement.md", "# Requirement\n")
    write(
        feature / "demo/prototype.md",
        "# Prototype\n\nPreview URL: http://localhost:3000/sample\n\nMock inventory: none\n",
    )
    write(feature / "prd.md", "# PRD\n")
    write(feature / "technical.md", "# Technical\n")
    write(feature / "spec.md", "# Spec\n")
    write(feature / "testcases.md", "# Testcases\n")
    write(feature / "progress.md", "# Progress\n")
    write(feature / "plan/integration-plan.md", "# Integration\n")
    write(
        feature / "plan/plan-01-core.md",
        "# Plan\n\n## File Map\n- src/a.ts\n\n## Task 1\nReferenced upstream artifacts: spec.md#core\nAllowed change boundary: src/a.ts\nForbidden change boundary: docs/**\nReady standard: referenced spec seed implemented and focused checks recorded\n",
    )
    write(feature / "reviews/demo-review.md", "**Status:** Approved\n")
    write(feature / "reviews/prd-review.md", "**Status:** Approved\n")
    write(feature / "reviews/technical-review.md", "**Status:** Approved\n")
    write(feature / "reviews/spec-review.md", "**Status:** Approved\n")
    write(feature / "reviews/testcase-review.md", "**Status:** Approved\n")
    write(feature / "reviews/plan-review.md", "**Status:** Approved\n")
    return feature


def test_validate_layout_and_freshness() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        feature = make_feature(Path(tmp))
        assert run(str(VALIDATE), str(feature), "--stage", "plan").returncode == 0

        time.sleep(0.02)
        os.utime(feature / "spec.md", None)
        result = run(str(VALIDATE), str(feature), "--stage", "plan", check=False)
        assert result.returncode == 1
        assert "review is older" in result.stderr

        write(feature / "reviews/spec-review.md", "**Status:** Approved\n")
        write(feature / "plan/plan-01-core.md", "# Plan\n\n## Task\nTODO\n")
        result = run(str(VALIDATE), str(feature), "--stage", "plan", check=False)
        assert result.returncode == 1
        assert (
            "contains placeholder" in result.stderr
            or "missing File Map" in result.stderr
            or "review is older" in result.stderr
        )


def test_demo_alignment_contract_is_threaded() -> None:
    contract = PLUGIN_ROOT / "shared/references/demo-implementation-alignment.md"
    assert contract.is_file()

    required_skills = [
        "build-demo",
        "create-demo",
        "review-demo",
        "create-prd",
        "create-technical",
        "create-spec",
        "create-testcases",
        "create-plan",
        "review-spec",
        "review-testcases",
        "review-plan",
        "tdd-coding",
        "local-e2e-verify",
        "debug-failure",
        "acceptance-rework",
    ]
    for skill in required_skills:
        text = (PLUGIN_ROOT / f"skills/{skill}/SKILL.md").read_text(encoding="utf-8")
        assert "demo-implementation-alignment.md" in text, skill
        assert (
            "approved demo" in text.lower()
            or "demo parity" in text.lower()
            or "frontend prototype" in text.lower()
        ), skill

    prompt_checks = {
        "shared/prompts/implementer-subagent.md": "approved demo",
        "shared/prompts/implementation-reviewer.md": "demo parity",
        "shared/prompts/plan-reviewer.md": "approved demo",
        "shared/prompts/spec-reviewer.md": "approved demo",
    }
    for rel, needle in prompt_checks.items():
        text = (PLUGIN_ROOT / rel).read_text(encoding="utf-8").lower()
        assert needle in text, rel


def test_frontend_prototype_demo_and_mock_retirement_contracts_are_threaded() -> None:
    demo_contract = (PLUGIN_ROOT / "shared/references/demo-contract.md").read_text(encoding="utf-8")
    for needle in [
        "real frontend codebase",
        "frontend-only mock",
        "80%",
        "restart local services",
        "preview URL",
        "Strictly do not modify backend code",
        "demo/prototype.md",
    ]:
        assert needle in demo_contract, needle

    retirement = (PLUGIN_ROOT / "shared/references/prototype-mock-retirement-contract.md").read_text(
        encoding="utf-8"
    )
    for needle in [
        "Prototype Mock Retirement Plan",
        "final mock residual review/audit",
        "must not survive as production runtime",
        "The final status must not be `DONE`",
    ]:
        assert needle in retirement, needle

    demo_skills = ["create-demo", "review-demo", "build-demo"]
    for skill in demo_skills:
        text = (PLUGIN_ROOT / f"skills/{skill}/SKILL.md").read_text(encoding="utf-8")
        for needle in [
            "demo-contract.md",
            "prototype-mock-retirement-contract.md",
            "frontend",
        ]:
            assert needle in text, f"{skill}: {needle}"
        assert "backend" in text.lower(), skill
        assert "preview URL" in text or "preview" in text, skill

    downstream = [
        "create-spec",
        "review-spec",
        "create-plan",
        "review-plan",
        "tdd-coding",
    ]
    for skill in downstream:
        text = (PLUGIN_ROOT / f"skills/{skill}/SKILL.md").read_text(encoding="utf-8")
        assert "prototype-mock-retirement-contract.md" in text, skill
        assert "Prototype Mock Retirement Plan" in text or "mock retirement" in text.lower(), skill

    cross_refs = [
        "shared/references/spec-format.md",
        "shared/references/development-input-contract.md",
        "shared/references/tdd-contract.md",
        "shared/references/subagent-execution-contract.md",
        "shared/prompts/spec-reviewer.md",
        "shared/prompts/plan-reviewer.md",
        "shared/prompts/implementer-subagent.md",
        "shared/prompts/implementation-reviewer.md",
    ]
    for rel in cross_refs:
        text = (PLUGIN_ROOT / rel).read_text(encoding="utf-8")
        assert "Prototype Mock Retirement Plan" in text or "mock residual" in text.lower(), rel

    tdd = (PLUGIN_ROOT / "skills/tdd-coding/SKILL.md").read_text(encoding="utf-8")
    assert "final mock residual review/audit" in tdd
    assert "Do not claim `DONE`" in tdd

    validator = (PLUGIN_ROOT / "shared/scripts/validate_opc_artifacts.py").read_text(
        encoding="utf-8"
    )
    assert "demo/prototype.md" in validator
    assert "demo/index.html" not in validator


def test_full_flow_boundary_contracts_are_threaded() -> None:
    for rel in [
        "shared/references/artifact-boundary-contract.md",
        "shared/references/review-trigger-policy.md",
        "shared/references/development-input-contract.md",
    ]:
        assert (PLUGIN_ROOT / rel).is_file(), rel

    expected_refs = {
        "create-technical": ["artifact-boundary-contract.md"],
        "review-technical": ["artifact-boundary-contract.md", "review-trigger-policy.md"],
        "create-spec": ["artifact-boundary-contract.md"],
        "review-spec": ["artifact-boundary-contract.md", "review-trigger-policy.md"],
        "create-plan": ["artifact-boundary-contract.md", "development-input-contract.md"],
        "review-plan": [
            "artifact-boundary-contract.md",
            "development-input-contract.md",
            "review-trigger-policy.md",
        ],
        "tdd-coding": [
            "artifact-boundary-contract.md",
            "development-input-contract.md",
            "review-trigger-policy.md",
        ],
        "loop-develop": ["development-input-contract.md", "review-trigger-policy.md"],
    }
    for skill, needles in expected_refs.items():
        text = (PLUGIN_ROOT / f"skills/{skill}/SKILL.md").read_text(encoding="utf-8")
        for needle in needles:
            assert needle in text, f"{skill}: {needle}"

    technical = (PLUGIN_ROOT / "shared/references/technical-format.md").read_text(encoding="utf-8")
    assert "One explicit technical approach" in technical
    assert "Public API input/output contracts" in technical
    assert "datastore/database" in technical
    assert "human architecture review" in technical

    spec = (PLUGIN_ROOT / "shared/references/spec-format.md").read_text(encoding="utf-8")
    assert "Internal implementation boundaries" in spec
    assert "Do not redefine public API input/output" in spec

    plan = (PLUGIN_ROOT / "shared/references/plan-tree-format.md").read_text(encoding="utf-8")
    assert "Plans are orchestration artifacts" in plan
    assert "Do not put API schemas" in plan


def test_validate_plan_rejects_old_red_green_contract() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        feature = make_feature(Path(tmp))
        write(
            feature / "plan/plan-01-core.md",
            "# Plan\n\n## File Map\n- src/a.ts\n\n## Task 1\n"
            "Referenced upstream artifacts: spec.md#core\n"
            "Allowed change boundary: src/a.ts\n"
            "Forbidden change boundary: docs/**\n"
            "RED command: npm test\n"
            "Expected RED failure: fails\n"
            "GREEN implementation scope: src/a.ts\n"
            "Expected pass signal: pass\n"
            "Ready standard: done\n",
        )
        result = run(str(VALIDATE), str(feature), "--stage", "plan", check=False)
        assert result.returncode == 1
        assert "contains RED/GREEN commands" in result.stderr


def test_mock_system_contract_is_threaded() -> None:
    contract = PLUGIN_ROOT / "shared/references/mock-system-contract.md"
    assert contract.is_file()
    contract_text = contract.read_text(encoding="utf-8")
    for needle in [
        "API mock",
        "Storage mock",
        "MOCK_MODE",
        ".dev/reports/mock-system/",
        "Relation To create-demo",
    ]:
        assert needle in contract_text, needle

    harness_init = (PLUGIN_ROOT / "skills/harness-init/SKILL.md").read_text(encoding="utf-8")
    assert "mock-system-contract.md" in harness_init
    assert "API mock, storage mock" in harness_init
    assert "Mock System Plan" in harness_init

    planning = (PLUGIN_ROOT / "skills/harness-init/references/planning-framework.md").read_text(
        encoding="utf-8"
    )
    for needle in [
        "Batch 5b: Mock System",
        "Mock System Baseline",
        "API mock plan",
        "storage mock plan",
        "At least one API mock scenario can run",
        "At least one storage mock scenario can reset",
    ]:
        assert needle in planning, needle

    harness_eval = (PLUGIN_ROOT / "skills/harness-eval/SKILL.md").read_text(encoding="utf-8")
    for needle in [
        "mock-system-contract.md",
        "Mock System And Fixture Isolation",
        "API mock",
        "storage mock",
        "Cap the Mock System dimension at 2.0",
        "Cap the overall score at 4.0",
        "Cap the overall score at 3.5",
        "Mock System Summary",
    ]:
        assert needle in harness_eval, needle

    harness_doc = (PLUGIN_ROOT / "shared/references/harness-doc.md").read_text(encoding="utf-8")
    for needle in [
        "## Mock System",
        "docs/technical/standards/mock-system.md",
        "docs/technical/runbooks/mock-system.md",
        "API mock",
        "storage mock",
        "fixture",
        ".dev/reports/mock-system/",
    ]:
        assert needle in harness_doc, needle


def test_branch_stage_contract_is_threaded() -> None:
    contract = PLUGIN_ROOT / "shared/references/branch-stage-contract.md"
    assert contract.is_file()
    contract_text = contract.read_text(encoding="utf-8")
    for needle in [
        "Once it is ready to write or update the committed feature requirement artifact",
        "Before writing `docs/features/<numbered-slug>/requirement.md`",
        "Starting with `create-demo`, every Full feature skill must operate on the corresponding feature branch",
        "default expected branch is `develop`",
        "worktree is only a tool",
        "Do not write `requirement.md` on `develop`, `main`, or `master`",
        "Do not run `create-demo` or any later Full feature skill on `develop`, `main`, or `master`",
    ]:
        assert needle in contract_text, needle

    for skill_path in sorted((PLUGIN_ROOT / "skills").glob("*/SKILL.md")):
        text = skill_path.read_text(encoding="utf-8")
        assert "branch-stage-contract.md" in text, skill_path

    brainstorm = (PLUGIN_ROOT / "skills/product-brainstorm/SKILL.md").read_text(encoding="utf-8")
    assert "Early brainstorming may stay on the current branch" in brainstorm
    assert "Once this skill is ready to write or update `requirement.md`" in brainstorm
    assert "Do not write `requirement.md` on `develop`, `main`, or `master`" in brainstorm

    feature_branch_skills = [
        "create-demo",
        "build-demo",
        "create-prd",
        "build-prd",
        "create-technical",
        "build-technical",
        "loop-design",
    ]
    for skill in feature_branch_skills:
        text = (PLUGIN_ROOT / f"skills/{skill}/SKILL.md").read_text(encoding="utf-8")
        assert "feature-branch-only workflow" in text, skill
        assert "Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch" in text, skill

    create_spec = (PLUGIN_ROOT / "skills/create-spec/SKILL.md").read_text(encoding="utf-8")
    assert "must already have been created or entered by `product-brainstorm`" in create_spec
    assert "Do not create or switch branches" in create_spec

    downstream = [
        "loop-develop",
        "create-testcases",
        "create-plan",
        "tdd-coding",
        "local-e2e-verify",
    ]
    for skill in downstream:
        text = (PLUGIN_ROOT / f"skills/{skill}/SKILL.md").read_text(encoding="utf-8")
        lower = text.lower()
        assert "product-brainstorm" in text, skill
        assert (
            "do not create a feature branch" in lower
            or "do not create feature branches" in lower
            or "do not create, switch" in lower
        ), skill
        assert "develop" in text and "main" in text and "master" in text, skill

    release = (PLUGIN_ROOT / "skills/release-verify/SKILL.md").read_text(encoding="utf-8").lower()
    assert "branch-stage-contract.md" in release
    assert "do not create feature branches" in release
    assert "start on the corresponding feature branch" in release

    lite = (PLUGIN_ROOT / "skills/lite-develop/SKILL.md").read_text(encoding="utf-8")
    assert "Lite is a current-branch workflow" in lite
    assert "Do not auto-checkout `develop`" in lite
    assert "do not use a worktree as the default response" in lite
    assert "git worktree add -b feature/<numbered-slug>" not in lite

    plan_format = (PLUGIN_ROOT / "shared/references/plan-tree-format.md").read_text(encoding="utf-8")
    assert "must not introduce a new branch creation step" in plan_format

    worktree_contract = (PLUGIN_ROOT / "shared/references/worktree-isolation-contract.md").read_text(
        encoding="utf-8"
    )
    assert "not a lifecycle stage" in worktree_contract
    assert "not from `develop` by default" in worktree_contract


def test_release_verify_does_not_require_human_acceptance_gate() -> None:
    release_skill = (PLUGIN_ROOT / "skills/release-verify/SKILL.md").read_text(encoding="utf-8")
    release_contract = (PLUGIN_ROOT / "shared/references/release-contract.md").read_text(encoding="utf-8")
    human_contract = (PLUGIN_ROOT / "shared/references/human-acceptance-contract.md").read_text(
        encoding="utf-8"
    )
    artifact_contract = (PLUGIN_ROOT / "shared/references/harness-artifact-contract.md").read_text(
        encoding="utf-8"
    )

    combined = "\n".join([release_skill, release_contract, human_contract, artifact_contract])
    for forbidden in [
        "Block if human acceptance is missing",
        "Release must not proceed unless `human-acceptance.md`",
        "passed human acceptance evidence",
        "`human-acceptance.md` with `**Human Acceptance:** Passed`",
    ]:
        assert forbidden not in combined, forbidden

    for needle in [
        "Human acceptance records are optional context",
        "Do not block merely because `human-acceptance.md` is missing",
        "Human acceptance is optional release context",
        "not a `release-verify` hard gate",
    ]:
        assert needle in combined, needle


def test_lite_develop_is_single_current_branch_flow() -> None:
    lite_develop_path = PLUGIN_ROOT / "skills/lite-develop/SKILL.md"
    lite_commit_path = PLUGIN_ROOT / "skills/lite-commit/SKILL.md"
    assert lite_develop_path.is_file()
    assert not lite_commit_path.exists()

    text = lite_develop_path.read_text(encoding="utf-8")
    for needle in [
        "current branch",
        "direct",
        "isolated-worktree",
        "Full flow escalation",
        "git worktree add -b lite/<slug>",
        "HEAD",
        "Settle Rules",
        "discard",
        "Do not stash, commit, discard, copy, or merge dirty changes without explicit user instruction",
    ]:
        assert needle in text, needle
    assert "merge or cherry-pick" in text.lower()

    assert "git worktree add -b feature/<numbered-slug>" not in text
    assert "lite-commit" not in text

    worktree_contract = (PLUGIN_ROOT / "shared/references/worktree-isolation-contract.md").read_text(
        encoding="utf-8"
    )
    for needle in [
        "For `lite-develop`",
        "current branch `HEAD`",
        "recorded parent branch",
        "Do not stash, commit, discard, or copy parent dirty changes automatically",
    ]:
        assert needle in worktree_contract, needle

    manifest = json.loads((PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    manifest_text = json.dumps(manifest, ensure_ascii=False)
    assert "lite-commit" not in manifest_text
    assert "current branch" in manifest_text.lower()


def main() -> int:
    test_next_feature_slug()
    test_parse_review_status()
    test_validate_layout_and_freshness()
    test_demo_alignment_contract_is_threaded()
    test_frontend_prototype_demo_and_mock_retirement_contracts_are_threaded()
    test_full_flow_boundary_contracts_are_threaded()
    test_validate_plan_rejects_old_red_green_contract()
    test_mock_system_contract_is_threaded()
    test_branch_stage_contract_is_threaded()
    test_release_verify_does_not_require_human_acceptance_gate()
    test_lite_develop_is_single_current_branch_flow()
    print("OK: opc helper script tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
