"""Generate a single plain-text reply to an authorized group mention."""

import asyncio
import logging
from pathlib import Path
import sqlite3

import httpx
from dialogue_log import DialogueLog, encode, journal_path


SKILL = Path(__file__).resolve().parents[1] / ".agents/skills/moribot-dialogue/SKILL.md"
MODEL = "deepseek-flash"
# OpenQQ v0.5.0 closes the signed POST after five seconds.
MODEL_TIMEOUT = 4.0
UNAVAILABLE = "茉莉这次没能接上话，等会儿再叫咱一下吧。"


class DeepSeekDialogue:
    def __init__(self, key: str, style: str, journal: DialogueLog, transport=None):
        self.client = httpx.AsyncClient(
            base_url="https://api.deepseek.com", headers={"Authorization": f"Bearer {key}"},
            trust_env=False, follow_redirects=False, transport=transport,
        )
        self.prompt = style.removeprefix("---").partition("\n---\n")[2].strip() or style
        self.journal = journal
        self.requests = 0
        self.failures = 0

    @classmethod
    def load(cls, runtime: Path, transport=None):
        try:
            key = (runtime / "deepseek-key").read_text(encoding="ascii").strip()
            style = SKILL.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            return None
        if not key or not style.strip():
            return None
        try:
            journal = DialogueLog(journal_path(runtime))
        except (OSError, sqlite3.Error):
            logging.exception("Cannot open private dialogue journal")
            return None
        return cls(key, style, journal, transport)

    async def close_journal(self):
        self.journal.db.close()

    async def answer(self, context: dict, event: dict, quote_event: dict | None) -> str:
        payload = {
            "model": MODEL, "thinking": {"type": "disabled"}, "max_tokens": 144,
            "messages": [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": encode(context)},
            ],
        }
        try:
            record_id = self.journal.begin(event, quote_event, payload)
        except sqlite3.Error:
            logging.exception("Cannot start private dialogue record")
            return UNAVAILABLE
        self.requests += 1
        http_status = body = error = None
        status, reply = "interrupted", UNAVAILABLE
        try:
            async with asyncio.timeout(MODEL_TIMEOUT):
                response = await self.client.post("/chat/completions", json=payload)
                http_status, body = response.status_code, response.text
                response.raise_for_status()
                choice = response.json()["choices"][0]
                content = choice["message"]["content"]
                if choice.get("finish_reason") != "stop" or not isinstance(content, str) or not content.strip():
                    raise ValueError("No complete text reply")
                status, reply = "ok", content.strip()
        except (httpx.HTTPError, TimeoutError, ValueError, KeyError, IndexError, TypeError) as exc:
            self.failures += 1
            status = "timeout" if isinstance(exc, (TimeoutError, httpx.TimeoutException)) else "error"
            error = type(exc).__name__
        finally:
            try:
                self.journal.finish(record_id, status, http_status, body, reply if status != "interrupted" else None, error)
            except sqlite3.Error:
                logging.exception("Cannot finish private dialogue record %s", record_id)
                reply = UNAVAILABLE
        return reply
