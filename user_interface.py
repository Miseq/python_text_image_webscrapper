import requests
import argparse

def print_basic_menu():
    print("1 - Pobierz wszystko "
          "\n2 - Pobierz tylko obrazy "
          "\n3 - Pokaz tylko text "
          "\n4 - Wyswietl logi pobierania"
          "\n5 - Wyswietl ponownie opis menu "
          "\n0 - Zakoncz dzialanie")

def download_menu(choice, app_url, app_port):
    media = 'all'    # default
    if choice == 1:
        media = 'all'
    elif choice == 2:
        media = 'images'
    elif choice == 3:
        media = 'text'

    print("Podaj adres url z ktorego nalezy pobrac wybrane media"
          "\n 0 - powrot")
    download_url = input('->')
    if download_url != 0:
        print(requests.post(f'http://{app_url}:{app_port}/', json={"url": download_url, "option": media}))



def show_interface(app_url, app_port):
    while True:
        print_basic_menu()
        user_input = int(input('->'))
        if user_input == 1 or user_input == 2 or user_input == 3:
            download_menu(user_input, app_url, app_port)
        elif user_input == 4:
            pass #TODO
        elif user_input == 5:
            pass
        elif user_input == 6:
            print_basic_menu()
        elif user_input == 0:
            break
        else:
            print("nie rozpoznano polecenia!")

if __name__ == '__main__':
   show_interface('127.0.0.1', 5000)
