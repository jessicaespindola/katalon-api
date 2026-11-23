"""Gera relatorio/ultima-execucao.html com as mesmas conferências dos test cases."""

from __future__ import annotations

import html
import json
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = "http://127.0.0.1:3000"
DESTINO = Path(__file__).with_name("ultima-execucao.html")


def chamar(method, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data, method=method)
    if body is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as res:
            raw = res.read()
            return res.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        return exc.code, json.loads(raw) if raw else None


def passo(method, path, body=None):
    status, resposta = chamar(method, path, body)
    return {
        "method": method,
        "path": path,
        "pedido": body,
        "status": status,
        "resposta": resposta,
    }


def caso(nome, o_que, passos, ok):
    return {"nome": nome, "o_que": o_que, "passos": passos, "ok": ok}


def executar():
    inicio = datetime.now()
    casos = []

    saude = passo("GET", "/health")
    casos.append(caso(
        "01 Verificar saude da API",
        "GET /health devolve 200, status ok e servico tarefas.",
        [saude],
        saude["status"] == 200
        and saude["resposta"].get("status") == "ok"
        and saude["resposta"].get("servico") == "tarefas",
    ))

    lista = passo("GET", "/tarefas")
    primeiro = lista["resposta"][0] if isinstance(lista["resposta"], list) and lista["resposta"] else {}
    casos.append(caso(
        "02 Listar tarefas",
        "A primeira tarefa da lista inicial é id 1, título Ler o README, feita false.",
        [lista],
        lista["status"] == 200
        and primeiro.get("id") == 1
        and primeiro.get("titulo") == "Ler o README"
        and primeiro.get("feita") is False,
    ))

    ausente = passo("GET", "/tarefas/99999")
    casos.append(caso(
        "03 Buscar tarefa inexistente",
        "Id desconhecido responde 404 com a mensagem Tarefa nao encontrada.",
        [ausente],
        ausente["status"] == 404 and ausente["resposta"].get("erro") == "Tarefa nao encontrada",
    ))

    invalida = passo("POST", "/tarefas", {"titulo": "", "feita": False})
    casos.append(caso(
        "04 Recusar tarefa sem titulo",
        "POST com título vazio responde 400 e não grava a tarefa.",
        [invalida],
        invalida["status"] == 400 and invalida["resposta"].get("erro") == "Informe o titulo",
    ))

    criada = passo("POST", "/tarefas", {"titulo": "Criada pelo teste 05", "feita": False})
    corpo = criada["resposta"] if isinstance(criada["resposta"], dict) else {}
    casos.append(caso(
        "05 Criar tarefa",
        "POST válido responde 201, devolve o título e um id numérico.",
        [criada],
        criada["status"] == 201
        and corpo.get("titulo") == "Criada pelo teste 05"
        and corpo.get("feita") is False
        and isinstance(corpo.get("id"), int)
        and corpo.get("id") > 0,
    ))

    fluxo_cria = passo("POST", "/tarefas", {"titulo": "Estudar o fluxo do Katalon", "feita": False})
    tarefa_id = fluxo_cria["resposta"].get("id") if isinstance(fluxo_cria["resposta"], dict) else None
    fluxo_get = passo("GET", f"/tarefas/{tarefa_id}")
    fluxo_put = passo("PUT", f"/tarefas/{tarefa_id}", {"titulo": "Estudar o fluxo do Katalon", "feita": True})
    fluxo_del = passo("DELETE", f"/tarefas/{tarefa_id}")
    fluxo_gone = passo("GET", f"/tarefas/{tarefa_id}")
    get_corpo = fluxo_get["resposta"] if isinstance(fluxo_get["resposta"], dict) else {}
    put_corpo = fluxo_put["resposta"] if isinstance(fluxo_put["resposta"], dict) else {}
    gone_corpo = fluxo_gone["resposta"] if isinstance(fluxo_gone["resposta"], dict) else {}
    casos.append(caso(
        "06 Fluxo completo de uma tarefa",
        "Cria, busca, marca como feita, apaga e confirma o 404.",
        [fluxo_cria, fluxo_get, fluxo_put, fluxo_del, fluxo_gone],
        fluxo_cria["status"] == 201
        and fluxo_get["status"] == 200
        and get_corpo.get("titulo") == "Estudar o fluxo do Katalon"
        and get_corpo.get("feita") is False
        and fluxo_put["status"] == 200
        and put_corpo.get("feita") is True
        and fluxo_del["status"] == 204
        and fluxo_gone["status"] == 404
        and gone_corpo.get("erro") == "Tarefa nao encontrada",
    ))

    fim = datetime.now()
    return inicio, fim, casos


def json_bonito(valor):
    if valor is None:
        return "sem corpo"
    return json.dumps(valor, ensure_ascii=False, indent=2)


def render(inicio, fim, casos):
    passou = sum(1 for item in casos if item["ok"])
    falhou = len(casos) - passou
    duracao_ms = int((fim - inicio).total_seconds() * 1000)
    linhas = []
    detalhes = []
    for item in casos:
        marca = "passou" if item["ok"] else "falhou"
        linhas.append(
            "<tr>"
            f"<td>{html.escape(item['nome'])}</td>"
            f"<td>{html.escape(item['o_que'])}</td>"
            f"<td class='{marca}'>{marca}</td>"
            "</tr>"
        )
        blocos = []
        for etapa in item["passos"]:
            pedido = ""
            if etapa["pedido"] is not None:
                pedido = f"<pre>{html.escape(json_bonito(etapa['pedido']))}</pre>"
            blocos.append(
                "<section class='passo'>"
                f"<h3>{html.escape(etapa['method'])} {html.escape(etapa['path'])} "
                f"<span>HTTP {etapa['status']}</span></h3>"
                f"{pedido}"
                f"<pre>{html.escape(json_bonito(etapa['resposta']))}</pre>"
                "</section>"
            )
        detalhes.append(
            f"<article class='{marca}'>"
            f"<h2>{html.escape(item['nome'])}</h2>"
            f"<p>{html.escape(item['o_que'])}</p>"
            + "".join(blocos)
            + "</article>"
        )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Relatório — API de tarefas</title>
  <style>
    :root {{ color-scheme: light; }}
    body {{ margin: 0; font-family: "Segoe UI", sans-serif; background: #f4f1ea; color: #1d1a16; }}
    main {{ max-width: 880px; margin: 0 auto; padding: 40px 20px 64px; }}
    h1 {{ font-size: 32px; margin: 0 0 8px; }}
    .resumo {{ display: flex; gap: 16px; margin: 24px 0; }}
    .resumo div {{ background: white; border: 1px solid #e2d9cc; border-radius: 12px; padding: 16px 18px; min-width: 120px; }}
    .resumo strong {{ display: block; font-size: 28px; }}
    table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; }}
    th, td {{ text-align: left; padding: 12px 14px; border-bottom: 1px solid #eee6db; vertical-align: top; }}
    th {{ font-size: 12px; letter-spacing: .04em; text-transform: uppercase; color: #6d645b; }}
    .passou {{ color: #0d6b3d; font-weight: 650; }}
    .falhou {{ color: #9d1c1c; font-weight: 650; }}
    article {{ background: white; border: 1px solid #e2d9cc; border-left: 6px solid #0d6b3d; border-radius: 12px; padding: 8px 18px 18px; margin-top: 16px; }}
    article.falhou {{ border-left-color: #9d1c1c; }}
    .passo h3 {{ font-size: 15px; margin-bottom: 8px; }}
    .passo span {{ color: #6d645b; font-weight: 500; }}
    pre {{ background: #f7f4ee; border-radius: 8px; padding: 12px; overflow: auto; }}
    .nota {{ color: #5c564e; line-height: 1.5; }}
  </style>
</head>
<body>
<main>
  <h1>Relatório da execução</h1>
  <p class="nota">API de tarefas em {html.escape(BASE)}. Gerado em {inicio.strftime("%d/%m/%Y %H:%M:%S")}. Duração {duracao_ms} ms.</p>
  <p class="nota">Estas são as conferências dos seis test cases. O Katalon Studio não estava instalado, então este arquivo não é o relatório do Studio. Quando a suíte rodar lá, o relatório oficial fica na pasta Reports.</p>
  <div class="resumo">
    <div><strong>{passou}</strong>passaram</div>
    <div><strong>{falhou}</strong>falharam</div>
    <div><strong>{len(casos)}</strong>casos</div>
  </div>
  <table>
    <thead><tr><th>Caso</th><th>Conferência</th><th>Resultado</th></tr></thead>
    <tbody>
      {''.join(linhas)}
    </tbody>
  </table>
  {''.join(detalhes)}
</main>
</body>
</html>
"""


def main():
    inicio, fim, casos = executar()
    DESTINO.write_text(render(inicio, fim, casos), encoding="utf-8")
    passou = sum(1 for item in casos if item["ok"])
    print(f"{passou}/{len(casos)} {DESTINO}")
    if passou != len(casos):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
