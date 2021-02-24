import sys
from life_generator_gui import *
from life_generator_data import *
import life_generator_debug as debug
from life_generator_debug import log


def main():
    debug.debug_init()
    options = [opt for opt in sys.argv if opt.startswith("-")]
    argv = [arg for arg in sys.argv if not arg.startswith("--")]
    argc = len(argv)

    for opt in options:
        if opt == "--debug":
            debug.DEBUG = True
        else:
            usage()
            return

    if argc == 1:
        start_gui()
    elif argc == 2:
        filepath = argv[1]
        process_input_file(filepath)
    else:
        usage()


def process_input_file(filepath):
    log(f"Filepath: {filepath}")
    td = ToyData()
    td.load()

    # output_path = td.outout_filepath
    # if path.exists(output_path):
    #     if not user_confirm_action('File "{output_path}" already exists. Overwrite?'):
    #         log("Aborting.")
    #         return

    try:
        td.calc_top_toys_from_file(
            filepath,
            lambda results: td.export(results),
        )
    except FileNotFoundError:
        print(f"Error: File does not exist: {filepath}")
    except:
        # TODO: make more robust
        print(f"Error: File not valid: {filepath}")


def usage():
    print(f"Usage: {sys.argv[0]} [<input.csv>]")


if __name__ == "__main__":
    main()