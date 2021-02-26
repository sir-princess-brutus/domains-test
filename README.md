
Lead Data Engineer Interview Task, Lavamap
==========================================

Algorithm for Nightly Script
-------------------------------

1. Pull list of domains by domain substring via API, given substring of "bean."
2. Pull current list of domains for that substring, where `deleted_at` IS NULL.
3. Determine changes to our database:
	1. Domains in the list from the API but not in the current list are added.
	2. Domains in the current list but not the API are deleted.
4. Log if no domains are added, if no domains are deleted.

Querying the Database
----------------------

To query the database for domains, you'll want to know the `domain_query_id`
for the `domain_queries` table:

	SELECT id FROM domain_queries WHERE domain_query LIKE 'bean'

then filter the domains table on that id:

	SELECT * FROM domains WHERE domain_query_id = <id>

To view the changes in a particular domain:

	SELECT * FROM domains WHERE domain LIKE 'xn--bean-3m6f8270b.xyz'

Specifically for the Notes in the task:
1. The WHERE clause on domains will be `domain_query_id = <id for bean> AND deleted_at IS NULL`
2. The WHERE clause on domains will be `domain LIKE '<domain to view>'`
	* `created_at` indicates when the domain was added.
	* `deleted_at` indicates when the domain was removed.

Definition of "Removed" Notes
------------------------------

When I first read the Assingment 3.a, I assumed "Remvoed" meant a domain no longer
shows up in the API request. Upon looking at the data after building the script,
the term "Removed" may mean the `isDead` field flipped from False to True in the API
request. To use this definition of "Removed" we would check if a domain is in the
the database `WHERE deleted_at IS NULL AND isDead = False`, then update `deleted_at`
to the current timestamp to delete it.

Feedback/Notes on Solution
----------------------------

1. Apologies for the delay on delivery, a couple things contributed to it:
	1. Setting up a postgres database server was new to me, but after that the database was familiar.
	2. I spent a bit of time trying to figure out if I was missing something on the API limitations.
	3. End of the month reports took a little more time than I expected.
2. I added the second table to make the database more general to accomodate different different queries.
	* This does introduce the problem of "bean" and "beans" overlapping.
	* In order to join the tables, third table connecting primary keys for many-to-many would be needed.
3. Rather than checking domains in Python, the domins from the API could be loaded into a temporary table
and it could be joined against the current domains, and that could be used to update/add domins.
