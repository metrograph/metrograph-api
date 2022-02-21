FROM python:3.7.0

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -i https://test.pypi.org/simple/ metrograph==0.0.1.post1
RUN mkdir -p /home/metrograph/uploads
RUN mkdir -p /home/metrograph/flat_tasks

COPY . .

CMD [ "python", "./metrograph-api.py" ]