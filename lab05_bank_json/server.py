import socket
import json

class Bank:
    """Хранит баланс счёта и предоставляет три операции."""

    def __init__(self, initial=0):
        self._balance = initial
    def balance(self):
        return self._balance

    def deposit(self, amount):
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        if amount <= self._balance:
            self._balance -= amount
            return self._balance
        return None  # недостаточно средств

PORT = 9092
bank = Bank()
sock = socket.socket()
sock.bind(('', PORT))
sock.listen(1)
print("Bank server on port", PORT)

conn, addr = sock.accept()
print("client", addr)

# 1. Принять байты и разобрать JSON
data = conn.recv(1024).decode()
req = json.loads(data)
# 2. Обработать запрошенное действие
action = req.get("action")
if action == "balance":
    reply = {"ok": True, "balance": bank.balance()}
elif action == "deposit":
    amount = req.get("amount", 0)
    bank.deposit(amount)
    reply = {"ok": True, "balance": bank.balance()}
elif action == "withdraw":
    amount = req.get("amount", 0)
    result = bank.withdraw(amount)
    if result is not None:
        reply = {"ok": True, "balance": result}
    else:
        reply = {"ok": False, "error": "insufficient funds", "balance": bank.balance()}
else:
    reply = {"ok": False, "error": "unknown action"}
# 3. Отправить JSON-ответ
conn.send(json.dumps(reply).encode())
conn.close()
sock.close()
