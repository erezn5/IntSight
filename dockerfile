FROM python:3.8.3

# Create app directory
WORKDIR /intSight

# copy the requirements file to the working directory
COPY requirements.txt ./

# then install the requirements before running the app
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the file
COPY . /intSight