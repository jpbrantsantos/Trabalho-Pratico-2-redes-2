"""
Disciplina: Redes de Computadores II
Exercício 1: Servidor TCP Multithread
Integrantes: João Pedro Brant Santos
"""

import socket
import threading
import argparse
from datetime import datetime


def atender_cliente(conn: socket.socket, addr: tuple):
    ip_cliente, porta_cliente = addr
    print(f"[+] Nova conexão de {ip_cliente}:{porta_cliente}")

    try:
        while True:
            dados = conn.recv(1024)
            if not dados:
                break

            mensagem = dados.decode("utf-8").strip()
            if not mensagem:
                continue

            agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"[{agora}] {ip_cliente}:{porta_cliente} -> {mensagem}")

            conn.sendall("Mensagem recebida".encode("utf-8"))
    except ConnectionResetError:
        print(f"[!] Conexão resetada abruptamente por {ip_cliente}:{porta_cliente}")
    except Exception as erro:
        print(f"[!] Erro ao atender {ip_cliente}:{porta_cliente}: {erro}")
    finally:
        conn.close()
        print(f"[-] Conexão encerrada: {ip_cliente}:{porta_cliente}")


def iniciar_servidor(host: str, porta: int):
    # SO_REUSEADDR evita erro de "Address already in use" ao reiniciar o servidor rápido
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, porta))
        srv.listen()
        print(f"Servidor TCP rodando em {host}:{porta}...")

        try:
            while True:
                conn, addr = srv.accept()
                t = threading.Thread(target=atender_cliente, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\nEncerrando servidor...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor TCP Multithread")
    parser.add_argument("--host", default="0.0.0.0", help="Endereço IP de escuta")
    parser.add_argument("--port", type=int, default=5000, help="Porta TCP de escuta")
    args = parser.parse_args()

    iniciar_servidor(args.host, args.port)
