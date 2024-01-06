FROM python:3.10

WORKDIR /containerized_RL

COPY requirements.txt .
COPY ./files ./files
RUN pip install -r requirements.txt
CMD [ "streamlit", "run", './files/Streamlit.py && ./files/Streamlit_multi_seg.py' ]