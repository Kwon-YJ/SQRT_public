import gdown
import os

file_id = "1JdOlqicvP-ZAj4KEIMfcnynl-Zu3MiQW"
output = "../data/"

os.makedirs(output, exist_ok=True)

gdown.download(id=file_id, output=output, quiet=False)

os.system("unzip ../data/euro.zip -d " + output)

os.system("rm ../data/euro.zip")
