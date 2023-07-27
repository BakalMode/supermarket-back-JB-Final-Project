FROM python:3.11.4-alpine

WORKDIR /supermarket

COPY . /supermarket

RUN pip install virtualenv
RUN python -m virtualenv myenv
RUN source myenv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt


# Expose the default Django development server port (8000) and the additional port (1235)
EXPOSE 8000 


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

