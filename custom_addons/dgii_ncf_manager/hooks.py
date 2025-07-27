

def post_init_hook(cr, registry):
    """Ensure partner NCF fields exist when installing."""
    cr.execute("""\
        ALTER TABLE res_partner
        ADD COLUMN IF NOT EXISTS ncf_required boolean DEFAULT FALSE
    """)
    cr.execute("""\
        ALTER TABLE res_partner
        ADD COLUMN IF NOT EXISTS default_ncf_type varchar
    """)
