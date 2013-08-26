define(['jquery', 'backbone'], function ($, Backbone) {

    "use strict";

    var Account = Backbone.Model.extend({

            // 

            urlRoot: "/api/accounts/",
            //url: "/api/accounts/",

            initialize: function () {
                // this.reports = new AccountCollection();
                // this.reports.url = this.urlRoot + "/" + this.id + "/reports";
            }

        }),

        AccountCollection = Backbone.Collection.extend({

            model: Account,

            url: "/api/accounts/",

            parse: function(response) {
                return response.results;
            }

        });

    return {
        Account: Account,
        AccountCollection: AccountCollection
    };

});