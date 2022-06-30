from typing import Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращает готовую строку с данными о тренировке."""
        message_string: str = (f'Тип тренировки: {self.training_type}; '
                               f'Длительность: {self.duration:.3f} ч.; '
                               f'Дистанция: {self.distance:.3f} км; '
                               f'Ср. скорость: {self.speed:.3f} км/ч; '
                               f'Потрачено ккал: {self.calories:.3f}.')
        return message_string


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
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
    def get_spent_calories(self) -> float:
        """Расчет затраченых калорий при беге."""
        speed: float = self.get_mean_speed()
        coeff_colorie_1: float = 18
        coeff_colorie_2: float = 20
        duration_in_min: float = self.duration * self.MIN_IN_HOUR
        calories: float = ((coeff_colorie_1 * speed - coeff_colorie_2) *
                           self.weight / self.M_IN_KM * duration_in_min)
        return calories
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчет затраченых калорий при ходьбе."""
        speed: float = self.get_mean_speed()
        coeff_colorie_1: float = 0.035
        coeff_colorie_2: float = 0.029
        duration_in_min: float = self.duration * self.MIN_IN_HOUR
        calories: float = ((coeff_colorie_1 * self.weight +
                           (speed ** 2 // self.height) *
                           coeff_colorie_2 * self.weight) *
                           duration_in_min)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Расчет средней скорости при плавании."""
        speed: float = (self.length_pool * self.count_pool /
                        self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Расчет затраченых колорий при плавании."""
        speed: float = self.get_mean_speed()
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: float = 2
        calories: float = ((speed + coeff_calorie_1) * coeff_calorie_2 *
                           self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_dict[workout_type](*data)


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
