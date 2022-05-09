import json
import time
from collections import OrderedDict
from cs_bot.util.lru_cache import LRUCache
from cs_bot.util.singleton import Singleton
from cs_bot.config import MAX_USERS_ONLINE


_DEFAULT_MAX_POLLS_BY_USER = 3


class Poll:
    class State:
        NOT_SENT = 'not_sent'
        WAIT_FOR_ANSWER = 'wait_for_answer'
        ANSWERED = 'answered'

    def __init__(self, chat_id, test_unit):
        self._chat_id = chat_id
        self._poll_id = None
        self._test_unit_id = test_unit['id']
        self._purpose = test_unit['purpose']
        self._difficulty = test_unit['difficulty']
        self._question = test_unit['question']
        self._options = json.loads(test_unit['options'])
        self._answer_ind = test_unit['answer_ind']
        self._explanation = test_unit['explanation']
        self._state = self.State.NOT_SENT
        self._user_answer_ind = None

    @property
    def test_unit_id(self):
        return self._test_unit_id

    @property
    def purpose(self):
        return self._purpose

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def question(self):
        return self._question

    @property
    def options(self):
        return self._options

    @property
    def answer_ind(self):
        return self._answer_ind

    @property
    def explanation(self):
        return self._explanation

    @property
    def state(self):
        return self._state

    @property
    def is_answer_correct(self):
        return self._user_answer_ind == self._answer_ind

    def on_sending(self, poll_id):
        self._poll_id = poll_id
        self._state = self.State.WAIT_FOR_ANSWER

    def on_answer(self, user_answer_ind):
        self._user_answer_ind = user_answer_ind
        self._state = self.State.ANSWERED


class PollSeria:
    def __init__(self, polls, tags=None):
        self._polls = polls
        self._tags = tags or []
        self._next_poll_ind = 0
        self._correct_answers = 0
        self._last_update = int(time.time())

    @property
    def tags(self):
        return self._tags

    @property
    def last_update(self):
        return self._last_update

    @property
    def correct_answers(self):
        return self._correct_answers

    @property
    def size(self):
        return len(self._polls)

    @property
    def next_poll(self):
        if self._next_poll_ind >= len(self._polls):
            return None
        return self._polls[self._next_poll_ind]

    def on_sending(self, poll_id):
        self.next_poll.on_sending(poll_id)
        self._last_update = int(time.time())

    def on_answer(self, user_answer_ind):
        self.next_poll.on_answer(user_answer_ind)
        self._correct_answers += self.next_poll.is_answer_correct
        self._next_poll_ind += 1
        self._last_update = int(time.time())

    def __iter__(self):
        return iter(self._polls)


class PollSeriaController(metaclass=Singleton):
    def __init__(self):
        self._max_users = MAX_USERS_ONLINE
        self._max_polls_by_user = _DEFAULT_MAX_POLLS_BY_USER
        self._state = LRUCache(max_size=self._max_users, default_value=OrderedDict())

    def has(self, chat_id, poll_id, tags=None, tags_like=None):
        if chat_id not in self._state or poll_id not in self._state[chat_id]:
            return False
        if tags is None and tags_like is None:
            return True
        poll_seria = self._state[chat_id][poll_id]
        if tags is not None:
            return len(poll_seria.tags) == len(tags) and poll_seria.tags == tags
        if tags_like is not None:
            if len(poll_seria.tags) != len(tags_like):
                return False
            for tag, tag_like in zip(poll_seria.tags, tags_like):
                if isinstance(tag_like, str) and tag != tag_like:
                    return False
                if isinstance(tag_like, list) and tag not in tag_like:
                    return False
        return True

    def get(self, chat_id, poll_id):
        if self.has(chat_id, poll_id):
            return self._state[chat_id][poll_id]
        return None

    def update(self, chat_id, poll_id, poll_seria, new_poll_id=None):
        if poll_id is not None:
            del self._state[chat_id][poll_id]
        if new_poll_id is not None:
            self._state[chat_id][new_poll_id] = poll_seria
