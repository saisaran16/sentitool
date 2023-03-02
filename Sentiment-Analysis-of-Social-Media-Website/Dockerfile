# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9.2

WORKDIR /user/src/app

# Install pip requirements
COPY './requirements.txt' .

RUN python -m pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
