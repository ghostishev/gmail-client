# gmail-client
To run this project:
```
docker-compose up -d
```
Then connect to web image
```
docker-compose exec web bash
```
And do migrations
```
python manage.py migrate
```
Then go to: [http://localhost](http://localhost)

note: You can change port in docker-compose.yml (in the root of repo)

# After instalation
* click on "Sing in with Google"
* give access to read emails
* click "Load messages" (at first time, may take up to 1 minute)
* last 100 emails (reduced) will apper below
