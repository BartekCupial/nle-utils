"""
Adapted from NLE-language-wrapper https://github.com/ngoodger/nle-language-wrapper
"""

from functools import lru_cache
from typing import Dict, List

import gymnasium as gym
import nle
import numpy as np
from nle import nle_language_obsv
from transformers import RobertaTokenizerFast


class NLETokenizer(gym.Wrapper):
    LRU_CACHE_SIZE = 1000

    def __init__(self, env, max_token_length, tokenize_keys: List[str] = []):
        super().__init__(env)
        self.max_token_length = max_token_length
        self.tokenize_keys = tokenize_keys

        obs_spaces = {
            "input_ids": gym.spaces.Box(0, 1000000, shape=(self.max_token_length,), dtype=np.int32),
            "attention_mask": gym.spaces.Box(0, 1, shape=(self.max_token_length,), dtype=np.int32),
        }
        obs_spaces.update([(k, self.observation_space[k]) for k in self.observation_space])
        self.observation_space = gym.spaces.Dict(obs_spaces)

        self.action_space = self.env.action_space
        self.tokenizer = RobertaTokenizerFast.from_pretrained("distilroberta-base", truncation_side="left")
        self.nle_language = nle_language_obsv.NLELanguageObsv()

    # We use caching to avoid re-tokenizing observations that are already seen.
    @lru_cache(maxsize=LRU_CACHE_SIZE)
    def _tokenize(self, str_obsv):
        tokens = self.tokenizer(
            str_obsv,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=self.max_token_length,
        )
        return tokens.data

    def _nle_obs_to_language(self, nle_obs: Dict):
        """Translate NLE Observation into a language observation.
        Args:
            nle_obs (dict): NLE observation from the base environment
        Returns:
            (dict): language observation
        """
        glyphs = nle_obs["glyphs"]
        blstats = nle_obs["blstats"]
        tty_cursor = nle_obs["tty_cursor"]
        inv_strs = nle_obs["inv_strs"]
        inv_letters = nle_obs["inv_letters"]
        text_message = (
            nle_obs["text_message"]
            if "text_message" in nle_obs
            else self.nle_language.text_message(nle_obs["tty_chars"]).decode("latin-1")
        )

        return {
            "text_glyphs": self.nle_language.text_glyphs(glyphs, blstats).decode("latin-1"),
            "text_message": text_message,
            "text_blstats": self.nle_language.text_blstats(blstats).decode("latin-1"),
            "text_inventory": self.nle_language.text_inventory(inv_strs, inv_letters).decode("latin-1"),
            "text_cursor": self.nle_language.text_cursor(glyphs, blstats, tty_cursor).decode("latin-1"),
        }

    def _populate_obs(self, obs_dict: Dict):
        lang_obs = self._nle_obs_to_language(obs_dict)
        text = ""

        if "text_inventory" in self.tokenize_keys:
            text += f"Inventory:\n{lang_obs['text_inventory']}\n\n"
        if "text_blstats" in self.tokenize_keys:
            text += f"Stats:\n{lang_obs['text_blstats']}\n\n"
        if "text_cursor" in self.tokenize_keys:
            text += f"Cursor:\n{lang_obs['text_cursor']}\n\n"
        if "text_glyphs" in self.tokenize_keys:
            text += f"Observation:\n{lang_obs['text_glyphs']}\n\n"
        if "text_message" in self.tokenize_keys:
            text += f"Message:\n{lang_obs['text_message']}\n\n"

        text_obs = self._tokenize(text)
        obs_dict.update(text_obs)

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self._populate_obs(obs)

        return obs, info

    def step(self, action):
        obs, reward, term, trun, info = self.env.step(action)
        self._populate_obs(obs)

        return obs, reward, term, trun, info


if __name__ == "__main__":
    env = gym.make("NetHackScore-v0")
    env = NLETokenizer(env, max_token_length=512)

    obs = env.reset()
