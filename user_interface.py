import requests
import argparse
import os


def print_basic_menu():
    print("1 - Download everything "
          "\n2 - Download only images "
          "\n3 - Download only text "
          "\n4 - Print download logs"
          "\n5 - Print again this menu "
          "\n0 - Exit from user interface")
    # TODO dodalbym mozliwosc restartowania app flaska i zamykania go stad


def download_menu(choice, app_url, app_port):

    media = 'all'    # default
    if choice == 1:
        media = 'all'
    elif choice == 2:
        media = 'images'
    elif choice == 3:
        media = 'text'

    print("Type url from which chosen media will be downloaded, or type 0 to go back")
    download_url = input('->')
    if download_url != 0:
        print(requests.post(f'http://{app_url}:{app_port}/', json={"url": download_url, "option": media}))


def print_logs():

    if os.path.exists("logs.txt"):
        with open("logs.txt", "r", encoding='utf-8') as logs:
            print(logs.read())
    else:
        print("Logs hasn't been made or ")


def show_interface(app_url, app_port):

    while True:
        print_basic_menu()
        user_input = input('->')
        if user_input == '1' or user_input == '2' or user_input == '3':
            download_menu(user_input, app_url, app_port)
        elif user_input == '4':
            print_logs()
        elif user_input == '5':
            pass
        elif user_input == '6':
            print_basic_menu()
        elif user_input == '0':
            break
        else:
            print("Input hasn't been recognized!")


if __name__ == '__main__':
    # TODO dodac argparsa o url i port apki
    show_interface('0.0.0.0', 5000)
