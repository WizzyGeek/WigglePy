from sys import argv, exit
from typing import Any, Dict, List, Literal, Union

from wiggle import Wiggler

class InvalidFlag(Exception):
    pass

def invalid(_):
    raise InvalidFlag

help_str = """
Wiggle
======
A cli to create wiggly lines

Usage
====+=============
    | wiggle <text> [wiggle|shm] [-I|--iterations, <value = infinity (integer)>] [-H|--height, <value = 40 (integer)>] [-W|--width, <value = 15 (integer)>] [-d|--delay, <value = 16 (float)>]]
====+=============
    | wiggle <text> [wiggle|shm] [-I|--iterations, <value = infinity (integer)>] [height = 40 (integer)] [width = 15 (integer)] [delay = 16.0 (float)]]
====+=============
    | text
    |     The text that will be wiggled.
----+----
    | wiggle | shm
    |     Type of wiggle. By default "wiggle".
----+----
    | -I|--iterations
    |     How many times to update. By default infinity.
----+----
    | -H | --height
    |     The height of the wiggle in muber of lines. By default 40
----+----
    | -W | --width
    |     The width of the wiggle. The actual width is twice this number. By default 15.
----+----
    | -d | --delay
    |     The delay between updates. By default 16.
====+=============
"""

def main(argv: List[str] = argv) -> int:
    convertors = Wiggler.__init__.__annotations__
    convertors["iterations"] = int

    flags = {j: i for i, j in zip(convertors.keys(), ("H", "W", "d"))}
    flags["I"] = "iterations"
    bool_flags = []
    method_flags = [("iterations", -1, "itr")]

    config = {}
    method_args = {}
    args = {}
    by_pos = []
    by_pos.append((0, argv[1]))

    current_flag = None
    for idx, i in enumerate(argv[1:]):
        if i.startswith("--"):
            d = i[2:]
            bool_val = True
            if d[4:] in bool_flags:
                d = d[4:]
                bool_val = False
            if d in bool_flags:
                config[d] = bool_val
            current_flag = d
        elif i.startswith("-"):
            d = i[1:]
            k = flags.get(d)
            if k:
                current_flag = k
            else:
                current_flag = d
        elif current_flag is not None:
            try:
                val = convertors.get(current_flag, invalid)(i)
            except (TypeError, ValueError):
                print("Invalid value", i, "for flag", current_flag, "expected a(n)", convertors.get(d))
                return 1
            except InvalidFlag:
                print(
                    "Unexpected flag '", current_flag, "' valid flags are:\n\t",
                    "\n\t".join("-" + i for i in flags), "\n\t", "\n\t".join("--" + i for i in flags.values)
                )
                return 1
            else:
                args[current_flag] = val
            current_flag = None
        else:
            if i in ["wiggle", "shm"]:
                continue
            if idx != 0:
                by_pos.append((idx, i))
    else:
        config["wiggle"] = True
        if "shm" in argv:
            config["wiggle"] = False

        if len(by_pos) == 0:
            print("Missing required poitional argument 'text'")
            return 1

        if len(by_pos) > 1:
            if by_pos[1][0] <= 3:
                diff = 0
                f_args = {}
                last_idx =  by_pos[0][0]
                for i, j, k, l in map(lambda x: (x[0][0], x[0][1], x[1][0], x[1][1]), zip(by_pos[1:], convertors.items())):
                    if diff > 1:
                        break
                    f_args[k] = l(j)
                    diff = i - last_idx
                    last_idx = i
                else:
                    args.update(f_args)

        for i, j, k in method_flags:
            method_args[k] = args.pop(i, j)

        wiggly = Wiggler(**{i: j for i, j in args.items() if i in convertors.keys()})
        method = wiggly.wiggle if config["wiggle"] else wiggly.shm

        try:
            method(by_pos[0][1], **method_args)
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
