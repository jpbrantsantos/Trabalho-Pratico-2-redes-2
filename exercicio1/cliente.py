"""
Disciplina: Redes de Computadores II
Exercício 1: Cliente TCP
Integrantes: João Pedro Brant Santos
"""

import socket
import argparse


def executar_cliente(host: str, porta: int):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
            cli.connect((host, porta))
            print(f"Conectado ao servidor {host}:{porta}. Digite 'sair' para encerrar.")

            while True:
                msg = input("> ")

                if msg.strip().lower() == "sair":
                    print("Encerrando conexão...")
                    break

                # Evita envio de string vazia ou apenas espaços
                if not msg.strip():
                    print("Aviso: mensagem vazia não foi enviada.")
                    continue

                cli.sendall(msg.encode("utf-8"))
                resposta = cli.recv(1024).decode("utf-8")

                if not resposta:
                    print("Servidor encerrou a conexão.")
                    break

                print(f"Servidor: {resposta}")

    except ConnectionRefusedError:
        print(f"Erro: não foi possível conectar a {host}:{porta}. Verifique se o servidor está ativo.")
    except KeyboardInterrupt:
        print("\nCliente finalizado pelo usuário.")
    except Exception as erro:
        print(f"Erro inesperado na comunicação: {erro}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente TCP")
    parser.add_argument("--host", default="127.0.0.1", help="IP do servidor")
    parser.add_argument("--port", type=int, default=5000, help="Porta TCP do servidor")
    args = parser.parse_args()

    executar_cliente(args.host, args.port)
