class InsufficientBalanceError(Exception):
    pass


class InvalidAmountError(Exception):
    pass


class CustomerNotFoundError(Exception):
    pass


class SameAccountTransferError(Exception):
    pass