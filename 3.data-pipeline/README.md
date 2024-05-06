# Mage.ai
## Local
### Project management
1. get local.env from owner to project directory and run genarate .env
```
make local-config
```
2. run start project
```
make local-start
```
or run force build and start project
```
make local-start-build
```
3. view on https://localhost:6789/ with username is 
```
admin@admin.com
``` 
and password is 
```
admin
```
4. stop project
```
make local-stop
```

## Additional config
### Python dependency
edit `requirements.txt` in path
```
./mage-ai/default_repo/requirements.txt
```