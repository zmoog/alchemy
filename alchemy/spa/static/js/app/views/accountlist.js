define(['jquery', 'underscore', 'backbone', 'app/models/account', 'app/views/accountitem', 'text!tpl/accountlist.html'], function ($, _, Backbone, models, AccountItemView, tpl) {

    "use strict";


    var template = _.template(tpl);

    return Backbone.View.extend({

    	initialize: function () {
    		this.collection = new models.AccountCollection();

			this.collection.fetch();

			this.listenTo( this.collection, 'add', this.renderAccount );
			this.listenTo( this.collection, 'reset', this.render );
    	},

        render: function () {
        	console.log('AccountListView::render')
            this.$el.html(template({accountlist: this.collection}));
            this.collection.each(function (item) {
            	this.renderAccount(item);
            });
            return this;
        },

        renderAccount: function (item) {
        	// console.log('AccountListView::renderAccount')
        	var accountItemView = new AccountItemView({model: item});
        	this.$el.append(accountItemView.render().el)
        }

    });

});