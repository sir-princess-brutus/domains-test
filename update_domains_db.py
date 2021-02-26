#!/usr/bin/python3
"""
	Usage:
		./update_domains_db.py <dq1> <dq2> ...

		Each dqi is a domain substring to check on domainsdb.info,
		for example 'lava' is the given domain to track.
"""
# System libraries
import sys, psycopg2, psycopg2.extras
from datetime import datetime as dt

# Project libraries
import domainsdb_lib, psql_lib

# All the domains to check and add to the database.
domain_queries = sys.argv[1:]

# Connect to database
conn = psycopg2.connect ("dbname=domainsdb")
cursor = conn.cursor (cursor_factory = psycopg2.extras.DictCursor)

# Open Log file
log_file = open ("domain_updates.log", "a")

# Remove half the API domains for testing deleting.
remove_half_api = False

for domain_query in domain_queries:
	# Get domain_query_id form our database, add if not 
	domain_query_id = psql_lib.get_add_domain_query_id (domain_query)

	# Get domain list from API
	[status, domain_info] = domainsdb_lib.query_domainsdb_domains ({"domain": domain_query})
	if (status != 200):
		sys.stderr.write (f"ERROR ({status}): Failed to get domains for {domain_query}.\n")
		continue


	# Get current domain list
	cursor.execute ("SELECT * FROM domains WHERE deleted_at IS NULL AND domain_query_id = %s",
					(domain_query_id,))
	domains_db_list = cursor.fetchall ()

	# Make sets of domains for comparison
	d_db_set = set ([ddb['domain'] for ddb in domains_db_list])
	if (remove_half_api):
		d_api_set = set ([di['domain'] for i, di in enumerate (domain_info) if (i % 2 == 0)])
	else:
		d_api_set = set ([di['domain'] for di in domain_info])

	# Calculate changes needed for database.
	now = dt.now ()
	domains_to_delete = list (d_db_set - d_api_set)
	delete_domains = [(now, ddb['id']) for ddb in domains_db_list if (ddb['domain'] in domains_to_delete)]

	domains_to_add = list (d_api_set - d_db_set)
	add_domains = [di for di in domain_info if (di['domain'] in domains_to_add)]

	log_message = dt.now ().strftime (f"[%H:%M:%S %m/%d/%Y] Query: {domain_query}\n")
	# Delete domains that are missing 
	if (len (delete_domains) > 0):
		cursor.executemany ("UPDATE domains SET deleted_at = %s WHERE id = %s", delete_domains)
		log_message += f"\t- {len(delete_domains)} Domains Removed\n"
		conn.commit ()
	else:
		log_message += f"\t- No Domains Removed\n"
	
	# Add new domains
	if (len (add_domains) > 0):
		psql_lib.insert_domains_into_domainsdb (domain_query_id, add_domains)
		log_message += f"\t- {len(add_domains)} Domains Added\n"
	else:
		log_message += f"\t- No Domains Added\n"

	log_file.write (log_message)

conn.close ()
log_file.close ()

