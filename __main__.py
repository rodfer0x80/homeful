from homeful.bot import *

def main():
    if len(sys.argv) == 2:
        run_mode = sys.argv[1]
    else:
        sys.stdout.write(f"Usage {sys.argv[0]} <mode=spam/search>\n")
        return 0
    bot = Bot(run_mode)
    try:
        bot.runme()
    except KeyboardInterrupt:
        sys.stdout.write("[!] Gracefully quitting\n")
    return 0

if __name__ == '__main__':
    sys.exit(main())
