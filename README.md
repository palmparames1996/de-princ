# de-princ
# Document
1. Share drive [link](https://drive.google.com/drive/folders/1n6n5myH8v6n1ckqdePMRc7jGPPdgf69x?usp=drive_link)
2. Architecture diagram [link](https://app.diagrams.net/#G1UByLyQ7g99ZrXpV32XSAHFqsCakOLm8t#%7B%22pageId%22%3A%22stoSwr8YLAssgLjYIWNs%22%7D)

# Data orchestration on local
1. Create .env in 3.data-pipeline folder
```
make local-env
```
2. Start Data orchestration on docker
```
make local-start
```
3. Use [IU](http://localhost:6789/)
4. Stop Data orchestration on docker
```
make local-stop
```
# Note
1. You can find my code on [Pipeline](http://localhost:6789/pipelines) consist of
- init pipeline : pull sqlite and google drive config from my private s3
- Scenario_1 pipeline : follow objective of Scenario 1
- Scenario_2 pipeline : follow objective of Scenario 2
- Scenario_3 pipeline : follow objective of Scenario 3
- Scenario_4 pipeline : follow objective of Scenario 4
2. You can't test on your local because project need my secret key for init pipeline but i can show on interview
3. I choose kubernetes because it is scalable. But it only made me finish the continuous integration (continuous delivery by manual) in a limited time.
4. I was able to find a way to automate sending emails on the internet. But I've never set up a smtp server. Therefore, this part is still missing.