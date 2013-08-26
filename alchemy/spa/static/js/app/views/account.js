define(['jquery', 'underscore', 'backbone', 'text!tpl/account.html'], function ($, _, Backbone, tpl) {

    "use strict";


    var template = _.template(tpl);

    return Backbone.View.extend({

        render: function () {
            this.$el.html(template({
            	account: this.model.toJSON()
            }));
            return this;
        }

    });

});