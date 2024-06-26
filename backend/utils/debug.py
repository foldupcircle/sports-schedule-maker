import re
import colorsys
import inspect
# from utils.log_mode import get_log_mode
from .log_config import log_config

def adjust_brightness(color, brightness_factor):
    hls = colorsys.rgb_to_hls(*[x/255.0 for x in color]) # Convert RGB to HLS
    hls = (hls[0], max(0, min(1, hls[1] + brightness_factor)), hls[2]) # Adjust lightness
    rgb = [int(x*255.0) for x in colorsys.hls_to_rgb(*hls)] # Convert back to RGB
    return rgb

# colors
red = (255, 0, 0)
light_red_1 = adjust_brightness(red, 0.15)
light_red_2 = adjust_brightness(red, 0.3)
orange = (255, 165, 0)
light_orange_1 = adjust_brightness(orange, 0.15)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_blue_1 = adjust_brightness(blue, 0.15)
purple = (128, 0, 128)
pink = (255, 192, 203)
white = (255, 255, 255)
black = (0, 0, 0)

MAIN_COLORS = {name: light_blue_1 for name in ['main']}
TEAM_COLORS = {f'Team.{name}': light_red_2 for name in ['__init__', '_set_conference', '_set_inter_conference_division', '_set_intra_conference_division']}
STADIUM_COLORS = {f'Stadium.{name}': light_red_2 for name in ['__init__']}
MATCHUPS_COLORS = {name: light_orange_1 for name in ['determine_matchups']}
UTIL_COLORS = {name: yellow for name in ['convert_teams_to_dict', 'choose_league', 'check_matchup']}
SOLVE_COLORS = {f'Solver.{name}': purple for name in ['__init__', 'solve', '_sort_matrix', '_add_constraints', '_add_cost']}

COLORS = {}
COLORS.update(MAIN_COLORS)
COLORS.update(TEAM_COLORS)
COLORS.update(STADIUM_COLORS)
COLORS.update(MATCHUPS_COLORS)
COLORS.update(UTIL_COLORS)
COLORS.update(SOLVE_COLORS)

def rgb_to_ansi(rgb):
    return '\033[38;2;{};{};{}m'.format(*rgb)

def bold_and_italicize_text(text):
    return f"\033[1m\033[3m{text}\033[0m"

def debug(*args, mode='debug'):
    frame = inspect.currentframe().f_back
    code = frame.f_code
    line_no = frame.f_lineno
    calling_function_name = frame.f_code.co_name
    with open(code.co_filename, 'r') as f:
        lines = f.readlines()
    line = lines[line_no - 1]
    leading_spaces = len(line) - len(line.lstrip(' '))
    indent = leading_spaces // 4
    arg_names = re.findall(r'debug\((.*?)\)', line)[0].split(', ')
    for arg_name, arg_value in zip(arg_names, args):
        indent_str = ' |\t' * indent
        if indent > 0:
            indent_str = indent_str[:-3] + ' |-- '
        is_text = isinstance(arg_value, str) and len(arg_name) > 2 and arg_name[1:len(arg_name)-1] == arg_value and not arg_name.endswith(")")
        function_print_str = calling_function_name if 'self' not in frame.f_locals else f'{frame.f_locals["self"].__class__.__name__}.{calling_function_name}'
        color = COLORS.get(function_print_str, white)
        if is_text:
            print_str = f"{rgb_to_ansi(color)}{indent_str}[{function_print_str}] : {bold_and_italicize_text(arg_value)}\033[0m"
        else:
            print_str = f"{rgb_to_ansi(color)}{indent_str}[{function_print_str}] : {arg_name} = {arg_value}\033[0m"
        # print("Debugging with MODE:", get_log_mode())
        log_config.debug_custom(print_str, mode)
        