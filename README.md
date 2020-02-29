# KUDrop

KUDrop is a chatbot for helping Kasetsart University students decide whether it's a good idea for them to drop a course during the middle of semester.

## Features
* Rule-based chatbot.
* Students automatically receives grade report via Line chat.
* GradePredictorGUI for easy updating grade data of each subject.
* One-click report grade to all students of each subject using GradePredictorGUI.
* AI based on machine learning algorithm with logistic regression for predicting the chances of failing each subject. 

## Usage
### Launch GradePredictorGUI
```
python myapp.py
```

### Requirements

python >= 3.6

### How to use: Teacher/Admin
* Launch GradePredictorGUI.exe
* Use **Browse** button inside **Input Train Data** to load train data from *.csv file
* Confirm that **Accuracy** of the module inside **AI-Rating** is between 0 and 1
* Use **Browse** button inside **Input Test Data** to load test data from *.csv file
* Wait until results show up in **Analyzation Result** field.
* Export to *.csv: use **Export to CSV** button
* Export to databse: use **Export to Database** button  
* Report grades to the students: use **Broadcast to Receivers** button  
    * Only students who registered their studentID via Line chat will receive the report. However, they can still view it through chatbot after registering the student ID.
    
### How to use: Student
* Add the linebot as a friend using QR code/Line ID.
* Type a correct 10-digits student ID and press send.
* The linebot will confirm the registration.

## Build
* The project uses heroku to host linebot and google sheet to store students' data.
