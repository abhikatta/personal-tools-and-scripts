import argparse
import time

parser = argparse.ArgumentParser(description="Create a quick timer from terminal")


parser.add_argument("-S", type=int, help="Seconds (1-60)")
parser.add_argument("-M", type=int, help="Minutes (1-60)")
parser.add_argument("-H", type=int, help="Hours (1-24)")


args = parser.parse_args()
total = 0


if args.S:
    if args.S >= 1 and args.S <= 60:
        total = total + (args.S * 1)
    else:
        print("Seconds must be in range 1-60")
        exit(1)
if args.M:
    if args.M >= 1 and args.M <= 60:
        total = total + (args.M * 60)
    else:
        print("Minutes must be in range 1-60")
        exit(1)
if args.H:
    if args.H >= 1 and args.H <= 24:
        total = total + (args.H * 60 * 60)
    else:
        print("Hours must be in range 1-24")
        exit(1)
if total == 0:
    print("Please pass at least one arg -S -M -H")
    exit(1)

print(f"total {total}")
time.sleep(total)

print("timer finished")
