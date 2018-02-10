FROM python:3
ENV PYTHONUNBUFFERED 1
ENV DIRAPP /code
RUN mkdir $DIRAPP
WORKDIR $DIRAPP
ADD requirements.txt $DIRAPP/
RUN pip install -r requirements.txt
# ADD . $DIRAPP/
