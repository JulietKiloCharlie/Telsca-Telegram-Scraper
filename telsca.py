import os
import csv
import json
from telethon.sync import TelegramClient
from telethon import errors
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

class TelegramScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("telsca - telegram scraper by osinttraining.info")
        self.root.withdraw()  # Hide the root window initially
        self.show_welcome_page()

    def show_welcome_page(self):
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome to Telegram Scraper")
        welcome_window.geometry("600x400")
        welcome_window.configure(bg='#181818')

        welcome_text = (
            "Welcome to Telegram Scraper!\n\n"
            "This tool allows you to scrape data from Telegram channels and groups, "
            "including messages, user information, and media files. You can save the "
            "scraped data in CSV or JSON format and download associated media files.\n\n"
            "Requirements:\n"
            "1. API ID and API Hash from Telegram.\n"
            "2. Phone number associated with your Telegram account.\n\n"
            "Setup:\n"
            "1. Enter your API ID, API Hash, and phone number.\n"
            "2. Authenticate by entering the code received on your phone.\n"
            "3. Select the chat you want to scrape.\n"
            "4. Choose the data options and save the scraped data.\n\n"
            "Designed and developed by Justin Casey.\n"
            "For more information or OSINT training, visit www.osinttraining.info."
        )

        welcome_label = tk.Label(
            welcome_window, text=welcome_text, bg='#181818', fg='#00ffff', wraplength=550, justify="left"
        )
        welcome_label.pack(pady=20, padx=20)

        def close_welcome():
            welcome_window.destroy()
            self.root.deiconify()  # Show the root window
            self.create_main_window()

        ttk.Button(welcome_window, text="Get Started", command=close_welcome).pack(pady=10)

    def create_main_window(self):
        self.client = None
        self.data_checkbuttons = {}
        self.root.geometry("600x400")
        self.create_widgets()
        self.style_widgets()

    def style_widgets(self):
        # Set the color scheme
        self.root.configure(bg='#181818')
        style = ttk.Style()
        style.configure("TLabel", background='#181818', foreground='#00ffff')
        style.configure("TButton", background='#333333', foreground='#00ffff', borderwidth=1)
        style.map("TButton", background=[('active', '#00ffff')], foreground=[('active', '#333333')])
        style.configure("TEntry", fieldbackground='#242424', foreground='#00ffff')
        style.configure("TCombobox", fieldbackground='#242424', foreground='#00ffff')
        style.configure("TCheckbutton", background='#181818', foreground='#00ffff')

    def create_widgets(self):
        # API ID
        ttk.Label(self.root, text="API ID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.api_id_entry = ttk.Entry(self.root)
        self.api_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # API Hash
        ttk.Label(self.root, text="API Hash:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.api_hash_entry = ttk.Entry(self.root, show="*")
        self.api_hash_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.show_hash_button = ttk.Button(self.root, text="Show", command=self.toggle_hash_visibility)
        self.show_hash_button.grid(row=1, column=2, padx=10, pady=10)

        # Phone Number
        ttk.Label(self.root, text="Phone Number:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.phone_entry = ttk.Entry(self.root)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Authenticate Button
        self.auth_button = ttk.Button(self.root, text="Authenticate", command=self.authenticate)
        self.auth_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # Chat List
        ttk.Label(self.root, text="Select Chat:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.chat_combobox = ttk.Combobox(self.root)
        self.chat_combobox.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        # Data Options
        ttk.Label(self.root, text="Data Options:").grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        self.data_options = {
            "Date": tk.BooleanVar(value=True),
            "Sender ID": tk.BooleanVar(value=True),
            "Sender Username": tk.BooleanVar(value=True),
            "Message ID": tk.BooleanVar(value=True),
            "Message": tk.BooleanVar(value=True),
            "Latitude": tk.BooleanVar(value=True),
            "Longitude": tk.BooleanVar(value=True),
            "Reply To Message ID": tk.BooleanVar(value=True),
            "Forwarded From": tk.BooleanVar(value=True),
            "Message Type": tk.BooleanVar(value=True),
            "Media Type": tk.BooleanVar(value=True),
            "File Name": tk.BooleanVar(value=True),
            "File Size": tk.BooleanVar(value=True),
            "Document Type": tk.BooleanVar(value=True),
            "User Profile ID": tk.BooleanVar(value=True),
            "User First Name": tk.BooleanVar(value=True),
            "User Last Name": tk.BooleanVar(value=True),
            "User Username": tk.BooleanVar(value=True),
            "User Phone": tk.BooleanVar(value=True),
            "User Profile Photo": tk.BooleanVar(value=True)
        }
        
        # Create checkbuttons in two columns
        col = 0
        row = 6
        for i, (option, var) in enumerate(self.data_options.items()):
            if i == len(self.data_options) // 2:
                col = 2
                row = 6
            self.data_checkbuttons[option] = tk.Checkbutton(self.root, text=option, variable=var, bg='#181818', fg='#00ffff', selectcolor='#242424')
            self.data_checkbuttons[option].grid(row=row, column=col, padx=10, pady=2, sticky="w")
            row += 1

        # Save As
        ttk.Label(self.root, text="Save As:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        self.file_name_entry = ttk.Entry(self.root)
        self.file_name_entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        self.file_type_var = tk.StringVar(value="csv")
        self.file_type_menu = ttk.Combobox(self.root, textvariable=self.file_type_var, values=["csv", "json"])
        self.file_type_menu.grid(row=row, column=2, padx=10, pady=10, sticky="ew")

        # Scrape Button
        self.scrape_button = ttk.Button(self.root, text="Scrape", command=self.scrape)
        self.scrape_button.grid(row=row + 1, column=0, columnspan=3, padx=10, pady=10)

        self.root.grid_columnconfigure(1, weight=1)

    def toggle_hash_visibility(self):
        if self.api_hash_entry.cget('show') == '*':
            self.api_hash_entry.config(show='')
            self.show_hash_button.config(text='Hide')
        else:
            self.api_hash_entry.config(show='*')
            self.show_hash_button.config(text='Show')
    
    def authenticate(self):
        api_id = self.api_id_entry.get()
        api_hash = self.api_hash_entry.get()
        phone = self.phone_entry.get()

        if not (api_id and api_hash and phone):
            messagebox.showerror("Error", "Please enter API ID, API Hash, and Phone Number.")
            return

        try:
            self.client = TelegramClient('session_name', api_id, api_hash)
            self.client.connect()

            if not self.client.is_user_authorized():
                self.client.send_code_request(phone)
                code = simpledialog.askstring("Authentication", "Please enter the code you received:", parent=self.root)
                self.client.sign_in(phone, code)

            self.chat_combobox['values'] = [f"{dialog.name} (ID: {dialog.id})" for dialog in self.client.iter_dialogs()]

            messagebox.showinfo("Success", "Authenticated successfully. Please select a chat.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def scrape(self):
        if not self.client:
            messagebox.showerror("Error", "Please authenticate first.")
            return

        chat = self.chat_combobox.get()
        if not chat:
            messagebox.showerror("Error", "Please select a chat.")
            return

        chat_id = chat.split("ID: ")[-1].strip(")")
        data_options = self.data_options
        file_name = self.file_name_entry.get() + '.' + self.file_type_var.get()
        file_type = self.file_type_var.get()

        try:
            data = []

            media_types = {'photo': False, 'video': False, 'audio': False, 'document': False}
            for message in self.client.iter_messages(int(chat_id), limit=1000):
                row = {}
                sender = None
                try:
                    sender = self.client.get_entity(message.sender_id) if message.sender_id else None
                except errors.rpcerrorlist.UsernameNotOccupiedError:
                    pass
                except errors.rpcerrorlist.UserDeactivatedError:
                    pass
                except Exception as e:
                    print(f"Error fetching sender: {e}")

                for key, value in data_options.items():
                    if not value.get():
                        continue
                    if key == "Date":
                        row["Date"] = message.date
                    elif key == "Sender ID":
                        row["Sender ID"] = message.sender_id
                    elif key == "Sender Username":
                        row["Sender Username"] = sender.username if sender and hasattr(sender, 'username') else ''
                    elif key == "Message ID":
                        row["Message ID"] = message.id
                    elif key == "Message":
                        row["Message"] = message.text
                    elif key == "Latitude" or key == "Longitude":
                        lat = lon = None
                        if message.media and hasattr(message.media, 'geo'):
                            lat = message.media.geo.lat
                            lon = message.media.geo.long
                        if key == "Latitude":
                            row["Latitude"] = lat
                        else:
                            row["Longitude"] = lon
                    elif key == "Reply To Message ID":
                        row["Reply To Message ID"] = message.reply_to_msg_id
                    elif key == "Forwarded From":
                        row["Forwarded From"] = message.forward.sender_id if message.forward else None
                    elif key == "Message Type":
                        row["Message Type"] = type(message).__name__
                    elif key == "Media Type":
                        row["Media Type"] = type(message.media).__name__ if message.media else None
                    elif key == "File Name":
                        row["File Name"] = message.file.name if message.file else None
                    elif key == "File Size":
                        row["File Size"] = message.file.size if message.file else None
                    elif key == "Document Type":
                        row["Document Type"] = message.file.mime_type if message.file else None
                    elif key == "User Profile ID":
                        row["User Profile ID"] = sender.id if sender else ''
                    elif key == "User First Name":
                        row["User First Name"] = sender.first_name if sender and hasattr(sender, 'first_name') else ''
                    elif key == "User Last Name":
                        row["User Last Name"] = sender.last_name if sender and hasattr(sender, 'last_name') else ''
                    elif key == "User Username":
                        row["User Username"] = sender.username if sender and hasattr(sender, 'username') else ''
                    elif key == "User Phone":
                        row["User Phone"] = sender.phone if sender and hasattr(sender, 'phone') else ''
                    elif key == "User Profile Photo":
                        row["User Profile Photo"] = None
                        if sender and hasattr(sender, 'photo'):
                            try:
                                row["User Profile Photo"] = sender.photo.photo_id
                            except Exception as e:
                                print(f"Error accessing photo_id: {e}")
                
                if message.media:
                    if message.photo:
                        media_types['photo'] = True
                    elif message.video:
                        media_types['video'] = True
                    elif message.audio:
                        media_types['audio'] = True
                    elif message.document:
                        media_types['document'] = True

                data.append(row)

            if file_type == 'csv':
                with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=[key for key, value in data_options.items() if value.get()])
                    writer.writeheader()
                    writer.writerows(data)
            elif file_type == 'json':
                with open(file_name, mode='w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

            self.show_media_download_dialog(chat_id, media_types, self.file_name_entry.get())

            messagebox.showinfo("Success", f"Data scraped and saved to {file_name}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_media_download_dialog(self, chat_id, media_types, base_file_name):
        media_options = [key for key, value in media_types.items() if value]
        if not media_options:
            return

        media_window = tk.Toplevel(self.root)
        media_window.title("Select Media to Download")
        media_window.geometry("300x200")
        media_window.configure(bg='#181818')
        media_window.lift(self.root)
        media_window.attributes('-topmost', True)
        media_vars = {option: tk.BooleanVar(value=False) for option in media_options}

        for i, option in enumerate(media_options):
            tk.Checkbutton(media_window, text=option.capitalize(), variable=media_vars[option], bg='#181818', fg='#00ffff', selectcolor='#242424').pack(anchor="w", padx=20, pady=5)

        def download_selected_media():
            selected_media = {option: var.get() for option, var in media_vars.items()}
            media_window.destroy()
            self.download_media(chat_id, selected_media, base_file_name)

        ttk.Button(media_window, text="Download", command=download_selected_media).pack(pady=10)

    def download_media(self, chat_id, selected_media, base_file_name):
        media_dir = filedialog.askdirectory(title="Select Directory to Save Media")
        if not media_dir:
            return

        media_subdir = os.path.join(media_dir, f"{base_file_name}_media")
        os.makedirs(media_subdir, exist_ok=True)

        try:
            for message in self.client.iter_messages(int(chat_id), limit=1000):
                if message.media:
                    try:
                        if selected_media.get('photo') and message.photo:
                            file_path = self.client.download_media(message.media, file=media_subdir)
                            print(f"Downloaded image to {file_path}")
                        elif selected_media.get('video') and message.video:
                            file_path = self.client.download_media(message.media, file=media_subdir)
                            print(f"Downloaded video to {file_path}")
                        elif selected_media.get('audio') and message.audio:
                            file_path = self.client.download_media(message.media, file=media_subdir)
                            print(f"Downloaded audio to {file_path}")
                        elif selected_media.get('document') and message.document:
                            file_path = self.client.download_media(message.media, file=media_subdir)
                            print(f"Downloaded document to {file_path}")
                    except Exception as e:
                        print(f"Error downloading media: {e}")

            messagebox.showinfo("Success", f"Media files downloaded successfully to {media_subdir}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TelegramScraperApp(root)
    root.mainloop()
