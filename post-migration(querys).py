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
    cr.execute(
        """
        UPDATE
            stock_manual_transfer
        SET concept = CASE x_studio_concepto
            WHEN 'Inventario Stock' THEN 'stock_inventory'
            WHEN 'Distribucion' THEN 'distribution'
            WHEN 'Corrección de Transferencia' THEN 'transfer_correction'
            WHEN 'Reubicacion' THEN 'relocation'
            WHEN 'Ajuste Multiplo' THEN 'multiple_setting'
            WHEN 'Garantia' THEN 'warranty'
            WHEN 'Compra' THEN 'purchase'
            ELSE NULL
            END,
            x_studio_concepto = ''
        WHERE
            x_studio_concepto IS NOT NULL AND x_studio_concepto != ''
        """
    )
    _logger.info("Field x_studio_concepto was set to concept on %d stock_manual_transfer table", cr.rowcount )
   # Set the 'x_studio_sucursal' field to 'branch' in event_registration.
    cr.execute(
       """
       UPDATE
        event_registration
       SET branch = CASE x_studio_sucursal
        WHEN 'TYP HERMOSILLO' THEN 'typ_hermosillo',
        WHEN 'TYP CULIACAN' THEN 'typ_culiacan',
        WHEN 'TYP NOGALES' THEN 'typ_nogales',
        WHEN 'TYP TIJUANA' THEN 'typ_tijuana',
        WHEN 'TYP OBREGON' THEN 'typ_obregon',
        WHEN 'TYP MEXICALI' THEN 'typ_mexicali',
        WHEN 'TYP LA PAZ' THEN 'typ_la_paz',
        WHEN 'TYP LOS MOCHIS' THEN 'typ_los_mochis',
        WHEN 'TYP GUADALAJARA' THEN 'typ_guadalajara',
        WHEN 'TYP QUERÉTARO' THEN 'typ_queretaro',
        WHEN 'TYP MONTERREY' THEN 'typ_monterrey',
        WHEN 'TYP SOPORTE' THEN 'typ_soporte',
        ELSE NULL
        END,
            x_studio_sucursal = ''
        WHERE
            x_studio_sucursal IS NOT NULL AND x_studio_sucursal != ''
       """
   )
    _logger.info("Field x_studio_sucursal was set to branch on %d event_registration table", cr.rowcount )
# Set the 'x_studio_info_adicional' field to 'aditional_info' in event_registration.
    cr.execute(
        """
        UPDATE
            event_registration
        SET
            additional_info = x_studio_info_adicional,
            x_studio_adicional = '',
        WHERE
            x_studio_info_adicional IS NOT NULL AND
            x_studio_info_adicional != '';
        """
    )
    _logger.info("Field x_studio_info_adicional was set to additional_info on %d event_registration table", cr.rowcount )
### CAMBIOS EN LAS TRADUCCIONES QUE ESTAN INCORRECTOS
#  Set 'banch_client' value to 'expenses' for 'reference' field, in  stock.landed.cost.guide
    cr.execute(
        """
        UPDATE
            stock_landed_cost_guide
        SET
            reference = 'expenses'
        WHERE
            reference = 'branch_client';
        """
    )
    _logger.info("Reference field was updated, for 'branch_client' to 'expenses' in stock_landed_cost_guide table.")
#  Set 'services' values to 'manual_transfers' for 'freight_type' in stock.landed.cost.guide
    cr.execute(
        """
        UPDATE
            stock_landed_cost_guide
        SET
            freight_type = 'manual_transfers'
        WHERE
            freight_type = 'services';
        """
    )
    _logger.info("Freight_type field was updated, for 'services' to 'manual_transfers' in stock_landed_cost_guide table.")
