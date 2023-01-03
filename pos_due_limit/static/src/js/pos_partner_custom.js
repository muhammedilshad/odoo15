odoo.define('point_of_sale.partner_due_limit', function(require) {
    "use strict";

    const ProductScreen = require('point_of_sale.ProductScreen');
    var models = require('point_of_sale.models');
    const { Gui } = require('point_of_sale.Gui');
    var Registries = require('point_of_sale.Registries');
    models.load_fields('res.partner', 'due_limit')


    const partner_due_limit = (ProductScreen) =>
    class extends ProductScreen {
    async _onClickPay() {
                  var customer = this.currentOrder.get_client();
                  var amount = this.currentOrder.get_total_with_tax();
                  if (!customer){
                      Gui.showPopup('ErrorPopup', {
                          'title': ('Warning : Customer not selected'),
                          'body': ('Select a customer for continue'),
                            });
                  }
                  else{
                      if (amount > customer.due_limit){
                              Gui.showPopup('ErrorPopup', {
                                   'title': ('Warning : crossed limit'),
                                   'body': ('Customer has crossed purchase limit'),
                           })
                      }
                      else{
                           await super._onClickPay();
                      }
                      }
    }
    };
    Registries.Component.extend(ProductScreen, partner_due_limit);

    return ProductScreen;
    });