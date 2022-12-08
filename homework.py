"""The logic of a working fitness tracker for training
at running, walking, swimming."""
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Stores data about training."""

    ROUND_FLOAT_VAR = ':.3f'
    MESSAGE_STATIC_TEXT = ('Тип тренировки: {training_type}; '
                           f'Длительность: {{duration{ROUND_FLOAT_VAR}}} ч.; '
                           f'Дистанция: {{distance{ROUND_FLOAT_VAR}}} км; '
                           f'Ср. скорость: {{speed{ROUND_FLOAT_VAR}}} км/ч; '
                           f'Потрачено ккал: {{calories{ROUND_FLOAT_VAR}}}.')
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Formats the data and return a str."""
        message: str = self.MESSAGE_STATIC_TEXT.format(**asdict(self))
        return message


class Training:
    """Base class training."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Converts the distance to km."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Calcukates the average speed of movement."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Redefined in child based on the type."""
        raise NotImplementedError(f'In class "{self.__class__.__name__}" '
                                  'is not implemented method '
                                  '"get_spent_calories"')

    def show_training_info(self) -> InfoMessage:
        """Saves information about the completed workout in a special class
        and return his."""
        info: InfoMessage = InfoMessage(self.__class__.__name__,
                                        self.duration,
                                        self.get_distance(),
                                        self.get_mean_speed(),
                                        self.get_spent_calories())
        return info


class Running(Training):
    """Analyzes data about running training."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Calculation spent calories based on the formula
        for running training"""
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                            * self.get_mean_speed()
                            + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.weight
                           / self.M_IN_KM
                           * (self.duration * self.MIN_IN_H))
        return calories


class SportsWalking(Training):
    """Analyzes data about sports walking training."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Calculation spent calories based on the formula
        for sports walking training"""
        calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                            + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                               / (self.height / self.CM_IN_M))
                            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                            * self.weight)
                           * (self.duration * self.MIN_IN_H))
        return calories


class Swimming(Training):
    """Analyzes data about swimming training."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 1.1
    CALORIES_WEIGHT_SHIFT: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Calcukates the average speed of movement for swimming training."""
        speed: float = (self.length_pool * self.count_pool / self.M_IN_KM
                        / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Calculation spent calories based on the formula
        for swimming training"""
        calories: float = ((self.get_mean_speed()
                            + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                           * self.CALORIES_WEIGHT_SHIFT * self.weight
                           * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Read data and choise training."""
    types_training: dict[str, type[Training]] = {'WLK': SportsWalking,
                                                 'RUN': Running,
                                                 'SWM': Swimming}
    if workout_type in types_training:
        selected_training: Training = types_training[workout_type](*data)
        return selected_training
    raise ValueError(f'Unknown type of training "{workout_type}"')


def main(training: Training) -> None:
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[float]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
