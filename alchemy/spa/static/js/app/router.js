define(['jquery', 'backbone', 'app/views/shell', 'app/views/home'], function($, Backbone, ShellView, HomeView) {

    "use strict";

    var $body = $('body'),
        shellView = new ShellView({el: $body}).render(),
        $content = $("#content", shellView.el),
        homeView = new HomeView({el: $content});

    // // Close the search dropdown on click anywhere in the UI
    // $body.click(function () {
    //     $('.dropdown').removeClass("open");
    // });

    // $("body").on("click", "#showMeBtn", function (event) {
    //     event.preventDefault();
    //     shellView.search();
    // });

    return Backbone.Router.extend({

        routes: {
            "": "home",
            "account": "accountlist",
            "account/:id": "accountDetail",
            "transfer": "transferlist",
            "transfer/:id": "transferDetail",
            "about": "about",
            "contact": "contact"
            //"employees/:id": "employeeDetails"
        },

        home: function () {
            homeView.delegateEvents(); // delegate events when the view is recycled
            homeView.render();
            //shellView.selectMenuItem('home-menu');
        },

        accountlist: function () {
            require(['app/views/accountlist'], function (AccountListView) {

                // _.forEach([1,2,3], function (account) { console.log(account)});
                
                // collection.fetch({results: {page: 1}, success: function(collection, response, options){
                //     // console.log('collection', collection);
                //     collection.each(function (account) { console.log(account)});
                // }});

                // console.log('json', collection.toJSON());
                // console.log('size', collection.size());
                // collection.fetch();
                // collection.each(function (account) { console.log(account)});

                //collection.fetch();

                var view = new AccountListView({el: $content});
                view.render();
            });
        },

        accountDetail: function (id) {
            console.log('accountDetail');
            require(["app/views/account", "app/models/account"], function (AccountView, models) {
                var account = new models.Account({id: id});
                account.fetch({
                    success: function (data) {
                        // Note that we could also 'recycle' the same instance of EmployeeFullView
                        // instead of creating new instances
                        var view = new AccountView({model: data, el: $content});
                        view.render();
                    }
                });
                // shellView.selectMenuItem();
            });
        },

        transferlist: function () {
            require(['app/views/transferlist'], function (TransferListView) {
                var view = new TransferListView({el: $content});
                //view.render();
            });
        },

       transferDetail: function (id) {
            console.log('transferDetail');
            require(["app/views/transfer", "app/models/transfer"], function (TransferView, models) {
                var transfer = new models.Transfer({id: id});
                transfer.fetch({
                    success: function (data) {
                        // Note that we could also 'recycle' the same instance of EmployeeFullView
                        // instead of creating new instances
                        var view = new TransferView({model: data, el: $content});
                        view.render();
                    }
                });
                // shellView.selectMenuItem();
            });
        },

        about: function () {
            require(['app/views/about'], function (AboutView) {
                var view = new AboutView({el: $content});
                view.render();
            });
        },

        contact: function () {
            require(['app/views/contact'], function (ContactView) {
                var view = new ContactView({el: $content});
                view.render();
            });
        }
        //contact: function () {
        //    require(["app/views/Contact"], function (ContactView) {
        //        var view = new ContactView({el: $content});
        //        view.render();
        //        shellView.selectMenuItem('contact-menu');
        //    });
        //},
//
        //employeeDetails: function (id) {
        //    require(["app/views/Employee", "app/models/employee"], function (EmployeeView, models) {
        //        var employee = new models.Employee({id: id});
        //        employee.fetch({
        //            success: function (data) {
        //                // Note that we could also 'recycle' the same instance of EmployeeFullView
        //                // instead of creating new instances
        //                var view = new EmployeeView({model: data, el: $content});
        //                view.render();
        //            }
        //        });
        //        shellView.selectMenuItem();
        //    });
        //}

    });

});