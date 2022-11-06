# Face Registration Application

## Installation Instruction

Upon Extracting the folder to a suitable place, open command line and navigate to the directory where facereg is extracted.
It will contain 2 directories : backend and frontend. 

in The command line , enter the following commands

```

cd backend

pip install -r requirements.txt

python app.py


```

After the Flask Server is running, Leave the terminal as it is.  

Go to the frontend directory, and open index.html in any browser. It is configured to send requests to that flask server that is running.


## Deployment Instruction

Front end can be deployed anywhere, it is independent from backend and does not have any dependency.

To Deploy Backend on internet, minor changes are needed. The Server's IP has to be entered in env.py file's HOME variable.