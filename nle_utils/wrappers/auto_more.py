import re

import gymnasium as gym
from nle.nethack import actions as A
from nle.nethack import tty_render


class AutoMore(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        obs["text_message"] = self.message_and_popup(obs)
        self.last_text_message = obs["text_message"]

        return obs, info

    def step(self, action):
        obs, reward, term, trun, info = self.env.step(action)
        done = term or trun

        message = self.message_and_popup(obs)

        while "--More--" in message and not done:
            message = message.replace("--More--", "")

            action_index = self.env.actions.index(A.MiscAction.MORE)
            obs, rew, term, trun, info = self.env.step(action_index)
            add = self.message_and_popup(obs)
            message += add
            reward += rew

        obs["text_message"] = message
        self.last_text_message = obs["text_message"]

        return obs, reward, term, trun, info

    def find_marker(self, lines):
        """Return (line, column) of markers:
        --More-- | (end) | (X of N)
        """
        regex = re.compile(r"(--More--|\(end\)|\(\d+ of \d+\))")
        if len(regex.findall(" ".join(lines))) > 1:
            raise ValueError("Too many markers")

        result, marker_type = None, None
        for i, line in enumerate(lines):
            res = regex.findall(line)
            if res:
                assert len(res) == 1
                j = line.find(res[0])
                result, marker_type = (i, j), res[0]
                break

        # Special case: adjust column position if marker starts at position
        if result is not None and result[1] == 1:
            result = (result[0], 0)  # Normalize to start of line
        return result, marker_type

    def message_and_popup(self, obs):
        # Decode and clean up message and TTY characters
        message = bytes(obs["message"]).decode("latin-1").strip("\0")

        popup = []
        lines = [bytes(line).decode("latin-1").strip("\0") for line in obs["tty_chars"]]
        marker_pos, marker_type = self.find_marker(lines)

        # If no marker found, combine message and popup directly
        if marker_pos is None:
            return self.combine_message_and_popup(message, popup)

        pref = ""
        message_lines_count = 0
        if message:
            # Try to find where the message ends in the TTY output
            for i, line in enumerate(lines[: marker_pos[0] + 1]):
                if i == marker_pos[0]:
                    line = line[: marker_pos[1]]
                message_lines_count += 1
                pref += line.strip()

                # Compare message and screen text (ignoring non-alphanumeric chars)
                def replace_func(x):
                    return "".join(c for c in x if c.isalnum())

                if replace_func(pref) == replace_func(message):
                    break
            else:
                # Handle special case for --More-- in first line
                if marker_pos[0] == 0:
                    return self.combine_message_and_popup(message, popup, marker_type)
                raise ValueError(f"Message:\n{repr(message)}\ndoesn't match the screen:\n{repr(pref)}")

        # Extract popup content (text between message and marker)
        for line in lines[message_lines_count : marker_pos[0]] + [lines[marker_pos[0]][: marker_pos[1]]]:
            line = line[marker_pos[1] :].strip()
            if line:
                popup.append(line)

        return self.combine_message_and_popup(message, popup, marker_type)

    def combine_message_and_popup(self, message, popup, marker_type=None):
        # Combine message, popup content, and marker into single string
        message = [message] if message else []
        result = message + popup
        if marker_type:
            result.append(marker_type)
        return "\n".join(result)

    def render(self, mode="human", **kwargs):
        if mode == "human":
            print(self.last_text_message)
            env = self.env.unwrapped
            obs = env.last_observation
            tty_chars = obs[env._observation_keys.index("tty_chars")]
            tty_colors = obs[env._observation_keys.index("tty_colors")]
            tty_cursor = obs[env._observation_keys.index("tty_cursor")].copy()
            tty_cursor[0] += 1
            print(tty_render(tty_chars[1:], tty_colors[1:], tty_cursor))
        else:
            return self.env.render(mode, **kwargs)
