"""MCP server untuk database toko TEN (modul 11, notebook 02).

Server ini menyediakan tool baca-saja (read-only) lewat Model Context Protocol,
sehingga bisa dipakai oleh client MCP mana pun: notebook ini, Claude Desktop,
Claude Code, atau aplikasi lain.

Menjalankan (biasanya dijalankan otomatis oleh client MCP lewat stdio):
    TOKO_DB=toko.db python server_toko.py

Penting: dengan transport stdio, stdout dipakai untuk protokol. Jangan print()
ke stdout di file ini; gunakan logging (ke stderr) bila perlu.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from mcp.server.mcpserver import MCPServer

DB_PATH = Path(os.environ.get("TOKO_DB", "toko.db")).resolve()
MAKS_BARIS = 50

server = MCPServer("toko-ten", instructions="Data penjualan fiktif Toko Elektronik Nusantara. Semua tool baca-saja.")


def _koneksi_baca_saja() -> sqlite3.Connection:
    # mode=ro: SQLite sendiri menolak semua operasi tulis
    return sqlite3.connect(f"{DB_PATH.as_uri()}?mode=ro", uri=True)


@server.tool()
def lihat_skema() -> str:
    """Tampilkan perintah CREATE TABLE semua tabel di database toko (nama tabel, kolom, tipe, dan komentar)."""
    with _koneksi_baca_saja() as con:
        return "\n\n".join(r[0] for r in con.execute("SELECT sql FROM sqlite_master WHERE type = 'table'"))


@server.tool()
def jalankan_sql(query: str) -> dict:
    """Jalankan SATU query SQLite SELECT (baca-saja) dan kembalikan maksimal 50 baris.

    Args:
        query: Query SELECT. Gunakan agregasi (SUM, COUNT, GROUP BY) agar hasilnya ringkas.
    """
    with _koneksi_baca_saja() as con:
        cur = con.execute(query)
        kolom = [d[0] for d in cur.description or []]
        baris = cur.fetchmany(MAKS_BARIS + 1)
    return {"kolom": kolom, "baris": [list(b) for b in baris[:MAKS_BARIS]], "terpotong": len(baris) > MAKS_BARIS}


if __name__ == "__main__":
    server.run("stdio")
