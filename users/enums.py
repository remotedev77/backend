from enum import Enum

class ClosedTestEnum(Enum):
    final_test = "Итоговое тестирование"
    simulation = "Симулятор экзамена"
    marathon = "Марафон"
    not_decide = "Не решал"
    know = "Знаю"
    make_mistake = "Делаю ошибки"
    not_know = "Не знаю"


class MessageStatus(Enum):

    @classmethod
    def get_string_value(cls, value):
        mapping = {
            0: "в очереди",
            1: "доставлено",
            2: "не доставлено",
            3: "передано",
            8: "на модерации",
            6: "сообщение отклонено",
            4: "ожидание статуса сообщения"
        }
        return mapping.get(value, "Unknown")