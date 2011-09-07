(function($, cloudStack) {
  cloudStack.dialog = {
    /**
     * Dialog with form
     */
    createForm: function(args) {
      var $formContainer = $('<div>').addClass('form-container');
      var $message = $('<span>').addClass('message').appendTo($formContainer).html(args.form.desc);
      var $form = $('<form>').appendTo($formContainer);

      $.each(args.form.fields, function(key) {
        var $formItem = $('<div>').addClass('form-item').appendTo($form);

        // Label field
        var $name = $('<div>').addClass('name')
              .appendTo($formItem)
              .append(
                $('<label>').html(this.label + ':')
              );

        // Input area
        var $value = $('<div>').addClass('value')
              .appendTo($formItem);
        var $input;

        // Determine field type of input
        if (this.select) {
          $input = $('<select>').attr({ name: key }).appendTo($value);
          $(this.select).each(function() {
            var $option = $('<option>')
                  .appendTo($input)
                  .val(this.id)
                  .html(this.description);
          });
        } else if (this.isBoolean) {
          $input = $('<input>').attr({ name: key, type: 'checkbox' }).appendTo($value);
        } else {
          $input = $('<input>').attr({ name: key, type: 'text' }).appendTo($value);
        }

        $input.data('validation-rules', this.validation);

        $('<label>').addClass('error').appendTo($value).html('*required');
      });

      var getFormValues = function() {
        var formValues = {};
        $.each(args.form.fields, function(key) {
        });
      };

      // Setup form validation
      $formContainer.find('form').validate();
      $formContainer.find('input, select').each(function() {
        if ($(this).data('validation-rules')) {
          $(this).rules('add', $(this).data('validation-rules'));
        }
      });

      return $formContainer.dialog({
        dialogClass: 'create-form',
        width: 400,
        title: args.form.title,
        buttons: [
          {
            text: 'Create',
            'class': 'ok',
            click: function() {
              if (!$formContainer.find('form').valid()) return false;

              $('div.overlay').remove();
              args.after($formContainer.find('form'));
              $(this).dialog('destroy');

              return true;
            }
          },
          {
            text: 'Cancel',
            'class': 'cancel',
            click: function() {
              $('div.overlay').remove();
              $(this).dialog('destroy');
            }
          }
        ]
      }).closest('.ui-dialog').overlay();
    },
    
    /**
     * Confirmation dialog
     */
    confirm: function(args) {
      return $(
        $('<span>').addClass('message').html(
          args.message
        )
      ).dialog({
        title: 'Confirm',
        dialogClass: 'confirm',
        zIndex: 5000,
        buttons: [
          {
            text: 'Cancel',
            'class': 'cancel',
            click: function() {
              $(this).dialog('destroy');
              $('div.overlay').remove();
            }
          },
          {
            text: 'Yes',
            'class': 'ok',
            click: function() {
              args.action();
              $(this).dialog('destroy');
              $('div.overlay').remove();
            }
          }
        ]
      }).closest('.ui-dialog').overlay();
    },

    /**
     * Notice dialog
     */
    notice: function(args) {
      return $(
        $('<span>').addClass('message').html(
          args.message
        )
      ).dialog({
        title: 'Status',
        dialogClass: 'notice',
        zIndex: 5000,
        buttons: [
          {
            text: 'Close',
            'class': 'close',
            click: function() {
              $(this).dialog('destroy');
            }
          }
        ]
      });
    }
  };
})(jQuery, cloudStack);
