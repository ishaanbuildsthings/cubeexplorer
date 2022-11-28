### Running the server
All commands should be run from the project root directory.
1. Start the virtual env with
  ```source env/bin/activate```
(To deactivate the virtual env, use `deactivate`)
2. Install dependencies with
  ```pip3 install -r requirements.txt```
3. Start the server with
  ```flask --app server/app run```

For subsequent runs, you can skip steps 1-2 if there are no changes to the dependencies.
