"""Server tiruan Claude Messages API untuk menguji notebook modul 08 TANPA API key (CI & lokal).

Server ini TIDAK memanggil model sungguhan. Jawabannya teks/JSON dummy yang bentuknya
sama dengan respons API asli, sehingga jalur kode notebook (SDK `anthropic`, parsing
respons, streaming, structured output, loop tool use) tetap teruji. Beberapa aturan
validasi API ikut ditiru (misalnya `temperature` ditolak model terbaru, `tool_choice`
paksa ditolak), agar kesalahan pemakaian parameter tertangkap di CI.

Pemakaian (dari root repo):
    python scripts/fake_anthropic_server.py --port 8765 &
    export ANTHROPIC_BASE_URL=http://127.0.0.1:8765 ANTHROPIC_API_KEY=kunci-uji
    python scripts/run_notebooks.py 08-llm-basics/02_claude_api_dasar.ipynb
"""

from __future__ import annotations

import argparse
import itertools
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Model yang menolak parameter sampling & tool_choice paksa (meniru API asli)
MODEL_TANPA_SAMPLING = {"claude-opus-5-5", "claude-sonnet-5-5", "claude-fable-5-1"}
MODEL_DIKENAL = MODEL_TANPA_SAMPLING | {"claude-opus-5", "claude-sonnet-5", "claude-opus-4-8", "claude-haiku-4-5"}
FALLBACK_BETA = "server-side-fallback-2026-07-01"
_id = itertools.count(1)


class ErrorPermintaan(Exception):
    def __init__(self, status: int, jenis: str, pesan: str):
        super().__init__(pesan)
        self.status, self.jenis, self.pesan = status, jenis, pesan


def contoh_dari_schema(schema: dict, defs: dict | None = None):
    """Membuat nilai dummy yang valid terhadap JSON schema (subset yang dipakai notebook)."""
    defs = defs or schema.get("$defs", {})
    if "$ref" in schema:
        return contoh_dari_schema(defs[schema["$ref"].split("/")[-1]], defs)
    if "const" in schema:
        return schema["const"]
    if "enum" in schema:
        return schema["enum"][0]
    for kunci in ("anyOf", "oneOf", "allOf"):
        if kunci in schema:
            return contoh_dari_schema(schema[kunci][0], defs)
    tipe = schema.get("type", "string")
    if isinstance(tipe, list):
        tipe = next(t for t in tipe if t != "null")
    if tipe == "object":
        props = schema.get("properties", {})
        return {k: contoh_dari_schema(v, defs) for k, v in props.items()}
    if tipe == "array":
        return [contoh_dari_schema(schema.get("items", {}), defs)]
    return {"string": "contoh", "integer": 1, "number": 1.0, "boolean": True, "null": None}[tipe]


def teks_user_terakhir(messages: list) -> str:
    for m in reversed(messages):
        if m["role"] != "user":
            continue
        if isinstance(m["content"], str):
            return m["content"]
        return " ".join(b.get("text", "") for b in m["content"] if b.get("type") == "text")
    return ""


def validasi(body: dict, beta: str) -> None:
    for wajib in ("model", "max_tokens", "messages"):
        if wajib not in body:
            raise ErrorPermintaan(400, "invalid_request_error", f"{wajib}: Field required")
    model = body["model"]
    if model not in MODEL_DIKENAL:
        raise ErrorPermintaan(404, "not_found_error", f"model: {model}")
    if model in MODEL_TANPA_SAMPLING:
        for p in ("temperature", "top_p", "top_k"):
            if p in body:
                raise ErrorPermintaan(400, "invalid_request_error", f"{p} is not supported on this model")
        if body.get("tool_choice", {}).get("type") in ("any", "tool"):
            raise ErrorPermintaan(400, "invalid_request_error", "forced tool_choice is not supported on this model")
        thinking = body.get("thinking", {})
        if thinking.get("type") == "disabled" or "budget_tokens" in thinking:
            raise ErrorPermintaan(400, "invalid_request_error", "thinking cannot be disabled on this model")
    if body.get("fallbacks") == "default" and FALLBACK_BETA not in beta:
        raise ErrorPermintaan(400, "invalid_request_error", f"fallbacks requires the {FALLBACK_BETA} beta")
    msgs = body["messages"]
    if not msgs or msgs[0]["role"] != "user":
        raise ErrorPermintaan(400, "invalid_request_error", "messages: first message must use the user role")
    for tool in body.get("tools", []):
        if tool.get("strict") and tool["input_schema"].get("additionalProperties") is not False:
            raise ErrorPermintaan(400, "invalid_request_error", "strict tools require additionalProperties: false")
    # Setiap tool_result harus menjawab tool_use pada pesan assistant tepat sebelumnya
    for i, m in enumerate(msgs):
        if m["role"] != "user" or isinstance(m["content"], str):
            continue
        hasil = {b["tool_use_id"] for b in m["content"] if b.get("type") == "tool_result"}
        if hasil:
            sebelum = msgs[i - 1]["content"] if i and msgs[i - 1]["role"] == "assistant" else []
            dipanggil = {b["id"] for b in sebelum if isinstance(b, dict) and b.get("type") == "tool_use"}
            if hasil != dipanggil:
                raise ErrorPermintaan(400, "invalid_request_error", "tool_result ids do not match tool_use ids")


def buat_konten(body: dict) -> tuple[list, str]:
    """Isi respons dummy + stop_reason, bergantung pada jenis permintaan."""
    msgs = body["messages"]
    terakhir = msgs[-1]["content"]
    baru_dapat_hasil_tool = not isinstance(terakhir, str) and any(
        b.get("type") == "tool_result" for b in terakhir)
    tools = [t for t in body.get("tools", []) if "input_schema" in t]
    konten = []
    if body.get("thinking", {}).get("display") == "summarized":
        konten.append({"type": "thinking", "thinking": "[ringkasan thinking tiruan]", "signature": "sig-uji"})

    if tools and not baru_dapat_hasil_tool:
        t = tools[0]
        konten.append({"type": "tool_use", "id": f"toolu_uji{next(_id)}", "name": t["name"],
                       "input": contoh_dari_schema(t["input_schema"])})
        return konten, "tool_use"

    fmt = (body.get("output_config") or {}).get("format") or body.get("output_format")
    if fmt and fmt.get("type") == "json_schema":
        konten.append({"type": "text", "text": json.dumps(contoh_dari_schema(fmt["schema"]))})
    else:
        konten.append({"type": "text", "text": f"[jawaban tiruan server uji] {teks_user_terakhir(msgs)[:80]}"})
    return konten, "end_turn"


def buat_pesan(body: dict) -> dict:
    konten, stop = buat_konten(body)
    keluar = sum(len(json.dumps(b)) for b in konten) // 4
    return {
        "id": f"msg_uji{next(_id)}", "type": "message", "role": "assistant", "model": body["model"],
        "content": konten, "stop_reason": stop, "stop_sequence": None, "stop_details": None,
        "usage": {"input_tokens": len(json.dumps(body)) // 4, "output_tokens": max(keluar, 1),
                  "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0},
    }


def event_stream(pesan: dict):
    """Memecah pesan menjadi rangkaian event SSE seperti API streaming asli."""
    awal = {**pesan, "content": [], "stop_reason": None, "usage": {**pesan["usage"], "output_tokens": 1}}
    yield "message_start", {"type": "message_start", "message": awal}
    for i, blok in enumerate(pesan["content"]):
        if blok["type"] == "text":
            yield "content_block_start", {"type": "content_block_start", "index": i,
                                          "content_block": {"type": "text", "text": ""}}
            teks = blok["text"]
            for j in range(0, len(teks), 12):
                yield "content_block_delta", {"type": "content_block_delta", "index": i,
                                              "delta": {"type": "text_delta", "text": teks[j:j + 12]}}
        elif blok["type"] == "thinking":
            yield "content_block_start", {"type": "content_block_start", "index": i,
                                          "content_block": {"type": "thinking", "thinking": "", "signature": ""}}
            yield "content_block_delta", {"type": "content_block_delta", "index": i,
                                          "delta": {"type": "thinking_delta", "thinking": blok["thinking"]}}
            yield "content_block_delta", {"type": "content_block_delta", "index": i,
                                          "delta": {"type": "signature_delta", "signature": blok["signature"]}}
        else:  # tool_use
            yield "content_block_start", {"type": "content_block_start", "index": i,
                                          "content_block": {**blok, "input": {}}}
            yield "content_block_delta", {"type": "content_block_delta", "index": i,
                                          "delta": {"type": "input_json_delta",
                                                    "partial_json": json.dumps(blok["input"])}}
        yield "content_block_stop", {"type": "content_block_stop", "index": i}
    yield "message_delta", {"type": "message_delta",
                            "delta": {"stop_reason": pesan["stop_reason"], "stop_sequence": None},
                            "usage": {"output_tokens": pesan["usage"]["output_tokens"]}}
    yield "message_stop", {"type": "message_stop"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # jangan penuhi log CI
        pass

    def kirim_json(self, status: int, data: dict) -> None:
        isi = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("request-id", f"req_uji{next(_id)}")
        self.send_header("content-length", str(len(isi)))
        self.end_headers()
        self.wfile.write(isi)

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("content-length", 0))) or b"{}")
        path = self.path.split("?")[0]
        try:
            if not self.headers.get("x-api-key", "").startswith("kunci-uji"):
                raise ErrorPermintaan(401, "authentication_error", "invalid x-api-key")
            if path == "/v1/messages/count_tokens":
                return self.kirim_json(200, {"input_tokens": len(json.dumps(body)) // 4})
            if path != "/v1/messages":
                raise ErrorPermintaan(404, "not_found_error", path)
            validasi(body, self.headers.get("anthropic-beta", ""))
            pesan = buat_pesan(body)
        except ErrorPermintaan as e:
            return self.kirim_json(e.status, {"type": "error", "error": {"type": e.jenis, "message": e.pesan}})

        if not body.get("stream"):
            return self.kirim_json(200, pesan)
        self.send_response(200)
        self.send_header("content-type", "text/event-stream")
        self.send_header("request-id", f"req_uji{next(_id)}")
        self.end_headers()
        for nama, data in event_stream(pesan):
            self.wfile.write(f"event: {nama}\ndata: {json.dumps(data)}\n\n".encode())
        self.wfile.flush()


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--port", type=int, default=8765)
    args = p.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Server tiruan Claude API di http://127.0.0.1:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
