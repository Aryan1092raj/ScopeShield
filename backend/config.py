# ScopeShield settings — all secrets via env, safe defaults for demo
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "ScopeShield"
    app_env: str = "local"  # local | render
    frontend_origin: str = "http://localhost:5173"

    # Tiger Data Postgres (pgvector). Empty => in-memory fallback for demo.
    database_url: str = ""

    # TabPFN (Prior Labs). Empty => heuristic fallback, still demo-able.
    tabpfn_api_key: str = ""

    # SerpApi. Empty => static fallback rate table.
    serpapi_api_key: str = ""

    # Gemma serving. ollama | vllm | stub (stub = deterministic local judge)
    gemma_mode: str = "stub"
    ollama_host: str = "http://localhost:11434"
    gemma_model: str = "gemma-2-9b-tinker-sow-v1"
    base_gemma_model: str = "gemma2:9b-instruct"

    # Sentry. Empty => tracing no-op locally.
    sentry_dsn: str = ""
    traces_sample_rate: float = 1.0


settings = Settings()
