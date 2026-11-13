"""
Disciplina: Redes de Computadores II
Exercício 4: Cliente de Hora TCP
Integrantes: João Pedro Brant Santos
"""

import socket
import argparse


def consultar_hora(host: str, porta: int):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
            cli.connect((host, porta))
            cli.sendall("GET_TIME".encode("utf-8"))

            resposta = cli.recv(1024).decode("utf-8")
            if resposta:
                print(f"Hora oficial do servidor ({host}:{porta}): {resposta}")
            else:
                print("Servidor fechou a conexão sem enviar a hora.")

    except ConnectionRefusedError:
        print(f"Erro: servidor indisponível em {host}:{porta}.")
    except Exception as erro:
        print(f"Erro de comunicação: {erro}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente de Hora TCP")
    parser.add_argument("--host", default="127.0.0.1", help="IP do servidor")
    parser.add_argument("--port", type=int, default=7000, help="Porta TCP do servidor")
    args = parser.parse_args()

    consultar_hora(args.host, args.port)
