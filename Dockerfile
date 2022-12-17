FROM python:3.8

WORKDIR /src/

COPY . .

EXPOSE 8501

COPY . .

RUN pip3 install --upgrade pip &&\
		pip3 install -r requirements.txt

CMD python -m streamlit run application.py server=“0.0.0.0” --server.enableCORS=false