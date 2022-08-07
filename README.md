# **Kaufen**
>- A Product trading **web-application**, developed to handle multi-user functionality ( persistance of user-session ). Configured backend apis from users to **buy** and **sell** the items.
>- Visualization of available items in the **database** that are not bought.
>- Built using the **lightweight web-app** framework **Flask**
>- Makes use of an **Object-Relational-Mapper** called **SQLAlchemy**, from which the **relational-database file** can be migrated into a **SQL / Postgres db**.
>- Contains **Dockerfile & Kubernetes-Config** files for production ready deployment on cloud service providers **( AZURE )**  

>![image](https://user-images.githubusercontent.com/72693780/183300179-16a2fd6e-6caf-40d0-9158-8ce173649900.png)

## **Install this on your machine ?**

### **First clone the repo**
```sh
# go to the directory you want
git clone https://github.com/Aryan-Deshpande/Kaufen.git
```
### **Install dependencies**
```sh
# make sure you have python
pip install -r requirements.txt
```
### **Run the web application locally**
```sh
flask run
```
## *AND YOUR READY TO TEST !*
![image](https://user-images.githubusercontent.com/72693780/183302335-85834aca-76eb-4dd2-811a-46f4392d20f0.png)
>### *For production the debugger mode will be removed, and will use a production server like **gunicorn***
