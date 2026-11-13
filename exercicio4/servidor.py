"""
Disciplina: Redes de Computadores II
Exercício 4: Servidor de Hora Multithread com Lock
Integrantes: João Pedro Brant Santos
"""

import socket
import threading
import argparse
from datetime import datetime

total_atendimentos = 0
lock_contador = threading.Lock()


def tratar_requisicao(conn: socket.socket, addr: tuple):
    global total_atendimentos
    ip_cli, porta_cli = addr

    try:
        # Aguarda a solicitação do cliente antes de responder
        solicitacao = conn.recv(1024)
        if not solicitacao:
            return

        agora = datetime.now()
        hora_formatada = agora.strftime("%H:%M:%S")
        data_log = agora.strftime("%Y-%m-%d %H:%M:%S")

        # Região crítica: garante incremento atômico do contador entre threads
        with lock_contador:
            total_atendimentos += 1
            num_atual = total_atendimentos

        conn.sendall(hora_formatada.encode("utf-8"))
        print(f"[{data_log}] Cliente {ip_cli}:{porta_cli} atendido | Hora enviada: {hora_formatada} | Total atendimentos: {num_atual}")

    except Exception as erro:
        print(f"[ERRO] Falha ao atender cliente {ip_cli}:{porta_cli}: {erro}")
    finally:
        conn.close()


def iniciar_servidor(host: str, porta: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, porta))
        srv.listen()
        print(f"Servidor de Hora TCP rodando em {host}:{porta}...")

        try:
            while True:
                conn, addr = srv.accept()
                t = threading.Thread(target=tratar_requisicao, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\nServidor de Hora finalizado.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor de Hora TCP Multithread")
    parser.add_argument("--host", default="0.0.0.0", help="IP de escuta")
    parser.add_argument("--port", type=int, default=7000, help="Porta TCP de escuta")
    args = parser.parse_args()

    iniciar_servidor(args.host, args.port)
