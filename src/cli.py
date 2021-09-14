from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, Callable, Optional

from text_utils.cli_core import (INFERENCE_ARROW_TYPE, WEIGHTS_ARROW_TYPE, change_symbols_in_map,
                                 print_map, print_symbols)

ARROW_TYPES = [WEIGHTS_ARROW_TYPE, INFERENCE_ARROW_TYPE]


def init_map_parser(parser: ArgumentParser) -> Callable[[str, str], None]:
  parser.add_argument("-p", "--path", type=Path, required=True,
                      help="Path to .json-file containing the map")
  parser.add_argument("-a", "--arrow_type", type=str, required=True,
                      help="Sets the direction of the arrow", choices=ARROW_TYPES)
  return print_map


def init_symbol_parser(parser: ArgumentParser) -> Callable[[str], None]:
  parser.add_argument("-p", "--path", type=Path, required=True,
                      help="Path to file containing the symbols")
  return print_symbols


def init_change_parser(parser: ArgumentParser) -> Callable[[str, str, Optional[str], Optional[str], Optional[str]], None]:
  parser.add_argument("-p", "--map_path", type=str, required=True,
                      help="Path to .json-file containing the map")
  parser.add_argument("-s", "--symbol_path", type=str, required=True,
                      help="Path to file containing the allowed symbols")
  parser.add_argument("-a", "--arrow_type", type=str, required=False,
                      help="Sets the direction of the arrow", choices=ARROW_TYPES)
  parser.add_argument("-t", "--to_key", type=str, required=False,
                      help="Key to which new symbol should be assigned")
  parser.add_argument("-m", "--map_symbol", type=str, required=False,
                      help="Symbol that should be assigned to chosen key")
  return change_symbols_in_map


def _add_parser_to(subparsers: Any, name: str, init_method: Callable) -> ArgumentParser:
  parser = subparsers.add_parser(name, help=f"{name} help")
  invoke_method = init_method(parser)
  parser.set_defaults(invoke_handler=invoke_method)
  return parser


def _init_parser() -> ArgumentParser:
  result = ArgumentParser()
  subparsers = result.add_subparsers(help='sub-command help')

  _add_parser_to(subparsers, "print_map", init_map_parser)
  _add_parser_to(subparsers, "print_symbols", init_symbol_parser)
  _add_parser_to(subparsers, "change_symbols", init_change_parser)
  return result


def _process_args(args: Namespace) -> None:
  params = vars(args)
  if "invoke_handler" in params:
    invoke_handler = params.pop("invoke_handler")
    invoke_handler(**params)
  else:
    print("Please specify which method you want to invoke.")


if __name__ == "__main__":
  main_parser = _init_parser()
  received_args = main_parser.parse_args()
  _process_args(received_args)
