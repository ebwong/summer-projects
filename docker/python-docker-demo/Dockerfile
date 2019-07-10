# escape=`
FROM python:3

WORKDIR C:\Users\Andrew\PycharmProjects\docker-demo

ADD fibonacci.py ./

ADD test_fibonacci_pytest.py ./

RUN pip install pytest

CMD [ "python", "./test_fibonacci_pytest.py" ]