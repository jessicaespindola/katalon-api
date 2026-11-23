"""API local de tarefas para estudar automação de API no Katalon Studio.

Não usa bibliotecas externas. Os dados ficam só em memória: ao encerrar
o processo, tudo volta ao estado inicial. Isso deixa os testes repetíveis.
"""

from __future__ import annotations

import json
import os
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "3000"))

_lock = threading.Lock()
_proximo_id = 3
_tarefas = {
    1: {"id": 1, "titulo": "Ler o README", "feita": False},
    2: {"id": 2, "titulo": "Subir a API local", "feita": True},
}


class TarefasHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        path = _caminho(self.path)
        if path == "/health":
            self._send(200, {"status": "ok", "servico": "tarefas"})
            return
        if path == "/tarefas":
            with _lock:
                corpo = list(_tarefas.values())
            self._send(200, corpo)
            return
        tarefa_id = _id_da_tarefa(path)
        if tarefa_id is not None:
            with _lock:
                tarefa = _tarefas.get(tarefa_id)
            if tarefa is None:
                self._send(404, {"erro": "Tarefa nao encontrada"})
            else:
                self._send(200, tarefa)
            return
        self._send(404, {"erro": "Rota nao encontrada"})

    def do_POST(self):
        if _caminho(self.path) != "/tarefas":
            self._send(404, {"erro": "Rota nao encontrada"})
            return
        dados = self._ler_json()
        if dados is None:
            return
        tarefa = _validar_tarefa(dados)
        if isinstance(tarefa, str):
            self._send(400, {"erro": tarefa})
            return
        with _lock:
            global _proximo_id
            novo_id = _proximo_id
            _proximo_id += 1
            criada = {"id": novo_id, "titulo": tarefa["titulo"], "feita": tarefa["feita"]}
            _tarefas[novo_id] = criada
        self._send(201, criada)

    def do_PUT(self):
        tarefa_id = _id_da_tarefa(_caminho(self.path))
        if tarefa_id is None:
            self._send(404, {"erro": "Rota nao encontrada"})
            return
        dados = self._ler_json()
        if dados is None:
            return
        tarefa = _validar_tarefa(dados)
        if isinstance(tarefa, str):
            self._send(400, {"erro": tarefa})
            return
        with _lock:
            if tarefa_id not in _tarefas:
                self._send(404, {"erro": "Tarefa nao encontrada"})
                return
            atualizada = {"id": tarefa_id, "titulo": tarefa["titulo"], "feita": tarefa["feita"]}
            _tarefas[tarefa_id] = atualizada
        self._send(200, atualizada)

    def do_DELETE(self):
        tarefa_id = _id_da_tarefa(_caminho(self.path))
        if tarefa_id is None:
            self._send(404, {"erro": "Rota nao encontrada"})
            return
        with _lock:
            if tarefa_id not in _tarefas:
                self._send(404, {"erro": "Tarefa nao encontrada"})
                return
            del _tarefas[tarefa_id]
        self._send(204)

    def _ler_json(self):
        tamanho = int(self.headers.get("Content-Length") or 0)
        if tamanho == 0:
            return {}
        bruto = self.rfile.read(tamanho)
        try:
            dados = json.loads(bruto.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send(400, {"erro": "JSON invalido"})
            return None
        if not isinstance(dados, dict):
            self._send(400, {"erro": "O corpo deve ser um objeto JSON"})
            return None
        return dados

    def _send(self, status, body=None):
        payload = b""
        if body is not None:
            payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        if body is not None:
            self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        if payload:
            self.wfile.write(payload)

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))


def _caminho(raw_path):
    path = urlparse(raw_path).path
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return path


def _id_da_tarefa(path):
    match = re.fullmatch(r"/tarefas/(\d+)", path)
    if match is None:
        return None
    return int(match.group(1))


def _validar_tarefa(dados):
    titulo = dados.get("titulo")
    if not isinstance(titulo, str) or not titulo.strip():
        return "Informe o titulo"
    feita = dados.get("feita", False)
    if not isinstance(feita, bool):
        return "O campo feita deve ser true ou false"
    return {"titulo": titulo.strip(), "feita": feita}


def main():
    server = ThreadingHTTPServer((HOST, PORT), TarefasHandler)
    base = f"http://{HOST}:{PORT}"
    print(f"API de tarefas em {base}", flush=True)
    print("  GET    /health", flush=True)
    print("  GET    /tarefas", flush=True)
    print("  POST   /tarefas", flush=True)
    print("  GET    /tarefas/{id}", flush=True)
    print("  PUT    /tarefas/{id}", flush=True)
    print("  DELETE /tarefas/{id}", flush=True)
    print("Ctrl+C encerra e apaga os dados criados durante os testes.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
