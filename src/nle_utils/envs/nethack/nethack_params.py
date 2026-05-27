import ast

from nle_utils.utils.utils import str2bool


def add_extra_params_nethack_env(parser):
    """
    Specify any additional command line arguments for NetHack environments.
    """
    # TODO: add help
    p = parser
    p.add_argument("--character", type=str, default="@")
    p.add_argument("--max_episode_steps", type=int, default=None)
    p.add_argument("--single_seed", type=int, default=None)
    p.add_argument("--penalty_step", type=float, default=-0.01)
    p.add_argument("--penalty_time", type=float, default=0.0)
    p.add_argument("--reward_shaping_coefficient", type=float, default=0.1)
    p.add_argument("--fn_penalty_step", type=str, default="constant")
    p.add_argument("--savedir", type=str, default=None)
    p.add_argument("--save_ttyrec_every", type=int, default=0)
    p.add_argument("--gameloaddir", type=ast.literal_eval, default=None)
    p.add_argument("--state_counter", type=str, default=None)
    p.add_argument("--autopickup", type=str2bool, default=False)
    p.add_argument("--pet", type=str2bool, default=True)
    p.add_argument("--allow_all_yn_questions", type=str2bool, default=True)
    p.add_argument("--allow_all_modes", type=str2bool, default=True)
    p.add_argument(
        "--use_prev_action",
        type=str2bool,
        default=True,
        help="If True, the model will use previous action. Defaults to `True`",
    )
    p.add_argument(
        "--add_image_observation",
        type=str2bool,
        default=True,
        help="If True, the model will use previous action. Defaults to `True`",
    )
    p.add_argument("--crop_dim", type=int, default=18, help="Crop image around the player. Defaults to `18`.")
    p.add_argument(
        "--pixel_size",
        type=int,
        default=1,
        help="Rescales each character to size of `(pixel_size, pixel_size). Defaults to `6`.",
    )
    p.add_argument(
        "--obs_keys",
        type=ast.literal_eval,
        default=["screen_image", "tty_chars", "tty_colors", "env_steps", "prev_actions"],
        help="what obs we want to leave for training",
    )
    p.add_argument(
        "--tokenize_keys",
        type=ast.literal_eval,
        default=["text_glyphs", "text_message", "text_blstats", "text_inventory", "text_cursor"],
        help="what obs we want to use for tokenization",
    )
