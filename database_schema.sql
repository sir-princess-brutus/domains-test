/*
		SQL Commands to create tables for tracking domains.

		The table domains holds:
			- id as primary key
			- created/updated/deleted_at timestamps (updated_at not yet used)
			- domain_query_id to identify which query added the record to the table
			- Other data from domainsdb.info

		The table domain_queries holds:
			- id, create/delete/update as domains table
			- domain_query, the text of the query that found the domain

		Foreign key from domain_query_id in domains to id in domain_queries.
*/

--	domain_queries table
--
		CREATE TABLE domain_queries
		(
			id SERIAL PRIMARY KEY,
			created_at TIMESTAMP DEFAULT NOW(),
			updated_at TIMESTAMP,
			deleted_at TIMESTAMP,
			domain_query VARCHAR (128) NOT NULL
		)
	
--	domains table
--
		CREATE TABLE domains
		(
			id SERIAL PRIMARY KEY,
			created_at TIMESTAMP DEFAULT NOW(),
			updated_at TIMESTAMP,
			deleted_at TIMESTAMP,
			domain_query_id INTEGER REFERENCES domain_queries,
			domain VARCHAR (255) NOT NULL,
			create_date TIMESTAMP,
			update_date TIMESTAMP,
			country VARCHAR (64),
			isDead BOOLEAN,
			A VARCHAR (255),
			NS VARCHAR (255),
			CNAME VARCHAR (255),
			MX VARCHAR (255),
			TXT VARCHAR (255)
		);

--	Creating a second index on the domains table
--
		CREATE INDEX domain_query_index ON domains (domain_query_id)
