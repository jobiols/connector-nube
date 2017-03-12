.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
:target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
Odoo TiendaNube Connector
=========================

This module connects Odoo and TiendaNube.

TiendaNube (https://www.tiendanube.com/) is a e-commerce available as Saas
this is not free.

This module allows the synchronization of the following objects from TiendaNube
to Odoo:

* Websites
* Stores and languages
* Carriers
* Product categories
* Products
* Combinations of products
* Partner categories
* Customers

Once these objects are synchronised, it will allow the import of sales orders,
together with the related customers.

As an extra feature, you can also export the stock quantities back to TiendaNube.

If you want to export from Odoo to TiendaNube changes made on the products,
product categories or product images, you need to install
*connector_tienda_nube_catalog_manager* module in this same repository.

This connector supports TiendaNube version up to v1.

Installation
============

It doesn't require any plug-in in TiendaNube, but requires an extra Python
library in Odoo server side, called tiendanube:

https://github.com/jobiols/tiendanube-python/


Configuration
=============

To configure this module, you need to set several things in both TiendaNube
and Odoo:

Steps in TiendaNube
-------------------

see doc/crear_aplicacion.md

Steps in Odoo
-------------

#. Go to *Connectors > TiendaNube > Backends*.
#. Create a new record for registering a TiendaNube backend. You will bind
   this backend to an specific company and warehouse.
#. Define the main URL of the TiendaNube web, and the webservice key you
   got in TiendaNube.
#. Define other parameters like the discount and shipping products, or if the
   taxes are included in the price.
#. Click on "Synchronize Metadata" button. This will bring the basic shop
   information that you can find on *Websites* and *Stores* menus.
#. Click on "Synchronize Base Data" button. This will import carriers,
   languages, tax groups and the rest of base data that are needed for the
   proper work.
#. Go to *Accounting > Configuration > Taxes > Tax Groups*, and include
   for each of the tax definition imported from TiendaNube, the corresponding
   taxes in Odoo.
#. Activate the job runner, checking the connector documentation for setting
   the server correctly for using it in
   http://odoo-connector.com/guides/jobrunner.html
#. Alternatively, if you are not able to activate it, you can enable the
   scheduled job called "Enqueue Jobs".
#. Activate the scheduled jobs for importing the records you want:

  * TiendaNube - Export Stock Quantities
  * TiendaNube - Import Carriers
  * TiendaNube - Import Customers and Groups
  * TiendaNube - Import Products and Categories
  * TiendaNube - Import Sales Orders
  * TiendaNube - Import suppliers
  * TiendaNube - Payment methods

Usage
=====

To use this module, you need to:

#. Go to *Connectors > Queue > Jobs*, and check the correct enqueuing of
   the tasks.
#. Check on each menu the resulting imported records (Customers, Sales
   Orders...)

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
:alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/108/8.0

Known issues / Roadmap
======================

* Work with multiple warehouses.
* Tests.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/connector-tienda_nube/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* `TiendaNube logo <http://seeklogo.com/tienda_nube-logo-178788.html>`_.
* `Odoo logo <https://www.odoo.com/es_ES/page/brand-assets>`_.
* `Cable <https://openclipart.org/detail/174134/cable-with-connector>`_.

Contributors
------------

* Jorge Obiols <jorge.obiols@gmail.com>
* Sébastien Beau <sebastien.beau@akretion.com>
* Benoît Guillot <benoit.guillot@akretion.com>
* Alexis de Lattre <alexis.delattre@akretion.com>
* Guewen Baconnier <guewen.baconnier@camptocamp.com>
* Sergio Teruel <sergio.teruel@tecnativa.com>
* Mikel Arregi <mikelarregi@avanzosc.es>
* Pedro M. Baeza <pedro.baeza@tecnativa.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
:alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by jeo Software.

To contribute to this module, please visit https://github.com/jobiols/jeo
