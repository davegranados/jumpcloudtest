JumpCloud Password Hash Testing Document

Assumptions:
As this is intended for production, all issues/design suggestions will be reported with that perspective in mind, and logged under the Issues tab on this repository: https://github.com/davegranados/jumpcloudtest/issues

Password Hash Design Review:
- This endpoint should be https
- Consider making the PORT value configurable via a config file, to handle the situation where the expected port is in use by another resource on the SUT.
- The same proposed config file would also have a value for the time before shutdown, so that a longer shutdown time could be used to make manually testing the shutdown specifications easier.
- Enhance the possible responses to deal with weak passwords/prohibited password characters. These could also be a part of the theoretical config file

Windows Specific issues:
The Jump Cload Password Hashing document ('The Document') has an issue with running curl on windows. Double quotes must be used in order for the commands to execute successfully. So:

curl -X POST -H "application/json" -d '{"password":"angrymonkey"}' http://127.0.0.1:8088/hash

Becomes (note the escaped double quotes, using an image here since Github apparently doesn't allow escaped backslashes in this file):
![image](https://user-images.githubusercontent.com/36861783/142569590-c051c7e1-78dd-4a7d-8414-9613908723bf.png)

curl -X POST -H "application/json" -d “{\"password\":\"angrymonkey\"}” http://127.0.0.1:8088/hash

and:

curl -X POST -d 'shutdown' http://127.0.0.1:8088/hash 

Becomes:

curl -X POST -d “shutdown” http://127.0.0.1:8088/hash 

Testing documents:
Located in this repository
Test Environment Setup Notes for Manual and Automated testing
Password Hash Testcases (spreadsheet)
Initial Automated Testcases

