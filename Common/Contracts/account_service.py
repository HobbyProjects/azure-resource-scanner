from abc import ABC, abstractmethod


class AccountService(ABC):

    @property
    def accounts(self):
        raise NotImplementedError("accounts is not implemented")
