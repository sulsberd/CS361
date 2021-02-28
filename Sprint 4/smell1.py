

def execute_script():
    email = raw_input("Please enter Facebook login email: ")
    password = getpass.getpass()
    eraser = Eraser(email=email, password=password, wait=args.wait)
    eraser.login()
    eraser.go_to_activity_page()


def main():
    """
    Main section of script
    """
    # set up the command line argument parser
    parser = ArgumentParser(description='Delete your Facebook activity.  Requires Firefox')
    parser.add_argument('--wait', type=float, default=1, help='Explicit wait time between page loads (default 1 second)')
    args = parser.parse_args()

    execute_script()

if __name__ == '__main__':
    main()


    # track failures
    fail_count = 0
    while True:
        if fail_count >= 3:
            print ('[*] Scrolling down')
            eraser.scroll_down()
            fail_count = 0
            sleep(5)
        try:
            print ('[*] Trying to delete element')
            eraser.delete_element()
            fail_count = 0
        except (Exception, ) as e:
            print ('[-] Problem finding element')
            fail_count += 1
            sleep(2)

