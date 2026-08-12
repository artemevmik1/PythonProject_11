import logging

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/masks.log", encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Функция проверяет размер номера карты на корректность
    и затем маскирует в формате XXXX XX** **** XXXX
    """
    logger.debug(f"Выполняем проверку на переданный номер карты {card_number}")
    if card_number is None:
        raise ValueError("номер карты не может быть None")

    logger.debug(f"Выполняем проверку на 16-ти значный номер карты {card_number}")
    if (len(card_number)) != 16 or not card_number.isdigit():
        raise ValueError("номер карты должен состоять и 16 цифр")

    logger.debug(f"Маскируем карту {card_number}")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(okaunt_number: str) -> str:
    """
    Функция проверяет размер номера счета на корректность
    и затем маскирует в формате **XXXX
    """
    logger.debug(f"Выполняем проверку на переданный номер счета{okaunt_number}")
    if okaunt_number is None:
        raise ValueError("номер счета не может быть None")

    logger.debug(f"Выполняем проверку на 20-ти значный номер карты {okaunt_number}")
    if (len(okaunt_number)) != 20 or not okaunt_number.isdigit():
        raise ValueError("номер счета должен состоять и 20 цифр")

    logger.debug(f"Маскируем счет {okaunt_number}")
    return f"**{okaunt_number[-4:]}"
