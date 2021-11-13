import os
from json import JSONDecodeError, dumps, loads
from typing import Any, Optional

from src.lib.rd import rd


class Store:
    """
    Store "interface" to define the structure of a store.
    The actual store must be a class called ``SessionStore`` and
    should inherit this class.
    See an example of a redis store defined below.
    """

    session_id: str

    def __init__(self, session_id: str):
        """
        Here's where you'll create a map for the session ID in the store
        :param session_id: ID of the session. Guaranteed to be unique
        """
        # Remember to call super()!
        self.session_id = session_id

    def get(self, value: str) -> Optional[Any]:
        """
        Get a value from the user's session
        :param value: Key of the value
        """
        pass

    def set(self, value: str, to_set: Any) -> None:
        """
        Set the user's session in the store
        :param value: Key of the value
        :param to_set: Value to set. Will be JSON serialisable
        """
        pass

    def delete(self, value: str) -> bool:
        """
        Delete a value from the user's session
        :return: True if the value existed, false otherwise
        """
        pass

    def reset(self, new_id: str) -> bool:
        """
        Delete the user's session from the store and re-create it
        :param new_id: New session's ID
        :return: True if the session existed, false otherwise
        """
        pass


class SessionStore(Store):
    @property
    def _redis_key(self):
        return "session-" + self.session_id

    def __expire_session(self):
        rd.expire(self._redis_key, int(os.getenv("SESSION_EXPIRY", str(86400 * 7))))

    def __create_session(self):
        rd.set(self._redis_key, dumps({}))
        self.__expire_session()

    def __delete_session(self) -> int:
        return rd.delete(self._redis_key)

    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.set("id", session_id)

    def get(self, value: str) -> Optional[Any]:
        try:
            from_rd = rd.get(self._redis_key)
            if from_rd is None:
                raise JSONDecodeError("", "", 0)
            data = loads(from_rd)
            if type(data) != dict:
                raise JSONDecodeError("", "", 0)
            return data.get(value)
        except JSONDecodeError:
            self.reset(self.session_id)
            return None

    def set(self, value: str, to_set: Any) -> None:
        try:
            from_rd = rd.get(self._redis_key)
            if from_rd is None:
                raise JSONDecodeError("", "", 0)
            data = loads(from_rd)
            if type(data) != dict:
                raise JSONDecodeError("", "", 0)
            data[value] = to_set
            rd.set(self._redis_key, dumps(data))
        except JSONDecodeError:
            self.reset(self.session_id)
            rd.set(self._redis_key, dumps({value: to_set, "id": self.session_id}))
        self.__expire_session()

    def delete(self, value: str) -> bool:
        try:
            from_rd = rd.get(self._redis_key)
            if from_rd is None:
                raise JSONDecodeError("", "", 0)
            data = loads(from_rd)
            if type(data) != dict:
                raise JSONDecodeError("", "", 0)
            del data[value]
            rd.set(self._redis_key, dumps(data))
            self.__expire_session()
            return True
        except JSONDecodeError:
            self.reset(self.session_id)
            return False

    def reset(self, new_id: str) -> bool:
        to_return = bool(self.__delete_session())
        self.session_id = new_id
        self.__create_session()
        self.set("id", new_id)
        return to_return
