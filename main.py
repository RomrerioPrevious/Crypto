from icecream import ic, install
from crypto import Logger, CryptoApp


def main():
    app = CryptoApp()
    app.run()


if __name__ == "__main__":
    ic.configureOutput(prefix=Logger.info,
                       outputFunction=Logger.write_log)
    install()
    main()
