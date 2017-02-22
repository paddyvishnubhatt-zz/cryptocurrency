/**
 * Created by pvishn200 on 2/4/17.
Objective editable input.
 **/
(function ($) {
    "use strict";

    var Objective = function (options) {
        this.init('objective', options, Objective.defaults);
    };

    //inherit from Abstract input
    $.fn.editableutils.inherit(Objective, $.fn.editabletypes.abstractinput);

    $.extend(Objective.prototype, {
        /**
        Renders input from tpl

        @method render()
        **/
        render: function() {
           this.$input = this.$tpl.find('input');
        },

        /**
        Default method to show value in element. Can be overwritten by display option.

        @method value2html(value, element)
        **/
        value2html: function(value, element) {
            if(!value) {
                $(element).empty();
                return;
            }
            var html = $('<div>').text(value.objectiveId).html() + ', ' +
                $('<div>').text(value.description).html() + ',' +
                $('<div>').text(value.weight).html();
            $(element).html('<span class="glyphicon glyphicon-plus"></span>');

            // $(element).html(html);
        },

        /**
        Gets value from element's html

        @method html2value(html)
        **/
        html2value: function(html) {
          /*
            you may write parsing method to get value by element's html
            e.g. "Moscow, st. Lenina, bld. 15" => {objectiveId: "Moscow", description: "Lenina", weight: "15"}
            but for complex structures it's not recommended.
            Better set value directly via javascript, e.g.
            editable({
                value: {
                    objectiveId: "Moscow",
                    description: "Lenina",
                    weight: "15"
                }
            });
          */
          return null;
        },

       /**
        Converts value to string.
        It is used in internal comparing (not for sending to server).

        @method value2str(value)
       **/
       value2str: function(value) {
           var str = '';
           if(value) {
               for(var k in value) {
                   str = str + k + ':' + value[k] + ';';
               }
           }
           return str;
       },

       /*
        Converts string to value. Used for reading value from 'data-value' attribute.

        @method str2value(str)
       */
       str2value: function(str) {
           /*
           this is mainly for parsing value defined in data-value attribute.
           If you will always set value by javascript, no need to overwrite it
           */
           return str;
       },

       /**
        Sets value of input.

        @method value2input(value)
        @param {mixed} value
       **/
       value2input: function(value) {
           if(!value) {
             return;
           }
           this.$input.filter('[name="objectiveId"]').val(value.objectiveId);
           this.$input.filter('[name="description"]').val(value.description);
           this.$input.filter('[name="weight"]').val(value.weight);
       },

       /**
        Returns value of input.

        @method input2value()
       **/
       input2value: function() {
           return {
              objectiveId: this.$input.filter('[name="objectiveId"]').val(),
              description: this.$input.filter('[name="description"]').val(),
              weight: this.$input.filter('[name="weight"]').val()
           };
       },

        /**
        Activates input: sets focus on the first field.

        @method activate()
       **/
       activate: function() {
            this.$input.filter('[name="objectiveId"]').focus();
       },

       /**
        Attaches handler to submit form in case of 'showbuttons=false' mode

        @method autosubmit()
       **/
       autosubmit: function() {
           this.$input.keydown(function (e) {
                if (e.which === 13) {
                    $(this).closest('form').submit();
                }
           });
       }
    });

    Objective.defaults = $.extend({}, $.fn.editabletypes.abstractinput.defaults, {
        tpl: '<div class="editable-objective"><label><span>Id: </span><input type="text" name="objectiveId" class="input-small"></label></div>'+
             '<div class="editable-objective"><label><span>Desc: </span><input type="text" name="description" class="input-small"></label></div>'+
             '<div class="editable-objective"><label><span>Weight: </span><input type="number" name="weight" class="input-small"min="1" max="5"></div>',

        inputclass: ''
    });

    $.fn.editabletypes.objective = Objective;

}(window.jQuery));