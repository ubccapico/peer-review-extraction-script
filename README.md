# Peer Review Extraction Script

## Introduction

The purpose of this script is to provide an easy way for instructors to gather the results of their peer review activity in Canvas. Currently, there is no easy way to collect student peer reviews in Canvas.

## Main Features
- Extracts each of the students Peer Reviews.
- Extraction includes the general comments posted by the reviewer, the score and comment they provided for each of the rubric criteria, as well as the "median" of all the total grades provided.
- Extracted reviews are exported as an organized excel sheet.
- The script can be modified to calculate the total grade differently.
- A separate log is created to list any errors that were encountered.

## Requirements
- Python 3
- A Canvas API Token 
- The base URL "https://canvas.ubc.ca"
- The course ID of the course. For example: https://ubc.instructure.com/courses/29 (the Course ID of this course is 29)

## How to get a Canvas API token
1. Log-in to canvas.ubc.ca
2. Click on "Account" on the left hand Global Navigation menu
3. Click on "Settings" 

![settings](https://github.com/jguarin16/screenshots/blob/master/account_settings.png)

4. Scroll to the very bottom of the page, then click on the ![new_access_token](https://github.com/jguarin16/screenshots/blob/master/access_token_button.png) button
5. Provide a purpose under the "Purpose feed", then click on "Generate Token"

![access-token-window](https://github.com/jguarin16/screenshots/blob/master/access_token_window.png)

6. Copy and Paste the token provided to you onto a secure/encrypted file called "token" in your local repository. Once you close this window, you will not be able to access the token again, so please be careful where you save your text file.

![access-token-details](https://github.com/jguarin16/screenshots/blob/master/save_token.png)

## How to run the script
1. To run using the terminal, navigate to the folder which contains the local repository and type in `python3 PeerReviewExtraction.py`
2. Enter the course id and assignment id
3. If it ran successfully, your IDLE window will print "Done".
4. You should see a "Data.xlsx" file within the same directory of the script, this is the output you provide to the instructor. 

If you encounter any errors, please contact arts.helpdesk@ubc.ca


