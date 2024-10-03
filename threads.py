from sqlalchemy.sql import text
from db import db
from flask import session

def get_all_areas():
    if "user_name" in session.keys():
        sql = "SELECT id, area FROM areas ORDER BY area"
        areas=db.session.execute(text(sql)).fetchall()
        sql = "SELECT area_id, area_name FROM private_areas ORDER BY area_id"
        all_areas_private=db.session.execute(text(sql)).fetchall()
        sql = "SELECT area_id, area_name FROM private_areas WHERE user_name='%s'" %session["user_name"]
        areas_private=db.session.execute(text(sql)).fetchall()
        for area_id in set(all_areas_private):
            if area_id not in areas_private:
                areas.remove(area_id)
        temp_areas=[]
        for area in areas:
            sql = "SELECT id, chain FROM chains WHERE area_id=%s" %area[0]
            chains=db.session.execute(text(sql)).fetchall()
            all_chain_messages=[]
            for chain in chains:
                sql = "SELECT sent_at FROM chain_messages WHERE chain_id=%s ORDER BY sent_at" %chain[0]
                chain_messages=db.session.execute(text(sql)).fetchall()
                for chain_message in chain_messages:
                    all_chain_messages.append(chain_message[0])
            all_chain_messages.sort()
            if len(chains) > 0 and len(all_chain_messages) > 0:
                temp_areas.append([area[0],area[1],len(chains),len(all_chain_messages),all_chain_messages[-1]])
            elif len(chains) > 0:
                temp_areas.append([area[0],area[1],len(chains),0,'Na'])
            else:
                temp_areas.append([area[0],area[1],0,0,'Na'])
        return temp_areas

def get_area_info(area_id):
    sql = "SELECT area FROM areas WHERE id=%s" %str(area_id)
    name=db.session.execute(text(sql)).fetchone()
    return name[0]


def add_area(area_id,chain,content):
    sql = "SELECT area_id, area_name FROM private_areas WHERE area_id=%s" %area_id
    all_areas_private=db.session.execute(text(sql)).fetchall()
    sql = "SELECT area_id, area_name FROM private_areas WHERE user_name='%s' AND area_id=%s" %(session["user_name"],area_id)
    areas_private=db.session.execute(text(sql)).fetchall()
    if len(all_areas_private) > 0 and len(areas_private) == 0:
        pass
    else:
        sql = "INSERT INTO chains (chain, area_id, creator_name) VALUES ('%s', %s, '%s');" %(chain,str(area_id),session["user_name"])
        db.session.execute(text(sql))
        db.session.commit()
        sql = "SELECT id FROM chains ORDER BY id"
        areas=db.session.execute(text(sql)).fetchall()
        sql = "INSERT INTO chain_messages (message, sent_at, chain_id, creator_name) VALUES ('%s', NOW(), %s, '%s');" %(content,str(areas[-1][0]),session["user_name"])
        db.session.execute(text(sql))
        db.session.commit()
    return ' '

def get_all_chains(area_id):
    sql = "SELECT area_id, area_name FROM private_areas WHERE area_id=%s" %area_id
    all_areas_private=db.session.execute(text(sql)).fetchall()
    sql = "SELECT area_id, area_name FROM private_areas WHERE user_name='%s' AND area_id=%s" %(session["user_name"],area_id)
    areas_private=db.session.execute(text(sql)).fetchall()
    if len(all_areas_private) > 0 and len(areas_private) == 0:
        return 0
    else:
        sql = "SELECT chain, id, area_id FROM chains WHERE area_id=%s ORDER BY chain" %area_id
        chains=db.session.execute(text(sql)).fetchall()
        temp_chains=[]
        for chain in chains:
            temp_chains.append([chain[0],chain[1]])
        return temp_chains

def get_all_messages(chain_id):
    sql = "SELECT area_id FROM chains WHERE id=%s" %chain_id
    area_id=db.session.execute(text(sql)).fetchall()
    sql = "SELECT area_id, area_name FROM private_areas WHERE area_id=%s" %area_id[0][0]
    all_areas_private=db.session.execute(text(sql)).fetchall()
    sql = "SELECT area_id, area_name FROM private_areas WHERE user_name='%s' AND area_id=%s" %(session["user_name"],area_id[0][0])
    areas_private=db.session.execute(text(sql)).fetchall()
    if len(all_areas_private) > 0 and len(areas_private) == 0:
        return 0
    else:
        sql = "SELECT message, id, sent_at, chain_id, creator_name FROM chain_messages WHERE chain_id=%s ORDER BY sent_at" %chain_id
        messages=db.session.execute(text(sql)).fetchall()
        temp_messages=[]
        for message in messages:
            temp_messages.append([message[0],message[1],message[2],message[4]])
        return temp_messages

def add_message(chain_id,message):
    sql = "SELECT area_id FROM chains WHERE id=%s" %chain_id
    area_id=db.session.execute(text(sql)).fetchall()
    sql = "SELECT area_id, area_name FROM private_areas WHERE area_id=%s" %area_id[0][0]
    all_areas_private=db.session.execute(text(sql)).fetchall()
    sql = "SELECT area_id, area_name FROM private_areas WHERE user_name='%s' AND area_id=%s" %(session["user_name"],area_id[0][0])
    areas_private=db.session.execute(text(sql)).fetchall()
    if len(all_areas_private) > 0 and len(areas_private) == 0:
        pass
    else:
        sql = "INSERT INTO chain_messages (message, sent_at, chain_id, creator_name) VALUES ('%s', NOW(), %s, '%s');" %(message,str(chain_id),session["user_name"])
        db.session.execute(text(sql))
        db.session.commit()
    return ' '

def add_new_area(area_name):
    sql = "INSERT INTO areas (area, role, creator_name) VALUES ('%s', 1, '%s');" %(area_name,session["user_name"])
    db.session.execute(text(sql))
    db.session.commit()
    return ' '

def get_areas():
    sql = "SELECT id, area FROM areas ORDER BY area"
    areas=db.session.execute(text(sql)).fetchall()
    return areas

def get_chains_messages():
    sql = "SELECT chain, id, creator_name FROM chains ORDER BY id"
    chains=db.session.execute(text(sql)).fetchall()
    chains_messages=[]
    for chain in chains:
        sql = "SELECT area_id FROM chains WHERE id=%s" %chain[1]
        area_id=db.session.execute(text(sql)).fetchall()
        sql = "SELECT area_id, area_name FROM private_areas WHERE area_id=%s" %area_id[0][0]
        all_areas_private=db.session.execute(text(sql)).fetchall()
        sql = "SELECT area_id, area_name FROM private_areas WHERE user_name='%s' AND area_id=%s" %(session["user_name"],area_id[0][0])
        areas_private=db.session.execute(text(sql)).fetchall()
        if len(all_areas_private) > 0 and len(areas_private) == 0:
            pass
        else:
            sql = "SELECT message, id, creator_name, sent_at FROM chain_messages WHERE chain_id='%s' ORDER BY id" %chain[1]
            messages=db.session.execute(text(sql)).fetchall()
            if len(messages) > 0:
                chains_messages.append([chain,messages])
            else:
                chains_messages.append([chain,[('Ei viestejä','','')]])
    return chains_messages

def get_users():
    sql = "SELECT name, id FROM users ORDER BY name"
    users=db.session.execute(text(sql)).fetchall()
#    temp=db.session.execute(text(sql)).fetchall()
#    users=[]
#    i=1
#    for user in temp:
#        users.append([user[0],i])
#        i=i+1
    return users

def check_users(username):
    sql = "SELECT name FROM users WHERE name='%s'" %username
    temp=db.session.execute(text(sql)).fetchall()
    return len(temp)

def check_areas(area_name):
    sql = "SELECT area FROM areas WHERE area='%s'" %area_name
    temp=db.session.execute(text(sql)).fetchall()
    return len(temp)


def delete_area(area_name):
    sql = "SELECT id FROM areas WHERE area='%s'" %area_name
    area_id=db.session.execute(text(sql)).fetchall()[0][0]
    sql = "SELECT id FROM chains WHERE area_id=%s" %area_id
    chain_ids=db.session.execute(text(sql)).fetchall()
    message_ids=[]
    for chain_id in chain_ids:
        sql = "SELECT id FROM chain_messages WHERE chain_id=%s" %chain_id[0]
        message_ids=message_ids+db.session.execute(text(sql)).fetchall()
    for message in message_ids:
        sql = "DELETE FROM chain_messages WHERE id=%s;" %str(message[0])
        db.session.execute(text(sql))
        db.session.commit()
    for chain in chain_ids:
        sql = "DELETE FROM chains WHERE id=%s;" %str(chain[0])
        db.session.execute(text(sql))
        db.session.commit()
    sql = "DELETE FROM areas WHERE id=%s;" %area_id
    db.session.execute(text(sql))
    db.session.commit()    
    return ' '

def search_messages(key_word):
    key_word_mod='%'+key_word+'%'
    sql = "SELECT id, message, chain_id FROM chain_messages WHERE message LIKE '%s'" %key_word_mod
    messages=db.session.execute(text(sql)).fetchall()
    for chain in messages:
        sql = "SELECT area_id FROM chains WHERE id=%s" %chain[2]
        area_id=db.session.execute(text(sql)).fetchall()
        sql = "SELECT area_id, area_name FROM private_areas WHERE area_id=%s" %area_id[0][0]
        all_areas_private=db.session.execute(text(sql)).fetchall()
        sql = "SELECT area_id, area_name FROM private_areas WHERE user_name='%s' AND area_id=%s" %(session["user_name"],area_id[0][0])
        areas_private=db.session.execute(text(sql)).fetchall()
        if len(all_areas_private) > 0 and len(areas_private) == 0:
            messages.remove(chain)
    sql = "SELECT id, chain, area_id FROM chains"
    all_chains=db.session.execute(text(sql)).fetchall()
    sql = "SELECT id, area FROM areas"
    all_areas=db.session.execute(text(sql)).fetchall()
    m={}
    for m1 in messages:
        if m1[2] not in m.keys():
            m[m1[2]]=[m1[1]]
        else:
            m[m1[2]].append(m1[1])
    c={}
    c0={}
    c_ids={}
    for c1 in all_chains:
        if c1[0] in m.keys():
            if c1[2] not in c.keys():
                c[c1[2]]=[c1[1]]
            else:
                c[c1[2]].append(c1[1])
            if c1[0] in m.keys():
                c0[c1[1]]=m[c1[0]]
            c_ids[c1[1]]=c1[0]
    a={}
    for a1 in all_areas:
        if a1[0] in c.keys():
            a[a1[1]]=c[a1[0]]
    all_messages=[]
    for a_key in a.keys():
        temp1=[]
        for c_key in a[a_key]:
            temp2=[]
            for message in c0[c_key]:
                temp2.append(message)
            temp1.append([c_key,c_ids[c_key],temp2])
        all_messages.append([a_key,temp1])
    print(all_messages)
    return all_messages

def add_private_area(area_name,users):
    sql = "INSERT INTO areas (area, role, creator_name) VALUES ('%s', 2, '%s');" %(area_name,session["user_name"])
    db.session.execute(text(sql))
    db.session.commit()
    sql = "SELECT id FROM areas ORDER BY id"
    areas=db.session.execute(text(sql)).fetchall()
    for user in users:
        sql = "INSERT INTO private_areas (area_name, user_name, area_id) VALUES ('%s', '%s', %s);" %(area_name,user,areas[-1][0])
        db.session.execute(text(sql))
        db.session.commit()
    return ' '

def get_chain_name(chain_id):
    sql = "SELECT chain FROM chains WHERE id=%s" %str(chain_id)
    all_chains=db.session.execute(text(sql)).fetchall()
    return all_chains[0]

def mod_delete_chain(chainid,newname):
    sql = "UPDATE chains SET chain = '%s' WHERE id = %s;" %(newname,str(chainid))
    db.session.execute(text(sql))
    db.session.commit()
    return ' '

def delete_chain(chainid):
    sql = "SELECT id FROM chain_messages WHERE chain_id=%s" %str(chainid)
    message_ids=db.session.execute(text(sql)).fetchall()
    for message in message_ids:
        sql = "DELETE FROM chain_messages WHERE id=%s;" %str(message[0])
        db.session.execute(text(sql))
        db.session.commit()
    sql = "DELETE FROM chains WHERE id=%s;" %str(chainid)
    db.session.execute(text(sql))
    db.session.commit()
    return ' '

def get_message_name(message_id):
    sql = "SELECT message FROM chain_messages WHERE id=%s" %str(message_id)
    all_messages=db.session.execute(text(sql)).fetchall()
    return all_messages[0]

def mod_delete_message(messageid,newname):
    sql = "UPDATE chain_messages SET message = '%s' WHERE id = %s;" %(newname,str(messageid))
    db.session.execute(text(sql))
    db.session.commit()
    return ' '

def delete_message(messageid):
    sql = "DELETE FROM chain_messages WHERE id=%s;" %str(messageid)
    db.session.execute(text(sql))
    db.session.commit()
    return ' '

def get_area_id(chain_id):
    sql = "SELECT area_id FROM chains WHERE id=%s" %str(chain_id)
    area_id=db.session.execute(text(sql)).fetchall()
    return area_id[0][0]