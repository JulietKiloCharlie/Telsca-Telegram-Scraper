## Telsca - Telegram Scraper by OSINTTraining.info

Telsca is a powerful open-source tool designed to scrape data from Telegram channels and groups. With Telsca, you can extract messages, user information, media files, and other metadata, saving the data in CSV or JSON format. It also allows you to download associated media files such as images, videos, and documents.

![welcome message](https://github.com/user-attachments/assets/ac1fedfa-c202-482d-aa14-c738e2d35cf7)


# Features:

   -Scrape messages from Telegram channels and groups.

   -Extract user information including profile photos.

   -Download media files (images, videos, audio, documents).

   -Save scraped data in CSV or JSON format.

   -User-friendly GUI with customizable data options.
   
   

# Requirements.
   
   -Python 3.x

   -API ID and API Hash from Telegram

   -Phone number associated with your Telegram account
   

# Installation

# Step 1: Clone the Repository


**First, clone the repository from GitHub to your local machine:**

```git clone https://github.com/JulietKiloCharlie/Telsca-Telegram-Scraper.git```

```cd Telsca-Telegram-Scrape```


# Step 2: Install the Required Libraries


**Install the required Python libraries using pip:**


```sudo apt install python3-tk```

```pip3 install telethon```


# Obtaining Telegram API ID and API Hash


**To use Telsca, you need to obtain an API ID and API Hash from Telegram. Follow these steps to get them:**


   -Go to my.telegram.org.

   -Log in with your Telegram account.

   -Click on "API development tools".

   -Create a new application by filling out the required details.

   -After creating the application, you will see your API ID and API Hash.
   


# Usage


![teslca](https://github.com/user-attachments/assets/0de66533-c71a-48f1-8562-7fb7e14560e5)


# Step 1: Run the Script


**Run the script using Python:**

```python3 telsca.py```


# Step 2: Follow the Steps in the GUI



**Welcome Page:**

The welcome page provides information about the tool, requirements, and setup instructions. Click "Get Started" to proceed.



**Main Interface:**

   -Enter API ID, API Hash, and Phone Number: Input your Telegram API credentials. Use the "Show" button to toggle the visibility of the API Hash.
        
   -Authenticate: Click "Authenticate" and enter the code received on your Telegram account.
        
   -Select Chat: Choose the Telegram channel or group you want to scrape from the dropdown list.
        
   -Select Data Options: Check the boxes for the data you want to scrape.
        
   -Save As: Enter the file name and choose the file format (CSV or JSON).
        
   -Scrape: Click "Scrape" to start scraping the data.
        
   -Download Media: A dialog will appear asking you to select which types of media to download (images, videos, audio, documents). Select the desired media types and specify the directory to save them.
   

# Example

**Run the script:**

```python3 telsca.py```

Follow the prompts to authenticate with your Telegram account.
Select the chat and data options.
Click "Scrape" and then select the media types to download.


# Contributing

Contributions are welcome! Please fork the repository and submit pull requests for new features, bug fixes, or improvements.


# License

This project is licensed under the MIT License. See the LICENSE file for details.


# Contact

For more information or OSINT training, visit www.osinttraining.info.
