# Project README.md

## Introduction

This project demonstrates how to automate the process of logging into a website that implements Two-Factor Authentication (2FA) using Python. The example uses Selenium WebDriver for web automation and Google's Gmail service for handling the 2FA OTPs.

## Prerequisites

- Python installed on your system.
- Selenium WebDriver installed (`pip install selenium`).
- A valid Gmail account configured for 2FA.

## Getting Started

### Step 1: Download and Extract Code

Download the provided code from the link below and extract its contents.

### Step 2: Study the Functionality

Thoroughly review the code to understand how it interacts with the target website and handles 2FA authentication.

### Step 3: Configure Your Details

Fill in the required details within the script:

- **Login URL**: The URL of the website you're trying to access.
- **Website Username**: Your username for the target website.
- **Website Password**: Your password for the target website.
- **Gmail Username**: Your Gmail address.
- **Gmail App Password**: An app-specific password generated from your Gmail account settings.

### Step 4: Update XPaths

Adjust the XPaths in the script to match the current structure of the target website's login form.

### Step 5: Run the Script

Execute the script in non-headless mode to observe the automation process. This will allow you to see the steps being performed live.


**Note**: This guide assumes the use of a Gmail account for generating OTPs. You may need to modify the code if you choose to use a different method for receiving OTPs.

## Additional Information

- Ensure your Selenium WebDriver is compatible with the version of the browser you intend to use.
- Running the script in headless mode is possible but requires additional setup for capturing screenshots or logs.

## Troubleshooting

If you encounter issues during execution, check the following:

- Verify all credentials and URLs are correctly entered.
- Confirm the XPaths match the current layout of the target website.
- Ensure your Selenium WebDriver is up-to-date and matches your browser version.

## Conclusion

By following these steps, you should be able to successfully automate the login process for websites with 2FA enabled using Python and Selenium. Remember, this approach relies heavily on the current state of the target website, so minor changes to the site's layout may require adjustments to the script.
