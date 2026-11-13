"""
Disciplina: Redes de Computadores II
Exercício 3: Servidor de Chat TCP
Integrantes: João Pedro Brant Santos
"""

import socket
import threading
import argparse

# Dicionário mapeando socket -> nickname e lock para acesso concorrente seguro
clientes = {}
lock_clientes = threading.Lock()


def broadcast(mensagem: str, remetente_conn: socket.socket = None):
    dados = mensagem.encode("utf-8")
    with lock_clientes:
        desconectados = []
        for conn in clientes:
            if conn != remetente_conn:
                try:
                    conn.sendall(dados)
                except Exception:
                    desconectados.append(conn)

        for conn in desconectados:
            clientes.pop(conn, None)


def gerenciar_usuario(conn: socket.socket, addr: tuple):
    nickname = None
    try:
        # Primeiro pacote recebido após conexão deve ser o nickname
        dados_nick = conn.recv(1024)
        if not dados_nick:
            return

        nickname = dados_nick.decode("utf-8").strip()
        if not nickname:
            nickname = f"Usuario_{addr[1]}"

        with lock_clientes:
            clientes[conn] = nickname

        print(f"[+] {nickname} ({addr[0]}:{addr[1]}) entrou no chat.")
        broadcast(f"*** {nickname} entrou na sala ***", remetente_conn=conn)

        while True:
            dados = conn.recv(1024)
            if not dados:
                break

            texto = dados.decode("utf-8").strip()
            if not texto:
                continue

            if texto.lower() == "sair":
                break

            msg_formatada = f"[{nickname}]: {texto}"
            print(msg_formatada)
            broadcast(msg_formatada, remetente_conn=conn)

    except ConnectionResetError:
        pass
    finally:
        with lock_clientes:
            nome_saida = clientes.pop(conn, nickname)
        conn.close()

        if nome_saida:
            print(f"[-] {nome_saida} saiu do chat.")
            broadcast(f"*** {nome_saida} saiu da sala ***")


def iniciar_servidor(host: str, porta: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, porta))
        srv.listen()
        print(f"Servidor de Chat ativo em {host}:{porta}...")

        try:
            while True:
                conn, addr = srv.accept()
                t = threading.Thread(target=gerenciar_usuario, args=(conn, addr), daemon=True)
                t.start()
        except KeyboardInterrupt:
            print("\nEncerrando servidor de chat...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor de Chat TCP")
    parser.add_argument("--host", default="0.0.0.0", help="IP de escuta")
    parser.add_argument("--port", type=int, default=5500, help="Porta TCP do chat")
    args = parser.parse_args()

    iniciar_servidor(args.host, args.port)
