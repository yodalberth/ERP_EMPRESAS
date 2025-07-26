DGII NCF Manager
================

This module manages fiscal receipt numbers (NCF) for the Dominican Republic.
It follows the OCA guidelines of modularity so the NCF functionality is
optional and independent from other custom modules.

Features
--------
* Manage ranges of NCF numbers and automatic expiration checks.
* Optional NCF on invoices via the "¿Aplicar NCF?" checkbox.
* Partners can require NCF and suggest a default NCF type.
* Journals can define a default NCF type.
* Scheduled job to mark exhausted or expired ranges.
* Post-init hook to create missing partner fields on upgraded databases.

Installation
------------
The module has no proprietary dependencies and is flagged as an application
so it can be located easily from Odoo's Apps list. It is compatible with
Odoo 18.0 Community Edition.
