from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_sonnet_identity():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "name: minmax-orchestrator-sonnet" in text
    assert "# MinMax Orchestrator Sonnet" in text
    assert "MinMax Orchestrator Luna" not in text


def test_anthropic_models_are_explicit():
    text = (ROOT / "references" / "model-routing.md").read_text(encoding="utf-8")
    for model in ["claude-haiku-4-5", "claude-sonnet-5", "claude-opus-5", "claude-fable-5"]:
        assert model in text
    assert "Claude Mythos 5 is not part of the normal routing policy" in text


def test_sonnet_effort_is_primary_ladder():
    text = (ROOT / "references" / "model-routing.md").read_text(encoding="utf-8")
    assert "Sonnet-first, effort-first, model-switch-last" in text
    assert "Sonnet effort is the primary ladder" in text
    assert "Sonnet low effort" in text
    assert "Sonnet max effort" in text
    assert "lowest Sonnet effort that is likely to complete the node reliably" in text


def test_haiku_is_offload_not_reasoning_rung():
    text = (ROOT / "references" / "model-routing.md").read_text(encoding="utf-8")
    assert "Haiku is a specialized offload path" in text
    assert "not the first reasoning rung" in text
    assert "keep the work on Sonnet" in text


def test_opus_and_fable_are_narrow_escalations():
    text = (ROOT / "references" / "model-routing.md").read_text(encoding="utf-8")
    assert "prefer an Opus advisor before replacing Sonnet as the executor" in text
    assert "Move a node to Opus execution only when" in text
    assert "Fable is a last-resort frontier path" in text
    assert "Prefer a narrow Fable consultation or isolated load-bearing node" in text


def test_anthropic_thinking_controls_are_safe():
    text = (ROOT / "references" / "model-routing.md").read_text(encoding="utf-8")
    assert "adaptive thinking by default" in text
    assert "Never use legacy `budget_tokens` instructions for Sonnet 5, Opus 5, or Fable 5" in text
    assert "do not add blanket self-check prompts" in text


def test_advisor_is_optional_and_not_terminal_evidence():
    text = (ROOT / "references" / "model-routing.md").read_text(encoding="utf-8")
    assert "If the runtime exposes Anthropic's Advisor tool" in text
    assert "advisor output is guidance, not authoritative terminal evidence" in text
