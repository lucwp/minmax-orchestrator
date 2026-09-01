from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sonnet_identity():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "name: minmax-orchestrator-sonnet-5" in text
    assert "# MinMax Orchestrator Sonnet 5" in text
    assert "MinMax Orchestrator Luna" not in text


def test_anthropic_ladder_is_explicit():
    text = (ROOT / "references" / "model-routing.md").read_text(encoding="utf-8")
    for model in ["claude-haiku-4-5", "claude-sonnet-5", "claude-opus-5", "claude-fable-5"]:
        assert model in text
    assert "Claude Mythos 5 is not part of the normal ladder" in text


def test_sonnet_is_default_and_frontier_is_rare():
    text = (ROOT / "references" / "model-routing.md").read_text(encoding="utf-8")
    assert "default root/workhorse" in text
    assert "Fable is the frontier tier, not the default premium tier" in text
    assert "Prefer escalating one load-bearing node" in text


def test_anthropic_thinking_controls_are_safe():
    text = (ROOT / "references" / "model-routing.md").read_text(encoding="utf-8")
    assert "adaptive thinking by default" in text
    assert "Never use legacy `budget_tokens` instructions for Sonnet 5, Opus 5, or Fable 5" in text
    assert "do not add blanket self-check prompts" in text


def test_advisor_is_optional_and_not_terminal_evidence():
    text = (ROOT / "references" / "model-routing.md").read_text(encoding="utf-8")
    assert "If the runtime exposes Anthropic's Advisor tool" in text
    assert "advisor output is guidance, not authoritative terminal evidence" in text
