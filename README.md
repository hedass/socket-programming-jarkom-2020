# socket-programming-jarkom-2020


## Quick Usage
1. Go to project root.
2. Set `PYTHONPATH`
   ```sh
   export PYTHONPATH=nodes
   ```
3. Start worker:
    ```sh
    python nodes/worker/app.py
    ```
4. Start master:
    ```sh
    python nodes/master/app.py
    ```
5. Start client:
    * Make sure you already installed all dependencies

        ```sh
        pip install -r nodes/client/requirements.txt
        ```

    * Set `FLASK_APP`

        ```sh
        export FLASK_APP=nodes/client/app.py
        ```

    * Run

        ```sh
        flask run
        ```
