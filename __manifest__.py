# -*- coding: utf-8 -*-
{
    'name': "UPOCAR",
    'summary': """Gestión de taller""",
    'description': """Gestión de un taller mecánico""",
    'author': "Pedro Martín Sánchez, Juan Carlos Ruiloba Calderón y Fernando Fuentes Pérez",
    'category': 'UPOCAR',
    'version': '0.1',
    'depends': ['base'],
    'data': ['views/reparacion_view.xml', 'views/vehiculo_view.xml', 'views/mecanico_view.xml', 
             'views/taller_view.xml', 'views/repuesto_view.xml', 'views/modelo_view.xml', 'views/marca_view.xml',
             'views/linea_reparacion_view.xml', 'views/cliente_view.xml', 'views/proveedor_view.xml',
             'views/linea_pedido_view.xml', 'views/pedido_view.xml'],
    'demo': ['demo/upocar_demo.xml'],
    'application': True
}
