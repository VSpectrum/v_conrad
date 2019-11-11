import sys
from display_interface import printTable
from data_access_layer import DAL
def main():
    cmd, *arguments = sys.argv[1:]
    if cmd == "remind":
        if arguments == []:
            printTable(DAL().get_reminders())
        else:
            for argument in arguments:
                DAL().set_reminder(argument)
    if cmd == "show":
        printTable(DAL().get_future_conferences())

if __name__ == "__main__":
    main()
