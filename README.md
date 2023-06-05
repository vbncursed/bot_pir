Telegram Bot for Remote File Processing

This repository contains code for a Telegram bot that handles a specific workflow for processing files on a remote server. The bot allows users to upload a RAR file containing a specific map file, performs several operations on the file on the remote server using SSH, and then provides the processed file back to the user.
Prerequisites

Before running the code, make sure you have the following:

    Python 3.x installed
    Access to a Telegram bot token
    Access to a remote server with SSH credentials

Installation

    Clone this repository to your local machine.

bash

git clone https://github.com/your_username/telegram-file-processing-bot.git

    Install the required dependencies by running the following command:

bash

pip install -r requirements.txt

    Set up the necessary environment variables:
        TOKEN: Your Telegram bot token
        HOST_NAME: The hostname or IP address of the remote server
        USER_NAME: Your username for the remote server
        PASSWORD: Your password for the remote server

Usage

To use the Telegram bot, follow these steps:

    Start the bot by running the main.py script:

bash

python main.py

    Start a conversation with the bot on Telegram.
    Send a RAR file containing a map file named srtm_25_23.tif.
    The bot will handle the following workflow:
        Download the RAR file from Telegram.
        Upload the RAR file to the remote server using SSH.
        Unpack the RAR file on the remote server.
        Execute a QGIS script on the remote server to create an export.csv file.
        Download the export.csv file from the remote server.
        Send the export.csv file back to the user.
        Delete the files from the remote server and the local machine.

File Description

    main.py: The main script that initializes the Telegram bot, registers message handlers, and starts the bot.
    bot.py: Contains the Telegram bot handlers for commands and document messages.
    ssh.py: Helper functions for SSH operations on the remote server.

Customization

Feel free to modify the code to suit your specific requirements. You can add more message handlers, implement additional SSH operations, or extend the functionality of the bot as needed.

Please note that this code assumes a specific workflow and file structure. Make sure to adapt it to your own setup if necessary.
License

This code is provided under the MIT License. Feel free to use and modify it according to your needs.

If you have any questions or encounter any issues, please don't hesitate to contact me.
