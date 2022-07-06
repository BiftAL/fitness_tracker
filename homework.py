from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFO_STRING: ClassVar[str] = ('Тип тренировки: {training_type};'
                                  ' Длительность: {duration:.3f} ч.;'
                                  ' Дистанция: {distance:.3f} км;'
                                  ' Ср. скорость: {speed:.3f} км/ч;'
                                  ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Возвращает готовую строку с данными о тренировке."""
        return self.INFO_STRING.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть объект с результатами тренировки."""
        training_type: str = self.__class__.__name__
        duration: float = self.duration
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        info_message: InfoMessage = InfoMessage(training_type, duration,
                                                distance, speed, calories)
        return info_message


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: ClassVar[float] = 18  # Не смог найти определения,
    COEFF_CALORIE_2: ClassVar[float] = 20  # просто коэффициенты из задания

    def get_spent_calories(self) -> float:
        """Расчет затраченных калорий при беге."""
        speed: float = self.get_mean_speed()
        duration_in_min: float = self.duration * self.MIN_IN_HOUR
        calories: float = ((self.COEFF_CALORIE_1 * speed
                           - self.COEFF_CALORIE_2)
                           * self.weight / self.M_IN_KM * duration_in_min)
        return calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float = 0

    COEFF_CALORIE_1: ClassVar[float] = 0.035
    COEFF_CALORIE_2: ClassVar[float] = 0.029
    DEGREE_OF_SPEED: ClassVar[int] = 2

    def get_spent_calories(self) -> float:
        """Расчет затраченных калорий при ходьбе."""
        speed: float = self.get_mean_speed()
        duration_in_min: float = self.duration * self.MIN_IN_HOUR
        calories: float = ((self.COEFF_CALORIE_1 * self.weight
                           + (speed ** self.DEGREE_OF_SPEED // self.height)
                           * self.COEFF_CALORIE_2 * self.weight)
                           * duration_in_min)
        return calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: int = 0
    count_pool: int = 0

    LEN_STEP: ClassVar[float] = 1.38
    COEFF_CALORIE_1: ClassVar[float] = 1.1
    COEFF_CALORIE_2: ClassVar[float] = 2

    def get_mean_speed(self) -> float:
        """Расчет средней скорости при плавании."""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Расчет затраченных калорий при плавании."""
        speed: float = self.get_mean_speed()
        calories: float = ((speed + self.COEFF_CALORIE_1)
                           * self.COEFF_CALORIE_2
                           * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return training_dict[workout_type](*data)
    except KeyError:
        print(f'Неизвестный вид тренировки {workout_type}.'
              ' для использования доступны следующие виды'
              f' тренировок: {list(training_dict)}')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
