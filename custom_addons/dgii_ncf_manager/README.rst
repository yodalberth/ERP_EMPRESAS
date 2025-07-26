DGII NCF Manager
================

Manage fiscal receipt numbers (NCF) for the Dominican Republic. The
implementation follows OCA guidelines so the NCF logic remains modular and
optional.

Features
--------
* Manage ranges of NCF numbers and automatic expiration checks.
* Optional NCF on invoices via the "¿Aplicar NCF?" checkbox.
* Partners can require NCF and suggest a default NCF type.
* Journals may define a default NCF type without enforcing it.
* Scheduled job to mark exhausted or expired ranges.
* Post-init hook creates missing partner fields on upgrades.

Installation
------------
The module has no proprietary dependencies and is flagged as an application,
so it is easily located from the Apps list. Compatible with Odoo 18.0
Community Edition.
