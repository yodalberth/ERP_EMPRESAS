DGII NCF Manager
================

This module manages fiscal receipt numbers (NCF) for the Dominican 
Republic. It follows the OCA guidelines of modularity and keeps the
NCF fields optional on customer invoices.

Features
--------
* Manage ranges of NCF numbers and automatic expiration checks.
* Optional NCF on invoices via the "¿Aplicar NCF?" checkbox.
* Partners can require NCF and suggest a default NCF type.
* Journals can define a default NCF type.
* Scheduled job to mark exhausted or expired ranges.
