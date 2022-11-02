FROM python:3.8
ENV url=$url
ENV profile=$profile
COPY requirements.txt .
RUN pip3 install -r requirements.txt
ADD main.py /
CMD ["sh", "-c", "python ./main.py","--url $url","--profile $profile"]
