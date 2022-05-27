FROM python:3.7.0

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -i https://test.pypi.org/simple/ metrograph==0.0.4
RUN mkdir -p /home/metrograph/templates
RUN mkdir -p /home/metrograph/actions
RUN git clone https://github.com/metrograph/metrograph-actions-templates.git /home/metrograph/templates

COPY . .

CMD [ "python", "./start.py" ]