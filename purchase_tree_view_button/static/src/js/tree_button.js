odoo.define('button_near_create.tree_button', function (require) {
    "use strict";
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var ajax = require('web.ajax');
    var viewRegistry = require('web.view_registry');
    var TreeButton = ListController.extend({
       buttons_template: 'button_near_create.buttons',
       events: _.extend({}, ListController.prototype.events, {
           'click .change_stage_action': '_ChangeStage',
       }),
       _ChangeStage: function () {
       var list = [];
       var checked = this.getSelectedIds()
       list.push(checked);
       ajax.jsonRpc('/purchase/change_state', 'call',{'data':list})
       window.location.reload();
        }
})
var PurchaseOrderListView = ListView.extend({
config: _.extend({}, ListView.prototype.config, {
Controller: TreeButton,
})
});
viewRegistry.add('button_in_tree', PurchaseOrderListView)
});