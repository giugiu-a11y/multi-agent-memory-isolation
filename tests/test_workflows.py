from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_security_workflow_scans_complete_history_without_download_script() -> None:
    content = (ROOT / ".github" / "workflows" / "security.yml").read_text(encoding="utf-8")

    assert "fetch-depth: 0" in content
    assert "gitleaks/gitleaks-action@e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e" in content
    assert "curl " not in content
    assert "sudo mv" not in content


def test_external_github_actions_are_pinned_to_full_commit_shas() -> None:
    external_uses: list[tuple[Path, str]] = []
    for workflow in (ROOT / ".github" / "workflows").glob("*.yml"):
        content = workflow.read_text(encoding="utf-8")
        for action in re.findall(r"^\s*-?\s*uses:\s*([^\s#]+)", content, flags=re.MULTILINE):
            if not action.startswith("./"):
                external_uses.append((workflow, action))

    assert external_uses
    for workflow, action in external_uses:
        assert "@" in action, (workflow, action)
        reference = action.rsplit("@", 1)[1]
        assert re.fullmatch(r"[0-9a-f]{40}", reference), (workflow, action)
