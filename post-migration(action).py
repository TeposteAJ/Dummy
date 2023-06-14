import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    set_studio_field(cr)


def set_studio_field(cr):
    """
    Set the 'x_studio_concepto' field to 'concept' in stock_manual_transfer.
    Set the 'x_studio_sucursal' field to 'branch' in event_registration.
    Set the 'x_studio_info_adicional' field to 'aditional_info' in event_registration.
    Set 'banch_client' value to 'expenses' for 'reference' field, in  stock_landed_cost_guide
    Set 'services' values to 'manual_transfers' for 'freight_type' in stock_landed_cost_guide
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    records_stock = env["stock.manual_transfer"].search([
        ("x_studio_concepto", "!=", False),
        ("x_studio_concepto", "!=", ""),
        ("x_studio_concepto", "!=", None),
        ])

    map_value = {
        'Inventario Stock' : 'stock_inventory',
        'Distribucion' : 'distribution',
        'Corrección de Transferencia' : 'transfer_correction',
        'Reubicacion' : 'relocation',
        'Ajuste Multiplo' : 'multiple_setting',
        'Garantia' : 'warranty',
        'Compra' : 'purchase',
    }

    for record in records_stock:
            studio_record = record.x_studio_concepto
            new_code_record = map_value.get(studio_record)
            record.concept = new_code_record
            record.x_studio_concepto = ""
    _logger.info("Field x_studio_concepto was set to concept with IDs %s", records_stock.ids)

    records_event = env["event.registration"].search([
        ("x_studio_sucursal", "!=", False),
        ("x_studio_sucursal", "!=", ""),
        ("x_studio_sucursal", "!=", None),
        ])

    map_value = {
        'TYP HERMOSILLO' : 'typ_hermosillo',
        'TYP CULIACAN' : 'typ_culiacan',
        'TYP NOGALES' : 'typ_nogales',
        'TYP TIJUANA' : 'typ_tijuana',
        'TYP OBREGON' : 'typ_obregon',
        'TYP MEXICALI' : 'typ_mexicali',
        'TYP LA PAZ' : 'typ_la_paz',
        'TYP LOS MOCHIS' : 'typ_los_mochis',
        'TYP GUADALAJARA' : 'typ_guadalajara',
        'TYP QUERÉTARO' : 'typ_queretaro',
        'TYP MONTERREY' : 'typ_monterrey',
        'TYP SOPORTE' : 'typ_soporte',
    }

    for record in records_event:
            studio_record = record.x_studio_sucursal
            new_code_record = map_value.get(studio_record)
            record.branch = new_code_record
            record.x_studio_sucursal = ""
    _logger.info("Field x_studio_sucursal was set to branch with IDs %s", records_event.ids)

    records_event_info = env["event.registration"].search([
        ("x_studio_info_adicional", "!=", False),
        ("x_studio_info_adicional", "!=", ""),
        ("x_studio_info_adicional", "!=", None),
        ])

    records_event_info.write({
        "additional_info": records_event_info.mapped("x_studio_info_adicional"),
        "x_studio_info_adicional": "",
    })
    _logger.info("Field x_studio_info_adicional was set to additional_info with IDs %s", records_event_info.ids)

    records_landed_cost = env["stock.landed.cost.guide"].search([
        ("reference", "=", "branch_client"),
        ])
    records_landed_cost.write({
        "reference": "expenses"
    })
    _logger.info("Reference field was updated, for 'branch_client' to 'expenses' with IDs %s", records_event_info.ids)

### CAMBIOS EN LAS TRADUCCIONES QUE ESTAN INCORRECTOS
    records_line_guide = env["stock.landed.cost.guide"].search([
        ("freight_type", "=", "services"),
        ])
    records_line_guide.write({
        "freight_type": "manual_transfers"
    })
    _logger.info("Freight_type field was updated, for 'services' to 'manual_transfers' with IDs %s", records_line_guide.ids)
