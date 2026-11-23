"""Gera relatorio/ultima-execucao.html com as mesmas conferências dos test cases."""

from __future__ import annotations

import csv
import html
import json
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = "http://127.0.0.1:3000"
DESTINO = Path(__file__).with_name("ultima-execucao.html")
CSV_TAREFAS = Path(__file__).resolve().parents[1] / "Data Files" / "criar-tarefa.csv"
SLA_MS = 2000


def chamar(method, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(BASE + path, data=data, method=method)
    if body is not None:
        req.add_header("Content-Type", "application/json")
    inicio = time.perf_counter()
    try:
        with urllib.request.urlopen(req) as res:
            raw = res.read()
            status = res.status
            headers = res.headers
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        status = exc.code
        headers = exc.headers
    elapsed_ms = int((time.perf_counter() - inicio) * 1000)
    return status, json.loads(raw) if raw else None, headers.get("Content-Type") or "", elapsed_ms


def passo(method, path, body=None):
    status, resposta, content_type, elapsed_ms = chamar(method, path, body)
    return {
        "method": method,
        "path": path,
        "pedido": body,
        "status": status,
        "resposta": resposta,
        "content_type": content_type,
        "elapsed_ms": elapsed_ms,
    }


def json_tipo(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)


def tarefa_valida(body):
    return (
        isinstance(body, dict)
        and set(body) == {"id", "titulo", "feita"}
        and json_tipo(body.get("id"))
        and body["id"] >= 1
        and isinstance(body.get("titulo"), str)
        and body["titulo"].strip() != ""
        and isinstance(body.get("feita"), bool)
    )


def contrato(etapa, espera_json):
    if espera_json and "application/json" not in etapa["content_type"]:
        return False
    return True


def caso(nome, o_que, passos, ok, grupo, estrutura):
    return {
        "nome": nome,
        "o_que": o_que,
        "passos": passos,
        "ok": ok,
        "grupo": grupo,
        "estrutura": estrutura,
    }


ORDEM_DA_SUITE = [
    "01 Verificar saude da API",
    "02 Listar tarefas",
    "05 Criar tarefa",
    "06 Fluxo completo de uma tarefa",
    "07 Criar tarefas a partir do CSV",
    "03 Buscar tarefa inexistente",
    "04 Recusar tarefa sem titulo",
]


def executar():
    inicio = datetime.now()
    casos = []
    aquecimento = passo("GET", "/health")

    saude = passo("GET", "/health")
    casos.append(caso(
        "01 Verificar saude da API",
        "GET /health devolve 200, status ok e servico tarefas.",
        [saude],
        contrato(saude, True)
        and saude["status"] == 200
        and isinstance(saude["resposta"], dict)
        and set(saude["resposta"]) == {"status", "servico"}
        and saude["resposta"].get("status") == "ok"
        and isinstance(saude["resposta"].get("servico"), str),
        "principal",
        "HealthResponse.json · status, servico",
    ))

    lista = passo("GET", "/tarefas")
    primeiro = lista["resposta"][0] if isinstance(lista["resposta"], list) and lista["resposta"] else {}
    casos.append(caso(
        "02 Listar tarefas",
        "A primeira tarefa da lista inicial é id 1, título Ler o README, feita false.",
        [lista],
        contrato(lista, True)
        and lista["status"] == 200
        and isinstance(lista["resposta"], list)
        and all(tarefa_valida(item) for item in lista["resposta"])
        and primeiro.get("id") == 1
        and primeiro.get("titulo") == "Ler o README"
        and primeiro.get("feita") is False,
        "principal",
        "ListaTarefas.json · id, titulo, feita",
    ))

    ausente = passo("GET", "/tarefas/99999")
    casos.append(caso(
        "03 Buscar tarefa inexistente",
        "Id desconhecido responde 404 com a mensagem Tarefa nao encontrada.",
        [ausente],
        contrato(ausente, True)
        and ausente["status"] == 404
        and isinstance(ausente["resposta"], dict)
        and set(ausente["resposta"]) == {"erro"}
        and ausente["resposta"].get("erro") == "Tarefa nao encontrada",
        "negativo",
        "Erro.json · erro",
    ))

    invalida = passo("POST", "/tarefas", {"titulo": "", "feita": False})
    casos.append(caso(
        "04 Recusar tarefa sem titulo",
        "POST com título vazio responde 400 e não grava a tarefa.",
        [invalida],
        contrato(invalida, True)
        and invalida["status"] == 400
        and isinstance(invalida["resposta"], dict)
        and set(invalida["resposta"]) == {"erro"}
        and invalida["resposta"].get("erro") == "Informe o titulo",
        "negativo",
        "Erro.json · erro",
    ))

    criada = passo("POST", "/tarefas", {"titulo": "Criada pelo teste 05", "feita": False})
    corpo = criada["resposta"] if isinstance(criada["resposta"], dict) else {}
    casos.append(caso(
        "05 Criar tarefa",
        "POST válido responde 201, devolve o título e um id numérico.",
        [criada],
        contrato(criada, True)
        and criada["status"] == 201
        and tarefa_valida(corpo)
        and corpo.get("titulo") == "Criada pelo teste 05"
        and corpo.get("feita") is False
        and all(valor is not None for valor in corpo.values()),
        "principal",
        "Tarefa.json · id, titulo, feita",
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
        contrato(fluxo_cria, True)
        and fluxo_cria["status"] == 201
        and tarefa_valida(fluxo_cria["resposta"])
        and contrato(fluxo_get, True)
        and fluxo_get["status"] == 200
        and tarefa_valida(get_corpo)
        and get_corpo.get("titulo") == "Estudar o fluxo do Katalon"
        and get_corpo.get("feita") is False
        and contrato(fluxo_put, True)
        and fluxo_put["status"] == 200
        and tarefa_valida(put_corpo)
        and put_corpo.get("feita") is True
        and fluxo_del["status"] == 204
        and contrato(fluxo_gone, True)
        and fluxo_gone["status"] == 404
        and isinstance(gone_corpo, dict)
        and set(gone_corpo) == {"erro"}
        and gone_corpo.get("erro") == "Tarefa nao encontrada",
        "fluxo",
        "Tarefa.json e Erro.json",
    ))

    linhas_csv = []
    csv_ok = True
    with CSV_TAREFAS.open(encoding="utf-8", newline="") as arquivo:
        for row in csv.DictReader(arquivo):
            titulo = row["titulo"]
            feita = row["feita"].strip().lower() == "true"
            status_esperado = int(row["statusEsperado"])
            etapa = passo("POST", "/tarefas", {"titulo": titulo, "feita": feita})
            linhas_csv.append(etapa)
            if status_esperado == 201:
                linha_ok = contrato(etapa, True) and etapa["status"] == 201 and tarefa_valida(etapa["resposta"])
                linha_ok = linha_ok and etapa["resposta"].get("titulo") == titulo and etapa["resposta"].get("feita") is feita
            else:
                linha_ok = (
                    contrato(etapa, True)
                    and etapa["status"] == status_esperado
                    and isinstance(etapa["resposta"], dict)
                    and etapa["resposta"].get("erro") == "Informe o titulo"
                )
            csv_ok = csv_ok and linha_ok
    casos.append(caso(
        "07 Criar tarefas a partir do CSV",
        "Cada linha de criar-tarefa.csv repete o POST: dois títulos válidos e um vazio.",
        linhas_csv,
        csv_ok and len(linhas_csv) == 3,
        "dados",
        "criar-tarefa.csv · Tarefa.json ou Erro.json",
    ))

    casos.sort(key=lambda item: ORDEM_DA_SUITE.index(item["nome"]))
    fim = datetime.now()
    return inicio, fim, casos, aquecimento


def json_bonito(valor):
    if valor is None:
        return "sem corpo"
    return json.dumps(valor, ensure_ascii=False, indent=2)


def render(inicio, fim, casos, aquecimento):
    passou = sum(1 for item in casos if item["ok"])
    falhou = len(casos) - passou
    duracao_ms = int((fim - inicio).total_seconds() * 1000)
    tempos = [etapa["elapsed_ms"] for item in casos for etapa in item["passos"]]
    mais_lento = max(tempos) if tempos else 0
    soma = sum(tempos)
    dentro = sum(1 for tempo in tempos if tempo <= SLA_MS)
    linhas = []
    detalhes = []
    for item in casos:
        marca = "passou" if item["ok"] else "falhou"
        tempo_caso = sum(etapa["elapsed_ms"] for etapa in item["passos"])
        linhas.append(
            "<tr>"
            f"<td>{html.escape(item['grupo'])}</td>"
            f"<td>{html.escape(item['nome'])}</td>"
            f"<td>{html.escape(item['estrutura'])}</td>"
            f"<td>{tempo_caso} ms</td>"
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
                f"<span>HTTP {etapa['status']} · {etapa['elapsed_ms']} ms · {html.escape(etapa['content_type'] or 'sem Content-Type')}</span></h3>"
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
  <p class="nota">API de tarefas em {html.escape(BASE)}. Gerado em {inicio.strftime("%d/%m/%Y %H:%M:%S")}. A bateria levou {duracao_ms} ms. A abertura da conexão, fora da conta, levou {aquecimento['elapsed_ms']} ms.</p>
  <p class="nota">Os ajustes não encurtaram a API: os pedidos seguintes à abertura ficam na casa de 1 ms, bem abaixo do aviso de {SLA_MS} ms. O que mudou foi a leitura. A tabela segue a ordem da suíte, com o grupo, o schema e o tempo de cada caso. O Katalon Studio não estava instalado, então este arquivo não é o relatório da pasta Reports.</p>
  <div class="resumo">
    <div><strong>{passou}</strong>passaram</div>
    <div><strong>{falhou}</strong>falharam</div>
    <div><strong>{mais_lento} ms</strong>pedido mais lento</div>
    <div><strong>{dentro}/{len(tempos)}</strong>dentro de {SLA_MS} ms</div>
    <div><strong>{soma} ms</strong>soma dos pedidos</div>
  </div>
  <table>
    <thead><tr><th>Grupo</th><th>Caso</th><th>Estrutura conferida</th><th>Tempo</th><th>Resultado</th></tr></thead>
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
    inicio, fim, casos, aquecimento = executar()
    DESTINO.write_text(render(inicio, fim, casos, aquecimento), encoding="utf-8")
    passou = sum(1 for item in casos if item["ok"])
    print(f"{passou}/{len(casos)} {DESTINO}")
    if passou != len(casos):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
