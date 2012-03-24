import Helper

Logger().setOutput("exception.log")

@CatchAndLogException
def main():
    Logger().debug("Hello world!")

if __name__ == "__main__":
    u = 1/0
    main()
