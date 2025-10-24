import json
import time
import sys
from pathlib import Path
from enum import Enum

from presentation_layer.utils.Session import Session


class AuthenticationAttemptsTracker():
    LOCKOUT_FILE = Path("lockout_state.json")
    MAX_ATTEMPTS = 5
    LOCK_DURATION = 60 * 5  # 5 minutes
    STRICT_LOCK_DURATION = 60 * 60 * 24  # a day

    def __init__(cls, ):
        pass

    @classmethod
    def load_state(cls):
        if cls.LOCKOUT_FILE.exists():
            with cls.LOCKOUT_FILE.open("r") as f:
                return json.load(f)
        return {"attempts": 0, "locked_until": 0, "banned": 0}

    @classmethod
    def save_state(cls, state):
        with cls.LOCKOUT_FILE.open("w") as f:
            json.dump(state, f)

    @classmethod
    def is_locked(cls, state):
        return time.time() < state["locked_until"]

    @classmethod
    def check_password(cls, password_input, correct_password):
        state = cls.load_state()

        if cls.is_locked(state):
            remaining = int(state["locked_until"] - time.time())
            print(f"Account locked. Try again in {remaining} seconds.")
            return AttemptsState.Locked

        if password_input == correct_password:
            print("Access granted.")
            cls.save_state({"attempts": 0, "locked_until": 0})
            return AttemptsState.Correct

        # Wrong password
        state["attempts"] = state.get("attempts", 0) + 1
        if state["attempts"] >= cls.MAX_ATTEMPTS:
            state["locked_until"] = time.time() + cls.LOCK_DURATION
            state["attempts"] = 0  # reset after lock
            print(f"Too many attempts! Locked for {cls.LOCK_DURATION//60} minutes.")
            cls.save_state(state)
            return AttemptsState.Locked
        else:
            print(f"Wrong password! {cls.MAX_ATTEMPTS - state['attempts']} attempts left.")
        cls.save_state(state)
        return AttemptsState.Wrong

    @classmethod
    def handle_tresspass(cls):
        state = cls.load_state()

        if cls.is_locked(state):
            return AttemptsState.Locked
        else:
            print("Error: Tresspass on system detected. Activity is logged.")
            state["banned"] = time.time() + cls.STRICT_LOCK_DURATION
            Session.set_loggedin_false()
            sys.exit()
            


class AttemptsState(Enum):
    Wrong = 0,
    Correct = 1,
    Locked = 2,
    Forbidden = 3
