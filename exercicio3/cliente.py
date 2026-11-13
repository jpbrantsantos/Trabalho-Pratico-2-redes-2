"""
Disciplina: Redes de Computadores II
Exercício 3: Cliente de Chat TCP
Integrantes: João Pedro Brant Santos
"""

import socket
import threading
import argparse


def receber_mensagens(sock: socket.socket, evento_parada: threading.Event):
    while not evento_parada.is_set():
        try:
            dados = sock.recv(1024)
            if not dados:
                print("\n[!] Conexão encerrada pelo servidor.")
                evento_parada.set()
                break
            # \r limpa a linha do prompt atual antes de imprimir a mensagem recebida
            print(f"\r{dados.decode('utf-8')}\n> ", end="", flush=True)
        except OSError:
            break


def iniciar_cliente(host: str, porta: int):
    nickname = ""
    while not nickname.strip():
        nickname = input("Escolha seu nickname: ").strip()

    evento_parada = threading.Event()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
            cli.connect((host, porta))
            cli.sendall(nickname.encode("utf-8"))

            print(f"Conectado ao chat como '{nickname}'. Digite 'sair' para desconectar.")

            thread_leitura = threading.Thread(
                target=receber_mensagens,
                args=(cli, evento_parada),
                daemon=True
            )
            thread_leitura.start()

            while not evento_parada.is_set():
                msg = input("> ")

                if evento_parada.is_set():
                    break

                if msg.strip().lower() == "sair":
                    cli.sendall("sair".encode("utf-8"))
                    evento_parada.set()
                    break

                if msg.strip():
                    cli.sendall(msg.encode("utf-8"))

    except ConnectionRefusedError:
        print(f"Erro: servidor indisponível em {host}:{porta}.")
    except KeyboardInterrupt:
        print("\nSaindo do chat...")
    finally:
        evento_parada.set()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente de Chat TCP")
    parser.add_argument("--host", default="127.0.0.1", help="IP do servidor")
    parser.add_argument("--port", type=int, default=5500, help="Porta TCP do servidor")
    args = parser.parse_args()

    iniciar_cliente(args.host, args.port)
