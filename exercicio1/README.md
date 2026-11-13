# Exercício 1 - Cliente-Servidor TCP

## Requisitos
- Python 3.10 ou superior
- Nenhuma biblioteca externa necessária (apenas biblioteca padrão)

## Como executar

1. Inicie o servidor em um terminal:
```bash
python3 servidor.py --host 0.0.0.0 --port 5000
```

2. Em outro(s) terminal(is), inicie um ou mais clientes:
```bash
python3 cliente.py --host 127.0.0.1 --port 5000
```
