# Exercício 2 - Servidor Echo UDP

## Requisitos
- Python 3.10 ou superior

## Como executar

1. Inicie o servidor UDP:
```bash
python3 servidor.py --host 0.0.0.0 --port 6000
```

2. Execute o cliente UDP:
```bash
python3 cliente.py --host 127.0.0.1 --port 6000 --timeout 3.0
```
