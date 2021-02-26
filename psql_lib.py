

import psycopg2, sys



def insert_domains_into_domainsdb (domain_query_id, domains_list):
	""" 
		Insert the domains_list into the database, adding the domain_query_id
		to the record.
	
		A returned id of -1 indicates an error.
	""" 
	return_code = -1
	insert_query = f"INSERT INTO domains (domain_query_id, "\
						+ ", ".join (domains_list[0].keys ()) + ")"\
				+ " VALUES (%s," + ", ".join (["%s"] * len (domains_list[0].keys ())) + ")" 
	insert_data = []
	for domain in domains_list:
		insert_element = [domain_query_id]
		for v in domain.values ():
			if (v is not None):
				insert_element.append (str (v)[:254])
			else:
				insert_element.append (v)
		insert_data.append (insert_element)

	try:
		conn = psycopg2.connect ("dbname=domainsdb")
		cur = conn.cursor ()
		cur.executemany (insert_query, insert_data)
		conn.commit ()
		return_code = 0
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
	finally:
		if (conn is not None):
			conn.close ()
			return return_code

def get_add_domain_query_id (domain_query):
	"""
		Check if the domain_query is in the database,
		add it if not.

		Return the id in either case.

		A returned id of -1 indicates an error.
	"""
	select_query = "SELECT id FROM domain_queries WHERE domain_query LIKE %s"
	insert_query = "INSERT INTO domain_queries (domain_query) VALUES (%s) RETURNING id"
	dq_id = -1
	try:
		conn = psycopg2.connect ("dbname=domainsdb")
		cur = conn.cursor ()
		cur.execute (select_query, (domain_query,))
		select_val = cur.fetchone ()
		if (select_val is None):
			cur.execute (insert_query, (domain_query,))
			dq_id = cur.fetchone ()[0]
			conn.commit ()
		else:
			dq_id = select_val[0]
	except (Exception, psycopg2.DatabaseError) as error:
		print (error)
	finally:
		if (conn is not None):
			conn.close ()
		return dq_id


