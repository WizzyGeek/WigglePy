from sys import argv, exit
from typing import Any, Dict, List, Literal, Union
from itertools import chain

from wiggle import Wiggler, __version__

class InvalidFlag(Exception): pass

def invalid(_):
    raise InvalidFlag(_)

help_str = """
Wiggle
======
A cli to create wiggly lines

Usage
====+=============
    | wiggle <text> [wiggle|shm] [-I|--iterations, <value = infinity (integer)>]
    |               [-H|--height, <value = 40 (integer)>] [-W|--width, <value = 15 (integer)>]
    |               [-d|--delay, <value = 16 (float)>]]
====+=============
    | wiggle <text> [wiggle|shm] [-I|--iterations, <value = infinity (integer)>]
    |               [height = 40 (integer)] [width = 15 (integer)] [delay = 16.0 (float)]]
====+=============
    | wiggle [--help|-h]
====+=============
    | -h | --help
    |     Shows this message
----+----
    | text
    |     The text that will be wiggled.
----+----
    | wiggle | shm
    |     Type of wiggle. By default "wiggle".
----+----
    | -I|--iterations
    |     How many times to update. By default infinity.
----+----
    | -H | --height, height
    |     The height of the wiggle in muber of lines. By default 40
----+----
    | -W | --width, width
    |     The width of the wiggle. The actual width is twice this number. By default 15.
----+----
    | -d | --delay, delay
    |     The delay between updates. By default 16.
====+=============
"""

def main(argv: List[str] = argv) -> int:
    help_ptr = "\nSee " + argv[0] + " --help for help"

    if "--help" in argv[1:] or "-h" in argv[1:] or len(argv) == 1:
        print(help_str)
        return 0

    convertors = Wiggler.__init__.__annotations__
    convertors["iterations"] = int

    flags = {j: i for i, j in zip(convertors.keys(), ("H", "W", "d"))}
    flags["I"] = "iterations"
    method_flags = [("iterations", -1, "itr")]

    config = {
        "wiggle": True,
    }
    method_args = {}
    args = {}
    rest = argv[2:]

    if rest:
        remain = rest.copy()

        if "wiggle" in remain:
            remain.remove("wiggle")
        elif "shm" in remain:
            config["wiggle"] = False
            remain.remove("shm")

        for i, j in map(lambda x: (("-" * ((len(x) > 1) + 1)) + x, flags.get(x, x)), chain(flags.values(), flags.keys())):
            if len(remain) < 2:
                break
            if i in remain:
                try:
                    f_arg = argv[argv.index(i) + 1]
                    args[j] = convertors.get(j, invalid)(f_arg)
                except IndexError:
                    print("Missing value for flag", i, help_ptr)
                    return 1
                except InvalidFlag:
                    print("Something is wrong with wiggle", __version__, "\nUpdate/Restore to the latest version if available.")
                    return 1
                except (TypeError, ValueError):
                    print("Invalid value", f_arg, "for flag", i, "expected a(n)", convertors.get(j), help_ptr)
                    return 1
                except Exception as e:
                    print("Something went wrong!")
                    return e
                else:
                    remain.pop(remain.index(i) + 1)
                    remain.remove(i)

        for i, j, k in method_flags:
            method_args[k] = args.pop(i, j)

        if remain:
            if not args:
                i = list(flags.values())[:3]
                for val, conv, key in zip(remain, convertors.values(), i):
                    try:
                        args[key] = conv(val)
                    except (TypeError, ValueError):
                        print(help_ptr)
                        return 1
                    except Exception as e:
                        print("Something went wrong!")
                        return e
            else:
                print("[WARNING] Received undeterminable extra positional args: ", ", ".join(args))
                try:
                    input("(Press any key to continue)")
                except KeyboardInterrupt:
                    return 0

        wiggly = Wiggler(**{i: j for i, j in args.items() if i in convertors.keys()})
        method = wiggly.wiggle if config["wiggle"] else wiggly.shm

        try:
            method(argv[1], **method_args)
        except Exception as err:
            return err
        except KeyboardInterrupt:
            print("\033[2J\033[H", end="")
            return 0
        else:
            return 0
        finally:
            from pathlib import Path
            from datetime import datetime
            datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            with (Path(__file__).parent / ".usage").open("a") as usg:
                print(datetime, *argv, file=usg)

if __name__ == "__main__":
    exit(main(argv))
