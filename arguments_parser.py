import argparse

from yaml import load

parser = argparse.ArgumentParser()  # Create ArgumentParser object
parser.add_argument(
    '-u', '--url', type=str, required=True,
    help='Target website with FUZZ params, for exapmle: \'http://abc.com/index.php?p=FUZZ\''  # noqa
)
parser.add_argument(
    '-t', '--thread', type=int, default=3, dest='thrd',
    help='Set working threads, default: 3'
)
parser.add_argument(
    '-f', '--file', type=str,
    default='./wordlist/simple_dirs.txt',
    help='Set wordlist'
)
parser.add_argument(
    '-e', '--exception', type=int,
    choices=[200, 302, 401, 403, 404, 500],
    help='Set status code for hidding, choose from provided list'
)
parser.add_argument(
    '-r', '--remove', type=int, help='Set Chars length for hidding'
)
parser.add_argument(
    '-p', '--proxy', type=str,
    help='Set network proxy, such as: http://127.0.0.1:8080'
)
parser.add_argument(
    '-c', '--custom', type=load,
    help='Custom header by adding json value, for example: "{\'User-Agent\':\'Firefox\', \'Cookies\':\'abcdef\'}"'  # noqa
)
args = parser.parse_args()  # Return opts and args
