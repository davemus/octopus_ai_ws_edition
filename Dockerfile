FROM python:3.6

RUN useradd -ms /bin/bash control
RUN apt-get update && \
    apt-get install unzip && \
    apt-get clean
RUN mkdir /app
RUN chown control /app

USER control
ADD requirements* /tmp/

RUN pip install --user -r /tmp/requirements.txt && \
    pip install --user -r /tmp/requirements_cpu.txt

ENV PATH=$PATH:/home/control/.local/bin
ENV PYTHONPATH=$PYTHONPATH:/app/

RUN jupyter contrib nbextension install --user

CMD "/bin/bash"
