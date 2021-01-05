from argparse import ArgumentParser

from text_utils.print_or_change_map_and_symbols import (init_change_parser,
                                                        init_map_parser,
                                                        init_symbol_parser)


def _add_parser_to(subparsers, name: str, init_method):
  parser = subparsers.add_parser(name, help=f"{name} help")
  invoke_method = init_method(parser)
  parser.set_defaults(invoke_handler=invoke_method)
  return parser


def _init_parser():
  result = ArgumentParser()
  subparsers = result.add_subparsers(help='sub-command help')

  _add_parser_to(subparsers, "print_map", init_map_parser)
  _add_parser_to(subparsers, "print_symbols", init_symbol_parser)
  _add_parser_to(subparsers, "change_symbols", init_change_parser)
  return result


def _process_args(args):
  params = vars(args)
  if "invoke_handler" in params:
    invoke_handler = params.pop("invoke_handler")
    invoke_handler(**params)
  else:
    print("Please specifiy which method you want to invoke.")


if __name__ == "__main__":
  main_parser = _init_parser()
  received_args = main_parser.parse_args()
  _process_args(received_args)
