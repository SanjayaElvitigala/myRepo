FROM python:3.10-slim

WORKDIR /containerized_RL

COPY requirements.txt ./requirements.txt
COPY ./files ./files
RUN pip install -r requirements.txt
WORKDIR /containerized_RL/files
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", 'Streamlit.py']