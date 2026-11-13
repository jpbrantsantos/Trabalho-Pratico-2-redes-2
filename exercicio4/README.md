# Exercício 4 - Servidor de Hora com Threads (TCP)

## Requisitos
- Python 3.10 ou superior

## Como executar

1. Inicie o servidor de hora:
```bash
python3 servidor.py --host 0.0.0.0 --port 7000
```

2. Execute o cliente para consultar a hora atual:
```bash
python3 cliente.py --host 127.0.0.1 --port 7000
```
