class GreenPotentialError(Exception):
    """Базовое исключение библиотеки."""


class EmptyDataError(GreenPotentialError):
    """Вызывается, когда GeoDataFrame пуст или не содержит подходящих данных."""


class InvalidGeometryError(GreenPotentialError):
    """Вызывается при отсутствии или невалидной геометрии."""


class MissingColumnError(GreenPotentialError):
    """Вызывается, когда в GeoDataFrame отсутствует обязательный столбец."""


class InvalidRoofTypeError(GreenPotentialError):
    """Вызывается при передаче недопустимого типа крыши."""


class InvalidYearError(GreenPotentialError):
    """Вызывается при некорректных данных о годе постройки."""
