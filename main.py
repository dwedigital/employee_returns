import time
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables from .env file
load_dotenv()

# Retrieve username and password from environment variables
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Ensure credentials are provided
if not username or not password:
    raise ValueError("Please provide both USERNAME and PASSWORD in the .env file.")


# Main function to perform the login
def login_to_website():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(
            headless=False
        )  # Set headless=True to run without UI

        page = browser.new_page()

        # Navigate to the login page
        page.goto("https://empret.jsytax.je/empweb")

        # print the html
        # print(page.inner_html("body"))

        # Wait for the login form to load
        page.wait_for_selector(
            'input[name="ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$LoginUser$UserName"]'
        )  # Update the selector if necessary

        # Fill in the login form
        page.fill(
            'input[name="ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$LoginUser$UserName"]',
            username,
        )  # Assuming the username input has this name
        page.fill(
            'input[name="ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$LoginUser$Password"]',
            password,
        )  # Assuming the password input has this name

        # Submit the form (assuming the submit button has this selector)
        page.click('input[type="submit"]')

        # check that text appears on the page
        page.wait_for_selector("#ContentPlaceHolder1_ContentPlaceHolder1_Label1")

        print("Login successful!")

        page.click('input[type="submit"]')
        page.wait_for_event("load")

        # find the first row in the table ()
        if page.is_visible("#ContentPlaceHolder1_ContentPlaceHolder1_grdReturnsNew"):
            print("returns to be processed")
            # get number of rows in the table
            rows = page.query_selector_all(
                "#ContentPlaceHolder1_ContentPlaceHolder1_grdReturnsNew > tbody > tr"
            )
            print(len(rows))
            for i in range(1, len(rows)):
                print(i)
                page.click(
                    f"#ContentPlaceHolder1_ContentPlaceHolder1_grdReturnsNew > tbody > tr:nth-child(2) > td:nth-child(4) > a"
                )
                page.click(
                    "#ContentPlaceHolder1_ContentPlaceHolder1_ContentPlaceHolder1_cmdNext"
                )
                page.click(
                    "#ContentPlaceHolder1_ContentPlaceHolder1_ContentPlaceHolder1_cmdNext"
                )
                page.click(
                    "#ContentPlaceHolder1_ContentPlaceHolder1_ContentPlaceHolder1_cmdNext"
                )
                page.click(
                    "#bodycontent > div.wizard-area > table > tbody > tr:nth-child(2) > td:nth-child(1) > a"
                )
                page.click(
                    "#bodycontent > div.wizard-area > table > tbody > tr:nth-child(1) > td:nth-child(2) > a"
                )
                page.click(
                    "#ContentPlaceHolder1_ContentPlaceHolder1_ContentPlaceHolder1_grdEmployees > tbody > tr:nth-child(2) > td:nth-child(6) > a:nth-child(1)"
                )
                page.fill(
                    "#ContentPlaceHolder1_ContentPlaceHolder1_ContentPlaceHolder1_txtGrossPay",
                    "0",
                )
                page.fill(
                    "#ContentPlaceHolder1_ContentPlaceHolder1_ContentPlaceHolder1_txtTaxDed",
                    "0",
                )

                page.click(
                    "#ContentPlaceHolder1_ContentPlaceHolder1_ContentPlaceHolder1_cmdNext"
                )
                page.click(
                    "#ContentPlaceHolder1_ContentPlaceHolder1_ContentPlaceHolder1_cmdNext"
                )
                page.click(
                    "#ContentPlaceHolder1_ContentPlaceHolder1_ContentPlaceHolder1_cmdNext"
                )
                page.wait_for_event("load")
                # Fill in the submitter details
                page.fill(
                    "#ContentPlaceHolder1_ContentPlaceHolder1_ContentPlaceHolder1_txtSubmitterPhoneNumber",
                    "07788275564",
                )
                time.sleep(1)
                page.check(
                    "#ContentPlaceHolder1_ContentPlaceHolder1_ContentPlaceHolder1_chkAgree"
                )
                page.click(
                    "#ContentPlaceHolder1_ContentPlaceHolder1_ContentPlaceHolder1_cmdSubmit"
                )
                page.goto(
                    "https://empret.jsytax.je/EmpWeb/Services/Employer/Default.aspx"
                )

        else:
            print("No returns to be processed")
        
        # print date and timestamp
        print(time.strftime("%Y-%m-%d %H:%M:%S"))

        # Wait for a few seconds to see the result
        time.sleep(5)

        # Close the browser
        browser.close()


if __name__ == "__main__":
    login_to_website()
