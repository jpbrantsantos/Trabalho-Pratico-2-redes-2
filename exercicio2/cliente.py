"""
Disciplina: Redes de Computadores II
Exercício 2: Cliente Echo UDP
Integrantes: João Pedro Brant Santos
"""

import socket
import argparse

MAX_PAYLOAD_UDP = 65507


def executar_cliente(host: str, porta: int, timeout: float):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cli:
        cli.settimeout(timeout)
        print(f"Pronto para enviar datagramas UDP para {host}:{porta} (timeout: {timeout}s).")
        print("Digite 'sair' para encerrar.")

        try:
            while True:
                msg = input("> ")

                if msg.strip().lower() == "sair":
                    break

                if not msg.strip():
                    print("Aviso: digite algum conteúdo antes de enviar.")
                    continue

                payload = msg.encode("utf-8")

                # Validação do limite máximo de bytes de um datagrama UDP
                if len(payload) > MAX_PAYLOAD_UDP:
                    print(f"Erro: mensagem excede o limite de {MAX_PAYLOAD_UDP} bytes ({len(payload)} bytes).")
                    continue

                cli.sendto(payload, (host, porta))

                try:
                    eco, servidor_addr = cli.recvfrom(MAX_PAYLOAD_UDP)
                    print(f"Eco de {servidor_addr[0]}:{servidor_addr[1]} -> {eco.decode('utf-8')}")
                except socket.timeout:
                    print("Timeout: nenhuma resposta recebida do servidor (pacote perdido ou servidor offline).")

        except KeyboardInterrupt:
            print("\nCliente UDP encerrado.")
        except OSError as erro:
            print(f"Erro de rede: {erro}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente Echo UDP")
    parser.add_argument("--host", default="127.0.0.1", help="IP do servidor")
    parser.add_argument("--port", type=int, default=6000, help="Porta UDP do servidor")
    parser.add_argument("--timeout", type=float, default=3.0, help="Tempo limite de resposta em segundos")
    args = parser.parse_args()

    executar_cliente(args.host, args.port, args.timeout)
