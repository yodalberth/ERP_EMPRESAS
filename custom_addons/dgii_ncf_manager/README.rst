DGII NCF Manager
================

This module manages fiscal receipt numbers (NCF) issued by the Dominican tax authority (DGII). It follows the OCA guidelines so features are modular and NCF usage is optional on each invoice.

Features
--------
* Maintain ranges of NCF numbers with automatic expiration checks.
* Add a checkbox "¿Aplicar NCF?" on invoices so sellers decide whether to assign an NCF.
* Partners can specify if they require NCF and which type is suggested by default.
* A boolean field ``Requiere NCF`` on partners preselects the NCF option when creating invoices.
* Journals may define a default NCF type without forcing it on all invoices.
* Scheduled job marks exhausted or expired ranges automatically.
* Post-init hook adds missing partner fields during upgrades.

Installation
------------
The module has no proprietary dependencies and is marked as an application, so it is easily located in the Apps list. Compatible with Odoo 18.0 Community Edition.

Usage
-----
Enable "¿Aplicar NCF?" on an invoice when the customer requires a fiscal receipt. The system will suggest the type according to partner or journal configuration but will not enforce it.
