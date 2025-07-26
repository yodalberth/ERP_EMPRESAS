import base64
import csv
import io

from odoo import models, fields


# Asistente para importar rangos de NCF desde un archivo CSV
class ImportNCFWizard(models.TransientModel):
    _name = 'import.ncf.wizard'
    _description = 'Importar rangos de NCF'

    file_data = fields.Binary(string='Archivo', required=True)
    file_name = fields.Char(string='Nombre del archivo')

    def action_import(self):
        """Crea rangos de NCF a partir del archivo cargado."""
        self.ensure_one()
        data = base64.b64decode(self.file_data)
        file_io = io.StringIO(data.decode())
        reader = csv.DictReader(file_io)
        for row in reader:
            self.env['ncf.range'].create({
                'name': row.get('name'),
                'ncf_type': row.get('ncf_type'),
                'sequence_start': row.get('sequence_start'),
                'sequence_end': row.get('sequence_end'),
                'expiration_date': row.get('expiration_date'),
            })
