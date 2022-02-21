# How to run the code
## CMD Commands to link github repo
### Step One: Initialise a git repo
`git init`
### Step Two: Link the remote branch to the github repo and pull the code
`git remote add origin https://github.com/scalablegrp/caproject.git`  
then  
`git pull origin main`
### Step Three: Create virtual environment(May be different command depending on Code Editor) and activate virtual environment
`python -m venv venv`  
then  
`source env/bin/activate` or `source venv\Scripts\activate`
### Step Four: Install Project dependencies
`pip install -r requirements.txt`
### Step Five: Enter hidden environment variable details
Create env.py file at project root and insert environment variables
### Step Six: Create the database schema
`python manage.py makemigrations`  
then  
`python manage.py migrate`
### Step Seven: Run the django project
change directory until located at project_config root and enter python manage.py runserver 8080 into the cmd line






