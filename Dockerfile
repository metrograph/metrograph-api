FROM python:3.8.0

# Copying Project
WORKDIR /usr/src/app
COPY . .
COPY requirements.txt ./

# Installing Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Making Actions folders structure
RUN mkdir -p /home/metrograph/templates
RUN mkdir -p /home/metrograph/actions

# ENV Configuration
ENV PYTHONDONTWRITEBYTECODE=1
ENV METROGRAPH_HOME=/home/metrograph

# Pulling latest Action Templates
RUN git clone https://github.com/metrograph/metrograph-actions-templates.git /home/metrograph/templates

CMD [ "python", "./start.py" ]