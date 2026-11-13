# Exercício 3 - Chat em Rede (TCP)

## Requisitos
- Python 3.10 ou superior

## Como executar

1. Inicie o servidor central:
```bash
python3 servidor.py --host 0.0.0.0 --port 5500
```

2. Abra múltiplos terminais e conecte os clientes:
```bash
python3 cliente.py --host 127.0.0.1 --port 5500
```
