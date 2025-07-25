Custom ERP Extension
====================

This module provides an example of extending Odoo 18 Community
with Dominican fiscal requirements and basic business features. It
follows the OCA guidelines of modularity and clean code.

Features
--------
* Adds a checkbox on quotations to indicate whether a NCF should be
  generated.
* Adds an optional NCF field on invoices.
* Adds a checkbox in the Point of Sale configuration to require NCF.
* Integrates with standard sales, purchases, inventory, and accounting
  modules without relying on Enterprise features.
* Placeholder hooks for payroll integration.

The module depends only on community editions of core apps and can be
installed alongside standard Odoo modules.
