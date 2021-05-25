import sys

def fast_string():
    # NOTE: only string, not integer, use int() to convert to int
    return sys.stdin.readline().strip()


def fast_inta():
    return list(map(int, sys.stdin.readline().strip().split()))

def fast_out(param):
    sys.stdout.write(f"{ param }" + "\n")