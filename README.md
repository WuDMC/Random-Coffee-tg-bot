
in 2022 that bot had helped 400+ people to find potential friends during very hard period.
![image](https://github.com/WuDMC/Batumi-Random-Coffee/assets/65350779/b664f9ca-2737-479d-8149-93b8f3ba6b1d)

One of the reasons of ending of the project is the issue linked with scaling: when number of users become more that 300 bot starts skipps some scheduled events =(

fix: use WebHooks instead of API and implement async methods


## Deploy:

```bash
echo "TELEGRAM_TOKEN=************
ADMINS=username1 username2" > .env
docker-compose up -d
```
