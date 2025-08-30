# -*- coding: utf-8 -*-
# Курс: AI+Python
# Модуль 11. ООП
# Тема: ООП. Частина 2
#  Завдання
# Напишіть клас Банківський рахунок з атрибутами:
#  ім'я клієнта
#  баланс
#  валюта
#  словник з курсом валют(однаковий для всіх)
# Додайте методи:
#  вивід загальної інформації
#  перевірка чи відома валюта(якщо ні, викликати
# ValueError)
#  перевести гроші з однієї валюти в іншу(ця операція
# часто використовується, тому зрочно реалізувати
# окремим методом)
#  зміна валюти
#  поповнення балансу(валюта та сама)
#  зняття грошей з балансу(валюта та сама).
import sys

# Режим тестування: якщо True — не завершуємо програму при помилках, лише повідомляємо
DEBUG: bool = True

def _gentle_exit(message: str, operation: str | None = None) -> None:
    """
    Виводить повідомлення про помилку.
    - У звичайному режимі завершує програму.
    - У режимі DEBUG — лише повідомляє і продовжує виконання.
    Також друкує пояснення, яка операція не виконана і чому.
    """
    suffix = " [DEBUG: продовжуємо виконання]" if DEBUG else ""
    print(f"{message}.{suffix}")
    if DEBUG:
        print(f"Операція не виконана: {operation or 'невідома операція'} — {message}")
    if not DEBUG:
        sys.exit(1)

# реалізація класу з валідацією, конвертацією та базовими операціями з балансом.
class BankAccount:
    """
    Клас Банківський рахунок.
    Курс обміну зберігається як значення 1 одиниці валюти у гривнях (UAH).
    Напр.: exchange_rates['USD'] = 41.0 означає 1 USD = 41.0 UAH.
    """

    # спільний для всіх екземплярів словник курсів валют
    # (одиниця валюти у гривнях)
    exchange_rates: dict[str, float] = {
        "UAH": 1.0,
        "USD": 41.0,
        "EUR": 45.0,
        "PLN": 10.0,
    }

    def __init__(self, client_name: str, balance: float, currency: str) -> None:
        self._validate_currency(currency, op="Ініціалізація рахунку")
        self._validate_non_negative(balance, "Початковий баланс має бути невід’ємним", op="Ініціалізація рахунку")
        # Безпечна ініціалізація у разі діагностичних помилок у DEBUG
        if currency is None or currency.upper() not in self.exchange_rates or balance is None or float(balance) < 0:
            self.client_name = client_name or "Невідомий"
            self.balance = 0.0
            self.currency = "UAH"
            return
        self.client_name = client_name
        self.balance = float(balance)
        self.currency = currency.upper()

    def __repr__(self) -> str:
        return f"BankAccount(client_name={self.client_name!r}, balance={self.balance:.2f}, currency={self.currency})"

    def __str__(self) -> str:
        return self.info()

    # --- Службові перевірки ---
    @classmethod
    def _validate_currency(cls, currency: str, op: str | None = None) -> None:
        if currency is None:
            _gentle_exit("валюта не задана", operation=op)
            return
        cur = currency.upper()
        if cur not in cls.exchange_rates:
            _gentle_exit(f"невідома валюта: {currency}", operation=op)
            return

    @staticmethod
    def _validate_positive(amount: float, message: str = "Сума має бути більшою за 0", op: str | None = None) -> None:
        if amount is None or float(amount) <= 0:
            _gentle_exit(message, operation=op)
            return

    @staticmethod
    def _validate_non_negative(amount: float, message: str = "Значення має бути невід’ємним", op: str | None = None) -> None:
        if amount is None or float(amount) < 0:
            _gentle_exit(message, operation=op)
            return

    # --- Загальна інформація ---
    def info(self) -> str:
        return f"Клієнт: {self.client_name} | Баланс: {self.balance:.2f} {self.currency}"

    # --- Конвертація валют ---
    @classmethod
    def convert(cls, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Конвертувати amount з from_currency у to_currency, використовуючи загальні курси.
        Курс зберігається як вартість 1 одиниці валюти у гривнях (UAH).
        Формула: amount * rate[from] / rate[to]
        """
        cls._validate_currency(from_currency, op="Конвертація")
        cls._validate_currency(to_currency, op="Конвертація")
        BankAccount._validate_non_negative(amount, "Сума для конвертації має бути невід’ємною", op="Конвертація")
        if amount is None or float(amount) < 0:
            return 0.0
        if from_currency is None or to_currency is None:
            return 0.0
        fr = from_currency.upper()
        to = to_currency.upper()
        if fr not in cls.exchange_rates or to not in cls.exchange_rates:
            return 0.0
        if float(amount) == 0:
            return 0.0
        return float(amount) * cls.exchange_rates[fr] / cls.exchange_rates[to]

    # --- Операції над рахунком ---
    def change_currency(self, new_currency: str) -> None:
        """
        Змінює валюту рахунку, конвертуючи поточний баланс у нову валюту.
        """
        self._validate_currency(new_currency, op="Зміна валюти")
        if new_currency is None:
            return
        new_cur = new_currency.upper()
        if new_cur not in self.exchange_rates:
            return
        if new_cur == self.currency:
            return
        self.balance = self.convert(self.balance, self.currency, new_cur)
        self.currency = new_cur

    def deposit(self, amount: float) -> None:
        """
        Поповнення балансу (у тій самій валюті рахунку).
        """
        self._validate_positive(amount, "Сума поповнення має бути більшою за 0", op="Поповнення")
        if amount is None or float(amount) <= 0:
            return
        self.balance += float(amount)

    def withdraw(self, amount: float) -> None:
        """
        Зняття коштів з балансу (у тій самій валюті рахунку).
        """
        self._validate_positive(amount, "Сума зняття має бути більшою за 0", op="Зняття коштів")
        if amount is None or float(amount) <= 0:
            return
        amount = float(amount)
        if amount > self.balance:
            _gentle_exit("недостатньо коштів на рахунку для цієї операції", operation="Зняття коштів")
            return
        self.balance -= amount

    # --- Робота з курсами ---
    @classmethod
    def set_exchange_rate(cls, currency: str, value_in_uah: float) -> None:
        """
        Встановити/оновити курс для валюти (одиниця валюти у гривнях).
        """
        if not currency:
            _gentle_exit("валюта не задана", operation="Оновлення курсу")
            return
        cls._validate_positive(value_in_uah, "Курс має бути більшим за 0", op="Оновлення курсу")
        if value_in_uah is None or float(value_in_uah) <= 0:
            return
        cls.exchange_rates[currency.upper()] = float(value_in_uah)

    @classmethod
    def set_exchange_rates(cls, rates: dict[str, float]) -> None:
        """
        Масове оновлення курсів. Усі значення мають бути > 0.
        """
        if not isinstance(rates, dict) or not rates:
            _gentle_exit("передано некоректний словник курсів", operation="Масове оновлення курсів")
            return
        for cur, val in rates.items():
            if not cur or float(val) <= 0:
                _gentle_exit(f"некоректний курс для {cur!r}: {val}", operation="Масове оновлення курсів")
                return
        # Оновлюємо одразу, якщо всі валюти валідні
        cls.exchange_rates.update({k.upper(): float(v) for k, v in rates.items()})


def run_demo() -> None:
    print("=== БАЗОВИЙ СЦЕНАРІЙ ===")
    acc = BankAccount("Іван Іванов", 1000, "UAH")
    print(acc.info())

    print("\n— Поповнення 500 UAH")
    acc.deposit(500)
    print(acc.info())

    print("\n— Конвертація 100 EUR → USD (приклад без впливу на баланс)")
    usd_amount = BankAccount.convert(100, "EUR", "USD")
    print(f"100 EUR = {usd_amount:.2f} USD")

    print("\n— Зміна валюти рахунку UAH → USD")
    acc.change_currency("USD")
    print(acc.info())

    print("\n— Зняття 50 USD (може бути недостатньо коштів)")
    acc.withdraw(50)
    print(acc.info())

    print("\n=== НЕКОРЕКТНІ СУМИ ===")
    print("— Поповнення 0")
    acc.deposit(0)
    print("— Поповнення -10")
    acc.deposit(-10)

    print("\n— Зняття 0")
    acc.withdraw(0)
    print("— Зняття -5")
    acc.withdraw(-5)

    print("\n=== КОНВЕРТАЦІЯ: НУЛЬ, ВІД’ЄМНА, НЕВІДОМА ВАЛЮТА ===")
    print("— Конвертація 0 USD → EUR")
    print("Результат:", BankAccount.convert(0, "USD", "EUR"))
    print("— Конвертація -100 USD → EUR")
    print("Результат:", BankAccount.convert(-100, "USD", "EUR"))
    print("— Конвертація 50 XXX → USD (невідома валюта)")
    print("Результат:", BankAccount.convert(50, "XXX", "USD"))

    print("\n=== ЗМІНА ВАЛЮТИ: ТА САМА, НЕВІДОМА ===")
    print("— Зміна валюти на поточну (USD → USD)")
    acc.change_currency("USD")
    print(acc.info())
    print("— Зміна валюти на невідому (YYY)")
    acc.change_currency("YYY")
    print(acc.info())

    print("\n=== ОНОВЛЕННЯ КУРСІВ ===")
    print("— Оновлення окремого курсу з помилкою (валюта не задана)")
    BankAccount.set_exchange_rate("", 50)
    print("— Оновлення окремого курсу з помилкою (некоректне значення)")
    BankAccount.set_exchange_rate("GBP", 0)
    print("— Оновлення окремого курсу коректно")
    BankAccount.set_exchange_rate("GBP", 52.5)
    print("Поточні курси:", BankAccount.exchange_rates)

    print("\n— Масове оновлення курсів: некоректний словник")
    BankAccount.set_exchange_rates({})
    print("— Масове оновлення курсів: є помилкове значення")
    BankAccount.set_exchange_rates({"CHF": -1, "JPY": 0.27})
    print("— Масове оновлення курсів: коректно")
    BankAccount.set_exchange_rates({"CHF": 46.0, "JPY": 0.27})
    print("Поточні курси:", BankAccount.exchange_rates)

    print("\n=== ЗАКІНЧЕННЯ ДЕМО ===")


if __name__ == "__main__":
    run_demo()