define(['jquery', 'underscore', 'backbone', 'text!tpl/accountitem.html'], function ($, _, Backbone, tpl) {

    "use strict";


    var template = _.template(tpl);

    return Backbone.View.extend({

    	el: '<li>',

        render: function () {
        	//console.log('rendering account');
            this.$el.html(template(this.model.toJSON()));
            return this;
        }

    });

});