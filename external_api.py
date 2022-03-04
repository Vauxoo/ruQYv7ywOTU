"""
External API - XML RPC

Odoo is usually extended internally via modules, but many of its features and all of 
its data are also available from the outside for external analysis or integration with 
various tools. Part of the Model Reference API is easily available over XML-RPC and 
accessible from a variety of languages.
"""

# These parameters should be configurable in the external system.
url = 'insert server URL'
db = 'insert database name'
username = 'admin'
password = 'insert password for your admin user (default: admin)'

# For this example we would be using the native xmlrpc python library.
import xmlrpc.client   
import json
import base64

# This is to test the connection with odoo server.
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
output = common.version()
print(str("Version: "), output)

# This call tests the credentials and returns the user ID for the next calls.
uid = common.authenticate(db, username, password, {})
print(str("User ID: "), uid)

# Initialize the models endpoint.
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# CALLING METHODS

# Example to read fields from a specific partner.
fields = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[
        ['is_company', '=', True], # Ignore contacts within the desired partner.
        ['vat', '=', 'BE0477472701'], # Search only for specific VAT.
    ]],
    {'fields': [
        'total_due', # Monetary: Total due.
        'total_invoiced', # Monetary: Total invoiced.
        'total_overdue', # Monetary: Total overdue.
        ], 'limit': 5})
print(str("Contact selected fields: "), fields)


# List records

fields = models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['is_company', '=', True]]])

print(str("List selected record fields: "), fields)


# Pagination using offset and limit

fields = models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['is_company', '=', True]]],
    {'offset': 10, 'limit': 3})

print(str("List selected filtered fields: "), fields)


# Count records

fields = models.execute_kw(db, uid, password,
    'res.partner', 'search_count',
    [[['is_company', '=', True]]])

print(str("Count record fields: "), fields)

# Read records

ids = models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['is_company', '=', True]]],
    {'limit': 1})
[record] = models.execute_kw(db, uid, password,
    'res.partner', 'read', [ids])
# count the number of fields fetched by default
len(record)

print(str("List of read records: "), ids)

details = models.execute_kw(db, uid, password,
    'res.partner', 'read',
    [ids], {'fields': ['name', 'country_id', 'comment']})

print(str("Details from list of record fields: "), details)


# Listing record fields

listing = models.execute_kw(
    db, uid, password, 'res.partner', 'fields_get',
    [], {'attributes': ['string', 'help', 'type']})

print(str("Listing record fields: "), listing)


# Search and read

search = models.execute_kw(db, uid, password,
    'res.partner', 'search_read',
    [[['is_company', '=', True]]],
    {'fields': ['name', 'country_id', 'comment'], 'limit': 5})


print(str("Search record fields: "), search)


# Create records

id  = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
    'name': "Vauxoo S.A. de C.V.",
}])

print(str("New partner record ID: "), id)


# Update records

models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {
    'phone': "+506 4000 2677",
    'email': "ventas@vauxoo.com",
}])
# get record name after having changed it

update = models.execute_kw(db, uid, password, 'res.partner', 'name_get', [[id]])


print(str("Updated information on record ID: "), update)


# Delete records

models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[id]])
# check if the deleted record is still in the database
unlink = models.execute_kw(db, uid, password,
    'res.partner', 'search', [[['id', '=', id]]])


print(str("Deleted records: "), unlink)


# Inspection and introspection

models.execute_kw(db, uid, password, 'ir.model', 'create', [{
    'name': "Custom Model",
    'model': "x_custom_model",
    'state': 'manual',
}])
meta = models.execute_kw(
    db, uid, password, 'x_custom_model', 'fields_get',
    [], {'attributes': ['string', 'help', 'type']})


print(str("Show metadata of the records: "), meta)


id = models.execute_kw(db, uid, password, 'ir.model', 'create', [{
    'name': "Custom Model",
    'model': "x_custom",
    'state': 'manual',
}])
models.execute_kw(
    db, uid, password,
    'ir.model.fields', 'create', [{
        'model_id': id,
        'name': 'x_name',
        'ttype': 'char',
        'state': 'manual',
        'required': True,
    }])
record_id = models.execute_kw(
    db, uid, password,
    'x_custom', 'create', [{
        'x_name': "test record",
    }])
meta = models.execute_kw(db, uid, password, 'x_custom', 'read', [[record_id]])

print(str("Show metadata of the records: "), meta)
