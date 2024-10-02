import os

import pywhatkit as kit

from twilio.rest import Client

import subprocess

import psutil

import requests

from art import text2art

import pyttsx3

from googlesearch import search



def text_to_speech(text, rate=150):

    engine = pyttsx3.init()

    engine.setProperty('rate', rate)  # Set the speed of speech

    engine.say(text)

    engine.runAndWait()



def send_whatsapp_message():

    number = input("Enter the recipient's number (with country code): ")

    message = input("Enter the message: ")

    hour = int(input("Enter the hour (24-hour format): "))

    minute = int(input("Enter the minute: "))

    kit.sendwhatmsg(number, message, hour, minute)



def speak_output():

    message = input("Enter the message to be spoken: ")

    text_to_speech(message, rate=165)

    print(message)



def send_email():

    recipient = input("Enter the recipient's email: ")

    subject = input("Enter the subject: ")

    body = input("Enter the body of the email: ")

    os.system(f'echo "{body}" | mail -s "{subject}" {recipient}')



def send_sms():

    account_sid = 'your_sid'

    auth_token = 'your_tocken'

    client = Client(account_sid, auth_token)

    to = input("Enter the recipient's number (with country code): ")

    from_ = '+14157893575'

    body = input("Enter the message: ")

    client.messages.create(to=to, from_=from_, body=body)



def post_to_social_media():

    platform = input("Enter the platform (telegram/instagram/facebook/discord): ").lower()

    message = input("Enter the message to post: ")

    if platform == 'telegram':

        # Add your Telegram bot code here

        pass

    elif platform == 'instagram':

        # Add your Instagram bot code here

        pass

    elif platform == 'facebook':

        # Add your Facebook bot code here

        pass

    elif platform == 'discord':

        # Add your Discord bot code here

        pass

    else:

        print("Unsupported platform")



def change_file_folder_colors():

    os.system('LS_COLORS="di=1;35" && export LS_COLORS')



def read_ram():

    print(psutil.virtual_memory())



def change_gnome_terminal_look():

    profile = input("Enter the GNOME Terminal profile name: ")

    os.system(f'dconf write /org/gnome/terminal/legacy/profiles:/:{profile}/background-color ":red/"')



def create_user_set_password():

    username = input("Enter the username: ")

    password = input("Enter the password: ")

    os.system(f'sudo useradd {username}')

    os.system(f'echo "{username}:{password}" | sudo chpasswd')



def run_linux_in_browser():

    os.system('jupyter notebook')



def google_search():

    query = input("Enter the search query: ")

    for result in search(query, tld="com", num=10, stop=10, pause=2):

        print(result)



def run_windows_software():

    software = input("Enter the Windows software to run: ")

    os.system(f'wine {software}')



def sync_folders():

    folder1 = input("Enter the first folder path: ")

    folder2 = input("Enter the second folder path: ")

    os.system(f'rsync -av --progress {folder1} {folder2}')



def print_ascii_art():

    text = input("Enter the text to convert to ASCII art: ")

    print(text2art(text))



def main_menu():

    while True:

        print("\nMenu:")

        print("1. Send WhatsApp Message")

        print("2. Speak Output")

        print("3. Send Email")

        print("4. Send SMS")

        print("5. Post to Social Media")

        print("6. Change File/Folder Colors")

        print("7. Read RAM")

        print("8. Change GNOME Terminal Look")

        print("9. Create User and Set Password")

        print("10. Run Linux in Browser")

        print("11. Google Search")

        print("12. Run Windows Software")

        print("13. Sync Folders")

        print("14. Print ASCII Art")

        print("15. Exit")



        choice = input("Enter your choice: ")



        if choice == '1':

            send_whatsapp_message()

        elif choice == '2':

            speak_output()

        elif choice == '3':

            send_email()

        elif choice == '4':

            send_sms()

        elif choice == '5':

            post_to_social_media()

        elif choice == '6':

            change_file_folder_colors()

        elif choice == '7':

            read_ram()

        elif choice == '8':

            change_gnome_terminal_look()

        elif choice == '9':

            create_user_set_password()

        elif choice == '10':

            run_linux_in_browser()

        elif choice == '11':

            google_search()

        elif choice == '12':

            run_windows_software()

        elif choice == '13':

            sync_folders()

        elif choice == '14':

            print_ascii_art()

        elif choice == '0':

            break

        else:

            print("Invalid choice. Please try again.")



if __name__ == "__main__":

    main_menu()