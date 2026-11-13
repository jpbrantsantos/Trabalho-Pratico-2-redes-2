"""
Disciplina: Redes de Computadores II
Exercício 2: Servidor Echo UDP
Integrantes: João Pedro Brant Santos
"""

import socket
import argparse

# Tamanho máximo teórico de payload UDP sobre IPv4 (65535 - 20 IP - 8 UDP)
MAX_PAYLOAD_UDP = 65507


def iniciar_servidor(host: str, porta: int):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as srv:
        srv.bind((host, porta))
        print(f"Servidor Echo UDP ouvindo em {host}:{porta}...")

        try:
            while True:
                dados, addr = srv.recvfrom(MAX_PAYLOAD_UDP)
                msg = dados.decode("utf-8", errors="replace")
                print(f"[{addr[0]}:{addr[1]}] Recebido ({len(dados)} bytes): {msg}")

                # Devolve exatamente os mesmos bytes ao remetente
                srv.sendto(dados, addr)
        except KeyboardInterrupt:
            print("\nServidor UDP finalizado.")
        except Exception as erro:
            print(f"Erro no servidor UDP: {erro}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor Echo UDP")
    parser.add_argument("--host", default="0.0.0.0", help="Endereço IP de escuta")
    parser.add_argument("--port", type=int, default=6000, help="Porta UDP de escuta")
    args = parser.parse_args()

    iniciar_servidor(args.host, args.port)
