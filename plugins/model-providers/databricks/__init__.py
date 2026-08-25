"""Databricks provider profile.

Databricks Model Serving exposes an OpenAI-compatible surface at
``https://<workspace-host>/serving-endpoints``; users supply their own base
URL at setup since endpoints are per-workspace. One profile covers all
three endpoint flavors — Foundation Model API pay-per-token endpoints
(``databricks-*``), external models proxied through the workspace, and
custom serving endpoints — because the ``model`` request field is simply
the serving-endpoint name.
"""

from providers import register_provider
from providers.base import ProviderProfile

databricks = ProviderProfile(
    name="databricks",
    aliases=("databricks-model-serving",),
    display_name="Databricks",
    description="Databricks Model Serving - OpenAI-compatible endpoint (user-supplied workspace URL)",
    signup_url="https://docs.databricks.com/aws/en/machine-learning/foundation-model-apis/",
    env_vars=("DATABRICKS_TOKEN", "DATABRICKS_BASE_URL"),
    base_url="",  # per-workspace; user provides https://<workspace-host>/serving-endpoints
    auth_type="api_key",
    # The OpenAI-compatible surface documents chat/completions and
    # responses but no /models listing route (endpoint discovery is
    # Databricks' native serving-endpoints API), so the doctor's
    # {base_url}/models probe would fail on healthy workspaces.
    supports_health_check=False,
    # FMAPI pay-per-token endpoints preconfigured in workspaces where
    # FMAPI is available; agentic tool-calling chat models only, per the
    # fallback_models contract. Custom serving endpoints are
    # workspace-specific, so users enter those endpoint names directly.
    fallback_models=(
        "databricks-claude-sonnet-5",
        "databricks-claude-opus-5",
        "databricks-claude-haiku-4-5",
        "databricks-gpt-5-5",
        "databricks-gemini-3-1-pro",
        "databricks-meta-llama-4-maverick",
        "databricks-gpt-oss-120b",
        "databricks-kimi-k3",
        "databricks-glm-5-2",
        "databricks-deepseek-v4-pro-0813",
    ),
    default_aux_model="databricks-claude-haiku-4-5",
)

register_provider(databricks)
