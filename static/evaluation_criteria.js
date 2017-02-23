/**
 * Created by pvishn200 on 2/4/17.
Objective editable input.
 **/
(function ($) {
    "use strict";

    var Evaluation_criteria = function (options) {
        this.init('evaluation_criteria', options, Evaluation_criteria.defaults);
    };

    //inherit from Abstract input
    $.fn.editableutils.inherit(Evaluation_criteria, $.fn.editabletypes.abstractinput);

    $.extend(Evaluation_criteria.prototype, {
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
            var html = $('<div>').text(value.evaluation_criterionId).html() + ', ' +
                $('<div>').text(value.evalution_criterion).html() + ',' +
                $('<div>').text(value.criterion_percentage).html();

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
            e.g. "Moscow, st. Lenina, bld. 15" => {evaluation_criterionId: "Moscow", evaluation_criterion: "Lenina", criterion_percentage: "15"}
            but for complex structures it's not recommended.
            Better set value directly via javascript, e.g.
            editable({
                value: {
                    evaluation_criterionId: "Moscow",
                    evaluation_criterion: "Lenina",
                    criterion_percentage: "15"
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
           this.$input.filter('[name="evaluation_criterionId"]').val(value.evaluation_criterionId);
           this.$input.filter('[name="evaluation_criterion"]').val(value.evaluation_criterion);
       },

       /**
        Returns value of input.

        @method input2value()
       **/
       input2value: function() {
           return {
              evaluation_criterionId: this.$input.filter('[name="evaluation_criterionId"]').val(),
              evaluation_criterion: this.$input.filter('[name="evaluation_criterion"]').val()
           };
       },

        /**
        Activates input: sets focus on the first field.

        @method activate()
       **/
       activate: function() {
            this.$input.filter('[name="evaluation_criterionId"]').focus();
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

    Evaluation_criteria.defaults = $.extend({}, $.fn.editabletypes.abstractinput.defaults, {
        tpl: '<div class="editable-evaluation_criteria" style="padding-right: 1px;" align="right"><label><span>Eval Criterion Id: </span><input type="text" name="evaluation_criterionId" class="input-small" ></label></div>'+
             '<div class="editable-evaluation_criteria" style="padding-right: 1px;" align="right"><label><span>Criterion: </span><input type="text" name="evaluation_criterion" class="input-small"></label></div>',

        inputclass: ''
    });

    $.fn.editabletypes.evaluation_criteria = Evaluation_criteria;

}(window.jQuery));