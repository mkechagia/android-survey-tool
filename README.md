# android-survey
This is an online survey for Android developers.

A. To activate the virtual environment:

cd android_survey/venv/bin
source activate

B. To setup the NotePad app from the command-line (requires the Android SDK):

unzip NotePad.zip
cd NotePad
android update project --path . --subprojects --target android-XX
ant clean debug

C. To run the app:

cd android_survey
python routes.py


Notes:


-Take care of the .css and .json libraries in the templates especially for the form_submit.html file.

-Find installed libraries for the venv in the requirements.txt. To install the libraries use:

pip install -r requirements.txt

-The web site uses Flask 0.11, Python 3.3 and sqlite3.


'''
Copyright 2016 Maria Kechagia
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
