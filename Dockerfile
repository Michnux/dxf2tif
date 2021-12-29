FROM python:3.8

COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --trusted-host=pypi.org --trusted-host=files.pythonhosted.org -r requirements.txt

COPY script_dir /home/script_dir/

CMD ["python", "/home/script_dir/main.py"]
#CMD ["sleep", "1d"]
