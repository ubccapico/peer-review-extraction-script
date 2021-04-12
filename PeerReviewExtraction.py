import requests
import json
import pprint
import string
import time
import CanvasAPI_functions as API
    
url = "https://ubc.instructure.com"
course_id = input("Enter course_id:")
assignment_id = input("Enter assignment_id:")
choice = input("Enter 1 for mean and 2 for median: ")
student_ids = {}
student_submissions = {}
column_letters = list(string.ascii_uppercase)
comments_received = {}
names = []
total_score = []
comment = []
score = []
log = open('log.txt', 'w')
current_time = time.strftime("%B %d, %Y %I:%M:%S %p")
log.write(current_time + ": Script start\n")
print("Processing token...")
try:
    with open('token', 'r') as token_file:
        token = token_file.read()
except FileNotFoundError:
    print("There was no token file found in this directory")
    token = input('Please enter your token:\n')

while True:
    test_request = requests.get(url + '/api/v1/users/self/profile',
                                headers = {'Authorization': 'Bearer ' + token})
    if test_request.status_code == requests.codes.ok:
        print("\nToken is valid, the program will proceed.\n")
        current_time = time.strftime("%B %d, %Y %I:%M:%S %p")
        log.write(current_time + ": Token processed\n")
        break
    else:
        print("\nThe token being used is invalid")
        token = input("Pleease enter a valid token:\n")
        current_time = time.strftime("%B %d, %Y %I:%M:%S %p")
        log.write(current_time + ": Token entered was invalid\n")

rubric_criterias = API.get_rubric_criterias(course_id, assignment_id, token)
    
current_time = time.strftime("%B %d, %Y %I:%M:%S %p")
log.write(current_time + ": Start gathering students\n")
user_request = requests.get(url + '/api/v1/courses/' + course_id +  '/users?per_page=100',
                            headers = {'Authorization': 'Bearer ' + token},
                            params = {'enrollment_type' : 'student'},
                            timeout = 60)
if user_request.status_code == requests.codes.ok:
    student_list = json.loads(user_request.text)
    student_ids = API.get_students(student_ids,
                                   user_request,
                                   student_list,
                                   log,
                                   url,
                                   course_id,
                                   token)
else:
    current_time = time.strftime("%B %d, %Y %I:%M:%S %p")
    log.write(current_time + ": ERROR! ERROR! Something went wrong gethering the students in the course!\n")
    log.write(current_time + ": Script Terminated\n")
    log.close()
    print("ERROR! ERROR! Something went wrong gethering the students in the course!")
    print(user_request.raise_for_status())
    

for student in student_ids.values():
    comments_received[student] = {}

current_time = time.strftime("%B %d, %Y %I:%M:%S %p")
log.write(current_time + ": Start gathering submissions\n")       
submission_request = requests.get(url + '/api/v1/courses/' + course_id +  '/assignments/' + assignment_id + '/submissions?per_page=100',
                                  headers = {'Authorization': 'Bearer ' + token},
                                  params = {'include': 'submission_comments'},
                                  timeout = 60)
if submission_request.status_code == requests.codes.ok:
    submissions = json.loads(submission_request.text)
    student_submissions = API.get_submissions(student_ids,
                                              student_submissions,
                                              comments_received,
                                              submission_request,
                                              submissions,
                                              log,
                                              url,
                                              course_id,
                                              token)
else:
    current_time = time.strftime("%B %d, %Y %I:%M:%S %p")
    log.write(current_time + ": ERROR! ERROR! Something went wrong gathering submissions in your course!!\n")
    log.write(current_time + ": Script Terminated\n")
    log.close()
    print("ERROR! ERROR! Something went wrong gathering submissions in your course!!")
    print(submission_request.raise_for_status())

current_time = time.strftime("%B %d, %Y %I:%M:%S %p")
log.write(current_time + ": Start rubric comments and scores\n")
assignment = requests.get(url + '/api/v1/courses/' + course_id +  '/assignments/' + assignment_id,
                          headers= {'Authorization': 'Bearer ' + token},
                          timeout = 60)
if assignment.status_code == requests.codes.ok:
    assignment_json = json.loads(assignment.text)
    rubric_id = assignment_json['rubric_settings']['id']
    rubric = requests.get(url + '/api/v1/courses/' + course_id +  '/rubrics/' + str(rubric_id),
                          headers = {'Authorization': 'Bearer ' + token},
                          params = {'include' : 'peer_assessments',
                                  'style' : 'full'},
                          timeout = 60)
    if rubric.status_code == requests.codes.ok:
        rubric_json = json.loads(rubric.text)
        comments_received = API.get_comments(student_ids,
                                             student_submissions,
                                             comments_received,
                                             rubric_criterias,
                                             rubric,
                                             rubric_json,
                                             log,
                                             url,
                                             course_id,
                                             token)
        if(choice == '1'):
             API.calc_mean(comments_received, log)
        else:
            API.calc_median(comments_received,
                        log)
    else:
        current_time = time.strftime("%B %d, %Y %I:%M:%S %p")
        log.write(current_time + ": ERROR! ERROR! Something went wrong with getting the rubric used for the assignment\n")
        log.write(current_time + ": Script Terminated\n")
        log.close()
        print("ERROR! ERROR! Something went wrong with getting the rubric used for the assignment")
        print(submission_request.raise_for_status())

else:
    current_time = time.strftime("%B %d, %Y %I:%M:%S %p")
    log.write(current_time + ": ERROR! ERROR! Something went wrong with getting the rubric used for the assignment\n")
    log.write(current_time + ": Script Terminated\n")
    log.close()
    print("ERROR! ERROR! Something went wrong with getting the rubric used for the assignment")
    print(submission_request.raise_for_status())

current_time = time.strftime("%B %d, %Y %I:%M:%S %p")
log.write(current_time + ": Start creating output file\n")
wb = API.create_spreadsheet(comments_received,
                            column_letters, choice)
current_time = time.strftime("%B %d, %Y %I:%M:%S %p")
log.write(current_time + ": output created\n")
log.write(current_time + ": script successful\n")
log.close()
wb.save('Data.xlsx')
print('Done')

